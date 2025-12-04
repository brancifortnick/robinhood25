# Quick Deployment Guide 🚀

## Prerequisites

1. **Get Alpha Vantage API Key** (Free!)
   - Visit: https://www.alphavantage.co/support/#api-key
   - Fill in the form and get your key instantly
   - No credit card required!

## Deploy to Heroku

### Step 1: Set Environment Variables

```bash
heroku config:set ALPHA_VANTAGE_API_KEY=your_api_key_here
heroku config:set SECRET_KEY=your_secret_key_here
```

Or via Heroku Dashboard:
1. Go to your app → Settings → Config Vars
2. Add `ALPHA_VANTAGE_API_KEY` with your API key

### Step 2: Deploy

```bash
git add .
git commit -m "Updated to Alpha Vantage API"
git push heroku main
```

### Step 3: Verify

```bash
heroku logs --tail
```

Look for successful API calls in the logs.

## Deploy to Other Platforms

### Render.com
1. Add environment variable: `ALPHA_VANTAGE_API_KEY`
2. Deploy from GitHub

### Railway.app
1. Add environment variable: `ALPHA_VANTAGE_API_KEY`
2. Deploy from GitHub

### DigitalOcean App Platform
1. Add environment variable: `ALPHA_VANTAGE_API_KEY`
2. Deploy from GitHub

## Local Testing

1. Create `.env` file:
```bash
cp .env.example .env
```

2. Edit `.env` and add your API key:
```
ALPHA_VANTAGE_API_KEY=your_key_here
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
flask db upgrade
```

5. Start the app:
```bash
flask run
```

6. Test in another terminal:
```bash
curl http://localhost:5000/api/stocks/AAPL
```

## What's Different?

✅ **Free API** - Alpha Vantage is 100% free for basic usage
✅ **No Credit Card** - Unlike some APIs, no payment info needed
✅ **Reliable** - Well-maintained and widely used
✅ **500 calls/day** - Plenty for development and small apps

## API Rate Limits

- Free tier: 25 calls/day (without signup)
- Free API key: 500 calls/day (recommended - still free!)
- Premium: Unlimited (if you need it later)

Your app will work with the free tier for development and small-scale production use.

## Next Steps

1. Get your API key ✅
2. Set environment variable ✅
3. Deploy ✅
4. Test with real stock data ✅
5. Launch! 🎉

Happy coding! 🚀
