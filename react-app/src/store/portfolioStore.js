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
        const portfolio = await response.json();
        dispatch(loadPortfolio(portfolio));
    }
};

export const updateStock = (ticker, operator) => async dispatch => {
    let response;
    if (operator === 'add' || operator === 'subtract') {
        response = await fetch(`/api/portfolio-stocks/${ticker}/${operator}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });
        if (response.ok) {
            const purchasedStock = await response.json();
            dispatch(addStock(purchasedStock));
        }
    }
};

const initialState = {};

export default function portfolioReducer(state = initialState, action) {
    switch (action.type) {
        case LOAD_PORTFOLIO: {
            let newState = {};
            if (Array.isArray(action.portfolio)) {
                action.portfolio.forEach(stock => {
                    newState[stock.ticker] = stock;
                });
            } else if (action.portfolio && typeof action.portfolio === 'object') {
                // Handle single stock object
                newState[action.portfolio.ticker] = action.portfolio;
            } else {
                console.error("action.portfolio is not an array or object:", action.portfolio);
            }
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