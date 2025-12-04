from app.models import db, WatchlistStocks


def seed_watchlist():
    """
    Seed watchlist with popular stocks for demo users
    """
    print("\n🌱 Seeding Watchlist Stocks...")
    
    # Watchlist data: popular tech and finance stocks
    watchlist_data = [
        # User 1 (Demo) - Tech focused
        {'ticker': 'AAPL', 'user_id': 1},
        {'ticker': 'TSLA', 'user_id': 1},
        {'ticker': 'MSFT', 'user_id': 1},
        {'ticker': 'GOOGL', 'user_id': 1},
        {'ticker': 'META', 'user_id': 1},
        {'ticker': 'NVDA', 'user_id': 1},
        {'ticker': 'AMD', 'user_id': 1},
        
        # User 2 (Marnie) - Mixed portfolio
        {'ticker': 'JPM', 'user_id': 2},
        {'ticker': 'GOOGL', 'user_id': 2},
        {'ticker': 'BAC', 'user_id': 2},
        {'ticker': 'WMT', 'user_id': 2},
        {'ticker': 'V', 'user_id': 2},
        
        # User 3 (Bobbie) - Growth stocks
        {'ticker': 'NVDA', 'user_id': 3},
        {'ticker': 'AMZN', 'user_id': 3},
        {'ticker': 'NFLX', 'user_id': 3},
        {'ticker': 'DIS', 'user_id': 3},
    ]
    
    for item in watchlist_data:
        watchlist_stock = WatchlistStocks(
            ticker=item['ticker'],
            user_id=item['user_id']
        )
        db.session.add(watchlist_stock)
    
    db.session.commit()
    print("✅ Watchlist stocks seeded successfully!\n")


def undo_watchlist():
    db.session.execute('TRUNCATE watchlist_stocks RESTART IDENTITY CASCADE;')
    db.session.commit()
