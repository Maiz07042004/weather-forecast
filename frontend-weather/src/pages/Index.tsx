import { useEffect, useMemo, useState } from "react";
import { WeatherHeader } from "@/components/WeatherHeader";
import { TimeSeriesCharts } from "@/components/TimeSeriesCharts";
import { TrendAnalysis } from "@/components/TrendAnalysis";
import { SeasonalAnalysis } from "@/components/SeasonalAnalysis";
import { CorrelationMatrix } from "@/components/CorrelationMatrix";
import { PredictionCards } from "@/components/PredictionCards";
import { FilterControls, FilterState } from "@/components/FilterControls";
import { getChartDays, getCorrelations, getForecast } from "@/api";

const Index = () => {
  // Initialize state
  const [rawWeatherData, setWeatherData] = useState([]);
  const [rawWeatherWeeklyData, setWeatherWeeklyData] = useState([]);
  const [rawWeatherMonthlyData, setWeatherMonthlyData] = useState([]);
  const [correlations, setCorrelations] = useState({});
  const [prediction, setPrediction] = useState(null);

  // Fetch data on mount
  useEffect(() => {
    const loadData = async () => {
      const weather = await getChartDays();
      const correlation = await getCorrelations();
      const forecast = await getForecast();

      setWeatherData(weather.daily_series);
      setWeatherWeeklyData(weather.weekly_series);
      setWeatherMonthlyData(weather.monthly_series);
      setCorrelations(correlation);
      setPrediction(forecast);
    };

    loadData();
  }, []);
  console.log("Raw Weather Data:", rawWeatherWeeklyData);
  // Apply filters to weather data
  const [filters, setFilters] = useState<FilterState>({
    temperatureRange: [-10, 50],
    humidityRange: [0, 100],
    weather_code: 0,
  });

  const weatherData = useMemo(() => {
    return rawWeatherData.filter((d) => {
      const tempInRange =
        d.temp_max >= filters.temperatureRange[0] &&
        d.temp_max <= filters.temperatureRange[1];
      const humidityInRange =
        d.humidity_max >= filters.humidityRange[0] &&
        d.humidity_max <= filters.humidityRange[1];
      const conditionMatch =
        filters.weather_code === 0 || d.weather_code === filters.weather_code;

      return tempInRange && humidityInRange && conditionMatch;
    });
  }, [rawWeatherData, filters]);

  // Get the latest weather data, ensuring it's defined before using it
  const latestData =
    weatherData[weatherData.length - 1] ||
    rawWeatherData[rawWeatherData.length - 1];

  if (!latestData) {
    // Optionally handle loading state, like a spinner or placeholder
    return <div>Loading...</div>;
  }

  const handleResetFilters = () => {
    setFilters({
      temperatureRange: [-10, 50],
      humidityRange: [0, 100],
      weather_code: 0,
    });
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-background to-primary/5">
      <div className="container mx-auto px-4 py-8 max-w-7xl">
        <div className="animate-fade-in">
          <WeatherHeader
            temp_max={latestData.temp_max}
            humidity_max={latestData.humidity_max}
            wind_speed_max={latestData.wind_speed_max}
            rain_sum={latestData.rain_sum}
          />
        </div>

        <div className="space-y-8 mt-8">
          <div className="animate-slide-up">
            <FilterControls
              filters={filters}
              onFilterChange={setFilters}
              onReset={handleResetFilters}
            />
          </div>

          <div className="glass-card rounded-xl p-6 animate-scale-in shadow-glow-sm">
            <p className="text-sm text-foreground/90">
              <span className="font-semibold text-primary">Filtered Data:</span>{" "}
              {weatherData.length} of {rawWeatherData.length} total records
            </p>
          </div>

          <div className="animate-fade-in">
            <TimeSeriesCharts
              data={weatherData}
              weeklyDataAggre={rawWeatherWeeklyData} // or undefined if you want to resample
              monthlyDataAggre={rawWeatherMonthlyData}
            />
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div
              className="animate-slide-up"
              style={{ animationDelay: "0.1s" }}
            >
              <TrendAnalysis
                weatherData={weatherData}
                weeklyData={rawWeatherWeeklyData} // or undefined if you want to resample
                monthlyData={rawWeatherMonthlyData} // or undefined if you want to resample
              />
            </div>
            <div
              className="animate-slide-up"
              style={{ animationDelay: "0.2s" }}
            >
              <SeasonalAnalysis
                data={rawWeatherMonthlyData}
                weeklyDataAggre={rawWeatherWeeklyData} // or undefined if you want to resample
                monthlyDataAggre={rawWeatherMonthlyData}
              />
            </div>
          </div>

          <div className="animate-fade-in">
            <CorrelationMatrix correlations={correlations} />
          </div>

          <div className="animate-slide-up">
            <PredictionCards prediction={prediction} />
          </div>
        </div>
      </div>
    </div>
  );
};

export default Index;
