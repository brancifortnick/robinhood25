import { setUser, SET_USER } from "./session"

export const updateBalance = (amount, operator) => async (dispatch) => {
  try {
    console.log(`Updating balance: ${operator} $${amount}`);
    const response = await fetch(`/api/users/balance/${amount}/${operator}`, {
      method: 'POST'
    })
    if (response.ok) {
      const user = await response.json()
      console.log('Updated user balance:', user.cash_balance);
      dispatch(setUser(user))
      return user;
    } else {
      const error = await response.json();
      console.error('Error updating balance:', error);
      throw new Error(error.error || 'Failed to update balance');
    }
  }    
  catch (e) {
    console.error('Error from userStore:', e)
    throw e;
  }
}

