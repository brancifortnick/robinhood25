from app.models import db, PortfolioStocks
import requests
import os
import time


def get_stock_price(ticker):
    """
    Fetch current stock price from Alpha Vantage API
    Returns the price or a fallback value if API fails
    """
    api_key = os.getenv('ALPHA_VANTAGE_API_KEY')
    
    if not api_key:
        print(f"⚠️  No API key found. Using fallback price for {ticker}")
        # Fallback prices if no API key
        fallback_prices = {
            'AAPL': 175.00,
            'TSLA': 240.00,
            'JPM': 145.00,
            'MSFT': 370.00,
            'GOOGL': 140.00,
            'AMZN': 150.00,
            'META': 330.00,
            'NVDA': 495.00
        }
        return fallback_prices.get(ticker, 100.00)
    
    try:
        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker}&apikey={api_key}"
        print(f"📊 Fetching price for {ticker}...")
        
        response = requests.get(url, timeout=10)
        data = response.json()
        
        # Check for rate limiting
        if 'Note' in data:
            print(f"⚠️  API rate limit reached. Using fallback price for {ticker}")
            time.sleep(1)  # Brief pause before next call
            return 100.00
        
        # Extract price from Global Quote
        global_quote = data.get('Global Quote', {})
        if global_quote and '05. price' in global_quote:
            price = float(global_quote['05. price'])
            print(f"✅ {ticker}: ${price:.2f}")
            time.sleep(12)  # Alpha Vantage free tier: 5 calls per minute (wait 12 seconds)
            return price
        else:
            print(f"⚠️  No price data for {ticker}. Using fallback.")
            return 100.00
            
    except Exception as e:
        print(f"❌ Error fetching {ticker}: {e}")
        return 100.00


def seed_portfolio_stocks():
    """
    Seed portfolio with real stock prices from Alpha Vantage API
    """
    print("\n" + "="*50)
    print("🌱 Seeding Portfolio Stocks with Real Prices")
    print("="*50 + "\n")
    
    # Define portfolio with tickers and quantities
    portfolio_data = [
        {'ticker': 'AAPL', 'shares': 5, 'user_id': 1},
        {'ticker': 'TSLA', 'shares': 3, 'user_id': 1},
        {'ticker': 'MSFT', 'shares': 2, 'user_id': 1},
        {'ticker': 'JPM', 'shares': 4, 'user_id': 2},
        {'ticker': 'GOOGL', 'shares': 2, 'user_id': 2},
        {'ticker': 'NVDA', 'shares': 3, 'user_id': 3},
    ]
    
    # Create portfolio stocks with real prices
    for stock_info in portfolio_data:
        ticker = stock_info['ticker']
        shares = stock_info['shares']
        user_id = stock_info['user_id']
        
        # Get real price from API
        price = get_stock_price(ticker)
        basis = price  # Use current price as basis
        
        portfolio_stock = PortfolioStocks(
            ticker=ticker,
            basis=basis,
            share_count=shares,
            user_id=user_id
        )
        
        db.session.add(portfolio_stock)
        print(f"   Added: {shares} shares of {ticker} @ ${basis:.2f} for User {user_id}")
    
    db.session.commit()
    
    print("\n" + "="*50)
    print("✅ Portfolio stocks seeded successfully!")
    print("="*50 + "\n")


def undo_portfolio_stocks():
    db.session.execute('TRUNCATE portfolio_stocks RESTART IDENTITY CASCADE;')
    db.session.commit()
