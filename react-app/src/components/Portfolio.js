import React, { useState, useEffect } from 'react'
import { useSelector } from 'react-redux';
import { Link } from 'react-router-dom';
import './Portfolio.css';


function Portfolio() {
  const portfolio = useSelector(state => state.portfolio || {});
  const stocks = Object.values(portfolio);
  const [stockPrices, setStockPrices] = useState({});
  const [hasFetched, setHasFetched] = useState(false);
  
  useEffect(() => {
    // Only fetch prices once when component mounts or portfolio changes significantly
    if (stocks.length > 0 && !hasFetched) {
      const fetchPrices = async () => {
        const prices = {};
        for (let stock of stocks) {
          try {
            const response = await fetch(`/api/stocks/${stock.ticker}`);
            if (response.ok) {
              const data = await response.json();
              prices[stock.ticker] = {
                currentPrice: data.currentPrice || data.price || 0,
                percentChange: data.percentChange || 0,
                companyName: data.companyName || stock.ticker,
                logoUrl: data.logoUrl,
                logoFallback: data.logoFallback
              };
            }
          } catch (error) {
            console.error(`Error fetching price for ${stock.ticker}:`, error);
          }
        }
        setStockPrices(prices);
        setHasFetched(true);
      };
      
      fetchPrices();
    }
  }, [stocks.length, hasFetched]);

  if (!stocks.length) {
    return (
      <div style={{ 
        textAlign: 'center', 
        padding: 'var(--spacing-3xl)',
        color: 'var(--rh-gray-600)'
      }}>
        <div style={{ fontSize: '48px', marginBottom: 'var(--spacing-lg)', opacity: 0.3 }}>📊</div>
        <h3 style={{ fontSize: '20px', marginBottom: 'var(--spacing-md)' }}>No stocks in portfolio</h3>
        <p style={{ fontSize: '15px' }}>Buy your first stock to get started!</p>
      </div>
    );
  }

  return (
    <div className="ticker-container-inner">
      <table>
        <thead>
          <tr>
            <th>Company</th>
            <th>Shares</th>
            <th>Avg Cost</th>
            <th>Current Price</th>
            <th>Total Value</th>
            <th>Gain/Loss</th>
            <th>Return %</th>
          </tr>
        </thead>
        <tbody>
          {stocks.map(stock => {
            const priceData = stockPrices[stock.ticker] || {};
            const currentPrice = priceData.currentPrice || stock.basis || 0;
            const totalCost = stock.basis * stock.share_count;
            const totalValue = currentPrice * stock.share_count;
            const gainLoss = totalValue - totalCost;
            const returnPercent = totalCost > 0 ? ((gainLoss / totalCost) * 100) : 0;
            const isPositive = gainLoss >= 0;

            return (
              <tr key={stock.ticker}>
                <td>
                  <Link to={`/stocks/${stock.ticker}`} style={{ 
                    display: 'flex', 
                    alignItems: 'center', 
                    gap: 'var(--spacing-md)',
                    textDecoration: 'none',
                    color: 'inherit'
                  }}>
                    {priceData.logoUrl && (
                      <img 
                        src={priceData.logoUrl} 
                        alt={stock.ticker}
                        onError={(e) => {
                          e.target.onerror = null;
                          e.target.src = priceData.logoFallback;
                        }}
                        style={{
                          width: '32px',
                          height: '32px',
                          borderRadius: 'var(--radius-sm)',
                          border: '1px solid var(--rh-gray-300)',
                          objectFit: 'cover'
                        }}
                      />
                    )}
                    <div>
                      <div style={{ fontWeight: 600 }}>{stock.ticker}</div>
                      <div style={{ fontSize: '13px', color: 'var(--rh-gray-600)' }}>
                        {priceData.companyName}
                      </div>
                    </div>
                  </Link>
                </td>
                <td>{stock.share_count}</td>
                <td>${stock.basis.toFixed(2)}</td>
                <td>${currentPrice.toFixed(2)}</td>
                <td>${totalValue.toFixed(2)}</td>
                <td className={isPositive ? 'positive' : 'negative'}>
                  {isPositive ? '+' : ''}${gainLoss.toFixed(2)}
                </td>
                <td className={isPositive ? 'positive' : 'negative'}>
                  {isPositive ? '+' : ''}{returnPercent.toFixed(2)}%
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}

export default Portfolio;