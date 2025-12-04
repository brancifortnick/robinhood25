# Alpha Vantage API Setup Guide

## What Changed?

Your app has been updated to use **Alpha Vantage API** instead of Polygon.io. Alpha Vantage is a free, reliable stock market API that provides:

- ✅ Real-time stock quotes
- ✅ Company information (name, description, market cap)
- ✅ Historical price data
- ✅ Free tier with 25 API calls/day (or 500 calls/day with a free API key)
- ✅ No credit card required

## Getting Your Free API Key

1. **Visit Alpha Vantage**: Go to https://www.alphavantage.co/support/#api-key

2. **Sign Up**: Fill in the simple form:
   - Your email address
   - Organization name (you can put "Personal" or your name)
   - Click "GET FREE API KEY"

3. **Receive Your Key**: You'll get your API key immediately on the screen and via email

## Setting Up Your Environment

### For Local Development

1. Create or update your `.env` file in the project root:
```bash
ALPHA_VANTAGE_API_KEY=your_api_key_here
SECRET_KEY=your_secret_key
DATABASE_URL=your_database_url
```

### For Heroku Deployment

Set the environment variable on Heroku:

```bash
heroku config:set ALPHA_VANTAGE_API_KEY=your_api_key_here
```

Or via the Heroku Dashboard:
1. Go to your app's Settings
2. Click "Reveal Config Vars"
3. Add a new variable:
   - KEY: `ALPHA_VANTAGE_API_KEY`
   - VALUE: your API key

## Files Updated

The following files have been updated to use Alpha Vantage:

1. **`app/api/external_stocks.py`** - External stock data endpoints
2. **`app/api/stocks.py`** - Main stock information endpoint
3. **`app/api/portfolio_stocks_routes.py`** - Portfolio stock price fetching

## API Rate Limits

- **Free Tier**: 25 API calls per day
- **Free API Key**: 500 calls per day (still free!)
- **Premium**: Unlimited calls (paid plans available)

For most development and small-scale apps, the free tier is sufficient.

## Testing Your Setup

After setting your API key, test it:

1. Start your Flask app:
```bash
flask run
```

2. Try accessing a stock (e.g., AAPL):
```bash
curl http://localhost:5000/api/stocks/AAPL
```

You should see real stock data returned!

## API Endpoints Used

Your app now uses these Alpha Vantage endpoints:

1. **Company Overview**: Get company information
   - `OVERVIEW` function

2. **Global Quote**: Get current stock price
   - `GLOBAL_QUOTE` function

3. **Time Series**: Get historical data
   - `TIME_SERIES_INTRADAY` for intraday data
   - `TIME_SERIES_DAILY` for daily historical data

## Troubleshooting

### "Invalid API call" error
- Make sure your API key is set correctly
- Check that you haven't exceeded your daily limit

### "Thank you for using Alpha Vantage" message
- This means your API key is working but you've hit the rate limit
- Wait 24 hours or upgrade to a premium plan

### No data returned
- Verify the ticker symbol is correct
- Some tickers might not be available in Alpha Vantage's database

## Deployment Checklist

Before deploying to production:

- [ ] Get your Alpha Vantage API key
- [ ] Set `ALPHA_VANTAGE_API_KEY` in Heroku config vars
- [ ] Remove old `POLYGON_API_KEY` from Heroku config vars (optional cleanup)
- [ ] Test your app locally first
- [ ] Deploy and verify stock data is loading

## Support

- Alpha Vantage Documentation: https://www.alphavantage.co/documentation/
- Support: https://www.alphavantage.co/support/

Your app is ready to deploy! 🚀
