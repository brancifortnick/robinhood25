# 🚀 Ready to Deploy Checklist

## Step 1: Get Your Free API Key (2 minutes)
- [ ] Visit https://www.alphavantage.co/support/#api-key
- [ ] Fill out the form (just email + name)
- [ ] Copy your API key (you'll get it instantly)

## Step 2: Test Locally (Optional but Recommended)
- [ ] Create `.env` file: `cp .env.example .env`
- [ ] Add your API key to `.env`:
      ```
      ALPHA_VANTAGE_API_KEY=your_key_here
      ```
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Test the API: `python test_api.py`
- [ ] Run migrations: `flask db upgrade`
- [ ] **Seed database with real stock data**: `flask seed all` (takes ~1-2 min)
- [ ] Run the app: `flask run`
- [ ] Visit http://localhost:5000 and test with Demo user
- [ ] Login credentials: `demo@aa.io` / `password`

## Step 3: Deploy to Heroku
- [ ] Set environment variable:
      ```bash
      heroku config:set ALPHA_VANTAGE_API_KEY=your_key_here
      ```
- [ ] Commit changes:
      ```bash
      git add .
      git commit -m "Updated to Alpha Vantage API with real stock seeding"
      ```
- [ ] Deploy:
      ```bash
      git push heroku main
      ```
- [ ] Run migrations on Heroku:
      ```bash
      heroku run flask db upgrade
      ```
- [ ] **Seed database on Heroku**:
      ```bash
      heroku run flask seed all
      ```
- [ ] Check logs:
      ```bash
      heroku logs --tail
      ```

## Step 4: Verify Deployment
- [ ] Open your app: `heroku open`
- [ ] Try searching for a stock (e.g., AAPL, TSLA, MSFT)
- [ ] Check that prices are loading
- [ ] Verify portfolio functionality works
- [ ] Test buy/sell features

## Step 5: Monitor & Optimize (Optional)
- [ ] Check API usage (you have 500 calls/day free)
- [ ] Monitor logs for any errors
- [ ] Consider adding caching for popular stocks
- [ ] Set up alerts for errors

## Troubleshooting

### "API key not found" error
✅ Make sure you set `ALPHA_VANTAGE_API_KEY` in Heroku config vars

### "Rate limit exceeded" error
✅ You've used your 500 daily calls - wait 24 hours or upgrade

### Stock data not loading
✅ Check Heroku logs: `heroku logs --tail`
✅ Verify API key is correct
✅ Try a different stock ticker

### Database errors
✅ Make sure migrations are run: `heroku run flask db upgrade`
✅ Check DATABASE_URL is set correctly

## Need Help?

- **API Issues:** Check [API_SETUP.md](API_SETUP.md)
- **Deployment Issues:** Check [DEPLOYMENT.md](DEPLOYMENT.md)
- **Migration Info:** Check [MIGRATION_SUMMARY.md](MIGRATION_SUMMARY.md)

## Success! 🎉

Once everything is working:
- ✅ Your app is live with real stock data
- ✅ Free API with 500 calls/day
- ✅ No credit card required
- ✅ Ready to show off your project!

**Share your deployed app and celebrate! 🚀**
