import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { getSingleStock } from '../store/stocksStore';
import { Line } from 'react-chartjs-2';
import { updateStock } from '../store/portfolioStore';
import WatchlistAddButton from './WatchlistAddButton'
import { updateBalance } from '../store/userStore';
import './Stock.css'

function Stock({ ticker }) {
  const [timePeriod, setTimePeriod] = useState('dailyPrices')
  const [data, setData] = useState({
    labels: [],
    datasets: []
  })
  const stocks = useSelector(state => state.stocks);
  const dispatch = useDispatch();
  
  const options = {
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false
      }
    },
    scales: {
      x: {
        display: false,
        grid: {
          display: false
        }
      },
      y: {
        display: false,
        grid: {
          display: false
        }
      }
    }
  };

  useEffect(() => {
    (async () => {
      await dispatch(getSingleStock(ticker));
    })();
  }, [dispatch, ticker])

  useEffect(() => {
    if (stocks[ticker] && stocks[ticker][timePeriod] && Array.isArray(stocks[ticker][timePeriod])) {
      const priceData = stocks[ticker][timePeriod];
      // Generate labels based on data length
      const labels = priceData.map((_, index) => index + 1);
      
      setData({
        labels: labels,
        datasets: [
          {
            label: ticker,
            data: priceData,
            fill: false,
            backgroundColor: 'rgb(0, 200, 5)',
            borderColor: 'rgba(0, 200, 5, 0.8)',
            borderWidth: 2,
            pointRadius: 0,
            pointHoverRadius: 4,
            tension: 0.1
          },
        ],
      })
    }
  }, [timePeriod, stocks, ticker])

  return (

    <div className="graphContainer">
      <div className={"stockstuff2"}>
        {stocks[ticker]?.logoUrl && (
          <img 
            src={stocks[ticker].logoUrl} 
            alt={`${ticker} logo`}
            style={{
              width: '48px',
              height: '48px',
              borderRadius: '8px',
              marginRight: '12px',
              objectFit: 'contain',
              background: 'white',
              padding: '4px'
            }}
            onError={(e) => {
              // Fallback to the backup logo if primary fails
              if (stocks[ticker]?.logoFallback) {
                e.target.src = stocks[ticker].logoFallback;
              }
            }}
          />
        )}
        <div>
          <div id="stock_name">{stocks[ticker]?.shortName}</div>
          <div id="stock-price-spacer">
            <span id="stock_price">${stocks[ticker]?.currentPrice}</span>
            <span id="stock_percent">{stocks[ticker]?.percentText}</span>
          </div>
        </div>
      </div>
      <div className="graph">
        {stocks[ticker] && data.datasets && data.datasets.length > 0 ? (
          <Line data={data}
            options={options}
            gridLines={false}
            height={400}
            width={"650px"}
          />
        ) : (
          <div style={{height: '400px', display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
            <h3>Loading chart data...</h3>
          </div>
        )}
      </div>


      <div className="graphButtonContainer">
        <div className="graphButtons">
          <button
            className="daily_prices graphButton button-selected"
            onClick={() => {
              setTimePeriod("dailyPrices");
            }}
          >
            1D
          </button>
          <button
            className="weekly_prices graphButton"
            onClick={() => {
              setTimePeriod("weeklyPrices");
            }}
          >
            1W
          </button>
          <button
            className="one_month_prices graphButton"
            onClick={() => {
              setTimePeriod("oneMonthPrices");
            }}
          >
            1M
          </button>
          <button
            className="yearly_prices graphButton"
            onClick={() => {
              setTimePeriod("yearlyPrices");
            }}
          >
            1Y
          </button>
          <button
            className="all_time_prices graphButton"
            onClick={() => {
              setTimePeriod("allTimePrices");
            }}
          >
            ALL
          </button>
        </div>
      </div>
      <div>

      </div>
    </div>


  );
}
export default Stock;