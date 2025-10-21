#!/usr/bin/env python3
"""
Rentrobe - Fashion Rental Platform
Complete Flask Backend Application
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, IntegerField, SelectField, DateField, validators
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
import os
import sys
from datetime import datetime, date, timedelta
import uuid
import json
import logging
from pathlib import Path
from sqlalchemy import or_, and_

# Try to import PIL for image processing, fallback if not available
try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("PIL not available - image processing disabled")

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'wearhouse-dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///wearhouse.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Session configuration
app.config['SESSION_COOKIE_SECURE'] = os.environ.get('SESSION_COOKIE_SECURE', 'False').lower() == 'true'
app.config['SESSION_COOKIE_HTTPONLY'] = os.environ.get('SESSION_COOKIE_HTTPONLY', 'True').lower() == 'true'
app.config['SESSION_COOKIE_SAMESITE'] = os.environ.get('SESSION_COOKIE_SAMESITE', 'Lax')
app.config['SESSION_COOKIE_DOMAIN'] = os.environ.get('SESSION_COOKIE_DOMAIN', None)
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)

# Ensure upload directory exists
Path(app.config['UPLOAD_FOLDER']).mkdir(parents=True, exist_ok=True)

# Initialize extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'api_login'

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database Models
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    city = db.Column(db.String(50), nullable=False)
    address = db.Column(db.Text, nullable=True)
    join_date = db.Column(db.DateTime, default=datetime.utcnow)
    is_verified = db.Column(db.Boolean, default=False)
    rating = db.Column(db.Float, default=0.0)
    reviews_count = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    items = db.relationship('Item', backref='owner', lazy=True, foreign_keys='Item.owner_id')
    rentals_as_renter = db.relationship('Rental', backref='renter', lazy=True, foreign_keys='Rental.renter_id')
    rentals_as_owner = db.relationship('Rental', backref='item_owner', lazy=True, foreign_keys='Rental.owner_id')
    reviews_given = db.relationship('Review', backref='reviewer', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'city': self.city,
            'address': self.address,
            'rating': self.rating,
            'reviews_count': self.reviews_count,
            'join_date': self.join_date.isoformat() if self.join_date else None
        }

class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    slug = db.Column(db.String(50), unique=True, nullable=False)
    icon = db.Column(db.String(10), nullable=True)
    description = db.Column(db.Text, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    items = db.relationship('Item', backref='category', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'icon': self.icon,
            'count': len([item for item in self.items if item.is_active])
        }

class Item(db.Model):
    __tablename__ = 'items'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    size = db.Column(db.String(10), nullable=False)
    price_per_day = db.Column(db.Integer, nullable=False)  # in paise (₹1 = 100 paise)
    security_deposit = db.Column(db.Integer, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(20), default='available')  # available, rented, unavailable
    condition = db.Column(db.String(20), default='excellent')
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    views = db.Column(db.Integer, default=0)
    rating = db.Column(db.Float, default=0.0)
    reviews_count = db.Column(db.Integer, default=0)
    
    # Relationships
    images = db.relationship('ItemImage', backref='item', lazy=True, cascade='all, delete-orphan')
    rentals = db.relationship('Rental', backref='item', lazy=True)
    reviews = db.relationship('Review', backref='item', lazy=True)

    def to_dict(self, include_owner=True):
        data = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'category': self.category.name if self.category else 'Unknown',
            'size': self.size,
            'price': self.price_per_day // 100,  # Convert paise to rupees
            'deposit': self.security_deposit // 100,
            'status': self.status,
            'condition': self.condition,
            'rating': self.rating,
            'reviews': self.reviews_count,
            'views': self.views,
            'images': [img.filename for img in self.images],
            'date_added': self.date_added.isoformat() if self.date_added else None
        }
        
        if include_owner and self.owner:
            data['owner'] = {
                'id': self.owner.id,
                'name': self.owner.name,
                'city': self.owner.city,
                'initial': self.owner.name[0].upper() if self.owner.name else 'U',
                'rating': self.owner.rating,
                'reviews_count': self.owner.reviews_count
            }
        
        return data

class ItemImage(db.Model):
    __tablename__ = 'item_images'
    
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    is_primary = db.Column(db.Boolean, default=False)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)

class Rental(db.Model):
    __tablename__ = 'rentals'
    
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    renter_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    total_amount = db.Column(db.Integer, nullable=False)
    security_deposit = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, approved, active, completed, cancelled
    message = db.Column(db.Text, nullable=True)
    date_requested = db.Column(db.DateTime, default=datetime.utcnow)
    date_approved = db.Column(db.DateTime, nullable=True)
    date_started = db.Column(db.DateTime, nullable=True)
    date_completed = db.Column(db.DateTime, nullable=True)
    
    # Payment tracking
    payment_status = db.Column(db.String(20), default='pending')
    payment_id = db.Column(db.String(100), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'item': self.item.to_dict(include_owner=False) if self.item else None,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'total_amount': self.total_amount // 100,
            'security_deposit': self.security_deposit // 100,
            'status': self.status,
            'message': self.message,
            'date_requested': self.date_requested.isoformat() if self.date_requested else None,
            'other_user': {
                'name': self.item_owner.name if hasattr(self, 'item_owner') and self.item_owner else 'Unknown',
                'city': self.item_owner.city if hasattr(self, 'item_owner') and self.item_owner else 'Unknown',
                'rating': self.item_owner.rating if hasattr(self, 'item_owner') and self.item_owner else 0
            }
        }

class Review(db.Model):
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    rental_id = db.Column(db.Integer, db.ForeignKey('rentals.id'), nullable=False)
    reviewer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1-5 stars
    comment = db.Column(db.Text, nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

# Login manager
@login_manager.user_loader
def load_user(user_id):
    logger.info(f"Loading user with ID: {user_id}")
    user = User.query.get(int(user_id))
    logger.info(f"Loaded user: {user.email if user else 'None'}")
    return user

# Utility functions
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def save_image(file):
    """Save uploaded image and return filename"""
    if file and allowed_file(file.filename):
        # Generate unique filename
        filename = str(uuid.uuid4()) + '.' + file.filename.rsplit('.', 1)[1].lower()
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        try:
            if PIL_AVAILABLE:
                # Resize and optimize image
                image = Image.open(file)
                
                # Convert RGBA to RGB if needed
                if image.mode in ('RGBA', 'LA', 'P'):
                    background = Image.new('RGB', image.size, (255, 255, 255))
                    background.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
                    image = background
                
                # Resize image
                image.thumbnail((800, 600), Image.Resampling.LANCZOS)
                image.save(filepath, 'JPEG', optimize=True, quality=85)
            else:
                # Save file directly if PIL not available
                file.save(filepath)
            
            return filename
        except Exception as e:
            logger.error(f"Error saving image: {e}")
            return None
    return None

def calculate_rental_cost(item, start_date, end_date):
    """Calculate total rental cost"""
    days = (end_date - start_date).days
    if days < 1:
        days = 1
    return days * item.price_per_day

# Error handlers
@app.errorhandler(404)
def not_found(error):
    if request.path.startswith('/api/'):
        return jsonify({'error': 'Not found'}), 404
    return render_template('index.html')

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    logger.error(f"Internal server error: {error}")
    if request.path.startswith('/api/'):
        return jsonify({'error': 'Internal server error'}), 500
    return render_template('index.html')

@app.errorhandler(RequestEntityTooLarge)
def handle_file_too_large(error):
    return jsonify({'error': 'File too large. Maximum size is 16MB.'}), 413

# Main routes
@app.route('/')
def index():
    """Main page - serves the complete HTML application"""
    return render_template('index.html')

@app.route('/static/uploads/<filename>')
def uploaded_file(filename):
    """Serve uploaded files"""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# SPA routes
@app.route('/<path:path>')
def spa_routes(path):
    """Single Page Application routes"""
    return render_template('index.html')

# API Routes
@app.route('/api/categories')
@login_required
def api_categories():
    """Get all categories"""
    try:
        categories = Category.query.filter_by(is_active=True).all()
        return jsonify([cat.to_dict() for cat in categories])
    except Exception as e:
        logger.error(f"Error fetching categories: {e}")
        return jsonify({'error': 'Failed to fetch categories'}), 500

@app.route('/api/items')
@login_required
def api_items():
    """Get items with filtering"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 12, type=int), 100)  # Max 100 items per page
        category = request.args.get('category')
        size = request.args.get('size')
        min_price = request.args.get('min_price', type=int)
        max_price = request.args.get('max_price', type=int)
        city = request.args.get('city')
        search = request.args.get('search')
        
        query = Item.query.filter(Item.is_active == True)
        
        # Apply filters
        if category:
            cat = Category.query.filter_by(slug=category).first()
            if cat:
                query = query.filter(Item.category_id == cat.id)
        
        if size:
            query = query.filter(Item.size == size)
        
        if min_price:
            query = query.filter(Item.price_per_day >= min_price * 100)
        
        if max_price:
            query = query.filter(Item.price_per_day <= max_price * 100)
        
        if city:
            query = query.join(User).filter(User.city.ilike(f'%{city}%'))
        
        if search:
            query = query.filter(or_(
                Item.title.ilike(f"%{search}%"),
                Item.description.ilike(f"%{search}%")
            ))
        
        # Order by date added (newest first)
        query = query.order_by(Item.date_added.desc())
        
        # Paginate
        pagination = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False,
            max_per_page=100
        )
        items = pagination.items
        
        return jsonify({
            'items': [item.to_dict() for item in items],
            'pagination': {
                'page': pagination.page,
                'pages': pagination.pages,
                'per_page': pagination.per_page,
                'total': pagination.total,
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev
            }
        })
    except Exception as e:
        logger.error(f"Error fetching items: {e}")
        return jsonify({'error': 'Failed to fetch items'}), 500

@app.route('/api/items/<int:item_id>')
@login_required
def api_item_detail(item_id):
    """Get item details"""
    try:
        item = Item.query.get_or_404(item_id)
        
        # Increment view count
        item.views += 1
        db.session.commit()
        
        return jsonify(item.to_dict())
    except Exception as e:
        logger.error(f"Error fetching item {item_id}: {e}")
        return jsonify({'error': 'Failed to fetch item'}), 500

@app.route('/api/auth/register', methods=['POST'])
def api_register():
    """User registration"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate required fields
        required_fields = ['name', 'email', 'password', 'phone', 'city']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        # Validate email format (basic check)
        email = data['email'].lower().strip()
        if '@' not in email or '.' not in email:
            return jsonify({'error': 'Invalid email format'}), 400
        
        # Check if email already exists
        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email already registered'}), 400
        
        # Validate password length
        if len(data['password']) < 6:
            return jsonify({'error': 'Password must be at least 6 characters'}), 400
        
        # Create new user
        password_hash = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        user = User(
            name=data['name'].strip(),
            email=email,
            password_hash=password_hash,
            phone=data['phone'].strip(),
            city=data['city'].strip(),
            address=data.get('address', '').strip()
        )
        
        db.session.add(user)
        db.session.commit()
        
        login_user(user)
        session.permanent = True
        
        logger.info(f"New user registered: {email}, session: {session}")
        return jsonify({
            'message': 'Registration successful',
            'user': user.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        logger.error(f"Registration error: {e}")
        return jsonify({'error': 'Registration failed'}), 500

@app.route('/api/auth/login', methods=['POST'])
def api_login():
    """User login"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        if not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email and password are required'}), 400
        
        email = data['email'].lower().strip()
        user = User.query.filter_by(email=email, is_active=True).first()
        
        if user and bcrypt.check_password_hash(user.password_hash, data['password']):
            login_user(user, remember=True)
            session.permanent = True
            logger.info(f"User logged in: {email}, session: {session}")
            return jsonify({
                'message': 'Login successful',
                'user': user.to_dict()
            })
        else:
            return jsonify({'error': 'Invalid email or password'}), 401
    
    except Exception as e:
        logger.error(f"Login error: {e}")
        return jsonify({'error': 'Login failed'}), 500

@app.route('/api/auth/logout', methods=['POST'])
@login_required
def api_logout():
    """User logout"""
    try:
        logger.info(f"User logged out: {current_user.email}")
        logout_user()
        return jsonify({'message': 'Logged out successfully'})
    except Exception as e:
        logger.error(f"Logout error: {e}")
        return jsonify({'error': 'Logout failed'}), 500

@app.route('/api/profile', methods=['GET', 'PUT'])
@login_required
def api_profile():
    """Get or update user profile"""
    try:
        if request.method == 'GET':
            logger.info(f"Profile request for user: {current_user.email if current_user else 'None'}")
            logger.info(f"Session data: {dict(session)}")
            return jsonify(current_user.to_dict())
        
        elif request.method == 'PUT':
            data = request.get_json()
            
            if not data:
                return jsonify({'error': 'No data provided'}), 400
            
            # Update allowed fields
            if 'name' in data and data['name'].strip():
                current_user.name = data['name'].strip()
            if 'phone' in data:
                current_user.phone = data['phone'].strip()
            if 'city' in data and data['city'].strip():
                current_user.city = data['city'].strip()
            if 'address' in data:
                current_user.address = data['address'].strip()
            
            db.session.commit()
            
            logger.info(f"Profile updated for user: {current_user.email}")
            return jsonify({'message': 'Profile updated successfully'})
    
    except Exception as e:
        db.session.rollback()
        logger.error(f"Profile error: {e}")
        return jsonify({'error': 'Profile operation failed'}), 500

@app.route('/api/items', methods=['POST'])
@login_required
def api_create_item():
    """Create new item listing"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate required fields
        required_fields = ['title', 'description', 'category_id', 'size', 'price_per_day', 'security_deposit']
        for field in required_fields:
            if field not in data or data[field] == '':
                return jsonify({'error': f'{field} is required'}), 400
        
        # Validate category exists
        category = Category.query.get(data['category_id'])
        if not category:
            return jsonify({'error': 'Invalid category'}), 400
        
        # Validate numeric fields
        try:
            price_per_day = int(data['price_per_day'])
            security_deposit = int(data['security_deposit'])
            if price_per_day <= 0 or security_deposit < 0:
                raise ValueError("Invalid amount")
        except (ValueError, TypeError):
            return jsonify({'error': 'Invalid price or deposit amount'}), 400
        
        # Validate size
        valid_sizes = ['XS', 'S', 'M', 'L', 'XL', 'XXL']
        if data['size'] not in valid_sizes:
            return jsonify({'error': 'Invalid size'}), 400
        
        # Create item
        item = Item(
            title=data['title'].strip(),
            description=data['description'].strip(),
            category_id=data['category_id'],
            size=data['size'],
            price_per_day=price_per_day * 100,  # Convert to paise
            security_deposit=security_deposit * 100,
            owner_id=current_user.id,
            condition=data.get('condition', 'excellent')
        )
        
        db.session.add(item)
        db.session.commit()
        
        logger.info(f"Item created by user {current_user.email}: {item.title}")
        return jsonify({
            'message': 'Item listed successfully',
            'item_id': item.id
        }), 201
    
    except Exception as e:
        db.session.rollback()
        logger.error(f"Item creation error: {e}")
        return jsonify({'error': 'Failed to create item'}), 500

@app.route('/api/items/<int:item_id>/upload', methods=['POST'])
@login_required
def api_upload_item_images(item_id):
    """Upload images for an item"""
    try:
        item = Item.query.get_or_404(item_id)
        
        # Check if user owns the item
        if item.owner_id != current_user.id:
            return jsonify({'error': 'Permission denied'}), 403
        
        if 'images' not in request.files:
            return jsonify({'error': 'No images provided'}), 400
        
        files = request.files.getlist('images')
        uploaded_images = []
        
        for i, file in enumerate(files[:5]):  # Limit to 5 images
            if file and file.filename and allowed_file(file.filename):
                filename = save_image(file)
                if filename:
                    image = ItemImage(
                        item_id=item.id,
                        filename=filename,
                        is_primary=(i == 0 and not item.images)  # First image is primary if no images exist
                    )
                    db.session.add(image)
                    uploaded_images.append(filename)
        
        db.session.commit()
        
        logger.info(f"Images uploaded for item {item_id}: {len(uploaded_images)} files")
        return jsonify({
            'message': f'{len(uploaded_images)} images uploaded successfully',
            'images': uploaded_images
        })
    
    except Exception as e:
        db.session.rollback()
        logger.error(f"Image upload error: {e}")
        return jsonify({'error': 'Failed to upload images'}), 500

@app.route('/api/user/items')
@login_required
def api_user_items():
    """Get current user's items"""
    try:
        items = Item.query.filter_by(owner_id=current_user.id, is_active=True).order_by(Item.date_added.desc()).all()
        return jsonify([item.to_dict(include_owner=False) for item in items])
    except Exception as e:
        logger.error(f"Error fetching user items: {e}")
        return jsonify({'error': 'Failed to fetch items'}), 500


@app.route('/api/rentals', methods=['POST'])
@login_required
def api_create_rental():
    """Create rental request"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        required_fields = ['item_id', 'start_date', 'end_date']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        # Get item
        item = Item.query.get_or_404(data['item_id'])
        
        # Check if item is available
        if not item.is_active or item.status != 'available':
            return jsonify({'error': 'Item is not available'}), 400
        
        # Check if user is not the owner
        if item.owner_id == current_user.id:
            return jsonify({'error': 'You cannot rent your own item'}), 400
        
        # Parse dates
        try:
            start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
            end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
        
        # Validate dates
        if start_date < date.today():
            return jsonify({'error': 'Start date cannot be in the past'}), 400
        
        if end_date <= start_date:
            return jsonify({'error': 'End date must be after start date'}), 400
        
        # Check for conflicting rentals
        conflicting_rental = Rental.query.filter(
            Rental.item_id == item.id,
            Rental.status.in_(['approved', 'active']),
            or_(
                and_(Rental.start_date <= start_date, Rental.end_date >= start_date),
                and_(Rental.start_date <= end_date, Rental.end_date >= end_date),
                and_(Rental.start_date >= start_date, Rental.end_date <= end_date)
            )
        ).first()
        
        if conflicting_rental:
            return jsonify({'error': 'Item is not available for the selected dates'}), 400
        
        # Calculate cost
        total_amount = calculate_rental_cost(item, start_date, end_date)
        
        # Create rental
        rental = Rental(
            item_id=item.id,
            renter_id=current_user.id,
            owner_id=item.owner_id,
            start_date=start_date,
            end_date=end_date,
            total_amount=total_amount,
            security_deposit=item.security_deposit,
            message=data.get('message', '')
        )
        
        db.session.add(rental)
        db.session.commit()
        
        logger.info(f"Rental request created by {current_user.email} for item {item.id}")
        return jsonify({
            'message': 'Rental request sent successfully',
            'rental_id': rental.id,
            'total_amount': total_amount // 100,  # Convert to rupees
            'security_deposit': item.security_deposit // 100
        }), 201
    
    except Exception as e:
        db.session.rollback()
        logger.error(f"Rental creation error: {e}")
        return jsonify({'error': 'Failed to create rental request'}), 500

@app.route('/api/user/rentals')
@login_required
def api_user_rentals():
    """Get user's rentals (as renter and as owner)"""
    try:
        rental_type = request.args.get('type', 'rented')  # 'rented' or 'rented_out'
        
        if rental_type == 'rented':
            # Items user has rented from others
            rentals = Rental.query.filter_by(renter_id=current_user.id).order_by(Rental.date_requested.desc()).all()
        else:
            # Items others have rented from user
            rentals = Rental.query.filter_by(owner_id=current_user.id).order_by(Rental.date_requested.desc()).all()
        
        return jsonify([rental.to_dict() for rental in rentals])
    
    except Exception as e:
        logger.error(f"Error fetching user rentals: {e}")
        return jsonify({'error': 'Failed to fetch rentals'}), 500

@app.route('/api/rentals/<int:rental_id>/status', methods=['PUT'])
@login_required
def api_update_rental_status(rental_id):
    """Update rental status (owner only)"""
    try:
        rental = Rental.query.get_or_404(rental_id)
        
        # Check if user is the item owner
        if rental.owner_id != current_user.id:
            return jsonify({'error': 'Permission denied'}), 403
        
        data = request.get_json()
        if not data or 'status' not in data:
            return jsonify({'error': 'Status is required'}), 400
        
        new_status = data['status']
        
        allowed_transitions = {
            'pending': ['approved', 'cancelled'],
            'approved': ['active', 'cancelled'],
            'active': ['completed']
        }
        
        if new_status not in allowed_transitions.get(rental.status, []):
            return jsonify({'error': 'Invalid status transition'}), 400
        
        rental.status = new_status
        
        if new_status == 'approved':
            rental.date_approved = datetime.utcnow()
        elif new_status == 'active':
            rental.date_started = datetime.utcnow()
            rental.item.status = 'rented'
        elif new_status == 'completed':
            rental.date_completed = datetime.utcnow()
            rental.item.status = 'available'
        elif new_status == 'cancelled':
            rental.item.status = 'available'
        
        db.session.commit()
        
        logger.info(f"Rental {rental_id} status updated to {new_status}")
        return jsonify({'message': f'Rental status updated to {new_status}'})
    
    except Exception as e:
        db.session.rollback()
        logger.error(f"Rental status update error: {e}")
        return jsonify({'error': 'Failed to update rental status'}), 500

@app.route('/api/reviews', methods=['POST'])
@login_required
def api_create_review():
    """Create review for completed rental"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        required_fields = ['rental_id', 'rating']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'{field} is required'}), 400
        
        rental = Rental.query.get_or_404(data['rental_id'])
        
        # Check if user is the renter and rental is completed
        if rental.renter_id != current_user.id:
            return jsonify({'error': 'Permission denied'}), 403
        
        if rental.status != 'completed':
            return jsonify({'error': 'Can only review completed rentals'}), 400
        
        # Check if review already exists
        existing_review = Review.query.filter_by(rental_id=rental.id, reviewer_id=current_user.id).first()
        if existing_review:
            return jsonify({'error': 'Review already exists'}), 400
        
        # Validate rating
        try:
            rating = int(data['rating'])
            if rating < 1 or rating > 5:
                raise ValueError("Rating out of range")
        except (ValueError, TypeError):
            return jsonify({'error': 'Rating must be between 1 and 5'}), 400
        
        # Create review
        review = Review(
            item_id=rental.item_id,
            rental_id=rental.id,
            reviewer_id=current_user.id,
            rating=rating,
            comment=data.get('comment', '').strip()
        )
        
        db.session.add(review)
        
        # Update item rating
        item = rental.item
        total_rating = (item.rating * item.reviews_count) + rating
        item.reviews_count += 1
        item.rating = round(total_rating / item.reviews_count, 1)
        
        db.session.commit()
        
        logger.info(f"Review created for item {item.id} by user {current_user.email}")
        return jsonify({'message': 'Review added successfully'})
    
    except Exception as e:
        db.session.rollback()
        logger.error(f"Review creation error: {e}")
        return jsonify({'error': 'Failed to create review'}), 500

@app.route('/api/test')
def api_test():
    """Test endpoint to verify database and user creation"""
    try:
        with app.app_context():
            # Check if demo user exists
            demo_user = User.query.filter_by(email='demo@wearhouse.com').first()
            if demo_user:
                return jsonify({
                    'status': 'success',
                    'demo_user_exists': True,
                    'user_name': demo_user.name,
                    'user_email': demo_user.email,
                    'total_users': User.query.count()
                })
            else:
                return jsonify({
                    'status': 'error',
                    'demo_user_exists': False,
                    'total_users': User.query.count()
                })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        })

@app.route('/api/search')
@login_required
def api_search():
    """Advanced search with suggestions"""
    try:
        query = request.args.get('q', '').strip()
        
        if len(query) < 2:
            return jsonify({'items': [], 'suggestions': []})
        
        # Search items
        items = Item.query.filter(
            Item.is_active == True,
            or_(
                Item.title.ilike(f"%{query}%"),
                Item.description.ilike(f"%{query}%")
            )
        ).limit(20).all()
        
        # Generate suggestions
        suggestions = []
        categories = Category.query.filter(Category.name.ilike(f'%{query}%')).limit(5).all()
        suggestions.extend([cat.name for cat in categories])
        
        # Add popular search terms
        popular_terms = ['evening dress', 'wedding suit', 'party dress', 'formal wear', 'casual outfit']
        suggestions.extend([term for term in popular_terms if query.lower() in term.lower()][:3])
        
        return jsonify({
            'items': [{
                'id': item.id,
                'title': item.title,
                'price': item.price_per_day // 100,
                'category': item.category.name if item.category else 'Unknown',
                'owner_city': item.owner.city if item.owner else 'Unknown'
            } for item in items],
            'suggestions': suggestions[:8]
        })
    
    except Exception as e:
        logger.error(f"Search error: {e}")
        return jsonify({'error': 'Search failed'}), 500

# Initialize database and create sample data
def init_db():
    """Initialize database with sample data"""
    try:
        db.create_all()
        
        # Create categories if they don't exist
        categories_data = [
            {'name': 'Formal Wear', 'slug': 'formal', 'icon': '👔'},
            {'name': 'Casual Wear', 'slug': 'casual', 'icon': '👕'},
            {'name': 'Party Outfits', 'slug': 'party', 'icon': '✨'},
            {'name': 'Traditional', 'slug': 'traditional', 'icon': '🥻'},
            {'name': 'Accessories', 'slug': 'accessories', 'icon': '👜'},
            {'name': 'Designer', 'slug': 'designer', 'icon': '💎'}
        ]
        
        for cat_data in categories_data:
            if not Category.query.filter_by(slug=cat_data['slug']).first():
                category = Category(**cat_data)
                db.session.add(category)
        
        # Create demo users if they don't exist
        demo_users = [
            {
                'name': 'Demo User',
                'email': 'demo@wearhouse.com',
                'password': 'password123',
                'phone': '+91 9876543210',
                'city': 'Mumbai',
                'address': '123 Fashion Street, Mumbai'
            },
            {
                'name': 'Arjav',
                'email': 'arjav@rentrobe.com',
                'password': 'arjav0302',
                'phone': '+91 8319337033',
                'city': 'Bhilai',
                'address': 'Bhilai, Chhattisgarh'
            },
            {
                'name': 'Ankita',
                'email': 'ankita@rentrobe.com',
                'password': 'ankita1001',
                'phone': '+91 9876543211',
                'city': 'Delhi',
                'address': 'Delhi, India'
            }
        ]
        
        for user_data in demo_users:
            if not User.query.filter_by(email=user_data['email']).first():
                demo_user = User(
                    name=user_data['name'],
                    email=user_data['email'],
                    password_hash=bcrypt.generate_password_hash(user_data['password']).decode('utf-8'),
                    phone=user_data['phone'],
                    city=user_data['city'],
                    address=user_data['address'],
                    is_verified=True
                )
                db.session.add(demo_user)
        
        db.session.commit()
        logger.info("Database initialized successfully!")
        
    except Exception as e:
        logger.error(f"Database initialization error: {e}")
        db.session.rollback()

def create_sample_data():
    """Create sample items for testing"""
    try:
        categories = Category.query.all()
        users = User.query.all()
        
        if not categories or not users:
            logger.warning("Categories or users not found. Run init_db first.")
            return
        
        # Check if sample data already exists
        if Item.query.count() > 0:
            logger.info("Sample data already exists")
            return
        
        sample_items = [
            {
                'title': 'Elegant Black Evening Gown',
                'description': 'Stunning black evening gown perfect for formal events. Designer piece in excellent condition with intricate beadwork.',
                'category_slug': 'formal',
                'size': 'M',
                'price': 800,
                'deposit': 2000
            },
            {
                'title': 'Designer Cocktail Dress',
                'description': 'Beautiful red cocktail dress from a premium brand. Perfect for parties and special occasions.',
                'category_slug': 'party',
                'size': 'S',
                'price': 600,
                'deposit': 1500
            },
            {
                'title': 'Classic Navy Blue Suit',
                'description': 'Professional navy blue suit, perfect for business meetings and formal events.',
                'category_slug': 'formal',
                'size': 'L',
                'price': 700,
                'deposit': 1800
            },
            {
                'title': 'Traditional Lehenga Set',
                'description': 'Beautiful traditional lehenga with intricate embroidery. Perfect for weddings and festivals.',
                'category_slug': 'traditional',
                'size': 'M',
                'price': 1200,
                'deposit': 3000
            }
        ]
        
        for item_data in sample_items:
            category = Category.query.filter_by(slug=item_data['category_slug']).first()
            if category:
                item = Item(
                    title=item_data['title'],
                    description=item_data['description'],
                    category_id=category.id,
                    size=item_data['size'],
                    price_per_day=item_data['price'] * 100,  # Convert to paise
                    security_deposit=item_data['deposit'] * 100,
                    owner_id=users[0].id
                )
                db.session.add(item)
        
        db.session.commit()
        logger.info("Sample data created successfully!")
        
    except Exception as e:
        logger.error(f"Sample data creation error: {e}")
        db.session.rollback()

# CLI Commands
@app.cli.command()
def init_database():
    """Initialize database with sample data"""
    init_db()

@app.cli.command()
def create_samples():
    """Create sample items for testing"""
    create_sample_data()

@app.cli.command()
def create_admin():
    """Create an admin user"""
    name = input('Admin name: ')
    email = input('Admin email: ').lower().strip()
    password = input('Admin password: ')
    
    if User.query.filter_by(email=email).first():
        print('Email already exists!')
        return
    
    admin = User(
        name=name,
        email=email,
        password_hash=bcrypt.generate_password_hash(password).decode('utf-8'),
        phone='+91 0000000000',
        city='Admin City',
        is_verified=True
    )
    
    db.session.add(admin)
    db.session.commit()
    print(f'Admin user {name} created successfully!')

# Run the application
if __name__ == '__main__':
    # Initialize database on first run
    with app.app_context():
        init_db()
        
        # Create sample data in development
        if app.debug:
            create_sample_data()
    
    # Run the Flask app
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )