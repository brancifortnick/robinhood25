# Seeding Your Database with Real Stock Data 🌱

## Overview

Your seed files have been updated to fetch **real stock prices** from the Alpha Vantage API when seeding your database. This ensures your demo users have realistic portfolios with current market prices.

## What's Been Updated

### 1. `app/seeds/portfolio_stocks.py` ✅
- **New Feature**: Fetches real-time stock prices from Alpha Vantage
- **Fallback System**: Uses default prices if API is unavailable
- **Rate Limiting**: Respects API limits (5 calls/minute)
- **Enhanced Portfolio**: More diverse stock holdings across users

**Sample Data:**
- User 1 (Demo): 5 AAPL, 3 TSLA, 2 MSFT
- User 2 (Marnie): 4 JPM, 2 GOOGL
- User 3 (Bobbie): 3 NVDA

### 2. `app/seeds/watchlist_stocks.py` ✅
- **Expanded Watchlists**: More stocks for each user
- **Popular Stocks**: AAPL, TSLA, MSFT, GOOGL, META, NVDA, AMD, JPM, etc.

### 3. `app/seeds/users.py` ✅
- **Better Balances**: More realistic starting cash
- **Demo**: $25,000
- **Marnie**: $50,000
- **Bobbie**: $15,000

## How to Seed Your Database

### Option 1: Quick Seed (Recommended)

```bash
# Make sure you're in the project root
cd /home/nicholas/projects_old/robin-hood/RobinCould

# Activate your virtual environment
source .venv/bin/activate

# Set your API key (if not already in .env)
export ALPHA_VANTAGE_API_KEY=your_api_key_here

# Run migrations (if needed)
flask db upgrade

# Seed the database
flask seed all
```

**⏱️ Timing:** Takes about 1-2 minutes due to API rate limiting (this is normal and expected!)

### Option 2: Test First, Then Seed

```bash
# Test the API integration first
python test_seed.py

# If successful, run the seed
flask seed all
```

### Option 3: Undo and Re-seed

```bash
# Remove existing seed data
flask seed undo

# Re-seed with fresh data
flask seed all
```

## What Happens During Seeding

1. **Users Created** 🧑‍💼
   - Demo, Marnie, and Bobbie accounts with cash balances

2. **API Calls Made** 📡
   - Fetches real prices for: AAPL, TSLA, MSFT, JPM, GOOGL, NVDA
   - Waits 12 seconds between calls (API rate limit compliance)
   - Shows progress in console

3. **Portfolio Stocks Added** 💼
   - Each stock gets current market price as "basis"
   - Share counts assigned per user

4. **Watchlists Populated** 👀
   - Popular stocks added to each user's watchlist
   - No API calls needed (just ticker symbols)

## Expected Console Output

```
==================================================
🌱 Seeding Users
==================================================

✅ Users seeded:
   • Demo - $25,000.00
   • Marnie - $50,000.00
   • Bobbie - $15,000.00

==================================================
🌱 Seeding Portfolio Stocks with Real Prices
==================================================

📊 Fetching price for AAPL...
✅ AAPL: $175.43
   Added: 5 shares of AAPL @ $175.43 for User 1

📊 Fetching price for TSLA...
✅ TSLA: $242.84
   Added: 3 shares of TSLA @ $242.84 for User 1

... (continues for all stocks)

==================================================
✅ Portfolio stocks seeded successfully!
==================================================

🌱 Seeding Watchlist Stocks...
✅ Watchlist stocks seeded successfully!
```

## Troubleshooting

### "No API key found" Message
**Solution:** Set your API key in `.env`:
```bash
ALPHA_VANTAGE_API_KEY=your_key_here
```

### "Rate limit reached" Message
**What it means:** You've made too many API calls
**Solution:** The script will use fallback prices automatically. Wait 1 minute and try again if needed.

### Seeding takes a long time
**This is normal!** With 6 stocks to fetch, and 12 seconds between calls, it takes about 60-70 seconds. This ensures we don't hit rate limits.

### Want faster seeding (for development)?
Edit `app/seeds/portfolio_stocks.py` and comment out the API calls:
```python
# For quick testing, use fallback prices
api_key = None  # This forces fallback prices
```

## Heroku Deployment

When deploying to Heroku, seeding works automatically:

```bash
# Set API key on Heroku
heroku config:set ALPHA_VANTAGE_API_KEY=your_key_here

# After deployment, seed the database
heroku run flask seed all

# Or reset and re-seed
heroku run flask seed undo
heroku run flask seed all
```

## API Key Requirements

- **Free API Key**: 500 calls/day (plenty for development)
- **Calls per seed**: 6 API calls (one per stock)
- **Can seed**: ~80+ times per day with free key
- **Get your key**: https://www.alphavantage.co/support/#api-key

## Fallback System

If the API is unavailable or rate limited, the seeder uses these fallback prices:

```python
AAPL: $175.00
TSLA: $240.00
JPM: $145.00
MSFT: $370.00
GOOGL: $140.00
NVDA: $495.00
```

This ensures seeding **always works**, even without internet or API access.

## Customization

### Add More Stocks

Edit `app/seeds/portfolio_stocks.py`:

```python
portfolio_data = [
    {'ticker': 'AAPL', 'shares': 5, 'user_id': 1},
    {'ticker': 'YOUR_STOCK', 'shares': 10, 'user_id': 1},  # Add this
]
```

### Change User Balances

Edit `app/seeds/users.py`:

```python
demo = User(
    username='Demo', 
    email='demo@aa.io', 
    password='password', 
    cash_balance=100000.00  # Change this
)
```

### Modify Watchlists

Edit `app/seeds/watchlist_stocks.py` and add more ticker entries.

## Summary

✅ Seed files updated to use real API data
✅ Automatic fallback if API unavailable
✅ Rate limiting handled automatically
✅ Enhanced demo data with popular stocks
✅ Ready for local development and production

Run `flask seed all` and you're ready to go! 🚀
