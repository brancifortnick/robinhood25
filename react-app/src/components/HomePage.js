import React, { useState, useEffect } from 'react';
import Stock from './Stock';
import Portfolio from './Portfolio.js';
import Watchlist from './Watchlist.js'
import "./HomePage.css"
import { useDispatch } from 'react-redux';
function HomePage({ ticker }) {
        const dispatch = useDispatch();

    const [data, setData] = useState(null);
    ticker = data?.results?.ticker || "AAPL"
    let tickerFunc= () => {
        return {
            ticker: ticker || "AAPL",
            logo_url: data?.results?.brands?.logo_url || "https://static.robinhood.com/assets/logos/robinhood.png"
            
        }
    }
    
    const trySafety = (func) => {
        
        try {
            return func(tickerFunc());
        } catch (e) {
            console.error("Error executing function:", e);
            return null;
        }
    };
    trySafety(tickerFunc)
    
    useEffect(() => {
        const fetchData = async () => {
            const response = await fetch(`/api/external-stocks/${ticker}/results/branding/${data?.results?.brands?.logo_url}`);
            const resData = await response.json();
            setData(resData);
        }
        fetchData();

    }, [ticker, dispatch]);

    return (
        <div id="home-container">


            <div id="homepage-left">
                <div id="homepage-chart">
                    <Stock ticker={"AAPL"} />
                </div>

                <div id="homepage-portfolio-title">Your Portfolio</div>
                <div id="homepage-portfolio"><Portfolio ticker={ticker} /></div>
            </div>


            <div id="homepage-right">
                <Watchlist />
            </div >


        </div>
    )
}
export default HomePage;