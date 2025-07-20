import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { getSingleStock } from '../store/stocksStore';
import { Line } from 'react-chartjs-2';
import WatchlistAddButton from './WatchlistAddButton';
import './Stock.css';

function Stock({ ticker }) {
  const [timePeriod, setTimePeriod] = useState('dailyPrices'); // Default to dailyPrices
  const [data, setData] = useState({ labels: [], datasets: [] });
  const stocks = useSelector(state => state.stocks);
  const dispatch = useDispatch();

  const options = {
    maintainAspectRatio: false,
    scales: {
      y: {
        beginAtZero: false,
      },
      x: {
        display: true,
        grid: { color: "#000000" }
      }
    }
  };

  useEffect(() => {
    dispatch(getSingleStock(ticker));
  }, [dispatch, ticker]);
  useEffect(() => {
    if (stocks[ticker]) {
      setData({
        labels: stocks[ticker][`${timePeriod}Labels`] || [],
        datasets: [
          {
            label: ticker,
            data: stocks[ticker][timePeriod] || [],
            fill: false,
            backgroundColor: 'rgb(255, 99, 132)',
            borderColor: 'rgba(255, 99, 132, 0.2)',
          },
        ],
      });
    }
  }, [timePeriod, stocks, ticker]);

  // Debug: log chart data
  console.log(stocks[ticker]?.[timePeriod], "Chart data");

  return (
    <div className="graphContainer">
      <div className="stockstuff2">
        <div id="stock_name">{stocks[ticker]?.shortName}</div>
        <div id="stock-price-spacer">
          <span id="stock_price">{stocks[ticker]?.currentPrice}</span>
          <span id="stock_percent">{stocks[ticker]?.percentText}</span>
        </div>
      </div>
      <div className="graph">
        {stocks[ticker] && data.labels.length > 0 ? (
          <Line
            data={data}
            options={options}
            height={400}
            width={650}
          />
        ) : (
          <h3>Loading...</h3>
        )}
      </div>
      <div className="graphButtonContainer">
        <div className="graphButtons">
          <button className="daily_prices graphButton" onClick={() => setTimePeriod("dailyPrices")}>1D</button>
          <button className="weekly_prices graphButton" onClick={() => setTimePeriod("weeklyPrices")}>1W</button>
          <button className="one_month_prices graphButton" onClick={() => setTimePeriod("oneMonthPrices")}>1M</button>
          <button className="yearly_prices graphButton" onClick={() => setTimePeriod("yearlyPrices")}>1Y</button>
          <button className="all_time_prices graphButton" onClick={() => setTimePeriod("allTimePrices")}>ALL</button>
        </div>
      </div>
    </div>
  );
}

export default Stock;