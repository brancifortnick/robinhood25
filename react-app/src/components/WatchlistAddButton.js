import React,{useEffect} from "react";
import { useDispatch } from "react-redux";
import { getAllInWatchList, addNewTicker } from "../store/watchlistStore";
import { useHistory } from "react-router-dom";
import './WatchlistAddButton.css'

function WatchlistAddButton({ ticker }) {
  const dispatch = useDispatch();
  const history = useHistory();



  return (
    // <div className="add-ticker-container">

    <button
      className="add-button"
      onClick={async () => {
        await dispatch(addNewTicker(ticker));
        await dispatch(getAllInWatchList());
       
      
      }}

    >
      ✔︎ Add {ticker} to Watchlist
    </button>


    // </div>
  );
}
export default WatchlistAddButton;
