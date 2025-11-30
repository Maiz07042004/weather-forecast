import { Card } from "@/components/ui/card";

interface CorrelationMatrixProps {
  correlations: { [key: string]: { [key: string]: number } };
}

export const CorrelationMatrix = ({ correlations }: CorrelationMatrixProps) => {
  const variables = Object.keys(correlations);
  const labels: { [key: string]: string } = {
    temp_max: "Temp",
    humidity_max: "Humidity",
    rain_sum: "Rain",
    wind_speed_max: "Wind",
    radiation_sum: "Radiation",
  };

  // Hàm để xác định màu sắc của ô trong bảng dựa trên giá trị tương quan
  const getColorForValue = (value: number) => {
    const intensity = Math.abs(value);
    if (value > 0) {
      return `hsl(217 ${Math.round(91 * intensity)}% ${
        60 - Math.round(20 * intensity)
      }%)`; // Tông màu xanh cho tương quan dương
    } else {
      return `hsl(0 ${Math.round(84 * intensity)}% ${
        60 - Math.round(20 * intensity)
      }%)`; // Tông màu đỏ cho tương quan âm
    }
  };

  return (
    <Card className="p-6 shadow-[var(--shadow-card)] border-border/50">
      <h2 className="text-2xl font-bold text-foreground mb-4">
        Correlation Matrix
      </h2>

      <div className="overflow-x-auto">
        <table className="w-full border-collapse">
          <thead>
            <tr>
              <th className="p-2 text-sm font-semibold text-foreground"></th>
              {variables.map((v) => (
                <th
                  key={v}
                  className="p-2 text-sm font-semibold text-foreground"
                >
                  {labels[v]}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {variables.map((var1) => (
              <tr key={var1}>
                <td className="p-2 text-sm font-semibold text-foreground">
                  {labels[var1]}
                </td>
                {variables.map((var2) => {
                  const value = correlations[var1][var2]; // Lấy giá trị tương quan giữa var1 và var2
                  return (
                    <td
                      key={var2}
                      className="p-2 text-center text-sm font-medium border border-border"
                      style={{
                        backgroundColor: getColorForValue(value), // Áp dụng màu sắc cho ô
                        color:
                          Math.abs(value) > 0.5
                            ? "white"
                            : "hsl(var(--foreground))", // Đổi màu chữ khi giá trị lớn
                      }}
                    >
                      {value.toFixed(2)}{" "}
                      {/* Hiển thị giá trị tương quan với 2 chữ số thập phân */}
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="mt-4 flex items-center justify-center gap-8 text-sm">
        <div className="flex items-center gap-2">
          <div
            className="w-8 h-4"
            style={{ backgroundColor: "hsl(217 91% 40%)" }}
          ></div>
          <span className="text-muted-foreground">Strong Positive</span>
        </div>
        <div className="flex items-center gap-2">
          <div
            className="w-8 h-4"
            style={{ backgroundColor: "hsl(0 84% 40%)" }}
          ></div>
          <span className="text-muted-foreground">Strong Negative</span>
        </div>
      </div>
    </Card>
  );
};
