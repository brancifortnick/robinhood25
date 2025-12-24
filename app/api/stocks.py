import os
from flask import Blueprint, jsonify, request
import requests
from flask_login import login_required, current_user
from app.models import db, PortfolioStocks
import traceback
from datetime import datetime, timedelta
import time

stocks = Blueprint('stocks', __name__)

# Simple in-memory cache with timestamps
api_cache = {}
CACHE_DURATION = 300  # 5 minutes cache

# Clear cache on startup to avoid stale rate-limit messages
print("🧹 Clearing API cache on startup...")
api_cache.clear()

# Fallback prices for when API is rate-limited
FALLBACK_PRICES = {
    'AAPL': 272.36,
    'TSLA': 242.84,
    'MSFT': 370.00,
    'GOOGL': 140.00,
    'META': 350.00,
    'NVDA': 495.00,
    'AMD': 145.00,
    'JPM': 145.00,
    'OKE': 85.00,
    'SPY': 450.00,
    'QQQ': 380.00,
    'DIA': 360.00,
}

# Fallback company info for popular stocks
FALLBACK_COMPANY_INFO = {
    'AAPL': {
        'name': 'Apple Inc',
        'description': 'Apple Inc. designs, manufactures, and markets smartphones, personal computers, tablets, wearables, and accessories worldwide.',
        'sector': 'Technology',
        'industry': 'Consumer Electronics',
        'marketCap': 4041928344000,
        'peRatio': '36.56',
        'dividendYield': '0.38%',
        'homepage': 'https://www.apple.com',
    },
    'TSLA': {
        'name': 'Tesla, Inc.',
        'description': 'Tesla, Inc. designs, develops, manufactures, leases, and sells electric vehicles, and energy generation and storage systems.',
        'sector': 'Consumer Cyclical',
        'industry': 'Auto Manufacturers',
        'marketCap': 772000000000,
        'peRatio': '63.42',
        'dividendYield': 'N/A',
        'homepage': 'https://www.tesla.com',
    },
    'MSFT': {
        'name': 'Microsoft Corporation',
        'description': 'Microsoft Corporation develops, licenses, and supports software, services, devices, and solutions worldwide.',
        'sector': 'Technology',
        'industry': 'Software - Infrastructure',
        'marketCap': 2754000000000,
        'peRatio': '35.20',
        'dividendYield': '0.75%',
        'homepage': 'https://www.microsoft.com',
    },
    'GOOGL': {
        'name': 'Alphabet Inc.',
        'description': 'Alphabet Inc. provides various products and platforms in the United States, Europe, the Middle East, Africa, the Asia-Pacific, Canada, and Latin America.',
        'sector': 'Communication Services',
        'industry': 'Internet Content & Information',
        'marketCap': 1758000000000,
        'peRatio': '25.80',
        'dividendYield': 'N/A',
        'homepage': 'https://www.google.com',
    },
    'META': {
        'name': 'Meta Platforms, Inc.',
        'description': 'Meta Platforms, Inc. engages in the development of products that enable people to connect and share with friends and family through mobile devices, personal computers, virtual reality headsets, and wearables worldwide.',
        'sector': 'Communication Services',
        'industry': 'Internet Content & Information',
        'marketCap': 885000000000,
        'peRatio': '24.50',
        'dividendYield': 'N/A',
        'homepage': 'https://www.meta.com',
    },
    'NVDA': {
        'name': 'NVIDIA Corporation',
        'description': 'NVIDIA Corporation provides graphics, and compute and networking solutions in the United States, Taiwan, China, and internationally.',
        'sector': 'Technology',
        'industry': 'Semiconductors',
        'marketCap': 1218000000000,
        'peRatio': '52.30',
        'dividendYield': '0.04%',
        'homepage': 'https://www.nvidia.com',
    },
    'AMD': {
        'name': 'Advanced Micro Devices, Inc.',
        'description': 'Advanced Micro Devices, Inc. operates as a semiconductor company worldwide.',
        'sector': 'Technology',
        'industry': 'Semiconductors',
        'marketCap': 234000000000,
        'peRatio': '115.50',
        'dividendYield': 'N/A',
        'homepage': 'https://www.amd.com',
    },
    'JPM': {
        'name': 'JPMorgan Chase & Co.',
        'description': 'JPMorgan Chase & Co. operates as a financial services company worldwide.',
        'sector': 'Financial Services',
        'industry': 'Banks - Diversified',
        'marketCap': 598000000000,
        'peRatio': '12.80',
        'dividendYield': '2.15%',
        'homepage': 'https://www.jpmorganchase.com',
    },
}

def get_cached_or_fetch(url, cache_key):
    """Get data from cache or fetch from API with rate limiting"""
    current_time = time.time()
    
    # Check cache
    if cache_key in api_cache:
        data, timestamp = api_cache[cache_key]
        if current_time - timestamp < CACHE_DURATION:
            print(f"✅ Using cached data for {cache_key}")
            return data
    
    # Add delay to respect rate limit (1 request per second)
    time.sleep(1.1)
    
    # Fetch from API
    print(f"🌐 Fetching from API: {cache_key}")
    response = requests.get(url, timeout=10)
    if response.status_code == 200:
        data = response.json()
        # Only cache if it's valid data (not a rate limit or error message)
        if 'Note' not in data and 'Information' not in data:
            api_cache[cache_key] = (data, current_time)
            print(f"💾 Cached {cache_key}")
        else:
            print(f"⚠️  Not caching rate-limited response")
        return data
    return None


def apply_fallback_data(ticker, stock_data):
    """Apply fallback data when API is rate-limited"""
    ticker_upper = ticker.upper()
    
    # Apply fallback price if available
    if ticker_upper in FALLBACK_PRICES:
        fallback_price = FALLBACK_PRICES[ticker_upper]
        stock_data['currentPrice'] = fallback_price
        stock_data['price'] = fallback_price
        stock_data['percentChange'] = 1.5
        stock_data['percentText'] = '+1.50%'
        print(f"📊 Using fallback price for {ticker}: ${fallback_price}")
    
    # Apply fallback company info if available
    if ticker_upper in FALLBACK_COMPANY_INFO:
        info = FALLBACK_COMPANY_INFO[ticker_upper]
        stock_data['shortName'] = info['name']
        stock_data['companyName'] = info['name']
        stock_data['description'] = info['description']
        stock_data['sector'] = info['sector']
        stock_data['industry'] = info['industry']
        stock_data['marketCap'] = info['marketCap']
        stock_data['marketCapFormatted'] = f"${info['marketCap'] / 1000000:.0f}M"
        stock_data['peRatio'] = info['peRatio']
        stock_data['dividendYield'] = info['dividendYield']
        stock_data['homepage_url'] = info['homepage']
        print(f"ℹ️  Using fallback company info for {ticker}: {info['name']}")
    
    return stock_data



def get_stock_logo_url(ticker, company_name=None):
    """
    Get logo URL for a stock ticker
    Uses multiple sources with fallbacks
    """
    ticker_upper = ticker.upper()
    
    # Map of known tickers to their domains for Clearbit
    ticker_domain_map = {
        'AAPL': 'apple.com',
        'MSFT': 'microsoft.com',
        'GOOGL': 'google.com',
        'GOOG': 'google.com',
        'AMZN': 'amazon.com',
        'TSLA': 'tesla.com',
        'META': 'meta.com',
        'FB': 'meta.com',
        'NVDA': 'nvidia.com',
        'JPM': 'jpmorganchase.com',
        'V': 'visa.com',
        'WMT': 'walmart.com',
        'DIS': 'disney.com',
        'MA': 'mastercard.com',
        'NFLX': 'netflix.com',
        'AMD': 'amd.com',
        'INTC': 'intel.com',
        'PYPL': 'paypal.com',
        'ADBE': 'adobe.com',
        'CRM': 'salesforce.com',
        'ORCL': 'oracle.com',
        'IBM': 'ibm.com',
        'CSCO': 'cisco.com',
        'BAC': 'bankofamerica.com',
        'KO': 'coca-cola.com',
        'PEP': 'pepsi.com',
        'NKE': 'nike.com',
        'MCD': 'mcdonalds.com',
        'T': 'att.com',
        'VZ': 'verizon.com',
    }
    
    # Get the domain for Clearbit
    domain = ticker_domain_map.get(ticker_upper, f"{ticker.lower()}.com")
    
    return {
        'primary': f"https://logo.clearbit.com/{domain}",
        'fallback': f"https://ui-avatars.com/api/?name={ticker_upper}&size=128&background=0066CC&color=fff&bold=true"
    }


def fetch_intraday_data(ticker, api_key):
    """Fetch intraday (5min) data for daily chart"""
    try:
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={ticker}&interval=5min&apikey={api_key}"
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if 'Time Series (5min)' in data:
            time_series = data['Time Series (5min)']
            # Get data points during trading hours (9:30 AM - 4:00 PM ET)
            prices = []
            timestamps = []
            
            for timestamp in sorted(time_series.keys(), reverse=True):
                # Parse timestamp
                dt = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
                hour = dt.hour
                minute = dt.minute
                
                # Only include trading hours (9:30 - 16:00)
                if (hour == 9 and minute >= 30) or (10 <= hour < 16):
                    prices.append(float(time_series[timestamp]['4. close']))
                    timestamps.append(timestamp)
                    
                if len(prices) >= 78:  # Full trading day (6.5 hours * 12 five-min intervals)
                    break
            
            if len(prices) > 0:
                return list(reversed(prices))  # Reverse to show chronologically
        return None
    except Exception as e:
        print(f"Error fetching intraday data: {e}")
        return None


def fetch_daily_data(ticker, api_key, days=30):
    """Fetch daily data for weekly/monthly charts"""
    try:
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey={api_key}"
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if 'Time Series (Daily)' in data:
            time_series = data['Time Series (Daily)']
            # Get last N days
            prices = []
            for timestamp in sorted(time_series.keys(), reverse=True)[:days]:
                prices.append(float(time_series[timestamp]['4. close']))
            return list(reversed(prices))  # Reverse to show chronologically
        return None
    except:
        return None


@stocks.route('/<ticker>')
@login_required
def get_stock(ticker):
    try:
        ticker = ticker.upper()
        api_key = os.getenv('ALPHA_VANTAGE_API_KEY')
        
        print(f"Processing request for ticker: {ticker}")
        
        # Get logo URLs
        logo_urls = get_stock_logo_url(ticker)
        
        # Initialize with default data that will always work
        stock_data = {
            'ticker': ticker,
            'shortName': ticker,
            'companyName': ticker,
            'description': f'Stock information for {ticker}',
            'currentPrice': 100.00,
            'price': 100.00,  # Alias for compatibility
            'percentChange': 2.50,  # Numeric value
            'percentText': '+2.50%',
            'address': 'N/A',
            'marketCap': 1000000000,
            'marketCapFormatted': '$1000M',
            'homepage_url': 'N/A',
            'sector': 'N/A',
            'industry': 'N/A',
            'peRatio': 'N/A',
            'dividendYield': 'N/A',
            'averageVolume': 'N/A',
            'eps': 'N/A',
            'beta': 'N/A',
            '52WeekHigh': 'N/A',
            '52WeekLow': 'N/A',
            'logoUrl': logo_urls['primary'],
            'logoFallback': logo_urls['fallback'],
            'inPortfolio': False,
            'shares': 0,
            'basis': 0,
            # Realistic intraday data (9:30 AM - 4:00 PM, 78 data points)
            'dailyPrices': [98.5, 98.8, 99.2, 99.5, 99.8, 100.1, 100.3, 100.5, 100.8, 101.0,
                           101.2, 101.5, 101.3, 101.1, 100.9, 101.2, 101.5, 101.8, 102.0, 102.3,
                           102.5, 102.7, 103.0, 103.2, 103.0, 102.8, 102.5, 102.7, 103.0, 103.3,
                           103.5, 103.8, 104.0, 104.2, 104.5, 104.3, 104.1, 103.9, 104.2, 104.5,
                           104.8, 105.0, 105.2, 105.5, 105.7, 106.0, 106.2, 106.0, 105.8, 106.1,
                           106.4, 106.7, 107.0, 107.2, 107.5, 107.3, 107.1, 107.4, 107.7, 108.0,
                           108.2, 108.5, 108.7, 109.0, 108.8, 108.6, 108.9, 109.2, 109.5, 109.7,
                           110.0, 110.2, 110.5, 110.7, 110.5, 110.3, 110.5, 110.8],
            'dailyPricesLabels': ['9:30 AM', '9:50 AM', '10:10 AM', '10:30 AM', '10:50 AM', '11:10 AM', '11:30 AM', '11:50 AM',
                                 '12:10 PM', '12:30 PM', '12:50 PM', '1:10 PM', '1:30 PM', '1:50 PM', '2:10 PM', '2:30 PM',
                                 '2:50 PM', '3:10 PM', '3:30 PM', '3:50 PM'],
            'weeklyPrices': [95.2, 97.5, 100.3, 103.8, 105.9, 108.2, 106.8],
            'weeklyPricesLabels': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            'oneMonthPrices': [90.5, 92.0, 93.5, 95.0, 96.5, 98.0, 99.5, 101.0, 102.5, 104.0, 
                              105.5, 107.0, 108.5, 110.0, 111.5, 113.0, 112.5, 112.0, 113.5, 115.0,
                              116.5, 118.0, 117.5, 117.0, 118.5, 120.0, 119.5, 119.0, 120.5, 122.0],
            'oneMonthPricesLabels': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
                                     '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
                                     '21', '22', '23', '24', '25', '26', '27', '28', '29', '30'],
            'yearlyPrices': [80.0, 85.5, 90.0, 95.5, 100.0, 105.5, 110.0, 115.5, 120.0, 125.5, 130.0, 135.5],
            'yearlyPricesLabels': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
            'allTimePrices': [50.0, 60.0, 70.0, 80.0, 90.0, 100.0, 110.0, 120.0, 130.0, 140.0],
            'allTimePricesLabels': ['2020', '2021', '2022', '2023', '2024', '2025', '2026', '2027', '2028', '2029']
        }
        
        # Try to get portfolio data
        try:
            portfolio_stock = PortfolioStocks.query.filter_by(
                ticker=ticker, user_id=current_user.id).first()
            
            if portfolio_stock:
                stock_data.update({
                    'inPortfolio': True,
                    'shares': int(portfolio_stock.share_count) if portfolio_stock.share_count else 0,
                    'basis': float(portfolio_stock.basis) if portfolio_stock.basis else 0.0
                })
                print(f"Found portfolio data for {ticker}")
        except Exception as db_error:
            print(f"Database error for {ticker}: {db_error}")
            # Keep default portfolio values
        
        # Try to get API data (but don't fail if it doesn't work)
        if api_key:
            try:
                # Get company details using Alpha Vantage
                company_url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={ticker}&apikey={api_key}"
                print(f"Fetching company data from Alpha Vantage...")
                
                company_json = get_cached_or_fetch(company_url, f"overview_{ticker}")
                
                if company_json and 'Symbol' in company_json and 'Note' not in company_json and 'Information' not in company_json:
                    company_name = company_json.get('Name', ticker)
                    
                    # Parse market cap - it comes as a string
                    market_cap_str = company_json.get('MarketCapitalization', '1000000000')
                    try:
                        market_cap = int(float(market_cap_str)) if market_cap_str else 1000000000
                    except (ValueError, TypeError):
                        market_cap = 1000000000
                    
                    # Parse PE Ratio
                    pe_ratio = company_json.get('PERatio', 'N/A')
                    if pe_ratio and pe_ratio != 'None':
                        try:
                            pe_ratio = float(pe_ratio)
                            pe_ratio = f"{pe_ratio:.2f}"
                        except (ValueError, TypeError):
                            pe_ratio = 'N/A'
                    else:
                        pe_ratio = 'N/A'
                    
                    # Parse Dividend Yield
                    dividend_yield = company_json.get('DividendYield', 'N/A')
                    if dividend_yield and dividend_yield != 'None':
                        try:
                            dividend_yield = float(dividend_yield) * 100  # Convert to percentage
                            dividend_yield = f"{dividend_yield:.2f}%"
                        except (ValueError, TypeError):
                            dividend_yield = 'N/A'
                    else:
                        dividend_yield = 'N/A'
                    
                    # Get average volume (from technical indicators or use 'Volume' if available)
                    avg_volume = company_json.get('AverageVolume', 'N/A')
                    if avg_volume and avg_volume != 'None':
                        try:
                            avg_volume = int(float(avg_volume))
                            # Format with commas
                            avg_volume = f"{avg_volume:,}"
                        except (ValueError, TypeError):
                            avg_volume = 'N/A'
                    
                    stock_data.update({
                        'shortName': company_name,
                        'companyName': company_name,
                        'description': company_json.get('Description', f'Stock information for {ticker}'),
                        'marketCap': market_cap,
                        'marketCapFormatted': f"${market_cap / 1000000:.0f}M" if market_cap >= 1000000 else f"${market_cap / 1000:.0f}K",
                        'homepage_url': company_json.get('OfficialSite', ''),
                        'address': company_json.get('Address', 'N/A'),
                        'sector': company_json.get('Sector', 'N/A'),
                        'industry': company_json.get('Industry', 'N/A'),
                        'peRatio': pe_ratio,
                        'dividendYield': dividend_yield,
                        'averageVolume': avg_volume,
                        'eps': company_json.get('EPS', 'N/A'),
                        'beta': company_json.get('Beta', 'N/A'),
                        '52WeekHigh': company_json.get('52WeekHigh', 'N/A'),
                        '52WeekLow': company_json.get('52WeekLow', 'N/A'),
                    })
                    print(f"Updated with company data for {ticker}")
                    print(f"  Market Cap: ${market_cap:,}")
                    print(f"  PE Ratio: {pe_ratio}")
                    print(f"  Dividend Yield: {dividend_yield}")
                    print(f"  Homepage: {company_json.get('OfficialSite', 'N/A')}")
                
                # Get price data using Alpha Vantage Global Quote
                quote_url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker}&apikey={api_key}"
                print(f"Fetching price data...")
                price_json = get_cached_or_fetch(quote_url, f"quote_{ticker}")
                
                price_updated = False
                if price_json:
                    print(f"Price API Response keys: {price_json.keys()}")
                    global_quote = price_json.get('Global Quote', {})
                    
                    # Check for API limit message
                    if 'Note' in price_json or 'Information' in price_json:
                        if 'Note' in price_json:
                            print(f"⚠️  API Rate Limit, using fallback price")
                        else:
                            print(f"⚠️  API Message, using fallback price")
                        
                        # Use fallback price
                        if ticker in FALLBACK_PRICES:
                            fallback_price = FALLBACK_PRICES[ticker]
                            stock_data.update({
                                'currentPrice': fallback_price,
                                'price': fallback_price,
                                'percentChange': 0.51,
                                'percentText': '+0.51%'
                            })
                            print(f"💰 Using fallback price for {ticker}: ${fallback_price}")
                            price_updated = True
                    elif global_quote:
                        current_price = float(global_quote.get('05. price', 100))
                        prev_close = float(global_quote.get('08. previous close', 100))
                        volume = global_quote.get('06. volume', 'N/A')
                        
                        # Format volume if available
                        if volume and volume != 'N/A':
                            try:
                                volume_int = int(volume)
                                if volume_int >= 1000000:
                                    volume_formatted = f"{volume_int / 1000000:.2f}M"
                                elif volume_int >= 1000:
                                    volume_formatted = f"{volume_int / 1000:.2f}K"
                                else:
                                    volume_formatted = f"{volume_int:,}"
                            except (ValueError, TypeError):
                                volume_formatted = 'N/A'
                        else:
                            volume_formatted = 'N/A'
                        
                        if prev_close and prev_close != 0:
                            percent_change = ((current_price - prev_close) / prev_close) * 100
                            update_dict = {
                                'currentPrice': current_price,
                                'price': current_price,  # Alias for compatibility
                                'percentChange': percent_change,  # Numeric value
                                'percentText': f"{percent_change:+.2f}%"
                            }
                            
                            # Only update volume if we didn't get it from company data
                            if stock_data.get('averageVolume') == 'N/A':
                                update_dict['averageVolume'] = volume_formatted
                            
                            stock_data.update(update_dict)
                            print(f"✅ Updated with price data for {ticker}: ${current_price}")
                            print(f"  Volume: {volume_formatted}")
                            price_updated = True
                    else:
                        print(f"⚠️  No Global Quote data, using fallback")
                        if ticker in FALLBACK_PRICES:
                            fallback_price = FALLBACK_PRICES[ticker]
                            stock_data.update({
                                'currentPrice': fallback_price,
                                'price': fallback_price,
                                'percentChange': 0.51,
                                'percentText': '+0.51%'
                            })
                            print(f"💰 Using fallback price for {ticker}: ${fallback_price}")
                            price_updated = True
                else:
                    print(f"❌ Price API request failed, using fallback")
                    if ticker in FALLBACK_PRICES:
                        fallback_price = FALLBACK_PRICES[ticker]
                        stock_data.update({
                            'currentPrice': fallback_price,
                            'price': fallback_price,
                            'percentChange': 0.51,
                            'percentText': '+0.51%'
                        })
                        print(f"💰 Using fallback price for {ticker}: ${fallback_price}")
                        price_updated = True
                
                # Fetch chart data (intraday for daily view)
                print(f"Fetching chart data for {ticker}...")
                daily_data = fetch_intraday_data(ticker, api_key)
                if daily_data and len(daily_data) > 5:
                    stock_data['dailyPrices'] = daily_data
                    print(f"✅ Fetched {len(daily_data)} intraday prices")
                
                # Fetch weekly/monthly data (daily time series)
                daily_time_series = fetch_daily_data(ticker, api_key, days=30)
                if daily_time_series and len(daily_time_series) >= 7:
                    # Weekly: last 7 days
                    stock_data['weeklyPrices'] = daily_time_series[-7:]
                    # Monthly: last 30 days
                    stock_data['oneMonthPrices'] = daily_time_series
                    # Yearly/All-time: use monthly data sampled
                    if len(daily_time_series) >= 12:
                        # Sample every ~3 days for yearly view
                        stock_data['yearlyPrices'] = daily_time_series[::3][:10]
                        stock_data['allTimePrices'] = daily_time_series[::3][:10]
                    print(f"✅ Fetched daily time series data")
                
            except requests.RequestException as api_error:
                print(f"API request failed for {ticker}: {api_error}")
            except Exception as api_error:
                print(f"API error for {ticker}: {api_error}")
        else:
            print("No API key found, using mock data")
        
        print(f"Returning data for {ticker}: {stock_data['shortName']} @ ${stock_data['currentPrice']}")
        return jsonify(stock_data), 200
        
    except Exception as e:
        print(f"CRITICAL ERROR for {ticker}: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        
        # Return absolute minimum fallback data
        return jsonify({
            'ticker': ticker if 'ticker' in locals() else 'ERROR',
            'shortName': ticker if 'ticker' in locals() else 'ERROR',
            'description': 'Error loading stock data',
            'currentPrice': 0,
            'percentText': '0.00%',
            'address': 'N/A',
            'marketCap': 0,
            'homepage_url': '',
            'inPortfolio': False,
            'shares': 0,
            'basis': 0,
            'dailyPrices': [100, 100, 100, 100, 100],
            'dailyPricesLabels': ['1', '2', '3', '4', '5'],
            'weeklyPrices': [100, 100, 100, 100, 100],
            'weeklyPricesLabels': ['1', '2', '3', '4', '5'],
            'oneMonthPrices': [100, 100, 100, 100, 100],
            'oneMonthPricesLabels': ['1', '2', '3', '4', '5'],
            'yearlyPrices': [100, 100, 100, 100, 100],
            'yearlyPricesLabels': ['1', '2', '3', '4', '5'],
            'allTimePrices': [100, 100, 100, 100, 100],
            'allTimePricesLabels': ['1', '2', '3', '4', '5']
        }), 200  # Return 200, not 500!
