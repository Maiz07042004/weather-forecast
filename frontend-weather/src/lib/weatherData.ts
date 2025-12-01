// Mock weather data generator for visualization
export interface WeatherDataPoint {
  date: Date;
  weather_code: number;
  temp_max: number;
  humidity_max: number;
  rain_sum: number;
  wind_speed_max: number;
  radiation_sum: number;
}
export interface WeatherDataReSamplePoint {
  date: Date;
  granularity: "W" | "ME";
  temp_avg: number;
  rain_total: number;
  humidity_avg: number;
}
// // Generate mock data for the last 90 days
// export const generateWeatherData = (): WeatherDataPoint[] => {
//   const data: WeatherDataPoint[] = [];
//   const now = new Date();

//   for (let i = 89; i >= 0; i--) {
//     const date = new Date(now);
//     date.setDate(date.getDate() - i);

//     // Add seasonal variation
//     const dayOfYear = Math.floor((date.getTime() - new Date(date.getFullYear(), 0, 0).getTime()) / 86400000);
//     const seasonalTemp = 20 + 10 * Math.sin((dayOfYear / 365) * 2 * Math.PI);

//     // Add daily variation with some randomness
//     const dailyVariation = Math.random() * 10 - 5;
//     const temperature = seasonalTemp + dailyVariation;

//     // Generate correlated data
//     const humidity = 60 + (30 - temperature) * 2 + Math.random() * 10;
//     const pressure = 1013 + Math.random() * 20 - 10;
//     const windSpeed = Math.abs(5 + Math.random() * 15);
//     const precipitation = humidity > 70 ? Math.random() * 10 : Math.random() * 2;

//     // Determine condition based on weather metrics
//     let condition: 'Sunny' | 'Cloudy' | 'Rainy' | 'Stormy';
//     if (precipitation > 7) {
//       condition = 'Stormy';
//     } else if (precipitation > 3) {
//       condition = 'Rainy';
//     } else if (humidity > 70) {
//       condition = 'Cloudy';
//     } else {
//       condition = 'Sunny';
//     }

//     data.push({
//       date,
//       timestamp: date.toISOString().split('T')[0],
//       temperature: Math.round(temperature * 10) / 10,
//       humidity: Math.round(humidity * 10) / 10,
//       pressure: Math.round(pressure * 10) / 10,
//       windSpeed: Math.round(windSpeed * 10) / 10,
//       precipitation: Math.round(precipitation * 10) / 10,
//       condition,
//     });
//   }

//   return data;
// };

// // Calculate correlation matrix
// export const calculateCorrelation = (data: WeatherDataPoint[]) => {
//   const variables = ['temperature', 'humidity', 'pressure', 'windSpeed', 'precipitation'];
//   const correlations: { [key: string]: { [key: string]: number } } = {};

//   variables.forEach(var1 => {
//     correlations[var1] = {};
//     variables.forEach(var2 => {
//       const values1 = data.map(d => d[var1 as keyof WeatherDataPoint] as number);
//       const values2 = data.map(d => d[var2 as keyof WeatherDataPoint] as number);
//       correlations[var1][var2] = calculatePearsonCorrelation(values1, values2);
//     });
//   });

//   return correlations;
// };

// const calculatePearsonCorrelation = (x: number[], y: number[]): number => {
//   const n = x.length;
//   const sumX = x.reduce((a, b) => a + b, 0);
//   const sumY = y.reduce((a, b) => a + b, 0);
//   const sumXY = x.reduce((acc, xi, i) => acc + xi * y[i], 0);
//   const sumX2 = x.reduce((acc, xi) => acc + xi * xi, 0);
//   const sumY2 = y.reduce((acc, yi) => acc + yi * yi, 0);

//   const numerator = n * sumXY - sumX * sumY;
//   const denominator = Math.sqrt((n * sumX2 - sumX * sumX) * (n * sumY2 - sumY * sumY));

//   return denominator === 0 ? 0 : numerator / denominator;
// };

// // Resample data to weekly or monthly averages
// export const resampleData = (
//   data: WeatherDataPoint[],
//   period: "week" | "month"
// ) => {
//   const grouped = new Map<string, WeatherDataPoint[]>();

//   data.forEach((point) => {
//     let key: string;
//     if (period === "week") {
//       const weekNumber = Math.floor(
//         (point.date.getTime() -
//           new Date(point.date.getFullYear(), 0, 1).getTime()) /
//           (7 * 24 * 60 * 60 * 1000)
//       );
//       key = `${point.date.getFullYear()}-W${weekNumber}`;
//     } else {
//       key = `${point.date.getFullYear()}-${String(
//         point.date.getMonth() + 1
//       ).padStart(2, "0")}`;
//     }

//     if (!grouped.has(key)) {
//       grouped.set(key, []);
//     }
//     grouped.get(key)!.push(point);
//   });

//     return Array.from(grouped.entries()).map(([key, points]) => {
//       const avg = (arr: number[]) => arr.reduce((a, b) => a + b, 0) / arr.length;
//       return {
//         period: key,
//         temperature: Math.round(avg(points.map(p => p.temp_max)) * 10) / 10,
//         humidity: Math.round(avg(points.map(p => p.humidity_max)) * 10) / 10,
//         pressure: Math.round(avg(points.map(p => p.pressure)) * 10) / 10,
//         windSpeed: Math.round(avg(points.map(p => p.wind_speed_max)) * 10) / 10,
//         precipitation: Math.round(avg(points.map(p => p.rain_sum)) * 10) / 10,
//       };
//     });
//   };

// // Predict tomorrow's weather using simple linear regression on recent trend
// export const predictTomorrow = (data: WeatherDataPoint[]) => {
//   const recent = data.slice(-7); // Last week
//   const avgTemp = recent.reduce((sum, d) => sum + d.temperature, 0) / recent.length;
//   const avgHumidity = recent.reduce((sum, d) => sum + d.humidity, 0) / recent.length;

//   // Simple trend calculation
//   const tempTrend = (recent[recent.length - 1].temperature - recent[0].temperature) / recent.length;
//   const humidityTrend = (recent[recent.length - 1].humidity - recent[0].humidity) / recent.length;

//   const predictedTemp = Math.round((avgTemp + tempTrend) * 10) / 10;
//   const predictedHumidity = Math.round((avgHumidity + humidityTrend) * 10) / 10;

//   let predictedCondition: 'Sunny' | 'Cloudy' | 'Rainy' | 'Stormy';
//   if (predictedHumidity > 80) {
//     predictedCondition = 'Rainy';
//   } else if (predictedHumidity > 70) {
//     predictedCondition = 'Cloudy';
//   } else {
//     predictedCondition = 'Sunny';
//   }

//   return {
//     temperature: predictedTemp,
//     humidity: predictedHumidity,
//     condition: predictedCondition,
//     confidence: 0.75 + Math.random() * 0.2, // Mock confidence
//   };
// };
