#!/bin/bash
# Flask Server Restart Script

echo "🔄 Restarting Flask Server..."
echo ""

# Kill any existing Flask processes
echo "Stopping existing Flask processes..."
pkill -f "flask run" 2>/dev/null || echo "No existing Flask process found"
sleep 2

# Load environment
echo "Loading environment variables..."
export $(cat .env | grep -v '^#' | xargs)

# Verify environment
echo ""
echo "✅ Environment Check:"
echo "   FLASK_APP: ${FLASK_APP:-app}"
echo "   DATABASE_URL: ${DATABASE_URL:0:30}..."
echo "   SECRET_KEY: ${SECRET_KEY:0:10}..."
echo "   ALPHA_VANTAGE_API_KEY: ${ALPHA_VANTAGE_API_KEY:0:10}..."
echo ""

# Start Flask
echo "🚀 Starting Flask server..."
echo ""
flask run

