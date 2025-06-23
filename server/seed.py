from app import db, Plant

def seed():
    # Clear existing data
    db.drop_all()
    db.create_all()
    
    # Add sample plants
    plants = [
        Plant(name="Aloe", image="./images/aloe.jpg", price=11.50, is_in_stock=True),
        Plant(name="Cactus", image="./images/cactus.jpg", price=15.00, is_in_stock=True),
    ]
    db.session.bulk_save_objects(plants)
    db.session.commit()
    print("Database seeded successfully!")

if __name__ == "__main__":
    from app import app
    with app.app_context():
        seed()