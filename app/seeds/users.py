from app.models import db, User


# Adds a demo user, you can add other users here if you want
def seed_users():
    """
    Seed demo users with starting cash balances
    """
    print("\n" + "="*50)
    print("🌱 Seeding Users")
    print("="*50 + "\n")
    
    demo = User(
        username='Demo', 
        email='demo@aa.io', 
        password='password', 
        cash_balance=25000.00
    )
    marnie = User(
        username='marnie', 
        email='marnie@aa.io', 
        password='password', 
        cash_balance=50000.00
    )
    bobbie = User(
        username='bobbie', 
        email='bobbie@aa.io', 
        password='password', 
        cash_balance=15000.00
    )

    db.session.add(demo)
    db.session.add(marnie)
    db.session.add(bobbie)

    db.session.commit()
    
    print("✅ Users seeded:")
    print(f"   • Demo - $25,000.00")
    print(f"   • Marnie - $50,000.00")
    print(f"   • Bobbie - $15,000.00")
    print()


# Uses a raw SQL query to TRUNCATE the users table.
# SQLAlchemy doesn't have a built in function to do this
# TRUNCATE Removes all the data from the table, and RESET IDENTITY
# resets the auto incrementing primary key, CASCADE deletes any
# dependent entities
def undo_users():
    db.session.execute('TRUNCATE users RESTART IDENTITY CASCADE;')
    db.session.commit()
