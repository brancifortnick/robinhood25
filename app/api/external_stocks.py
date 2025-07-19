from flask import Blueprint
import requests


external_stocks = Blueprint('external_stocks', __name__)


# route
# /api/stocks /: ticker


@external_stocks.route('/<ticker>')
def get_single_stock(ticker):
    httpResponse = requests.get(
        "https://api.polygon.io/v2/aggs/ticker/" + ticker)
    pythonData = httpResponse.json()
    print(f' ticker + {ticker}')
    return pythonData


# returned object
# {
#     "adjusted": true,
#     "next_url": "https://api.polygon.io/v2/aggs/ticker/AAPL/range/1/day/1578114000000/2020-01-10?cursor=bGltaXQ9MiZzb3J0PWFzYw",
#     "queryCount": 2,
#     "request_id": "6a7e466379af0a71039d60cc78e72282",
#     "results": [
#         {
#             "c": 75.0875,
#             "h": 75.15,
#             "l": 73.7975,
#             "n": 1,
#             "o": 74.06,
#             "t": 1577941200000,
#             "v": 135647456,
#             "vw": 74.6099
#         },
#         {
#             "c": 74.3575,
#             "h": 75.145,
#             "l": 74.125,
#             "n": 1,
#             "o": 74.2875,
#             "t": 1578027600000,
#             "v": 146535512,
#             "vw": 74.7026
#         }
#     ],
#     "resultsCount": 2,
#     "status": "OK",
#     "ticker": "AAPL"
# }
# {
#     "request_id": "1dadb735223cb3ee6c9e1c354d34408b",
#     "results": {
#         "ticker": "AAPL",
#         "name": "Apple Inc.",
#         "market": "stocks",
#         "locale": "us",
#         "primary_exchange": "XNAS",
#         "type": "CS",
#         "active": true,
#         "currency_name": "usd",
#         "cik": "0000320193",
#         "composite_figi": "BBG000B9XRY4",
#         "share_class_figi": "BBG001S5N8V8",
#         "market_cap": 3153849018160,
#         "phone_number": "(408) 996-1010",
#         "address": {
#             "address1": "ONE APPLE PARK WAY",
#             "city": "CUPERTINO",
#             "state": "CA",
#             "postal_code": "95014"
#         },
#         "description": "Apple is among the largest companies in the world, with a broad portfolio of hardware and software products targeted at consumers and businesses. Apple's iPhone makes up a majority of the firm sales, and Apple's other products like Mac, iPad, and Watch are designed around the iPhone as the focal point of an expansive software ecosystem. Apple has progressively worked to add new applications, like streaming video, subscription bundles, and augmented reality. The firm designs its own software and semiconductors while working with subcontractors like Foxconn and TSMC to build its products and chips. Slightly less than half of Apple's sales come directly through its flagship stores, with a majority of sales coming indirectly through partnerships and distribution.",
#         "sic_code": "3571",
#         "sic_description": "ELECTRONIC COMPUTERS",
#         "ticker_root": "AAPL",
#         "homepage_url": "https://www.apple.com",
#         "total_employees": 164000,
#         "list_date": "1980-12-12",
#         "branding": {
#             "logo_url": "https://api.polygon.io/v1/reference/company-branding/YXBwbGUuY29t/images/2025-04-04_logo.svg",
#             "icon_url": "https://api.polygon.io/v1/reference/company-branding/YXBwbGUuY29t/images/2025-04-04_icon.png"
#         },
#         "share_class_shares_outstanding": 14935826000,
#         "weighted_shares_outstanding": 14935826000,
#         "round_lot": 100
#     },
#     "status": "OK"
# }
