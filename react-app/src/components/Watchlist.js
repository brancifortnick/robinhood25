import React, { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { Link } from "react-router-dom";

import { getAllInWatchList, deleteTickerThunk } from "../store/watchlistStore";
import { getSingleStock, getMultipleStocks } from "../store/stocksStore";
import "./Watchlist.css";

function Watchlist() {
  const stocks = useSelector((state) => state.stocks);
  const watchlist = useSelector((state) => state.watchlist);
  const dispatch = useDispatch();
  const [hasFetchedStocks, setHasFetchedStocks] = useState(false);

  useEffect(() => {
    dispatch(getAllInWatchList());
  }, [dispatch]);

  useEffect(() => {
    const watchlistValuesArray = Object.values(watchlist);
    if (watchlistValuesArray.length > 0 && !hasFetchedStocks) {
      console.log('Fetching stocks for watchlist items...');
      for (const stock of watchlistValuesArray) {
        dispatch(getSingleStock(stock.ticker));
      }
      setHasFetchedStocks(true);
    }
  }, [watchlist.length, dispatch, hasFetchedStocks]);


  return (
    <div className="add-to-watchlist-container">
      <div id='watchlist-title'>Watchlist</div>
      {watchlist && Object.keys(watchlist).length > 0 ? (
        Object.values(watchlist).map((watchedStock) => {
          const stockData = stocks[watchedStock.ticker];
          return (
            <Link 
              to={`/asset/${watchedStock.ticker}`} 
              key={watchedStock.ticker}
              className="link-look"
              style={{width: '100%', textDecoration: 'none', color: 'inherit'}}
            >
              <div className="watchlist-components">
                <div className="watchlist-stock-info">
                  {stockData?.logoUrl && (
                    <img 
                      src={stockData.logoUrl}
                      alt={`${watchedStock.ticker} logo`}
                      className="stock-logo"
                      onError={(e) => {
                        if (stockData?.logoFallback) {
                          e.target.src = stockData.logoFallback;
                        }
                      }}
                    />
                  )}
                  <div className="ticker-info">
                    <div className="ticker-name">{watchedStock.ticker}</div>
                    <div className="company-name">{stockData?.shortName || 'Loading...'}</div>
                  </div>
                </div>
                
                <div className="price-info">
                  <div className="current-price">
                    ${stockData?.currentPrice?.toFixed(2) || '---'}
                  </div>
                  <div className={`percent-change ${stockData?.percentText?.startsWith('+') ? 'positive' : 'negative'}`}>
                    {stockData?.percentText || '---'}
                  </div>
                </div>

                <button
                  className="delete-button"
                  onClick={async (e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    await dispatch(deleteTickerThunk(watchedStock.ticker));
                    await dispatch(getAllInWatchList());
                  }}>
                  ×
                </button>
              </div>
            </Link>
          );
        })
      ) : (
        <div style={{padding: '20px', textAlign: 'center', color: '#666'}}>
          No stocks in watchlist
        </div>
      )}
    </div >
  );
}
export default Watchlist;
