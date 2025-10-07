#!/usr/bin/env python3
"""
Interactive database editor for wearhouse.db
"""

from app import app, db, Item, User, Category, Rental, ItemImage
from datetime import datetime

def show_menu():
    print("\n" + "="*50)
    print("WEARHOUSE DATABASE EDITOR")
    print("="*50)
    print("1. View all items")
    print("2. View all users")
    print("3. View all categories")
    print("4. View all rentals")
    print("5. Edit an item")
    print("6. Edit a user")
    print("7. Add new item")
    print("8. Add new user")
    print("9. Delete an item")
    print("10. Delete a user")
    print("0. Exit")
    print("="*50)

def view_items():
    with app.app_context():
        items = Item.query.all()
        print(f"\nTOTAL ITEMS: {len(items)}")
        print("-" * 80)
        for item in items:
            print(f"ID: {item.id}")
            print(f"Title: {item.title}")
            print(f"Owner: {item.owner.name if item.owner else 'Unknown'}")
            print(f"Category: {item.category.name if item.category else 'Unknown'}")
            print(f"Price: Rs.{item.price_per_day//100}/day")
            print(f"Status: {item.status}")
            print("-" * 80)

def view_users():
    with app.app_context():
        users = User.query.all()
        print(f"\nTOTAL USERS: {len(users)}")
        print("-" * 60)
        for user in users:
            print(f"ID: {user.id}")
            print(f"Name: {user.name}")
            print(f"Email: {user.email}")
            print(f"City: {user.city}")
            print(f"Phone: {user.phone}")
            print("-" * 60)

def view_categories():
    with app.app_context():
        categories = Category.query.all()
        print(f"\nTOTAL CATEGORIES: {len(categories)}")
        print("-" * 40)
        for cat in categories:
            print(f"ID: {cat.id}")
            print(f"Name: {cat.name}")
            print(f"Slug: {cat.slug}")
            print("-" * 40)

def view_rentals():
    with app.app_context():
        rentals = Rental.query.all()
        print(f"\nTOTAL RENTALS: {len(rentals)}")
        print("-" * 80)
        for rental in rentals:
            print(f"ID: {rental.id}")
            print(f"Item: {rental.item.title if rental.item else 'Unknown'}")
            print(f"Renter: {rental.renter.name if rental.renter else 'Unknown'}")
            print(f"Owner: {rental.item_owner.name if rental.item_owner else 'Unknown'}")
            print(f"Status: {rental.status}")
            print(f"Dates: {rental.start_date} to {rental.end_date}")
            print("-" * 80)

def edit_item():
    with app.app_context():
        item_id = input("\nEnter item ID to edit: ")
        try:
            item = Item.query.get(int(item_id))
            if not item:
                print("Item not found!")
                return
            
            print(f"\nEditing: {item.title}")
            print("Press Enter to keep current value")
            
            new_title = input(f"Title [{item.title}]: ").strip()
            if new_title:
                item.title = new_title
            
            new_desc = input(f"Description [{item.description}]: ").strip()
            if new_desc:
                item.description = new_desc
            
            new_price = input(f"Price per day [{item.price_per_day//100}]: ").strip()
            if new_price:
                item.price_per_day = int(new_price) * 100
            
            new_deposit = input(f"Security deposit [{item.security_deposit//100}]: ").strip()
            if new_deposit:
                item.security_deposit = int(new_deposit) * 100
            
            new_status = input(f"Status [{item.status}]: ").strip()
            if new_status:
                item.status = new_status
            
            db.session.commit()
            print("Item updated successfully!")
            
        except ValueError:
            print("Invalid item ID!")
        except Exception as e:
            print(f"Error: {e}")
            db.session.rollback()

def edit_user():
    with app.app_context():
        user_id = input("\nEnter user ID to edit: ")
        try:
            user = User.query.get(int(user_id))
            if not user:
                print("User not found!")
                return
            
            print(f"\nEditing: {user.name}")
            print("Press Enter to keep current value")
            
            new_name = input(f"Name [{user.name}]: ").strip()
            if new_name:
                user.name = new_name
            
            new_city = input(f"City [{user.city}]: ").strip()
            if new_city:
                user.city = new_city
            
            new_phone = input(f"Phone [{user.phone}]: ").strip()
            if new_phone:
                user.phone = new_phone
            
            db.session.commit()
            print("User updated successfully!")
            
        except ValueError:
            print("Invalid user ID!")
        except Exception as e:
            print(f"Error: {e}")
            db.session.rollback()

def add_item():
    with app.app_context():
        print("\nAdding new item...")
        try:
            title = input("Title: ").strip()
            description = input("Description: ").strip()
            size = input("Size (XS/S/M/L/XL/XXL): ").strip().upper()
            price = int(input("Price per day (Rs): "))
            deposit = int(input("Security deposit (Rs): "))
            
            # Get categories
            categories = Category.query.all()
            print("\nAvailable categories:")
            for cat in categories:
                print(f"{cat.id}. {cat.name}")
            
            category_id = int(input("Category ID: "))
            category = Category.query.get(category_id)
            if not category:
                print("Invalid category ID!")
                return
            
            # Get users
            users = User.query.all()
            print("\nAvailable users:")
            for user in users:
                print(f"{user.id}. {user.name} ({user.email})")
            
            owner_id = int(input("Owner ID: "))
            owner = User.query.get(owner_id)
            if not owner:
                print("Invalid owner ID!")
                return
            
            item = Item(
                title=title,
                description=description,
                category_id=category_id,
                size=size,
                price_per_day=price * 100,
                security_deposit=deposit * 100,
                owner_id=owner_id,
                status='available',
                condition='excellent'
            )
            
            db.session.add(item)
            db.session.commit()
            print(f"Item '{title}' added successfully!")
            
        except ValueError:
            print("Invalid input!")
        except Exception as e:
            print(f"Error: {e}")
            db.session.rollback()

def add_user():
    with app.app_context():
        print("\nAdding new user...")
        try:
            name = input("Name: ").strip()
            email = input("Email: ").strip()
            phone = input("Phone: ").strip()
            city = input("City: ").strip()
            
            # Check if email already exists
            if User.query.filter_by(email=email).first():
                print("Email already exists!")
                return
            
            user = User(
                name=name,
                email=email,
                password_hash='demo_password_hash',  # Demo password
                phone=phone,
                city=city,
                is_verified=True
            )
            
            db.session.add(user)
            db.session.commit()
            print(f"User '{name}' added successfully!")
            
        except Exception as e:
            print(f"Error: {e}")
            db.session.rollback()

def delete_item():
    with app.app_context():
        item_id = input("\nEnter item ID to delete: ")
        try:
            item = Item.query.get(int(item_id))
            if not item:
                print("Item not found!")
                return
            
            confirm = input(f"Are you sure you want to delete '{item.title}'? (yes/no): ")
            if confirm.lower() == 'yes':
                # Delete associated images first
                ItemImage.query.filter_by(item_id=item.id).delete()
                # Delete the item
                db.session.delete(item)
                db.session.commit()
                print("Item deleted successfully!")
            else:
                print("Deletion cancelled.")
                
        except ValueError:
            print("Invalid item ID!")
        except Exception as e:
            print(f"Error: {e}")
            db.session.rollback()

def delete_user():
    with app.app_context():
        user_id = input("\nEnter user ID to delete: ")
        try:
            user = User.query.get(int(user_id))
            if not user:
                print("User not found!")
                return
            
            confirm = input(f"Are you sure you want to delete '{user.name}'? (yes/no): ")
            if confirm.lower() == 'yes':
                # Delete user's items and associated data
                items = Item.query.filter_by(owner_id=user.id).all()
                for item in items:
                    ItemImage.query.filter_by(item_id=item.id).delete()
                    db.session.delete(item)
                
                db.session.delete(user)
                db.session.commit()
                print("User and all associated data deleted successfully!")
            else:
                print("Deletion cancelled.")
                
        except ValueError:
            print("Invalid user ID!")
        except Exception as e:
            print(f"Error: {e}")
            db.session.rollback()

def main():
    while True:
        show_menu()
        choice = input("\nEnter your choice (0-10): ").strip()
        
        if choice == '0':
            print("Goodbye!")
            break
        elif choice == '1':
            view_items()
        elif choice == '2':
            view_users()
        elif choice == '3':
            view_categories()
        elif choice == '4':
            view_rentals()
        elif choice == '5':
            edit_item()
        elif choice == '6':
            edit_user()
        elif choice == '7':
            add_item()
        elif choice == '8':
            add_user()
        elif choice == '9':
            delete_item()
        elif choice == '10':
            delete_user()
        else:
            print("Invalid choice! Please try again.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
