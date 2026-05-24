import { useState } from 'react'
import { EmployeeForm } from '@/components/employees/EmployeeForm'
import { Button } from '@/components/ui/button'
import { api } from '@/lib/api'

export default function App() {
  const [formOpen, setFormOpen] = useState(false)

  async function handleCreate(data: Parameters<typeof api.employees.create>[0]) {
    await api.employees.create(data)
    setFormOpen(false)
  }

  return (
    <div className="p-6">
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold">Salary Management</h1>
        <Button onClick={() => setFormOpen(true)}>+ Add Employee</Button>
      </div>

      <EmployeeForm
        open={formOpen}
        onClose={() => setFormOpen(false)}
        onSubmit={handleCreate}
      />
    </div>
  )
}
