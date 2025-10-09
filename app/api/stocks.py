import os
from flask import Blueprint, jsonify, request
import requests
from flask_login import login_required, current_user
from app.models import db, PortfolioStocks
from app.forms import BuyForm


stocks = Blueprint('stocks', __name__)

# Your /api/stocks/<ticker> route only returns stocks from the user's portfolio, not external data.
# If the ticker is not in the user's portfolio, you get a 404 error.


@stocks.route('/<ticker>')
@login_required
def get_stock(ticker):
    ticker = ticker.upper()
    stock = PortfolioStocks.query.filter_by(
        ticker=ticker, user_id=current_user.id).first()
    if stock:
        return {'stock': stock.to_dict()}
    # If not in portfolio, fetch from Polygon.io
    api_key = os.getenv('POLYGON_API_KEY')
    url = f"https://api.polygon.io/v3/reference/tickers/{ticker}/?apiKey={api_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return {'error': f'Could not fetch data for {ticker}.'}, 500
