export const getChartDays = async () => {
  const response = await fetch(`http://localhost:8004/api/dashboard/charts`);
  if (!response.ok) {
    throw new Error("Failed to fetch data");
  }
  const data = await response.json();
  return {
    daily_series: data.daily_series,
    weekly_series: data.weekly_series,
    monthly_series: data.monthly_series,
  };
};

export const getCorrelations = async () => {
  const response = await fetch(
    `http://localhost:8004/api/dashboard/correlation`
  );
  if (!response.ok) {
    throw new Error("Failed to fetch data");
  }
  const data = await response.json();
  return data.matrix;
};

export const getForecast = async () => {
  const response = await fetch(`http://localhost:8004/api/dashboard/forecast`);
  if (!response.ok) {
    throw new Error("Failed to fetch data");
  }
  const data = await response.json();
  return data;
};
