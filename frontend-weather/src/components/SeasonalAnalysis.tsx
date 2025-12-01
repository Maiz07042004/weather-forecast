import { Card } from "@/components/ui/card";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";
import { WeatherDataPoint, WeatherDataReSamplePoint } from "@/lib/weatherData";

interface SeasonalAnalysisProps {
  data: WeatherDataPoint[];
  weeklyDataAggre: WeatherDataReSamplePoint[];
  monthlyDataAggre: WeatherDataReSamplePoint[];
}

export const SeasonalAnalysis = ({
  data,
  weeklyDataAggre,
  monthlyDataAggre,
}: SeasonalAnalysisProps) => {
  // Group by season (Spring, Summer, Fall, Winter)
  const seasonAverages = new Map<
    string, // key = season name (e.g., "Spring 2022")
    { temp: number[]; humidity: number[]; count: number }
  >();

  monthlyDataAggre.forEach((point) => {
    const validDate = new Date(point.date);
    const month = validDate.getMonth(); // Get month (0 to 11)
    const year = validDate.getFullYear();

    // Group months into seasons (Spring, Summer, Fall, Winter)
    let season = "";
    if (month >= 1 && month <= 3) {
      season = `Spring ${year}`;
    } else if (month >= 4 && month <= 6) {
      season = `Summer ${year}`;
    } else if (month >= 7 && month <= 9) {
      season = `Fall ${year}`;
    } else {
      season = `Winter ${year}`;
    }

    if (!seasonAverages.has(season)) {
      seasonAverages.set(season, { temp: [], humidity: [], count: 0 });
    }

    const stats = seasonAverages.get(season)!;
    stats.temp.push(point.temp_avg);
    stats.humidity.push(point.humidity_avg);
    stats.count++;
  });

  // Prepare the data for the chart
  const seasonNames = ["Spring", "Summer", "Fall", "Winter"];
  const seasonalData = Array.from(seasonAverages.entries())
    .sort((a, b) => {
      const [seasonA, yearA] = a[0].split(" ");
      const [seasonB, yearB] = b[0].split(" ");
      const seasonOrder =
        seasonNames.indexOf(seasonA) - seasonNames.indexOf(seasonB);
      return seasonOrder === 0 ? Number(yearA) - Number(yearB) : seasonOrder;
    })
    .map(([seasonYear, stats]) => ({
      season: seasonYear,
      temperature:
        Math.round(
          (stats.temp.reduce((a, b) => a + b, 0) / stats.temp.length) * 10
        ) / 10,
      humidity:
        Math.round(
          (stats.humidity.reduce((a, b) => a + b, 0) / stats.humidity.length) *
            10
        ) / 10,
    }));

  return (
    <Card className="p-6 shadow-[var(--shadow-card)] border-border/50">
      <h2 className="text-2xl font-bold text-foreground mb-4">
        Seasonal Patterns
      </h2>

      <ResponsiveContainer width="100%" height={400}>
        <LineChart data={seasonalData}>
          <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
          <XAxis dataKey="season" stroke="hsl(var(--muted-foreground))" />
          <YAxis stroke="hsl(var(--muted-foreground))" />
          <Tooltip
            contentStyle={{
              backgroundColor: "hsl(var(--card))",
              border: "1px solid hsl(var(--border))",
            }}
          />
          <Legend />
          <Line
            type="monotone"
            dataKey="temperature"
            stroke="hsl(var(--chart-1))"
            name="Avg Temperature (°C)"
            strokeWidth={3}
            dot={{ fill: "hsl(var(--chart-1))", r: 5 }}
          />
          <Line
            type="monotone"
            dataKey="humidity"
            stroke="hsl(var(--chart-2))"
            name="Avg Humidity (%)"
            strokeWidth={3}
            dot={{ fill: "hsl(var(--chart-2))", r: 5 }}
          />
        </LineChart>
      </ResponsiveContainer>

      <p className="mt-4 text-sm text-muted-foreground">
        Seasonal patterns show average values for each season across the
        available data period.
      </p>
    </Card>
  );
};
