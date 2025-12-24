import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import Stock from './Stock';
import Portfolio from './Portfolio.js';
import Watchlist from './Watchlist.js'
import { getSingleStock } from '../store/stocksStore';
import { getPortfolio } from '../store/portfolioStore';
import "./HomePage.css"

function HomePage() {
    const dispatch = useDispatch();
    const [defaultTicker] = useState("AAPL");
    const portfolio = useSelector(state => state.portfolio);
    const stocks = useSelector(state => state.stocks);
    
    // Get the first stock from portfolio or use AAPL
    const portfolioTickers = Object.keys(portfolio || {});
    const displayTicker = portfolioTickers[0] || defaultTicker;

    useEffect(() => {
        // Fetch portfolio on mount
        dispatch(getPortfolio());
    }, [dispatch]);

    useEffect(() => {
        // Fetch the default stock data when ticker changes
        if (displayTicker) {
            dispatch(getSingleStock(displayTicker));
        }
    }, [dispatch, displayTicker]);

    return (
        <div id="home-container">
            <div id="homepage-left">
                <div id="homepage-chart">
                    <Stock ticker={displayTicker} />
                </div>

                <div id="homepage-portfolio-title">Your Portfolio</div>
                <div id="homepage-portfolio"><Portfolio /></div>
            </div>

            <div id="homepage-right">
                <Watchlist />
            </div>
        </div>
    )
}
export default HomePage;