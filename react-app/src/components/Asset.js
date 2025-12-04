import React, { useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { useParams } from 'react-router-dom';
import { getSingleStock } from '../store/stocksStore';
import Stock from './Stock';
import BuyPanel from './BuyPanel';

export default function Asset() {
    const { ticker } = useParams();
    const dispatch = useDispatch();
    const stock = useSelector(state => state.stocks[ticker]);
    const newsArray = [1, 2, 3];

    useEffect(() => {
        if (ticker) {
            dispatch(getSingleStock(ticker));
        }
    }, [dispatch, ticker]);

    return (
        <div id="mega-container">
            <div id="asset-container">
                <div id="chart">
                    <Stock ticker={ticker} />
                </div>
                <div className="titles">About</div>
                <div id="company-description">
                    {stock?.description ? stock.description.slice(0, 500) : "Loading company information..."}
                    <span style={{ "color": "rgb(0,200,5)", "fontWeight": "700" }}>Read More</span>
                    <br />
                    <br />
                </div>
                <div className={"about"}>
                    <div><p>Market Cap</p><span>${stock?.marketCap ? (stock.marketCap / 1000000).toFixed(0) : 0}M</span></div>
                    <div><p>Homepage</p><span>{stock?.homepage_url || 'N/A'}</span></div>
                    <div><p>Current Price</p><span>${stock?.currentPrice || '0.00'}</span></div>
                    <div><p>Price Change</p><span>{stock?.percentText || '0%'}</span></div>
                </div>
                <div className="titles">Key Statistics</div>
                <div className={"key-statistics"}>
                    <div><p style={{"paddingRight":"4px"}}>Price-Earnings Ratio</p><span>N/A</span></div>
                    <div><p>Dividend Yield</p><span>N/A</span></div>
                    <div><p>Average Volume</p><span>N/A</span></div>
                </div>
                <div className="titles">News</div>
                <div id="news-container">
                    <div>News integration coming soon...</div>
                </div>
            </div>
            <div id="right-panel">
                <BuyPanel ticker={ticker}/>
            </div>
        </div>
    )
}
