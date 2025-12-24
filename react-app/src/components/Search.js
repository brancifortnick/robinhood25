import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { Redirect } from 'react-router';
import { useHistory } from 'react-router-dom';
import { getSingleStock } from '../store/stocksStore';
import { tickerList } from './assets';
import './Search.css';

function Search() {
  const [searchQuery, setSearchQuery] = useState('');
  const [tickersShown, setTickersShown] = useState([]);
  let history = useHistory();

  let tickersRegex = new RegExp(searchQuery, "i")

  const filterTickers = () => {
    if(searchQuery.length > 0) {
      let newTickers = tickerList.filter(ticker => {
        return tickersRegex.test(ticker)
      })
      if (newTickers.length > 9) newTickers.length = 9;
      setTickersShown(newTickers)
    } else if (searchQuery.length === 0) {
      setTickersShown([])
    }
  }

  function handleClick() {
    history.push(`/search-results/${searchQuery}`);
    setSearchQuery('');
    window.location.reload(false);
  }

  function handleClickSuggestions(ticker) {
    history.push(`/search-results/${ticker}`);
    setSearchQuery('');
    window.location.reload(false);
  }

  useEffect(() => {
    tickersRegex = new RegExp(('^' + searchQuery), "i")
    filterTickers()
  }, [searchQuery])

  return (
    <div className="search-wrapper">
      <div className="search-input-container">
        <svg 
          className="search-icon" 
          width="20" 
          height="20" 
          viewBox="0 0 24 24" 
          fill="none" 
          stroke="currentColor" 
          strokeWidth="2"
        >
          <circle cx="11" cy="11" r="8"></circle>
          <path d="m21 21-4.35-4.35"></path>
        </svg>
        <input
          value={searchQuery}
          onInput={e => setSearchQuery(e.target.value)}
          type="search"
          id="search-form"
          className="search-bar-input"
          placeholder="Search stocks..."
          autoComplete="off"
        />
      </div>
      {searchQuery && tickersShown.length > 0 && (
        <div className="suggested-search-box">
          {tickersShown.map((ticker, index) => (
            <div 
              key={index}
              className="search-result-item" 
              onClick={() => handleClickSuggestions(ticker)}
            >
              <div className="search-result-ticker">{ticker}</div>
            </div>
          ))}
        </div>
      )}
      {searchQuery && tickersShown.length === 0 && (
        <div className="suggested-search-box">
          <div className="search-no-results">
            No results found for "{searchQuery}"
          </div>
        </div>
      )}
    </div>
  );
}
export default Search;
