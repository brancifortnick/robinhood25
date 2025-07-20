const LOAD_MULTIPLE_STOCKS = 'stocks/LOAD_MULTIPLE_STOCKS';
const LOAD_SINGLE_STOCK = 'stocks/LOAD_SINGLE_STOCK';

const loadManyStocks = stocks => ({
  type: LOAD_MULTIPLE_STOCKS,
  stocks,
});

const loadOneStock = stock => ({
  type: LOAD_SINGLE_STOCK,
  stock,
});

export const getSingleStock = (ticker) => async dispatch => {
  try {
    const response = await fetch(`/api/stocks/${ticker}`);
    if (response.ok) {
      const stock = await response.json();
      dispatch(loadOneStock(stock));
    }
  } catch (error) {
    console.log(error);
  }
};

export const getMultipleStocks = (tickersList) => async dispatch => {
  const stocks = [];
  for (const ticker of tickersList) {
    const response = await fetch(`/api/stocks/${ticker}`);
    if (response.ok) {
      const json = await response.json();
      stocks.push(json);
    }
  }
  dispatch(loadManyStocks(stocks));
};

const initialState = {};

export default function stockReducer(state = initialState, action) {
  switch (action.type) {
    case LOAD_MULTIPLE_STOCKS: {
      const newState = { ...state };
      action.stocks.forEach(stock => {
        newState[stock.ticker] = stock;
      });
      return newState;
    }
    case LOAD_SINGLE_STOCK: {
      const newState = { ...state };
      newState[action.stock.ticker] = action.stock;
      return newState;
    }
    default:
      return state;
  }
}