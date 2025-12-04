from flask import Blueprint, jsonify, request
import requests
import os
from datetime import datetime, timedelta

external_stocks = Blueprint('external_stocks', __name__)

# --- Single stock info route ---
@external_stocks.route('/<ticker>', methods=['GET'])
def get_single_stock(ticker):
    api_key = os.getenv('ALPHA_VANTAGE_API_KEY')
    
    # Get company overview
    url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={ticker}&apikey={api_key}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Alpha Vantage returns different structure
        if 'Symbol' in data:
            return jsonify({
                'status': 'OK',
                'results': {
                    'ticker': data.get('Symbol'),
                    'name': data.get('Name'),
                    'description': data.get('Description'),
                    'market_cap': int(data.get('MarketCapitalization', 0)) if data.get('MarketCapitalization') else 0,
                    'homepage_url': '',
                    'address': data.get('Address', 'N/A'),
                    'sector': data.get('Sector'),
                    'industry': data.get('Industry')
                }
            }), 200
        else:
            return jsonify({"error": f"No data found for {ticker}"}), 404
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Failed to fetch data for {ticker}: {str(e)}"}), 500


# --- Chart / historical data route ---
@external_stocks.route('/<ticker>/chart', methods=['GET'])
def get_chart_data(ticker):
    api_key = os.getenv('ALPHA_VANTAGE_API_KEY')

    timespan = request.args.get('timespan', 'day')
    
    # Map timespan to Alpha Vantage function
    if timespan == 'day' or timespan == 'minute':
        function = 'TIME_SERIES_INTRADAY'
        interval = '5min'
        url = f"https://www.alphavantage.co/query?function={function}&symbol={ticker}&interval={interval}&apikey={api_key}"
    else:
        function = 'TIME_SERIES_DAILY'
        url = f"https://www.alphavantage.co/query?function={function}&symbol={ticker}&apikey={api_key}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Transform Alpha Vantage format to match expected format
        if 'Time Series (5min)' in data:
            time_series = data['Time Series (5min)']
        elif 'Time Series (Daily)' in data:
            time_series = data['Time Series (Daily)']
        else:
            return jsonify({"error": "No time series data found"}), 404
        
        # Convert to expected format
        results = []
        for timestamp, values in sorted(time_series.items()):
            results.append({
                't': int(datetime.strptime(timestamp.split()[0], '%Y-%m-%d').timestamp() * 1000),
                'o': float(values['1. open']),
                'h': float(values['2. high']),
                'l': float(values['3. low']),
                'c': float(values['4. close']),
                'v': int(values['5. volume'])
            })
        
        return jsonify({
            'status': 'OK',
            'results': results,
            'ticker': ticker
        }), 200
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error fetching chart data for {ticker}: {str(e)}"}), 500
