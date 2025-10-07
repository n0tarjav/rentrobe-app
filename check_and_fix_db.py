#!/usr/bin/env python3
"""
Check and fix sample data in the database
"""

from app import app, db, Item, User, Category, ItemImage
from datetime import datetime
import os

def check_database():
    """Check current database content"""
    with app.app_context():
        print("=== DATABASE CONTENT CHECK ===")
        
        # Check categories
        categories = Category.query.all()
        print(f"\nCategories ({len(categories)}):")
        for cat in categories:
            print(f"  - {cat.name} (slug: {cat.slug})")
        
        # Check users
        users = User.query.all()
        print(f"\nUsers ({len(users)}):")
        for user in users[:5]:  # Show first 5
            print(f"  - {user.name} ({user.email}) - {user.city}")
        if len(users) > 5:
            print(f"  ... and {len(users) - 5} more users")
        
        # Check items
        items = Item.query.all()
        print(f"\nItems ({len(items)}):")
        for item in items:
            category_name = item.category.name if item.category else "No Category"
            owner_name = item.owner.name if item.owner else "No Owner"
            print(f"  - {item.title} | {category_name} | {owner_name} | Rs.{item.price_per_day//100}/day")
        
        # Check images
        images = ItemImage.query.all()
        print(f"\nImages ({len(images)}):")
        for img in images[:5]:  # Show first 5
            print(f"  - Item {img.item_id}: {img.filename[:50]}...")
        if len(images) > 5:
            print(f"  ... and {len(images) - 5} more images")

def clear_and_recreate_sample_data():
    """Clear existing sample data and recreate it properly"""
    with app.app_context():
        print("\n=== CLEARING AND RECREATING SAMPLE DATA ===")
        
        # Clear existing data
        print("Clearing existing items and images...")
        ItemImage.query.delete()
        Item.query.delete()
        db.session.commit()
        
        # Get categories (create if needed)
        categories_data = [
            {'name': 'Formal Wear', 'slug': 'formal', 'icon': '👔'},
            {'name': 'Casual Wear', 'slug': 'casual', 'icon': '👕'},
            {'name': 'Party Outfits', 'slug': 'party', 'icon': '✨'},
            {'name': 'Traditional', 'slug': 'traditional', 'icon': '👘'},
            {'name': 'Accessories', 'slug': 'accessories', 'icon': '👜'}
        ]
        
        for cat_data in categories_data:
            existing = Category.query.filter_by(slug=cat_data['slug']).first()
            if not existing:
                category = Category(**cat_data)
                db.session.add(category)
        db.session.commit()
        
        # Get categories
        formal = Category.query.filter_by(slug='formal').first()
        casual = Category.query.filter_by(slug='casual').first()
        party = Category.query.filter_by(slug='party').first()
        traditional = Category.query.filter_by(slug='traditional').first()
        accessories = Category.query.filter_by(slug='accessories').first()
        
        # Get or create users
        users_data = [
            {'name': 'Priya Sharma', 'email': 'priya.sharma@example.com', 'city': 'Mumbai'},
            {'name': 'Anjali Reddy', 'email': 'anjali.reddy@example.com', 'city': 'Bangalore'},
            {'name': 'Rajesh Kumar', 'email': 'rajesh.kumar@example.com', 'city': 'Delhi'},
            {'name': 'Meera Patel', 'email': 'meera.patel@example.com', 'city': 'Ahmedabad'},
            {'name': 'Rahul Singh', 'email': 'rahul.singh@example.com', 'city': 'Pune'},
            {'name': 'Sneha Gupta', 'email': 'sneha.gupta@example.com', 'city': 'Chennai'},
            {'name': 'Kavya Nair', 'email': 'kavya.nair@example.com', 'city': 'Kochi'},
            {'name': 'Riya Jain', 'email': 'riya.jain@example.com', 'city': 'Jaipur'},
            {'name': 'Arjun Mehta', 'email': 'arjun.mehta@example.com', 'city': 'Hyderabad'},
            {'name': 'Lakshmi Iyer', 'email': 'lakshmi.iyer@example.com', 'city': 'Chennai'},
            {'name': 'Vikram Shah', 'email': 'vikram.shah@example.com', 'city': 'Mumbai'},
            {'name': 'Rohit Agarwal', 'email': 'rohit.agarwal@example.com', 'city': 'Delhi'},
            {'name': 'Pooja Kapoor', 'email': 'pooja.kapoor@example.com', 'city': 'Chandigarh'},
            {'name': 'Neha Verma', 'email': 'neha.verma@example.com', 'city': 'Lucknow'},
            {'name': 'Sanjay Gupta', 'email': 'sanjay.gupta@example.com', 'city': 'Varanasi'},
            {'name': 'Divya Rao', 'email': 'divya.rao@example.com', 'city': 'Bangalore'},
            {'name': 'Amit Sharma', 'email': 'amit.sharma@example.com', 'city': 'Gurgaon'},
            {'name': 'Shreya Patel', 'email': 'shreya.patel@example.com', 'city': 'Surat'},
            {'name': 'Karan Singh', 'email': 'karan.singh@example.com', 'city': 'Amritsar'},
            {'name': 'Anita Joshi', 'email': 'anita.joshi@example.com', 'city': 'Jodhpur'},
            {'name': 'Rahul Khanna', 'email': 'rahul.khanna@example.com', 'city': 'Mumbai'},
            {'name': 'Priyanka Das', 'email': 'priyanka.das@example.com', 'city': 'Kolkata'},
            {'name': 'Natasha Malhotra', 'email': 'natasha.malhotra@example.com', 'city': 'Delhi'},
            {'name': 'Suresh Kumar', 'email': 'suresh.kumar@example.com', 'city': 'Patna'},
            {'name': 'Geeta Sharma', 'email': 'geeta.sharma@example.com', 'city': 'Varanasi'}
        ]
        
        for user_data in users_data:
            existing = User.query.filter_by(email=user_data['email']).first()
            if not existing:
                user = User(
                    name=user_data['name'],
                    email=user_data['email'],
                    password_hash='demo_password_hash',
                    phone='9876543210',
                    city=user_data['city'],
                    is_verified=True
                )
                db.session.add(user)
        db.session.commit()
        
        # Create sample items matching the frontend exactly
        sample_items = [
            {
                'title': 'Black Evening Gown',
                'description': 'Elegant black evening gown perfect for formal events.',
                'category': formal,
                'size': 'M',
                'price': 800,
                'deposit': 2000,
                'owner_email': 'priya.sharma@example.com',
                'images': [
                    'https://images.unsplash.com/photo-1657023855158-3878cac29205?w=400&h=400&fit=crop&crop=center',
                    'https://images.unsplash.com/photo-1657023799657-df1cee617db5?w=400&h=400&fit=crop&crop=center'
                ]
            },
            {
                'title': 'Premium Cocktail Dress',
                'description': 'Beautiful red cocktail dress from premium brand.',
                'category': party,
                'size': 'S',
                'price': 600,
                'deposit': 1500,
                'owner_email': 'anjali.reddy@example.com',
                'images': [
                    'https://images.unsplash.com/photo-1721182421063-19a6c711b719?w=400&h=600&fit=crop&crop=center',
                    'https://images.unsplash.com/photo-1721182420935-29bfb69dd26c?w=400&h=600&fit=crop&crop=center'
                ]
            },
            {
                'title': 'Navy Blue Business Suit',
                'description': 'Professional navy suit perfect for business meetings.',
                'category': formal,
                'size': 'L',
                'price': 700,
                'deposit': 1800,
                'owner_email': 'rajesh.kumar@example.com',
                'images': [
                    'https://plus.unsplash.com/premium_photo-1679440414275-f9950b562c7f?w=400&h=600&fit=crop&crop=center',
                    'https://plus.unsplash.com/premium_photo-1679440413349-556c1366112f?w=400&h=600&fit=crop&crop=center'
                ]
            },
            {
                'title': 'Traditional Lehenga',
                'description': 'Beautiful traditional lehenga with embroidery work.',
                'category': traditional,
                'size': 'M',
                'price': 1200,
                'deposit': 3000,
                'owner_email': 'meera.patel@example.com',
                'images': [
                    'https://plus.unsplash.com/premium_photo-1682096032284-0b2ab20b65dd?w=400&h=600&fit=crop&crop=center',
                    'https://plus.unsplash.com/premium_photo-1682096067532-3e89ab323ebf?w=400&h=600&fit=crop&crop=center'
                ]
            },
            {
                'title': 'Casual Denim Jacket',
                'description': 'Trendy denim jacket perfect for casual outings.',
                'category': casual,
                'size': 'L',
                'price': 300,
                'deposit': 800,
                'owner_email': 'rahul.singh@example.com',
                'images': [
                    'https://images.unsplash.com/photo-1517841905240-472988babdf9?w=400&h=600&fit=crop&crop=center',
                    'https://images.unsplash.com/photo-1520423465871-0866049020b7?w=400&h=600&fit=crop&crop=center'
                ]
            },
            {
                'title': 'Luxury Handbag',
                'description': 'Luxury handbag in pristine condition.',
                'category': accessories,
                'size': 'One Size',
                'price': 500,
                'deposit': 1200,
                'owner_email': 'sneha.gupta@example.com',
                'images': [
                    'https://images.unsplash.com/photo-1652427019217-3ded1a356f10?w=400&h=600&fit=crop&crop=center',
                    'https://images.unsplash.com/photo-1652427019219-0be0fb8855c1?w=400&h=600&fit=crop&crop=center'
                ]
            },
            {
                'title': 'White Wedding Dress',
                'description': 'Stunning white wedding dress with lace details.',
                'category': formal,
                'size': 'S',
                'price': 1500,
                'deposit': 4000,
                'owner_email': 'kavya.nair@example.com',
                'images': [
                    'https://images.unsplash.com/photo-1594736797933-d0401ba2fe65?w=400&h=600&fit=crop&crop=center'
                ]
            },
            {
                'title': 'Pink Party Dress',
                'description': 'Vibrant pink dress perfect for parties and celebrations.',
                'category': party,
                'size': 'M',
                'price': 450,
                'deposit': 1000,
                'owner_email': 'riya.jain@example.com',
                'images': [
                    'https://images.unsplash.com/photo-1515372039744-b8f02a3ae446?w=400&h=600&fit=crop&crop=center'
                ]
            },
            {
                'title': 'Blue Casual Shirt',
                'description': 'Comfortable blue casual shirt for everyday wear.',
                'category': casual,
                'size': 'M',
                'price': 200,
                'deposit': 500,
                'owner_email': 'arjun.mehta@example.com',
                'images': [
                    'https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=400&h=600&fit=crop&crop=center'
                ]
            },
            {
                'title': 'Golden Saree',
                'description': 'Traditional golden saree with intricate work.',
                'category': traditional,
                'size': 'One Size',
                'price': 900,
                'deposit': 2200,
                'owner_email': 'lakshmi.iyer@example.com',
                'images': [
                    'https://images.unsplash.com/photo-1583391733956-6c78276477e2?w=400&h=600&fit=crop&crop=center'
                ]
            },
            {
                'title': 'Luxury Watch',
                'description': 'Luxury watch in excellent condition.',
                'category': accessories,
                'size': 'One Size',
                'price': 800,
                'deposit': 2000,
                'owner_email': 'vikram.shah@example.com',
                'images': [
                    'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400&h=400&fit=crop&crop=center'
                ]
            },
            {
                'title': 'Black Tuxedo',
                'description': 'Classic black tuxedo for formal occasions.',
                'category': formal,
                'size': 'L',
                'price': 1000,
                'deposit': 2500,
                'owner_email': 'rohit.agarwal@example.com',
                'images': [
                    'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=600&fit=crop&crop=center'
                ]
            },
            {
                'title': 'Green Cocktail Dress',
                'description': 'Elegant green cocktail dress for special events.',
                'category': party,
                'size': 'S',
                'price': 550,
                'deposit': 1300,
                'owner_email': 'pooja.kapoor@example.com',
                'images': [
                    'https://images.unsplash.com/photo-1566479179817-c0c8e5c7b7b8?w=400&h=600&fit=crop&crop=center'
                ]
            },
            {
                'title': 'White Sneakers',
                'description': 'Trendy white sneakers perfect for casual outfits.',
                'category': casual,
                'size': '8',
                'price': 250,
                'deposit': 600,
                'owner_email': 'neha.verma@example.com',
                'images': [
                    'https://images.unsplash.com/photo-1549298916-b41d501d3772?w=400&h=400&fit=crop&crop=center'
                ]
            },
            {
                'title': 'Red Traditional Kurta',
                'description': 'Beautiful red kurta with traditional embroidery.',
                'category': traditional,
                'size': 'L',
                'price': 400,
                'deposit': 900,
                'owner_email': 'sanjay.gupta@example.com',
                'images': [
                    'https://images.unsplash.com/photo-1622470953794-aa9c70b0fb9d?w=400&h=600&fit=crop&crop=center'
                ]
            },
            {
                'title': 'Pearl Necklace',
                'description': 'Elegant pearl necklace for special occasions.',
                'category': accessories,
                'size': 'One Size',
                'price': 600,
                'deposit': 1500,
                'owner_email': 'divya.rao@example.com',
                'images': [
                    'https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=400&h=400&fit=crop&crop=center'
                ]
            },
            {
                'title': 'Grey Business Suit',
                'description': 'Professional grey suit for corporate meetings.',
                'category': formal,
                'size': 'M',
                'price': 750,
                'deposit': 1900,
                'owner_email': 'amit.sharma@example.com',
                'images': [
                    'https://images.unsplash.com/photo-1594938298603-c8148c4dae35?w=400&h=600&fit=crop&crop=center'
                ]
            },
            {
                'title': 'Purple Party Gown',
                'description': 'Stunning purple gown perfect for evening parties.',
                'category': party,
                'size': 'L',
                'price': 700,
                'deposit': 1700,
                'owner_email': 'shreya.patel@example.com',
                'images': [
                    'https://images.unsplash.com/photo-1566479179817-c0c8e5c7b7b8?w=400&h=600&fit=crop&crop=center'
                ]
            },
            {
                'title': 'Denim Jeans',
                'description': 'Classic blue denim jeans for casual wear.',
                'category': casual,
                'size': '32',
                'price': 180,
                'deposit': 450,
                'owner_email': 'karan.singh@example.com',
                'images': [
                    'https://images.unsplash.com/photo-1542272604-787c3835535d?w=400&h=600&fit=crop&crop=center'
                ]
            },
            {
                'title': 'Silk Dupatta',
                'description': 'Beautiful silk dupatta with golden border.',
                'category': traditional,
                'size': 'One Size',
                'price': 300,
                'deposit': 700,
                'owner_email': 'anita.joshi@example.com',
                'images': [
                    'https://images.unsplash.com/photo-1583391733956-6c78276477e2?w=400&h=600&fit=crop&crop=center'
                ]
            },
            {
                'title': 'Premium Sunglasses',
                'description': 'Stylish sunglasses with UV protection.',
                'category': accessories,
                'size': 'One Size',
                'price': 350,
                'deposit': 800,
                'owner_email': 'rahul.khanna@example.com',
                'images': [
                    'https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=400&h=400&fit=crop&crop=center'
                ]
            },
            {
                'title': 'Maroon Blazer',
                'description': 'Elegant maroon blazer for formal occasions.',
                'category': formal,
                'size': 'S',
                'price': 650,
                'deposit': 1600,
                'owner_email': 'priyanka.das@example.com',
                'images': [
                    'https://images.unsplash.com/photo-1594938298603-c8148c4dae35?w=400&h=600&fit=crop&crop=center'
                ]
            },
            {
                'title': 'Silver Sequin Dress',
                'description': 'Glamorous silver sequin dress for parties.',
                'category': party,
                'size': 'M',
                'price': 800,
                'deposit': 2000,
                'owner_email': 'natasha.malhotra@example.com',
                'images': [
                    'https://images.unsplash.com/photo-1515372039744-b8f02a3ae446?w=400&h=600&fit=crop&crop=center'
                ]
            },
            {
                'title': 'Cotton T-Shirt',
                'description': 'Comfortable cotton t-shirt for daily wear.',
                'category': casual,
                'size': 'L',
                'price': 150,
                'deposit': 350,
                'owner_email': 'suresh.kumar@example.com',
                'images': [
                    'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400&h=600&fit=crop&crop=center'
                ]
            },
            {
                'title': 'Banarasi Silk Saree',
                'description': 'Exquisite Banarasi silk saree with gold work.',
                'category': traditional,
                'size': 'One Size',
                'price': 1100,
                'deposit': 2800,
                'owner_email': 'geeta.sharma@example.com',
                'images': [
                    'https://images.unsplash.com/photo-1583391733956-6c78276477e2?w=400&h=600&fit=crop&crop=center'
                ]
            }
        ]
        
        print(f"Adding {len(sample_items)} items...")
        
        for item_data in sample_items:
            # Find owner
            owner = User.query.filter_by(email=item_data['owner_email']).first()
            if not owner:
                print(f"Warning: Owner not found for {item_data['title']}")
                continue
                
            # Create item
            item = Item(
                title=item_data['title'],
                description=item_data['description'],
                category_id=item_data['category'].id,
                size=item_data['size'],
                price_per_day=item_data['price'] * 100,  # Convert to paise
                security_deposit=item_data['deposit'] * 100,  # Convert to paise
                owner_id=owner.id,
                status='available',
                condition='excellent'
            )
            
            db.session.add(item)
            db.session.flush()  # Get the item ID
            
            # Add images
            for i, image_url in enumerate(item_data['images']):
                image = ItemImage(
                    item_id=item.id,
                    filename=image_url,
                    is_primary=(i == 0)
                )
                db.session.add(image)
            
            print(f"  ✓ Added: {item_data['title']}")
        
        db.session.commit()
        print(f"\n✅ Successfully added {len(sample_items)} items to database!")

def main():
    """Main function"""
    print("WEARHOUSE DATABASE CHECKER AND FIXER")
    print("=" * 50)
    
    # First check what's currently in the database
    check_database()
    
    # Ask user what to do
    print("\n" + "=" * 50)
    print("OPTIONS:")
    print("1. Clear and recreate all sample data")
    print("2. Just check database content (done above)")
    print("3. Exit")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == '1':
        clear_and_recreate_sample_data()
        print("\n" + "=" * 50)
        print("FINAL DATABASE STATE:")
        check_database()
    elif choice == '2':
        print("Database check completed.")
    else:
        print("Exiting...")

if __name__ == "__main__":
    main()
