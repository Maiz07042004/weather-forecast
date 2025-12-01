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

interface TrendAnalysisProps {
  weatherData: WeatherDataPoint[];
  weeklyData: WeatherDataReSamplePoint[];
  monthlyData: WeatherDataReSamplePoint[];
}

export const TrendAnalysis = ({
  weatherData,
  weeklyData,
  monthlyData,
}: TrendAnalysisProps) => {
  // const weeklyData = resampleData(data, "week");
  // const monthlyData = resampleData(data, "month");

  // Use monthly if we have enough data, otherwise weekly
  const trendData = monthlyData.length >= 3 ? monthlyData : weeklyData;
  const periodType = monthlyData.length >= 3 ? "Monthly" : "Weekly";

  return (
    <Card className="p-6 shadow-[var(--shadow-card)] border-border/50">
      <h2 className="text-2xl font-bold text-foreground mb-4">
        Trend Analysis ({periodType} Resampling)
      </h2>

      <ResponsiveContainer width="100%" height={400}>
        <LineChart data={monthlyData}>
          <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
          <XAxis dataKey="date" stroke="hsl(var(--muted-foreground))" />
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
            dataKey="temp_avg"
            stroke="hsl(var(--chart-1))"
            name="Temperature (°C)"
            strokeWidth={3}
            dot={{ fill: "hsl(var(--chart-1))", r: 4 }}
          />
          <Line
            type="monotone"
            dataKey="humidity_avg"
            stroke="hsl(var(--chart-2))"
            name="Humidity (%)"
            strokeWidth={3}
            dot={{ fill: "hsl(var(--chart-2))", r: 4 }}
          />
          <Line
            type="monotone"
            dataKey="rain_total"
            stroke="hsl(var(--chart-4))"
            name="Rain Total (mm)"
            strokeWidth={3}
            dot={{ fill: "hsl(var(--chart-4))", r: 4 }}
          />
        </LineChart>
      </ResponsiveContainer>

      <p className="mt-4 text-sm text-muted-foreground">
        Trend shows {periodType.toLowerCase()} averages of key weather metrics
        over the analysis period.
      </p>
    </Card>
  );
};
