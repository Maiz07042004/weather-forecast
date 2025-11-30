import { Card } from "@/components/ui/card";
import {
  TrendingUp,
  CloudRain,
  Sun,
  Cloud,
  CloudDrizzle,
  CloudSnow,
  Cloudy,
} from "lucide-react";
import { Badge } from "@/components/ui/badge";

interface Prediction {
  predicted_temp: number;
  weather_code: number;
  forecast_date: string;
}

interface PredictionCardsProps {
  prediction: Prediction;
}

export const PredictionCards = ({ prediction }: PredictionCardsProps) => {
  const getWeatherIcon = (weather_code: number) => {
    switch (weather_code) {
      case 3: //Sky and Cloud
        return <Cloudy className="w-12 h-12 text-chart-4" />;
      case 51: //Drizzle
        return <CloudDrizzle className="w-12 h-12 text-muted-foreground" />;
      case 61: //Rainy
        return <CloudRain className="w-12 h-12 text-chart-2" />;
      case 75: // Snowy
        return <CloudSnow className="w-12 h-12 text-primary" />;
      default:
        return <Cloud className="w-12 h-12" />;
    }
  };

  const getLoadDemand = (temp: number) => {
    if (temp > 30 || temp < 10) return "High";
    if (temp > 25 || temp < 15) return "Medium";
    return "Low";
  };

  const loadDemand = getLoadDemand(prediction.predicted_temp);

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <Card className="glass-card p-8 hover-lift relative overflow-hidden group">
        <div className="absolute top-0 right-0 w-64 h-64 bg-gradient-to-br from-primary/10 to-transparent rounded-full blur-3xl -translate-y-32 translate-x-32 group-hover:scale-150 transition-transform duration-700" />

        <div className="relative">
          <div className="flex items-center gap-3 mb-6">
            <div className="p-2 rounded-xl bg-primary/10">
              <TrendingUp className="w-6 h-6 text-primary" />
            </div>
            <h2 className="text-2xl font-bold text-foreground">
              Tomorrow's Prediction
            </h2>
          </div>

          <div className="space-y-6">
            <div className="flex items-center justify-between p-4 rounded-xl bg-gradient-to-br from-primary/5 to-transparent">
              <div>
                <p className="text-sm text-muted-foreground mb-2">
                  Temperature
                </p>
                <p className="text-5xl font-bold text-foreground">
                  {prediction.predicted_temp}°C
                </p>
              </div>
              {getWeatherIcon(prediction.weather_code)}
            </div>

            <div className="p-4 rounded-xl bg-gradient-to-br from-accent/5 to-transparent">
              <p className="text-sm text-muted-foreground mb-2">
                Thời tiết đẹp
              </p>
              <p className="text-3xl font-bold text-foreground">Hehe</p>
            </div>
          </div>
        </div>
      </Card>

      <Card className="glass-card p-8 hover-lift relative overflow-hidden group">
        <div className="absolute top-0 left-0 w-64 h-64 bg-gradient-to-br from-accent/10 to-transparent rounded-full blur-3xl -translate-y-32 -translate-x-32 group-hover:scale-150 transition-transform duration-700" />

        <div className="relative">
          <div className="flex items-center gap-3 mb-6">
            <div className="p-2 rounded-xl bg-accent/10">
              {getWeatherIcon(prediction.weather_code)}
            </div>
            <h2 className="text-2xl font-bold text-foreground">
              Weather Classification
            </h2>
          </div>

          <div className="space-y-6">
            {/* <div className="p-4 rounded-xl bg-gradient-to-br from-accent/5 to-transparent">
              <p className="text-sm text-muted-foreground mb-3">Condition</p>
              <div className="flex items-center gap-4">
                {getWeatherIcon(prediction.condition)}
                <span className="text-4xl font-bold text-foreground">
                  {prediction.condition}
                </span>
              </div>
            </div> */}

            <div className="p-4 rounded-xl bg-gradient-to-br from-primary/5 to-transparent">
              <p className="text-sm text-muted-foreground mb-3">Forecast</p>
              <Badge
                variant={
                  loadDemand === "High"
                    ? "destructive"
                    : loadDemand === "Medium"
                    ? "default"
                    : "secondary"
                }
                className="text-xl px-6 py-2 font-semibold"
              >
                {prediction.weather_code === 3
                  ? "Sky and Cloud"
                  : prediction.weather_code === 51
                  ? "Drizzle"
                  : prediction.weather_code === 61
                  ? "Rainy"
                  : prediction.weather_code === 75
                  ? "Snowy"
                  : "default"}
              </Badge>
            </div>

            <p className="text-sm text-muted-foreground pt-4 border-t border-border/50 leading-relaxed">
              Based on predicted rain sum and wind speed levels, the weather is
              expected to be{" "}
              <span className="font-semibold text-foreground">
                {(prediction.weather_code === 3
                  ? "Sky and Cloud"
                  : prediction.weather_code === 51
                  ? "Drizzle"
                  : prediction.weather_code === 61
                  ? "Rainy"
                  : prediction.weather_code === 75
                  ? "Snowy"
                  : "default"
                ).toUpperCase()}
              </span>
              .
            </p>
          </div>
        </div>
      </Card>
    </div>
  );
};
