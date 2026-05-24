import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import {
  Sheet, SheetContent, SheetHeader, SheetTitle, SheetFooter,
} from '@/components/ui/sheet'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import type { Employee } from '@/lib/api'

const schema = z.object({
  full_name: z.string().min(1, 'Full name is required'),
  email: z.string().min(1, 'Email is required').email('Must be a valid email'),
  job_title: z.string().min(1, 'Job title is required'),
  department: z.string().min(1, 'Department is required'),
  country: z.string().min(1, 'Country is required'),
  salary: z.coerce.number().positive('Salary must be greater than 0'),
})

type EmployeeFormInput = z.input<typeof schema>   // salary: unknown (raw field value)
type EmployeeFormData = z.output<typeof schema>   // salary: number (after coercion)

interface Props {
  open: boolean
  onClose: () => void
  onSubmit: (data: EmployeeFormData) => void
  employee?: Employee
}

const FIELDS: { name: keyof EmployeeFormInput; label: string; type: string }[] = [
  { name: 'full_name', label: 'Full Name', type: 'text' },
  { name: 'email', label: 'Email', type: 'email' },
  { name: 'job_title', label: 'Job Title', type: 'text' },
  { name: 'department', label: 'Department', type: 'text' },
  { name: 'country', label: 'Country', type: 'text' },
  { name: 'salary', label: 'Salary', type: 'number' },
]

export function EmployeeForm({ open, onClose, onSubmit, employee }: Props) {
  const { register, handleSubmit, reset, formState: { errors } } = useForm<EmployeeFormInput, unknown, EmployeeFormData>({
    resolver: zodResolver(schema),
    values: employee
      ? { full_name: employee.full_name, email: employee.email, job_title: employee.job_title, department: employee.department, country: employee.country, salary: employee.salary }
      : undefined,
  })

  function handleClose() {
    reset()
    onClose()
  }

  return (
    <Sheet open={open} onOpenChange={(o) => !o && handleClose()}>
      <SheetContent className="sm:max-w-md" showCloseButton={false}>
        <SheetHeader>
          <SheetTitle>{employee ? 'Edit Employee' : 'Add Employee'}</SheetTitle>
        </SheetHeader>

        <form
          onSubmit={handleSubmit((data) => onSubmit(data))}
          className="flex flex-col gap-4 px-4 py-6"
          noValidate
        >
          {FIELDS.map(({ name, label, type }) => (
            <div key={name} className="flex flex-col gap-1.5">
              <Label htmlFor={name}>{label}</Label>
              <Input id={name} type={type} {...register(name)} />
              {errors[name] && (
                <p className="text-xs text-destructive">{errors[name]?.message}</p>
              )}
            </div>
          ))}

          <SheetFooter className="mt-2 flex-row justify-end gap-2 px-0">
            <Button type="button" variant="outline" onClick={handleClose}>Cancel</Button>
            <Button type="submit">Save</Button>
          </SheetFooter>
        </form>
      </SheetContent>
    </Sheet>
  )
}
