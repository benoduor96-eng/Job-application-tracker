export function buildChartData(byStatus = []) {
  return byStatus.map((entry) => ({
    label: entry.status,
    value: entry.total,
  }));
}
