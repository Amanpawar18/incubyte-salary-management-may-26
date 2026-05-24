import { Skeleton } from '@/components/ui/skeleton'
import type { SalaryMetrics } from '@/lib/api'

interface Props {
  metrics: SalaryMetrics
  loading?: boolean
}

function fmt(value: number | null): string {
  if (value === null) return '—'
  return `$${value.toLocaleString('en-US')}`
}

export function MetricsPanel({ metrics, loading }: Props) {
  if (loading) {
    return (
      <div className="space-y-4">
        <div className="grid grid-cols-2 gap-3">
          {Array.from({ length: 4 }).map((_, i) => (
            <div key={i} className="rounded-xl border bg-background px-4 py-3 shadow-sm space-y-2">
              <Skeleton className="h-3 w-24" />
              <Skeleton className="h-7 w-20" />
            </div>
          ))}
        </div>
        <div className="rounded-xl border bg-background shadow-sm">
          <Skeleton className="h-8 m-3 w-32" />
          {Array.from({ length: 5 }).map((_, i) => (
            <Skeleton key={i} className="h-8 mx-3 mb-2" />
          ))}
        </div>
        <div className="rounded-xl border bg-background shadow-sm">
          <Skeleton className="h-8 m-3 w-24" />
          {Array.from({ length: 5 }).map((_, i) => (
            <Skeleton key={i} className="h-8 mx-3 mb-2" />
          ))}
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-4">
      <div className="grid grid-cols-2 gap-3">
        <StatCard label="Total Employees" value={String(metrics.total)} />
        <StatCard label="Average Salary" value={fmt(metrics.average_salary)} />
        <StatCard label="Min Salary" value={fmt(metrics.min_salary)} />
        <StatCard label="Max Salary" value={fmt(metrics.max_salary)} />
      </div>

      {metrics.by_department.length > 0 && (
        <BreakdownTable
          title="By Department"
          rows={metrics.by_department.map(d => ({ label: d.department, count: d.count, average_salary: d.average_salary }))}
        />
      )}
      {metrics.by_country.length > 0 && (
        <BreakdownTable
          title="By Country"
          rows={metrics.by_country.map(c => ({ label: c.country, count: c.count, average_salary: c.average_salary }))}
        />
      )}
    </div>
  )
}

function StatCard({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-xl border bg-background px-4 py-3 shadow-sm">
      <p className="text-xs text-muted-foreground">{label}</p>
      <p className="mt-1 text-xl font-semibold">{value}</p>
    </div>
  )
}

function BreakdownTable({ title, rows }: { title: string; rows: { label: string; count: number; average_salary: number }[] }) {
  return (
    <div className="rounded-xl border bg-background shadow-sm">
      <p className="border-b px-4 py-2 text-sm font-medium">{title}</p>
      <table className="w-full text-sm">
        <thead>
          <tr className="border-b text-left text-xs text-muted-foreground">
            <th className="px-4 py-2 font-medium">Name</th>
            <th className="px-4 py-2 font-medium">Count</th>
            <th className="px-4 py-2 font-medium">Avg Salary</th>
          </tr>
        </thead>
        <tbody>
          {rows.map(row => (
            <tr key={row.label} className="border-b last:border-0">
              <td className="px-4 py-2">{row.label}</td>
              <td className="px-4 py-2">{row.count}</td>
              <td className="px-4 py-2">{fmt(row.average_salary)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
