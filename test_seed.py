#!/usr/bin/env python3
"""
Seed Data Helper Script
Tests the Alpha Vantage API integration for seeding
"""

import os
import sys
import requests
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def test_single_stock(ticker):
    """Test fetching a single stock price"""
    api_key = os.getenv('ALPHA_VANTAGE_API_KEY')
    
    if not api_key:
        print("❌ ERROR: ALPHA_VANTAGE_API_KEY not found!")
        print("Please set your API key in .env file")
        return None
    
    print(f"\n📊 Fetching {ticker}...")
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker}&apikey={api_key}"
    
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if 'Note' in data:
            print("⚠️  API Rate limit reached")
            print(data['Note'])
            return None
        
        global_quote = data.get('Global Quote', {})
        if global_quote:
            price = float(global_quote.get('05. price', 0))
            print(f"✅ {ticker}: ${price:.2f}")
            return price
        else:
            print(f"❌ No data returned for {ticker}")
            print(f"Response: {data}")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def test_multiple_stocks():
    """Test fetching multiple stocks (with rate limiting)"""
    print("\n" + "="*50)
    print("Testing Multiple Stock Fetches")
    print("="*50)
    
    tickers = ['AAPL', 'TSLA', 'MSFT', 'GOOGL']
    results = {}
    
    for ticker in tickers:
        price = test_single_stock(ticker)
        if price:
            results[ticker] = price
        
        # Alpha Vantage free tier: 5 calls per minute
        # Wait 12 seconds between calls to be safe
        if ticker != tickers[-1]:  # Don't wait after last ticker
            print("⏳ Waiting 12 seconds (API rate limit)...")
            time.sleep(12)
    
    print("\n" + "="*50)
    print("Results Summary")
    print("="*50)
    for ticker, price in results.items():
        print(f"{ticker}: ${price:.2f}")
    
    return results


def show_seed_preview():
    """Show what the seed data will look like"""
    print("\n" + "="*50)
    print("Seed Data Preview")
    print("="*50)
    
    print("\n📊 Portfolio Stocks (will use real prices):")
    print("   User 1 (Demo):")
    print("   • 5 shares of AAPL")
    print("   • 3 shares of TSLA")
    print("   • 2 shares of MSFT")
    print("\n   User 2 (Marnie):")
    print("   • 4 shares of JPM")
    print("   • 2 shares of GOOGL")
    print("\n   User 3 (Bobbie):")
    print("   • 3 shares of NVDA")
    
    print("\n👀 Watchlist Stocks:")
    print("   User 1: AAPL, TSLA, MSFT, GOOGL, META, NVDA, AMD")
    print("   User 2: JPM, GOOGL, BAC, WMT, V")
    print("   User 3: NVDA, AMZN, NFLX, DIS")
    
    print("\n💰 User Balances:")
    print("   • Demo: $25,000.00")
    print("   • Marnie: $50,000.00")
    print("   • Bobbie: $15,000.00")


def main():
    """Main function"""
    print("="*50)
    print("Alpha Vantage Seed Data Test")
    print("="*50)
    
    api_key = os.getenv('ALPHA_VANTAGE_API_KEY')
    if not api_key:
        print("\n❌ No API key found!")
        print("\nPlease:")
        print("1. Get a free API key from: https://www.alphavantage.co/support/#api-key")
        print("2. Add it to your .env file:")
        print("   ALPHA_VANTAGE_API_KEY=your_key_here")
        sys.exit(1)
    
    print(f"\n✅ API Key found: {api_key[:8]}...{api_key[-4:]}")
    
    print("\n" + "="*50)
    print("What would you like to test?")
    print("="*50)
    print("1. Test single stock (AAPL)")
    print("2. Test multiple stocks (takes ~1 minute)")
    print("3. Show seed data preview")
    print("4. All of the above")
    print("="*50)
    
    choice = input("\nEnter choice (1-4): ").strip()
    
    if choice == '1':
        test_single_stock('AAPL')
    elif choice == '2':
        test_multiple_stocks()
    elif choice == '3':
        show_seed_preview()
    elif choice == '4':
        test_single_stock('AAPL')
        show_seed_preview()
        test_multiple_stocks()
    else:
        print("Invalid choice")
    
    print("\n" + "="*50)
    print("Ready to seed your database!")
    print("="*50)
    print("\nRun these commands:")
    print("1. flask db upgrade")
    print("2. flask seed all")
    print("\nNote: Seeding will take ~1-2 minutes due to API rate limits")
    print("="*50 + "\n")


if __name__ == "__main__":
    main()
