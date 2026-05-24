import { useState, useEffect, useCallback } from 'react'
import { toast, Toaster } from 'sonner'
import { EmployeeDetail } from '@/components/employees/EmployeeDetail'
import { EmployeeForm } from '@/components/employees/EmployeeForm'
import { EmployeeTable } from '@/components/employees/EmployeeTable'
import { MetricsPanel } from '@/components/employees/MetricsPanel'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { api, type Employee, type EmployeePage, type SalaryMetrics } from '@/lib/api'

export default function App() {
  const [formOpen, setFormOpen] = useState(false)
  const [editingEmployee, setEditingEmployee] = useState<Employee | null>(null)
  const [detailOpen, setDetailOpen] = useState(false)
  const [selectedEmployee, setSelectedEmployee] = useState<Employee | null>(null)
  const [page, setPage] = useState(1)
  const [nameInput, setNameInput] = useState('')
  const [countryInput, setCountryInput] = useState('')
  const [name, setName] = useState('')
  const [country, setCountry] = useState('')
  const [data, setData] = useState<EmployeePage>({ items: [], total: 0, page: 1, page_size: 20 })
  const [metrics, setMetrics] = useState<SalaryMetrics>({ total: 0, average_salary: 0, min_salary: null, max_salary: null, by_department: [], by_country: [] })
  const [loadingEmployees, setLoadingEmployees] = useState(true)
  const [loadingMetrics, setLoadingMetrics] = useState(true)

  const fetchEmployees = useCallback(
    () => api.employees.list({ page, page_size: 20, name, country }),
    [page, name, country]
  )

  useEffect(() => {
    fetchEmployees()
      .then(res => setData(res.data))
      .catch(() => toast.error('Failed to load employees'))
      .finally(() => setLoadingEmployees(false))

    api.employees.metrics()
      .then(res => setMetrics(res.data))
      .catch(() => toast.error('Failed to load metrics'))
      .finally(() => setLoadingMetrics(false))
  }, [fetchEmployees])

  async function handleView(id: number) {
    const res = await api.employees.get(id)
    setSelectedEmployee(res.data)
    setDetailOpen(true)
  }

  function handleSearch() {
    setName(nameInput)
    setCountry(countryInput)
    setPage(1)
  }

  function refreshAll() {
    fetchEmployees().then(res => setData(res.data))
    api.employees.metrics().then(res => setMetrics(res.data))
  }

  async function handleCreate(payload: Parameters<typeof api.employees.create>[0]) {
    try {
      await api.employees.create(payload)
      setFormOpen(false)
      refreshAll()
      toast.success('Employee created')
    } catch {
      toast.error('Failed to create employee')
    }
  }

  async function handleDelete(id: number) {
    try {
      await api.employees.delete(id)
      setDetailOpen(false)
      setSelectedEmployee(null)
      refreshAll()
      toast.success('Employee deleted')
    } catch {
      toast.error('Failed to delete employee')
    }
  }

  function handleEditClick(employee: Employee) {
    setDetailOpen(false)
    setEditingEmployee(employee)
    setFormOpen(true)
  }

  async function handleUpdate(payload: Parameters<typeof api.employees.create>[0]) {
    if (!editingEmployee) return
    try {
      await api.employees.update(editingEmployee.id, payload)
      setFormOpen(false)
      setEditingEmployee(null)
      refreshAll()
      toast.success('Employee updated')
    } catch {
      toast.error('Failed to update employee')
    }
  }

  return (
    <div className="min-h-screen bg-muted/40">
      <header className="border-b bg-background px-6 py-4">
        <h1 className="text-xl font-semibold tracking-tight">Salary Management</h1>
      </header>

      <main className="w-full px-6 py-6">
        <div className="flex flex-col gap-6 lg:flex-row lg:items-start">
          {/* Left — 30% metrics */}
          <aside className="w-full lg:w-[30%] lg:shrink-0">
            <MetricsPanel metrics={metrics} loading={loadingMetrics} />
          </aside>

          {/* Right — 70% employee CRUD */}
          <section className="min-w-0 flex-1 space-y-4">
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
                onView={handleView}
                loading={loadingEmployees}
              />
            </div>
          </section>
        </div>
      </main>

      <EmployeeForm
        open={formOpen}
        employee={editingEmployee ?? undefined}
        onClose={() => { setFormOpen(false); setEditingEmployee(null) }}
        onSubmit={editingEmployee ? handleUpdate : handleCreate}
      />

      <Toaster richColors position="top-right" />

      <EmployeeDetail
        employee={selectedEmployee}
        open={detailOpen}
        onClose={() => setDetailOpen(false)}
        onEdit={handleEditClick}
        onDelete={handleDelete}
      />
    </div>
  )
}
