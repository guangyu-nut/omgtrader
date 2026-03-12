import type { CurvePoint } from "../api/results";

export function buildEquityCurveOptions(points: CurvePoint[]) {
  return {
    series: [
      {
        data: points.map((point) => point.value),
        type: "line",
      },
    ],
    xAxis: {
      data: points.map((point) => point.label),
    },
  };
}
