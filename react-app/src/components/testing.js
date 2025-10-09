import { restClient } from '@polygon.io/client-js';

const apiKey = "HeaU3koUzBjxghGHFDLnA6QytX5uPZv7";
const rest = restClient(apiKey, 'https://api.polygon.io');

async function example_getTicker() {
  try {
    const response = await rest.getTicker(
      {
        ticker: "AAPL",
      }
    );
    console.log('Response:', response);
  } catch (e) {
    console.error('An error happened:', e);
  }
}

example_getTicker();