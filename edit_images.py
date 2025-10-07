#!/usr/bin/env python3
"""
Script to edit image links in the database
"""

from app import app, db, Item, ItemImage

def show_items_with_images():
    with app.app_context():
        items = Item.query.all()
        print("\n" + "="*80)
        print("ITEMS WITH IMAGES")
        print("="*80)
        
        for item in items:
            images = ItemImage.query.filter_by(item_id=item.id).all()
            print(f"\nItem ID: {item.id}")
            print(f"Title: {item.title}")
            print(f"Images ({len(images)}):")
            
            for i, img in enumerate(images, 1):
                print(f"  {i}. {img.filename} (Primary: {img.is_primary})")
            print("-" * 80)

def edit_image_link():
    with app.app_context():
        show_items_with_images()
        
        item_id = input("\nEnter item ID to edit images: ")
        try:
            item = Item.query.get(int(item_id))
            if not item:
                print("Item not found!")
                return
            
            images = ItemImage.query.filter_by(item_id=item.id).all()
            if not images:
                print("No images found for this item!")
                return
            
            print(f"\nEditing images for: {item.title}")
            print("Current images:")
            for i, img in enumerate(images, 1):
                print(f"  {i}. {img.filename} (Primary: {img.is_primary})")
            
            image_choice = input(f"\nWhich image to edit (1-{len(images)}): ")
            try:
                image_index = int(image_choice) - 1
                if 0 <= image_index < len(images):
                    selected_image = images[image_index]
                    print(f"\nCurrent URL: {selected_image.filename}")
                    
                    new_url = input("Enter new image URL: ").strip()
                    if new_url:
                        selected_image.filename = new_url
                        db.session.commit()
                        print("Image URL updated successfully!")
                    else:
                        print("No changes made.")
                else:
                    print("Invalid image number!")
            except ValueError:
                print("Invalid input!")
                
        except ValueError:
            print("Invalid item ID!")
        except Exception as e:
            print(f"Error: {e}")
            db.session.rollback()

def add_image_to_item():
    with app.app_context():
        show_items_with_images()
        
        item_id = input("\nEnter item ID to add image to: ")
        try:
            item = Item.query.get(int(item_id))
            if not item:
                print("Item not found!")
                return
            
            print(f"\nAdding image to: {item.title}")
            new_url = input("Enter new image URL: ").strip()
            if not new_url:
                print("No URL provided!")
                return
            
            # Check if this will be the first image (primary)
            existing_images = ItemImage.query.filter_by(item_id=item.id).count()
            is_primary = existing_images == 0
            
            new_image = ItemImage(
                item_id=item.id,
                filename=new_url,
                is_primary=is_primary
            )
            
            db.session.add(new_image)
            db.session.commit()
            print("Image added successfully!")
            
        except ValueError:
            print("Invalid item ID!")
        except Exception as e:
            print(f"Error: {e}")
            db.session.rollback()

def delete_image():
    with app.app_context():
        show_items_with_images()
        
        item_id = input("\nEnter item ID to delete image from: ")
        try:
            item = Item.query.get(int(item_id))
            if not item:
                print("Item not found!")
                return
            
            images = ItemImage.query.filter_by(item_id=item.id).all()
            if not images:
                print("No images found for this item!")
                return
            
            print(f"\nDeleting image from: {item.title}")
            print("Current images:")
            for i, img in enumerate(images, 1):
                print(f"  {i}. {img.filename} (Primary: {img.is_primary})")
            
            image_choice = input(f"\nWhich image to delete (1-{len(images)}): ")
            try:
                image_index = int(image_choice) - 1
                if 0 <= image_index < len(images):
                    selected_image = images[image_index]
                    confirm = input(f"Delete '{selected_image.filename}'? (yes/no): ")
                    if confirm.lower() == 'yes':
                        db.session.delete(selected_image)
                        db.session.commit()
                        print("Image deleted successfully!")
                    else:
                        print("Deletion cancelled.")
                else:
                    print("Invalid image number!")
            except ValueError:
                print("Invalid input!")
                
        except ValueError:
            print("Invalid item ID!")
        except Exception as e:
            print(f"Error: {e}")
            db.session.rollback()

def main():
    while True:
        print("\n" + "="*50)
        print("IMAGE EDITOR")
        print("="*50)
        print("1. View all items with images")
        print("2. Edit image URL")
        print("3. Add new image to item")
        print("4. Delete image from item")
        print("0. Exit")
        print("="*50)
        
        choice = input("Enter your choice (0-4): ").strip()
        
        if choice == '0':
            print("Goodbye!")
            break
        elif choice == '1':
            show_items_with_images()
        elif choice == '2':
            edit_image_link()
        elif choice == '3':
            add_image_to_item()
        elif choice == '4':
            delete_image()
        else:
            print("Invalid choice! Please try again.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
