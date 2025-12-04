from flask import Blueprint, jsonify, request
import requests
from flask_login import login_required, current_user
from app.models import db, PortfolioStocks
from app.forms import BuyForm
import os

portfolio_stocks_routes = Blueprint('portfolio_stocks', __name__)

# You'll need to set this in your environment variables or config
ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY')


@portfolio_stocks_routes.route('/test')
@login_required
def get_stock_price(ticker):
    try:
        # Get current price from Alpha Vantage Global Quote
        response = requests.get(
            f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker}&apikey={ALPHA_VANTAGE_API_KEY}")
        data = response.json()

        global_quote = data.get('Global Quote', {})
        if global_quote:
            # '05. price' is the current price
            current_price = float(global_quote.get('05. price', 0))
            return current_price

        return None
    except:
        return None

# GET /api/portfolio-stocks/


@portfolio_stocks_routes.route('/')
@login_required
def portfolio():
    portfolio_stocks = PortfolioStocks.query.filter(
        PortfolioStocks.user_id == current_user.id).all()
    return {'portfolio': [stock.to_dict() for stock in portfolio_stocks]}

# /api/portfolio-stocks/:ticker/:operator

@portfolio_stocks_routes.route('/<ticker>/<operator>', methods=['POST'])
@login_required
def add_ticker_to_portfolio(ticker, operator):
    ticker = ticker.upper()
    
    print(f"=== ADD/SUBTRACT STOCK REQUEST ===")
    print(f"Ticker: {ticker}, Operator: {operator}")
    print(f"Request content type: {request.content_type}")
    print(f"Request data: {request.get_data()}")

    # Validate operator
    if operator not in ['add', 'subtract']:
        print(f"ERROR: Invalid operator: {operator}")
        return {'error': 'Invalid operation'}, 400

    stock_already_in_portfolio = PortfolioStocks.query.filter(
        PortfolioStocks.user_id == current_user.id,
        PortfolioStocks.ticker == ticker
    ).one_or_none()

    # Get current price from request body or fetch from API
    request_data = request.get_json(silent=True) or {}
    print(f"Parsed JSON: {request_data}")
    current_price = request_data.get('price')
    print(f"Price from request: {current_price}")
    
    if current_price is None:
        # Fall back to API if price not provided
        print("No price provided, fetching from API...")
        current_price = get_stock_price(ticker)
        if current_price is None:
            # Use a default basis if API fails
            current_price = stock_already_in_portfolio.basis if stock_already_in_portfolio else 100.0
            print(f"Warning: Could not fetch price for {ticker}, using fallback: ${current_price}")
    
    print(f"Final price to use: ${current_price}")

    if stock_already_in_portfolio:
        print(f"Stock found in portfolio: {stock_already_in_portfolio.share_count} shares")
        if operator == 'add':
            expanded_basis = round(
                stock_already_in_portfolio.share_count * stock_already_in_portfolio.basis, 2)
            stock_already_in_portfolio.share_count += 1
            new_basis = round((expanded_basis + current_price) /
                              stock_already_in_portfolio.share_count, 2)
            print(f'New basis calculated: {new_basis}')
            stock_already_in_portfolio.basis = new_basis
        else:  # subtract
            if stock_already_in_portfolio.share_count > 0:
                stock_already_in_portfolio.share_count -= 1
                print(f"Sold 1 share, new count: {stock_already_in_portfolio.share_count}")
            else:
                print("ERROR: No shares to sell")
                return {'error': 'Cannot sell - no shares to sell'}, 400

        db.session.add(stock_already_in_portfolio)
        db.session.commit()
        print(f"SUCCESS: Updated portfolio stock")
        print(stock_already_in_portfolio.to_dict(),
              "backend ------<><><><><> PORTFOLIO STOCKS!!!!!!!!!!!!!!!!!!")
        return stock_already_in_portfolio.to_dict()
    else:
        print("Stock not in portfolio")
        if operator == 'subtract':
            print("ERROR: Cannot sell stock not owned")
            return {'error': 'Cannot sell stock not in portfolio'}, 400

        print("Creating new portfolio entry...")
        purchased_stock = PortfolioStocks(
            ticker=ticker,
            basis=current_price,
            share_count=1,
            user_id=current_user.id
        )
        db.session.add(purchased_stock)
        db.session.commit()
        print("SUCCESS: Added new stock to portfolio")
        return purchased_stock.to_dict()
