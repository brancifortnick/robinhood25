#!/bin/bash

echo "🚀 Starting RobinHood Clone..."
echo ""
echo "This will start both Flask (backend) and React (frontend) servers."
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}📋 Instructions:${NC}"
echo "1. Open a new terminal and run: flask run"
echo "2. Open another terminal and run: cd react-app && npm start"
echo ""
echo "Or use these shortcuts:"
echo ""

echo -e "${GREEN}🐍 Flask Backend:${NC}"
echo "cd /home/nicholas/projects_old/robin-hood/RobinCould"
echo "flask run"
echo ""

echo -e "${GREEN}⚛️  React Frontend:${NC}"
echo "cd /home/nicholas/projects_old/robin-hood/RobinCould/react-app"
echo "npm start"
echo ""

echo "✨ After both servers start, open: http://localhost:3000"
echo ""
echo "🎯 Quick Test:"
echo "1. Login with demo user"
echo "2. Navigate to any stock (e.g., AAPL)"
echo "3. Try buying a share"
echo "4. Check your portfolio on the home page"
echo ""
