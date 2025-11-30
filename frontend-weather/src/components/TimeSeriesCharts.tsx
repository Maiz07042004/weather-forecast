import { useState } from "react";
import { Card } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Button } from "@/components/ui/button";
import { ZoomIn, ZoomOut } from "lucide-react";
import {
  LineChart,
  Line,
  ScatterChart,
  Scatter,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  Brush,
  ReferenceArea,
} from "recharts";
import { WeatherDataPoint, WeatherDataReSamplePoint } from "@/lib/weatherData";

interface TimeSeriesChartsProps {
  data: WeatherDataPoint[];
  weeklyDataAggre: WeatherDataReSamplePoint[];
  monthlyDataAggre: WeatherDataReSamplePoint[];
}

export const TimeSeriesCharts = ({
  data,
  weeklyDataAggre,
  monthlyDataAggre,
}: TimeSeriesChartsProps) => {
  const [zoomState, setZoomState] = useState<{
    refAreaLeft: string | null;
    refAreaRight: string | null;
    left: number;
    right: number;
  }>({
    refAreaLeft: null,
    refAreaRight: null,
    left: 0,
    right: data.length - 1,
  });
  // Hàm chuyển đổi đối tượng Date thành chuỗi "MM-DD"
  const formatDate = (date: any) => {
    const validDate = new Date(date); // Chuyển đổi thành đối tượng Date nếu không phải là đối tượng Date
    const month = String(validDate.getMonth() + 1).padStart(2, "0"); // Tháng (1-12)
    const day = String(validDate.getDate()).padStart(2, "0"); // Ngày (1-31)
    return `${month}-${day}`;
  };

  // Lấy dữ liệu trong 7 ngày, 30 ngày và toàn bộ dữ liệu
  const dailyData = data
    .slice(-7)
    .map((d) => ({ ...d, date: formatDate(d.date) }));
  const weeklyData = data
    .slice(-30)
    .map((d) => ({ ...d, date: formatDate(d.date) }));
  const monthlyData = data
    .slice(-90)
    .map((d) => ({ ...d, date: formatDate(d.date) }));

  // Chuẩn bị dữ liệu cho biểu đồ histogram của nhiệt độ
  const tempHistogram = Array.from({ length: 10 }, (_, i) => {
    const min = i * 5;
    const max = (i + 1) * 5;
    const count = monthlyDataAggre.filter(
      (d) => d.temp_avg >= min && d.temp_avg < max
    ).length;
    return { range: `${min}-${max}°C`, count };
  });

  const resetZoom = () => {
    setZoomState({
      refAreaLeft: null,
      refAreaRight: null,
      left: 0,
      right: monthlyDataAggre.length - 1,
    });
  };

  const zoom = () => {
    if (
      zoomState.refAreaLeft === zoomState.refAreaRight ||
      !zoomState.refAreaRight
    ) {
      setZoomState({ ...zoomState, refAreaLeft: null, refAreaRight: null });
      return;
    }

    // Tính phạm vi zoom (tìm chỉ mục của các ngày tương ứng)
    const left = Math.min(
      monthlyData.findIndex((d) => d.date === zoomState.refAreaLeft),
      monthlyData.findIndex((d) => d.date === zoomState.refAreaRight)
    );
    const right = Math.max(
      monthlyData.findIndex((d) => d.date === zoomState.refAreaLeft),
      monthlyData.findIndex((d) => d.date === zoomState.refAreaRight)
    );

    if (left >= 0 && right >= 0) {
      setZoomState({
        refAreaLeft: null,
        refAreaRight: null,
        left,
        right,
      });
    }
  };

  const getZoomedData = (originalData: any[]) => {
    return originalData.slice(zoomState.left, zoomState.right + 1);
  };

  return (
    <Card className="p-6 shadow-[var(--shadow-card)] border-border/50">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-2xl font-bold text-foreground">
          Time Series Analysis
        </h2>
        <Button
          variant="outline"
          size="sm"
          onClick={resetZoom}
          className="gap-2"
        >
          <ZoomOut className="w-4 h-4" />
          Reset Zoom
        </Button>
      </div>

      <Tabs defaultValue="line" className="w-full">
        <TabsList className="grid w-full grid-cols-3 mb-6">
          <TabsTrigger value="line">Line Chart</TabsTrigger>
          <TabsTrigger value="scatter">Scatter Plot</TabsTrigger>
          <TabsTrigger value="histogram">Histogram</TabsTrigger>
        </TabsList>

        <TabsContent value="line" className="space-y-6">
          <div>
            <h3 className="text-lg font-semibold text-foreground mb-3">
              Daily (Last 7 Days)
            </h3>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={dailyData}>
                <CartesianGrid
                  strokeDasharray="3 3"
                  stroke="hsl(var(--border))"
                />
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
                  dataKey="temp_max"
                  stroke="hsl(var(--chart-1))"
                  name="Temperature (°C)"
                  strokeWidth={2}
                />
                <Line
                  type="monotone"
                  dataKey="humidity_max"
                  stroke="hsl(var(--chart-2))"
                  name="Humidity (%)"
                  strokeWidth={2}
                />
                <Brush
                  dataKey="date"
                  height={30}
                  stroke="hsl(var(--primary))"
                  fill="hsl(var(--muted))"
                />
              </LineChart>
            </ResponsiveContainer>
          </div>

          <div>
            <h3 className="text-lg font-semibold text-foreground mb-3">
              Weekly (Last 30 Days)
            </h3>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={weeklyData}>
                <CartesianGrid
                  strokeDasharray="3 3"
                  stroke="hsl(var(--border))"
                />
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
                  dataKey="temp_max"
                  stroke="hsl(var(--chart-1))"
                  name="Temperature (°C)"
                  strokeWidth={2}
                />
                <Line
                  type="monotone"
                  dataKey="wind_speed_max"
                  stroke="hsl(var(--chart-3))"
                  name="Wind Speed (m/s)"
                  strokeWidth={2}
                />
                <Brush
                  dataKey="date"
                  height={30}
                  stroke="hsl(var(--primary))"
                  fill="hsl(var(--muted))"
                />
              </LineChart>
            </ResponsiveContainer>
          </div>

          <div>
            <h3 className="text-lg font-semibold text-foreground mb-3">
              Monthly (Last 90 Days) - Drag to zoom
            </h3>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={getZoomedData(monthlyData)}>
                <CartesianGrid
                  strokeDasharray="3 3"
                  stroke="hsl(var(--border))"
                />
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
                  dataKey="temp_max"
                  stroke="hsl(var(--chart-1))"
                  name="Temperature (°C)"
                  strokeWidth={2}
                />
                <Line
                  type="monotone"
                  dataKey="wind_speed_max"
                  stroke="hsl(var(--chart-4))"
                  name="Wind Speed (m/s)"
                  strokeWidth={2}
                />
                {zoomState.refAreaLeft && zoomState.refAreaRight && (
                  <ReferenceArea
                    x1={zoomState.refAreaLeft}
                    x2={zoomState.refAreaRight}
                    strokeOpacity={0.3}
                    fill="hsl(var(--primary))"
                    fillOpacity={0.3}
                  />
                )}
                <Brush
                  dataKey="date"
                  height={30}
                  stroke="hsl(var(--primary))"
                  fill="hsl(var(--muted))"
                />
              </LineChart>
            </ResponsiveContainer>
            <p className="text-sm text-muted-foreground mt-2">
              💡 Drag on the chart to select a zoom area, or use the brush below
              to navigate
            </p>
          </div>
        </TabsContent>

        <TabsContent value="scatter">
          <div className="space-y-6">
            <div>
              <h3 className="text-lg font-semibold text-foreground mb-3">
                Temperature vs Humidity
              </h3>
              <ResponsiveContainer width="100%" height={400}>
                <ScatterChart>
                  <CartesianGrid
                    strokeDasharray="3 3"
                    stroke="hsl(var(--border))"
                  />
                  <XAxis
                    dataKey="temp_avg"
                    name="Temperature"
                    unit="°C"
                    stroke="hsl(var(--muted-foreground))"
                  />
                  <YAxis
                    dataKey="humidity_avg"
                    name="Humidity"
                    unit="%"
                    stroke="hsl(var(--muted-foreground))"
                  />
                  <Tooltip
                    cursor={{ strokeDasharray: "3 3" }}
                    contentStyle={{
                      backgroundColor: "hsl(var(--card))",
                      border: "1px solid hsl(var(--border))",
                    }}
                  />
                  <Legend />
                  <Scatter
                    name="Weather Data"
                    data={weeklyDataAggre}
                    fill="hsl(var(--chart-1))"
                  />
                </ScatterChart>
              </ResponsiveContainer>
            </div>

            <div>
              <h3 className="text-lg font-semibold text-foreground mb-3">
                Temperature vs Rain_sum
              </h3>
              <ResponsiveContainer width="100%" height={400}>
                <ScatterChart>
                  <CartesianGrid
                    strokeDasharray="3 3"
                    stroke="hsl(var(--border))"
                  />
                  <XAxis
                    dataKey="temp_avg"
                    name="Temperature"
                    unit="°C"
                    stroke="hsl(var(--muted-foreground))"
                  />
                  <YAxis
                    dataKey="rain_total"
                    name="Rain Total"
                    unit="mm"
                    stroke="hsl(var(--muted-foreground))"
                  />
                  <Tooltip
                    cursor={{ strokeDasharray: "3 3" }}
                    contentStyle={{
                      backgroundColor: "hsl(var(--card))",
                      border: "1px solid hsl(var(--border))",
                    }}
                  />
                  <Legend />
                  <Scatter
                    name="Weather Data"
                    data={weeklyDataAggre}
                    fill="hsl(var(--chart-2))"
                  />
                </ScatterChart>
              </ResponsiveContainer>
            </div>
          </div>
        </TabsContent>

        <TabsContent value="histogram">
          <div>
            <h3 className="text-lg font-semibold text-foreground mb-3">
              Temperature Distribution
            </h3>
            <ResponsiveContainer width="100%" height={400}>
              <BarChart data={tempHistogram}>
                <CartesianGrid
                  strokeDasharray="3 3"
                  stroke="hsl(var(--border))"
                />
                <XAxis dataKey="range" stroke="hsl(var(--muted-foreground))" />
                <YAxis stroke="hsl(var(--muted-foreground))" />
                <Tooltip
                  contentStyle={{
                    backgroundColor: "hsl(var(--card))",
                    border: "1px solid hsl(var(--border))",
                  }}
                />
                <Legend />
                <Bar
                  dataKey="count"
                  fill="hsl(var(--chart-1))"
                  name="Frequency"
                />
                <Brush
                  dataKey="range"
                  height={30}
                  stroke="hsl(var(--primary))"
                  fill="hsl(var(--muted))"
                />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </TabsContent>
      </Tabs>
    </Card>
  );
};
