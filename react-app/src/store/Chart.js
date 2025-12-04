const chartData = {
  labels: data.results.map(item => new Date(item.t).toLocaleDateString()),
  datasets: [{
    label: ticker,
    data: data.results.map(item => item.c), // closing prices
  }]
};