#!/usr/bin/env python3
"""
Test script for Alpha Vantage API integration
Run this to verify your API key is working correctly
"""

import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_api_key():
    """Test if the Alpha Vantage API key is valid"""
    api_key = os.getenv('ALPHA_VANTAGE_API_KEY')
    
    if not api_key:
        print("❌ ERROR: ALPHA_VANTAGE_API_KEY not found in environment variables")
        print("\nPlease set your API key in .env file or environment variables")
        print("Get your free key at: https://www.alphavantage.co/support/#api-key")
        return False
    
    print(f"✓ API Key found: {api_key[:8]}...{api_key[-4:]}")
    print("\nTesting API connection with AAPL stock...")
    
    # Test Global Quote endpoint
    try:
        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=AAPL&apikey={api_key}"
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if 'Global Quote' in data and data['Global Quote']:
            quote = data['Global Quote']
            print("\n✅ API Connection Successful!")
            print("\n--- AAPL Stock Data ---")
            print(f"Symbol: {quote.get('01. symbol', 'N/A')}")
            print(f"Price: ${quote.get('05. price', 'N/A')}")
            print(f"Volume: {quote.get('06. volume', 'N/A')}")
            print(f"Latest Trading Day: {quote.get('07. latest trading day', 'N/A')}")
            print(f"Previous Close: ${quote.get('08. previous close', 'N/A')}")
            print(f"Change: {quote.get('09. change', 'N/A')}")
            print(f"Change Percent: {quote.get('10. change percent', 'N/A')}")
            return True
        elif 'Note' in data:
            print("\n⚠️  WARNING: API Rate Limit Reached")
            print(data['Note'])
            print("\nYour API key is valid, but you've hit the rate limit.")
            print("Wait a minute and try again, or upgrade your plan.")
            return True
        elif 'Error Message' in data:
            print(f"\n❌ API Error: {data['Error Message']}")
            return False
        else:
            print(f"\n❌ Unexpected response: {data}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Network Error: {e}")
        return False
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

def test_company_overview():
    """Test company overview endpoint"""
    api_key = os.getenv('ALPHA_VANTAGE_API_KEY')
    
    if not api_key:
        return False
    
    print("\n" + "="*50)
    print("Testing Company Overview endpoint...")
    print("="*50)
    
    try:
        url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol=AAPL&apikey={api_key}"
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if 'Symbol' in data:
            print("\n✅ Company Overview Successful!")
            print("\n--- AAPL Company Info ---")
            print(f"Name: {data.get('Name', 'N/A')}")
            print(f"Description: {data.get('Description', 'N/A')[:100]}...")
            print(f"Sector: {data.get('Sector', 'N/A')}")
            print(f"Industry: {data.get('Industry', 'N/A')}")
            print(f"Market Cap: ${data.get('MarketCapitalization', 'N/A')}")
            return True
        elif 'Note' in data:
            print("\n⚠️  Rate limit reached for this endpoint")
            return True
        else:
            print(f"\n❌ Unexpected response: {data}")
            return False
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

def main():
    """Main test function"""
    print("="*50)
    print("Alpha Vantage API Test Script")
    print("="*50)
    
    if test_api_key():
        test_company_overview()
        print("\n" + "="*50)
        print("✅ Your API is configured correctly!")
        print("You're ready to deploy your app!")
        print("="*50)
    else:
        print("\n" + "="*50)
        print("❌ API configuration failed")
        print("Please check your API key and try again")
        print("="*50)

if __name__ == "__main__":
    main()
