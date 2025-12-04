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
    console.log(portfolio, "portfilio object so i can query price>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    console.log(portfolio, "stocks object------------------------")
    
    useEffect(() => {
        dispatch(getPortfolio())
    }, [dispatch])

    // Safety checks
    if (!user) {
        return <div>Loading user data...</div>
    }

    const stockData = portfolio?.[ticker]
    const shareCount = stockData?.share_count || 0
    const cashBalance = user?.cash_balance || 0

    return (
        <>


            <div id="buy-panel">
                <div id="buy-1">Buy {ticker} </div>

                <div id="buy-2">
                    <span>Cur. Quantity</span>
                    <span>{shareCount}</span>
                </div>

            <div id="buy-3">
                <button id='buy' onClick={async () => {
                    if (!stockData?.basis) {
                        console.error('Portfolio data not available for', ticker);
                        alert('Unable to complete purchase. Please try again.');
                        return;
                    }
                    await dispatch(updateStock(ticker, "add"));
                    await dispatch(
                        updateBalance(stockData.basis, "subtract")
                    );
                }}>Buy 1</button>
                <br></br>
                <button style={{ "background-color": "salmon" }} id='sell' onClick={async () => {
                    if (!stockData?.basis) {
                        console.error('Portfolio data not available for', ticker);
                        alert('Unable to complete sale. Please try again.');
                        return;
                    }
                    if (shareCount <= 0) {
                        alert('You do not own any shares of this stock.');
                        return;
                    }
                    await dispatch(updateStock(ticker, "subtract"));
                    await dispatch(
                        updateBalance(stockData.basis, "add")
                    );
                }}>Sell 1</button>
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
