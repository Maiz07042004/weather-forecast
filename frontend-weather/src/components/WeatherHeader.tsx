import { Cloud, Droplets, Wind, Gauge } from "lucide-react";
import { Card } from "@/components/ui/card";

interface WeatherHeaderProps {
  temp_max: number;
  humidity_max: number;
  wind_speed_max: number;
  rain_sum: number;
}

export const WeatherHeader = ({
  temp_max,
  humidity_max,
  wind_speed_max,
  rain_sum,
}: WeatherHeaderProps) => {
  return (
    <div className="mb-12">
      <div className="mb-8 text-center lg:text-left">
        <h1 className="text-5xl lg:text-6xl font-bold mb-3">
          <span className="gradient-text">Weather Analytics</span>
        </h1>
        <p className="text-lg text-muted-foreground">
          Comprehensive weather data visualization and analysis
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card className="glass-card p-6 hover-lift group relative overflow-hidden">
          <div className="absolute inset-0 bg-gradient-to-br from-primary/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />
          <div className="relative flex items-center justify-between">
            <div>
              <p className="text-sm text-muted-foreground mb-2">Temperature</p>
              <p className="text-4xl font-bold text-foreground">{temp_max}°C</p>
            </div>
            <div className="p-3 rounded-2xl bg-primary/10">
              <Cloud className="w-8 h-8 text-primary" />
            </div>
          </div>
        </Card>

        <Card className="glass-card p-6 hover-lift group relative overflow-hidden">
          <div className="absolute inset-0 bg-gradient-to-br from-accent/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />
          <div className="relative flex items-center justify-between">
            <div>
              <p className="text-sm text-muted-foreground mb-2">Humidity</p>
              <p className="text-4xl font-bold text-foreground">
                {humidity_max}%
              </p>
            </div>
            <div className="p-3 rounded-2xl bg-accent/10">
              <Droplets className="w-8 h-8 text-accent" />
            </div>
          </div>
        </Card>

        <Card className="glass-card p-6 hover-lift group relative overflow-hidden">
          <div className="absolute inset-0 bg-gradient-to-br from-chart-3/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />
          <div className="relative flex items-center justify-between">
            <div>
              <p className="text-sm text-muted-foreground mb-2">Wind Speed</p>
              <p className="text-4xl font-bold text-foreground">
                {wind_speed_max} m/s
              </p>
            </div>
            <div className="p-3 rounded-2xl bg-[hsl(var(--chart-3))]/10">
              <Wind className="w-8 h-8 text-[hsl(var(--chart-3))]" />
            </div>
          </div>
        </Card>

        <Card className="glass-card p-6 hover-lift group relative overflow-hidden">
          <div className="absolute inset-0 bg-gradient-to-br from-chart-4/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />
          <div className="relative flex items-center justify-between">
            <div>
              <p className="text-sm text-muted-foreground mb-2">Rainfall</p>
              <p className="text-4xl font-bold text-foreground">
                {rain_sum} mm
              </p>
            </div>
            <div className="p-3 rounded-2xl bg-[hsl(var(--chart-4))]/10">
              <Gauge className="w-8 h-8 text-[hsl(var(--chart-4))]" />
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
};
