import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useParams } from 'react-router-dom';
import { getSingleStock } from '../store/stocksStore';
import { Line } from 'react-chartjs-2';
import { updateStock } from '../store/portfolioStore';
import WatchlistAddButton from './WatchlistAddButton'
import { updateBalance } from '../store/userStore';
import './Stock.css'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js';

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

function Stock() {
  const { ticker } = useParams();
  const [timePeriod, setTimePeriod] = useState('dailyPrices')
  const [hoveredPrice, setHoveredPrice] = useState(null)
  const [hoveredTime, setHoveredTime] = useState(null)
  const [data, setData] = useState({
    labels: [],
    datasets: []
  })
  const stocks = useSelector(state => state.stocks);
  const dispatch = useDispatch();
  
  // Generate time labels based on period
  const getTimeLabels = (period, dataLength) => {
    const now = new Date();
    
    switch(period) {
      case 'dailyPrices': {
        // Intraday - show hours (9:30 AM to 4:00 PM)
        const labels = [];
        const startHour = 9;
        const startMinute = 30;
        
        for (let i = 0; i < dataLength; i++) {
          const totalMinutes = startMinute + (i * 20); // 20-minute intervals
          const hours = startHour + Math.floor(totalMinutes / 60);
          const minutes = totalMinutes % 60;
          
          if (hours > 12) {
            labels.push(`${hours - 12}:${minutes.toString().padStart(2, '0')} PM`);
          } else {
            labels.push(`${hours}:${minutes.toString().padStart(2, '0')} AM`);
          }
        }
        return labels;
      }
      
      case 'weeklyPrices': {
        // Weekly - show days of week
        const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'];
        return days.slice(0, dataLength);
      }
      
      case 'oneMonthPrices': {
        // Monthly - show dates
        const labels = [];
        for (let i = 0; i < dataLength; i++) {
          const date = new Date(now);
          date.setDate(date.getDate() - (dataLength - 1 - i));
          labels.push(`${date.getMonth() + 1}/${date.getDate()}`);
        }
        return labels;
      }
      
      case 'yearlyPrices': {
        // Yearly - show months
        const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
        return months.slice(0, dataLength);
      }
      
      case 'allTimePrices': {
        // All time - show years
        const labels = [];
        const currentYear = now.getFullYear();
        for (let i = 0; i < dataLength; i++) {
          labels.push(`${currentYear - (dataLength - 1 - i)}`);
        }
        return labels;
      }
      
      default:
        return Array.from({ length: dataLength }, (_, i) => i + 1);
    }
  };
  
  const options = {
    responsive: true,
    maintainAspectRatio: false,
    interaction: {
      mode: 'index',
      intersect: false,
    },
    onHover: (event, activeElements) => {
      if (activeElements && activeElements.length > 0) {
        const dataIndex = activeElements[0].index;
        const price = data.datasets[0].data[dataIndex];
        const time = data.labels[dataIndex];
        setHoveredPrice(price);
        setHoveredTime(time);
      } else {
        setHoveredPrice(null);
        setHoveredTime(null);
      }
    },
    plugins: {
      legend: {
        display: false
      },
      tooltip: {
        enabled: true,
        backgroundColor: 'rgba(0, 0, 0, 0.8)',
        padding: 12,
        titleFont: {
          size: 14,
          weight: '600'
        },
        bodyFont: {
          size: 13
        },
        displayColors: false,
        callbacks: {
          title: function(context) {
            return context[0].label;
          },
          label: function(context) {
            return '$' + context.parsed.y.toFixed(2);
          }
        }
      }
    },
    scales: {
      x: {
        display: true,
        grid: {
          display: false,
          drawBorder: false
        },
        ticks: {
          color: '#6F7380',
          font: {
            size: 12,
            weight: '500'
          },
          maxRotation: 0,
          autoSkip: true,
          maxTicksLimit: 8
        }
      },
      y: {
        display: true,
        position: 'right',
        grid: {
          display: true,
          color: 'rgba(0, 0, 0, 0.05)',
          drawBorder: false
        },
        ticks: {
          color: '#6F7380',
          font: {
            size: 12,
            weight: '500'
          },
          callback: function(value) {
            return '$' + value.toFixed(0);
          },
          maxTicksLimit: 6
        }
      }
    }
  };

  useEffect(() => {
    // Fetch stock data only when ticker changes
    dispatch(getSingleStock(ticker));
  }, [dispatch, ticker])

  useEffect(() => {
    if (stocks[ticker] && stocks[ticker][timePeriod] && Array.isArray(stocks[ticker][timePeriod])) {
      const priceData = stocks[ticker][timePeriod];
      const labels = getTimeLabels(timePeriod, priceData.length);
      
      // Determine if prices are going up or down for color
      const firstPrice = priceData[0];
      const lastPrice = priceData[priceData.length - 1];
      const isPositive = lastPrice >= firstPrice;
      
      // Robinhood-style colors
      const lineColor = isPositive ? 'rgb(0, 200, 5)' : 'rgb(255, 80, 0)';
      const gradientColor = isPositive 
        ? 'rgba(0, 200, 5, 0.1)' 
        : 'rgba(255, 80, 0, 0.1)';
      
      setData({
        labels: labels,
        datasets: [
          {
            label: ticker,
            data: priceData,
            fill: true,
            backgroundColor: (context) => {
              const ctx = context.chart.ctx;
              const gradient = ctx.createLinearGradient(0, 0, 0, 400);
              gradient.addColorStop(0, gradientColor);
              gradient.addColorStop(1, 'rgba(255, 255, 255, 0)');
              return gradient;
            },
            borderColor: lineColor,
            borderWidth: 2.5,
            pointRadius: 0,
            pointHoverRadius: 6,
            pointHoverBorderWidth: 2,
            pointHoverBackgroundColor: '#FFFFFF',
            pointHoverBorderColor: lineColor,
            tension: 0.4,
            cubicInterpolationMode: 'monotone'
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
        <div style={{ flex: 1 }}>
          <div id="stock_name">{stocks[ticker]?.shortName}</div>
          <div id="stock-price-spacer">
            <span id="stock_price">
              ${hoveredPrice ? hoveredPrice.toFixed(2) : stocks[ticker]?.currentPrice}
            </span>
            {!hoveredPrice && (
              <span id="stock_percent" className={stocks[ticker]?.percentText?.startsWith('+') ? 'positive' : 'negative'}>
                {stocks[ticker]?.percentText}
              </span>
            )}
            {hoveredTime && (
              <span style={{ 
                fontSize: '13px', 
                color: 'var(--rh-gray-600)', 
                marginLeft: '8px',
                fontWeight: '500'
              }}>
                {hoveredTime}
              </span>
            )}
          </div>
        </div>
      </div>
      <div className="graph">
        {stocks[ticker] && data.datasets && data.datasets.length > 0 ? (
          <Line 
            data={data}
            options={options}
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
            className={`graphButton ${timePeriod === 'dailyPrices' ? 'active' : ''}`}
            onClick={() => {
              setTimePeriod("dailyPrices");
            }}
          >
            1D
          </button>
          <button
            className={`graphButton ${timePeriod === 'weeklyPrices' ? 'active' : ''}`}
            onClick={() => {
              setTimePeriod("weeklyPrices");
            }}
          >
            1W
          </button>
          <button
            className={`graphButton ${timePeriod === 'oneMonthPrices' ? 'active' : ''}`}
            onClick={() => {
              setTimePeriod("oneMonthPrices");
            }}
          >
            1M
          </button>
          <button
            className={`graphButton ${timePeriod === 'yearlyPrices' ? 'active' : ''}`}
            onClick={() => {
              setTimePeriod("yearlyPrices");
            }}
          >
            1Y
          </button>
          <button
            className={`graphButton ${timePeriod === 'allTimePrices' ? 'active' : ''}`}
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