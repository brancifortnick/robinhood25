from flask import Blueprint, jsonify, request
import requests
from flask_login import login_required, current_user
from app.models import db, PortfolioStocks
from app.forms import BuyForm
import os

portfolio_stocks_routes = Blueprint('portfolio_stocks', __name__)

# You'll need to set this in your environment variables or config
POLYGON_API_KEY = os.getenv('POLYGON_API_KEY')


def get_stock_price(ticker):
    try:
        # Get previous close price from Polygon.io
        response = requests.get(
            f"https://api.polygon.io/v2/aggs/ticker/{ticker}/prev?adjusted=true&apikey={POLYGON_API_KEY}")
        data = response.json()

        if data.get('status') == 'OK' and data.get('resultsCount', 0) > 0:
            results = data.get('results', [])
            if results:
                # 'c' is close price
                current_price = float(results[0].get('c'))
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


@login_required
@portfolio_stocks_routes.route('/<ticker>/<operator>', methods=['POST'])
def add_ticker_to_portfolio(ticker, operator):
    ticker = ticker.upper()

    # Validate operator
    if operator not in ['add', 'subtract']:
        return {'error': 'Invalid operation'}, 400

    stock_already_in_portfolio = PortfolioStocks.query.filter(
        PortfolioStocks.user_id == current_user.id,
        PortfolioStocks.ticker == ticker
    ).one_or_none()

    # Get current price from Polygon.io
    current_price = get_stock_price(ticker)
    if current_price is None:
        return {'error': 'Unable to fetch stock price'}, 503

    if stock_already_in_portfolio:
        if operator == 'add':
            expanded_basis = round(
                stock_already_in_portfolio.share_count * stock_already_in_portfolio.basis, 2)
            stock_already_in_portfolio.share_count += 1
            new_basis = round((expanded_basis + current_price) /
                              stock_already_in_portfolio.share_count, 2)
            stock_already_in_portfolio.basis = new_basis
        else:  # subtract
            if stock_already_in_portfolio.share_count > 0:
                stock_already_in_portfolio.share_count -= 1
            else:
                return {'error': 'Cannot sell - no shares to sell'}, 400

        db.session.add(stock_already_in_portfolio)
        db.session.commit()
        print(stock_already_in_portfolio.to_dict(),
              "backend ------<><><><><> PORTFOLIO STOCKS!!!!!!!!!!!!!!!!!!")
        return stock_already_in_portfolio.to_dict()
    else:
        if operator == 'subtract':
            return {'error': 'Cannot sell stock not in portfolio'}, 400

        purchased_stock = PortfolioStocks(
            ticker=ticker,
            basis=current_price,
            share_count=1,
            user_id=current_user.id
        )
        db.session.add(purchased_stock)
        db.session.commit()
        return purchased_stock.to_dict()
