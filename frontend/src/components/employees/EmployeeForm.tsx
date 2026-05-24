import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'

const schema = z.object({
  full_name: z.string().min(1, 'Full name is required'),
  email: z.string().min(1, 'Email is required').email('Must be a valid email'),
  job_title: z.string().min(1, 'Job title is required'),
  department: z.string().min(1, 'Department is required'),
  country: z.string().min(1, 'Country is required'),
  salary: z.coerce.number().positive('Salary must be greater than 0'),
})

type EmployeeFormData = z.infer<typeof schema>

interface Props {
  open: boolean
  onClose: () => void
  onSubmit: (data: EmployeeFormData) => void
}

const FIELDS: { name: keyof EmployeeFormData; label: string; type: string }[] = [
  { name: 'full_name', label: 'Full Name', type: 'text' },
  { name: 'email', label: 'Email', type: 'email' },
  { name: 'job_title', label: 'Job Title', type: 'text' },
  { name: 'department', label: 'Department', type: 'text' },
  { name: 'country', label: 'Country', type: 'text' },
  { name: 'salary', label: 'Salary', type: 'number' },
]

export function EmployeeForm({ open, onClose, onSubmit }: Props) {
  const { register, handleSubmit, reset, formState: { errors } } = useForm<EmployeeFormData>({
    resolver: zodResolver(schema),
  })

  if (!open) return null

  function handleClose() {
    reset()
    onClose()
  }

  return (
    <div className="flex flex-col gap-4 p-6">
      <h2 className="text-lg font-semibold">Add Employee</h2>
      <form onSubmit={handleSubmit((data) => onSubmit(data))} className="grid grid-cols-2 gap-4" noValidate>
        {FIELDS.map(({ name, label, type }) => (
          <div key={name} className="flex flex-col gap-1">
            <Label htmlFor={name}>{label}</Label>
            <Input id={name} type={type} {...register(name)} />
            {errors[name] && (
              <p className="text-xs text-red-500">{errors[name]?.message}</p>
            )}
          </div>
        ))}
        <div className="col-span-2 flex justify-end gap-2">
          <Button type="button" variant="outline" onClick={handleClose}>Cancel</Button>
          <Button type="submit">Save</Button>
        </div>
      </form>
    </div>
  )
}
