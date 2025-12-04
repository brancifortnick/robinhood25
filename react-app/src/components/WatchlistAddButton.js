import React, { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { getAllInWatchList, addNewTicker, deleteTickerThunk } from "../store/watchlistStore";
import { useHistory } from "react-router-dom";
import './WatchlistAddButton.css'

function WatchlistAddButton({ ticker }) {
  const dispatch = useDispatch();
  const history = useHistory();
  const watchlist = useSelector(state => state.watchlist);
  const [isInWatchlist, setIsInWatchlist] = useState(false);
  const [isAdding, setIsAdding] = useState(false);
  const [hasLoaded, setHasLoaded] = useState(false);

  useEffect(() => {
    // Only fetch watchlist once on mount
    if (!hasLoaded) {
      dispatch(getAllInWatchList());
      setHasLoaded(true);
    }
  }, [dispatch, hasLoaded]);

  useEffect(() => {
    // Check if ticker is in watchlist
    const inWatchlist = Object.values(watchlist).some(stock => stock.ticker === ticker);
    setIsInWatchlist(inWatchlist);
  }, [watchlist, ticker]);

  const handleClick = async () => {
    setIsAdding(true);
    try {
      if (isInWatchlist) {
        await dispatch(deleteTickerThunk(ticker));
      } else {
        await dispatch(addNewTicker(ticker));
      }
      await dispatch(getAllInWatchList());
    } catch (error) {
      console.error('Error updating watchlist:', error);
    } finally {
      setTimeout(() => setIsAdding(false), 300);
    }
  };

  return (
    <button
      className={`add-watchlist-button ${isInWatchlist ? 'in-watchlist' : ''} ${isAdding ? 'adding' : ''}`}
      onClick={handleClick}
      disabled={isAdding}
    >
      <span className="button-icon">
        {isInWatchlist ? '★' : '☆'}
      </span>
      <span className="button-text">
        {isInWatchlist ? `Remove from Watchlist` : `Add to Watchlist`}
      </span>
    </button>
  );
}
export default WatchlistAddButton;
