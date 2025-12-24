import React, { useEffect, useState } from 'react';
import ReactDOM from "react-dom";
import { useDispatch, useSelector } from "react-redux";
import { getPortfolio } from '../store/portfolioStore';
import { getSingleStock } from '../store/stocksStore';
import "./BuyPanel.css"
import WatchlistAddButton from './WatchlistAddButton';
import { updateStock } from '../store/portfolioStore';
import { updateBalance } from '../store/userStore';
import { authenticate } from '../store/session';

export default function BuyPanel({ ticker }) {

    console.log(ticker, "ticker in buy panel------------------------")
    const dispatch = useDispatch();
    const user = useSelector(state => state.session.user)
    const portfolio = useSelector(state => state.portfolio)
    const stocks = useSelector(state => state.stocks)
    const [currentPrice, setCurrentPrice] = useState(null);
    const [loading, setLoading] = useState(true);
    const [isProcessing, setIsProcessing] = useState(false);
    
    useEffect(() => {
        // Fetch portfolio and user data on mount
        dispatch(getPortfolio())
        dispatch(authenticate())
    }, [dispatch])

    // Get current stock price from Redux store
    useEffect(() => {
        const stockData = stocks[ticker];
        if (stockData && stockData.currentPrice) {
            setCurrentPrice(stockData.currentPrice);
            setLoading(false);
        } else {
            // Fetch stock data if not available
            dispatch(getSingleStock(ticker));
            setLoading(false);
        }
    }, [ticker, stocks, dispatch]);

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

    const handleBuy = async () => {
        if (isProcessing) return;
        
        if (!stockPrice || stockPrice <= 0) {
            alert('Unable to fetch current stock price. Please try again.');
            return;
        }
        if (cashBalance < stockPrice) {
            alert(`Insufficient funds. You need $${stockPrice.toFixed(2)} but only have $${cashBalance.toFixed(2)}`);
            return;
        }
        
        setIsProcessing(true);
        try {
            // Update stock portfolio with price
            await dispatch(updateStock(ticker, "add", stockPrice));
            // Update user's cash balance (subtract the cost)
            await dispatch(updateBalance(stockPrice, "subtract"));
            // Refresh portfolio and user data
            await dispatch(getPortfolio());
            await dispatch(authenticate());
            console.log('Buy completed successfully');
        } catch (error) {
            console.error('Error buying stock:', error);
            alert('Error buying stock: ' + error.message);
        } finally {
            setIsProcessing(false);
        }
    };

    const handleSell = async () => {
        if (isProcessing) return;
        
        if (shareCount <= 0) {
            alert('You do not own any shares of this stock.');
            return;
        }
        
        setIsProcessing(true);
        try {
            // Update stock portfolio with price
            await dispatch(updateStock(ticker, "subtract", stockPrice));
            // Update user's cash balance (add the sale proceeds)
            await dispatch(updateBalance(stockPrice, "add"));
            // Refresh portfolio and user data
            await dispatch(getPortfolio());
            await dispatch(authenticate());
            console.log('Sell completed successfully');
        } catch (error) {
            console.error('Error selling stock:', error);
            alert('Error selling stock: ' + error.message);
        } finally {
            setIsProcessing(false);
        }
    };

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
                <button 
                    id='buy' 
                    onClick={handleBuy}
                    disabled={isProcessing || cashBalance < stockPrice}
                    style={{opacity: isProcessing ? 0.6 : 1}}
                >
                    {isProcessing ? 'Processing...' : 'Buy 1 Share'}
                </button>
                <br></br>
                <button 
                    id='sell' 
                    onClick={handleSell}
                    disabled={isProcessing || shareCount <= 0}
                    style={{opacity: isProcessing ? 0.6 : 1}}
                >
                    {isProcessing ? 'Processing...' : 'Sell 1 Share'}
                </button>
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
