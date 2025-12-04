import React, { useEffect, useState } from 'react';
import ReactDOM from "react-dom";
import { useDispatch, useSelector } from "react-redux";
import { getPortfolio } from '../store/portfolioStore';
import { getSingleStock } from '../store/stocksStore';
import "./BuyPanel.css"
import WatchlistAddButton from './WatchlistAddButton';
import { updateStock } from '../store/portfolioStore';
import { updateBalance } from '../store/userStore';

export default function BuyPanel({ ticker }) {

    console.log(ticker, "ticker in buy panel------------------------")
    const dispatch = useDispatch();
    const user = useSelector(state => state.session.user)
    const portfolio = useSelector(state => state.portfolio)
    const stocks = useSelector(state => state.stocks)
    const [currentPrice, setCurrentPrice] = useState(null);
    const [loading, setLoading] = useState(true);
    
    useEffect(() => {
        dispatch(getPortfolio())
        dispatch(getSingleStock(ticker))
    }, [dispatch, ticker])

    // Fetch current stock price
    useEffect(() => {
        const fetchPrice = async () => {
            try {
                const response = await fetch(`/api/stocks/${ticker}`);
                if (response.ok) {
                    const data = await response.json();
                    setCurrentPrice(data.currentPrice || data.price || 0);
                }
            } catch (error) {
                console.error('Error fetching stock price:', error);
            } finally {
                setLoading(false);
            }
        };
        fetchPrice();
    }, [ticker]);

    // Safety checks
    if (!user) {
        return <div>Loading user data...</div>
    }

    if (loading) {
        return <div id="buy-panel"><div id="buy-1">Loading...</div></div>
    }

    const stockData = portfolio?.[ticker]
    const shareCount = stockData?.share_count || 0
    const cashBalance = user?.cash_balance || 0
    const stockPrice = currentPrice || stockData?.basis || 0

    return (
        <>


            <div id="buy-panel">
                <div id="buy-1">Buy {ticker} </div>

                <div id="buy-2">
                    <span>Shares Owned</span>
                    <span>{shareCount}</span>
                </div>

                <div id="buy-2">
                    <span>Market Price</span>
                    <span>${stockPrice.toFixed(2)}</span>
                </div>

            <div id="buy-3">
                <button id='buy' onClick={async () => {
                    if (!stockPrice || stockPrice <= 0) {
                        alert('Unable to fetch current stock price. Please try again.');
                        return;
                    }
                    if (cashBalance < stockPrice) {
                        alert(`Insufficient funds. You need $${stockPrice.toFixed(2)} but only have $${cashBalance.toFixed(2)}`);
                        return;
                    }
                    await dispatch(updateStock(ticker, "add"));
                    await dispatch(getPortfolio());
                }}>Buy 1 Share</button>
                <br></br>
                <button id='sell' onClick={async () => {
                    if (shareCount <= 0) {
                        alert('You do not own any shares of this stock.');
                        return;
                    }
                    await dispatch(updateStock(ticker, "subtract"));
                    await dispatch(getPortfolio());
                }}>Sell 1 Share</button>
            </div>
                <div id="buy-4">
                    ${cashBalance.toFixed(2)} buying power available
                </div>
            </div>


            <br></br>



            <div id="watchlist-wrapper">
                <WatchlistAddButton ticker={ticker} />
            </div>

        </>


    )
}
