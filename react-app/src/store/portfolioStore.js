const LOAD_PORTFOLIO = "portfolio/LOAD_PORTFOLIO";
const BUY_STOCK = "portfolio/BUY_STOCK";

const loadPortfolio = portfolio => ({
    type: LOAD_PORTFOLIO,
    portfolio,
});

const addStock = stockObj => ({
    type: BUY_STOCK,
    stockObj
});

export const getPortfolio = () => async dispatch => {
    const response = await fetch('/api/portfolio-stocks/');
    if (response.ok) {
        const data = await response.json();
        const portfolio = data.portfolio || data; // Handle both formats
        dispatch(loadPortfolio(Array.isArray(portfolio) ? portfolio : []));
    }
};

export const updateStock = (ticker, operator, price) => async dispatch => {
    if (operator === 'add' || operator === 'subtract') {
        const response = await fetch(`/api/portfolio-stocks/${ticker}/${operator}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ price })
        });
        if (response.ok) {
            const purchasedStock = await response.json();
            dispatch(addStock(purchasedStock));
        } else {
            const error = await response.json();
            console.error('Error updating stock:', error);
            throw new Error(error.error || 'Failed to update stock');
        }
    }
};

const initialState = {};

export default function portfolioReducer(state = initialState, action) {
    switch (action.type) {
        case LOAD_PORTFOLIO: {
            if (!Array.isArray(action.portfolio)) {
                console.warn("Portfolio is not an array:", action.portfolio);
                return state;
            }
            const newState = {};
            action.portfolio.forEach(stock => {
                newState[stock.ticker] = stock;
            });
            return newState;
        }
        case BUY_STOCK: {
            return {
                ...state,
                [action.stockObj.ticker]: action.stockObj
            };
        }
        default:
            return state;
    }
}