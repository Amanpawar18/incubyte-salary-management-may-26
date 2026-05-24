import { useState, useEffect, useCallback } from 'react'
import { EmployeeForm } from '@/components/employees/EmployeeForm'
import { EmployeeTable } from '@/components/employees/EmployeeTable'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { api, type EmployeePage } from '@/lib/api'

export default function App() {
  const [formOpen, setFormOpen] = useState(false)
  const [page, setPage] = useState(1)
  const [nameInput, setNameInput] = useState('')
  const [countryInput, setCountryInput] = useState('')
  const [name, setName] = useState('')
  const [country, setCountry] = useState('')
  const [data, setData] = useState<EmployeePage>({ items: [], total: 0, page: 1, page_size: 20 })

  const fetchEmployees = useCallback(async () => {
    const res = await api.employees.list({ page, page_size: 20, name, country })
    setData(res.data)
  }, [page, name, country])

  useEffect(() => { fetchEmployees() }, [fetchEmployees])

  function handleSearch() {
    setName(nameInput)
    setCountry(countryInput)
    setPage(1)
  }

  async function handleCreate(payload: Parameters<typeof api.employees.create>[0]) {
    await api.employees.create(payload)
    setFormOpen(false)
    fetchEmployees()
  }

  return (
    <div className="min-h-screen bg-muted/40">
      <header className="border-b bg-background px-6 py-4">
        <h1 className="text-xl font-semibold tracking-tight">Salary Management</h1>
      </header>

      <main className="mx-auto max-w-6xl p-6 space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-medium">Employees</h2>
          <Button onClick={() => setFormOpen(true)}>+ Add Employee</Button>
        </div>

        <div className="flex gap-3">
          <Input
            placeholder="Search by name..."
            className="max-w-xs"
            value={nameInput}
            onChange={e => setNameInput(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && handleSearch()}
          />
          <Input
            placeholder="Filter by country..."
            className="max-w-xs"
            value={countryInput}
            onChange={e => setCountryInput(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && handleSearch()}
          />
          <Button variant="outline" onClick={handleSearch}>Search</Button>
        </div>

        <div className="rounded-xl border bg-background shadow-sm">
          <EmployeeTable
            items={data.items}
            total={data.total}
            page={page}
            pageSize={data.page_size}
            onPageChange={setPage}
          />
        </div>
      </main>

      <EmployeeForm
        open={formOpen}
        onClose={() => setFormOpen(false)}
        onSubmit={handleCreate}
      />
    </div>
  )
}
