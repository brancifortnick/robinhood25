import React, { useState } from 'react'
import Stock from './Stock'
import { useSelector } from 'react-redux';


function Portfolio() {
  const stocks = useSelector(state => Object.values(state.portfolio || {}));
  return (
    <div>
      {stocks.map(stock => (
        <div key={stock.ticker}>
          <h2>{stock.ticker}</h2>
          <Stock ticker={stock.ticker} />
          <div>
            {stock.description ? stock.description.slice(0, 500) : ""}
          </div>
        </div>
      ))}
      </div>
  );
}
export default Portfolio;