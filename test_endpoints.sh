#!/bin/bash
# Quick API Test Script

echo "Testing Flask API endpoints..."
echo ""

# Test if server is running
echo "1. Testing if Flask is running..."
curl -s http://localhost:5000/api/auth/ 2>&1 | head -5
echo ""

# Test stock endpoint (requires login, will show unauthorized)
echo "2. Testing stock API structure..."
echo "   (Should show 'Unauthorized' - that's expected)"
curl -s http://localhost:5000/api/stocks/AAPL 2>&1 | head -5
echo ""

echo ""
echo "✅ If you see 'Unauthorized' above, Flask is running correctly!"
echo ""
echo "To see full stock data with logos:"
echo "1. Login to your app in the browser"
echo "2. Open DevTools (F12)"
echo "3. Go to Network tab"
echo "4. Navigate to a stock page (e.g., AAPL)"
echo "5. Look for the /api/stocks/AAPL request"
echo "6. You should see 'logoUrl' and 'logoFallback' in the response"
echo ""
echo "If logos aren't showing:"
echo "  → Restart Flask: Ctrl+C in python3.9 terminal, then 'flask run'"
echo "  → Restart React: Ctrl+C in npm terminal, then 'npm start'"
