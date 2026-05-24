import {
  Sheet, SheetContent, SheetHeader, SheetTitle,
} from '@/components/ui/sheet'
import type { Employee } from '@/lib/api'

interface Props {
  employee: Employee | null
  open: boolean
  onClose: () => void
}

const FIELDS: { label: string; key: keyof Employee }[] = [
  { label: 'Full Name', key: 'full_name' },
  { label: 'Email', key: 'email' },
  { label: 'Job Title', key: 'job_title' },
  { label: 'Department', key: 'department' },
  { label: 'Country', key: 'country' },
  { label: 'Salary', key: 'salary' },
]

export function EmployeeDetail({ employee, open, onClose }: Props) {
  return (
    <Sheet open={open} onOpenChange={(o) => !o && onClose()}>
      <SheetContent className="sm:max-w-md">
        <SheetHeader>
          <SheetTitle>Employee Details</SheetTitle>
        </SheetHeader>

        {employee && (
          <div className="flex flex-col gap-4 px-4 py-6">
            {FIELDS.map(({ label, key }) => (
              <div key={key} className="flex flex-col gap-1">
                <span className="text-xs font-medium text-muted-foreground">{label}</span>
                <span className="text-sm">
                  {key === 'salary'
                    ? `$${(employee[key] as number).toLocaleString()}`
                    : String(employee[key])}
                </span>
              </div>
            ))}
          </div>
        )}
      </SheetContent>
    </Sheet>
  )
}
