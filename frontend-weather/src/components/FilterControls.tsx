import { Card } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Slider } from "@/components/ui/slider";
import { Button } from "@/components/ui/button";
import { Filter, RotateCcw } from "lucide-react";

export interface FilterState {
  temperatureRange: [number, number];
  humidityRange: [number, number];
  weather_code: number | "all";
}

interface FilterControlsProps {
  filters: FilterState;
  onFilterChange: (filters: FilterState) => void;
  onReset: () => void;
}

export const FilterControls = ({
  filters,
  onFilterChange,
  onReset,
}: FilterControlsProps) => {
  return (
    <Card className="p-6 shadow-[var(--shadow-card)] border-border/50">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <Filter className="w-5 h-5 text-primary" />
          <h3 className="text-lg font-semibold text-foreground">
            Data Filters
          </h3>
        </div>
        <Button variant="outline" size="sm" onClick={onReset} className="gap-2">
          <RotateCcw className="w-4 h-4" />
          Reset
        </Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="space-y-3">
          <Label className="text-sm font-medium text-foreground">
            Temperature Range: {filters.temperatureRange[0]}°C -{" "}
            {filters.temperatureRange[1]}°C
          </Label>
          <Slider
            min={-10}
            max={50}
            step={1}
            value={filters.temperatureRange}
            onValueChange={(value) =>
              onFilterChange({
                ...filters,
                temperatureRange: value as [number, number],
              })
            }
            className="w-full"
          />
        </div>

        <div className="space-y-3">
          <Label className="text-sm font-medium text-foreground">
            Humidity Range: {filters.humidityRange[0]}% -{" "}
            {filters.humidityRange[1]}%
          </Label>
          <Slider
            min={0}
            max={100}
            step={5}
            value={filters.humidityRange}
            onValueChange={(value) =>
              onFilterChange({
                ...filters,
                humidityRange: value as [number, number],
              })
            }
            className="w-full"
          />
        </div>

        <div className="space-y-3">
          <Label className="text-sm font-medium text-foreground">
            Weather Condition
          </Label>
          <Select
            value={filters.weather_code.toString()}
            onValueChange={(value) =>
              onFilterChange({
                ...filters,
                weather_code: value === "0" ? 0 : parseInt(value),
              })
            }
          >
            <SelectTrigger>
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="0">All Conditions</SelectItem>
              <SelectItem value="3">Sky and Cloud</SelectItem>
              <SelectItem value="51">Drizzle</SelectItem>
              <SelectItem value="61">Rainy</SelectItem>
              <SelectItem value="75">Snow</SelectItem>
            </SelectContent>
          </Select>
        </div>
      </div>
    </Card>
  );
};
