import {
  Table, TableBody, TableCell, TableHead, TableHeader, TableRow,
} from '@/components/ui/table'
import { Button } from '@/components/ui/button'
import type { Employee } from '@/lib/api'

interface Props {
  items: Employee[]
  total: number
  page: number
  pageSize: number
  onPageChange: (page: number) => void
  onView?: (id: number) => void
}

export function EmployeeTable({ items, total, page, pageSize, onPageChange, onView }: Props) {
  const totalPages = Math.ceil(total / pageSize)
  const start = (page - 1) * pageSize + 1
  const end = Math.min(page * pageSize, total)

  if (items.length === 0) {
    return (
      <p className="py-12 text-center text-muted-foreground">No employees found.</p>
    )
  }

  return (
    <div className="space-y-3">
      <Table className="table-fixed">
        <TableHeader>
          <TableRow>
            <TableHead className="w-[14%]">Name</TableHead>
            <TableHead className="w-[18%]">Job Title</TableHead>
            <TableHead className="w-[14%]">Department</TableHead>
            <TableHead className="w-[12%]">Country</TableHead>
            <TableHead className="w-[10%]">Salary</TableHead>
            <TableHead className="w-[24%]">Email</TableHead>
            <TableHead className="w-[8%]" />
          </TableRow>
        </TableHeader>
        <TableBody>
          {items.map((emp) => (
            <TableRow key={emp.id}>
              <TableCell className="font-medium truncate max-w-0">{emp.full_name}</TableCell>
              <TableCell className="truncate max-w-0">{emp.job_title}</TableCell>
              <TableCell className="truncate max-w-0">{emp.department}</TableCell>
              <TableCell className="truncate max-w-0">{emp.country}</TableCell>
              <TableCell>${emp.salary.toLocaleString()}</TableCell>
              <TableCell className="truncate max-w-0">{emp.email}</TableCell>
              <TableCell>
                {onView && (
                  <Button variant="outline" size="sm" onClick={() => onView(emp.id)}>
                    View
                  </Button>
                )}
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>

      <div className="flex items-center justify-between px-4 pb-4 text-sm text-muted-foreground">
        <span>{start}–{end} of {total}</span>
        <div className="flex gap-2">
          <Button
            variant="outline"
            size="sm"
            disabled={page <= 1}
            onClick={() => onPageChange(page - 1)}
          >
            Prev
          </Button>
          <Button
            variant="outline"
            size="sm"
            disabled={page >= totalPages}
            onClick={() => onPageChange(page + 1)}
          >
            Next
          </Button>
        </div>
      </div>
    </div>
  )
}
