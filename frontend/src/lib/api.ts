const BASE_URL = 'http://localhost:8000'

export interface Employee {
  id: number
  full_name: string
  job_title: string
  department: string
  country: string
  salary: number
  email: string
  created_at: string
  updated_at: string
}

export interface EmployeeFormData {
  full_name: string
  email: string
  job_title: string
  department: string
  country: string
  salary: number
}

export interface EmployeePage {
  items: Employee[]
  total: number
  page: number
  page_size: number
}

export interface DepartmentMetrics {
  department: string
  count: number
  average_salary: number
}

export interface CountryMetrics {
  country: string
  count: number
  average_salary: number
  min_salary: number
  max_salary: number
}

export interface SalaryMetrics {
  total: number
  average_salary: number
  min_salary: number | null
  max_salary: number | null
  by_department: DepartmentMetrics[]
  by_country: CountryMetrics[]
}

async function request<T>(url: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE_URL}${url}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Request failed' }))
    throw new Error(err.detail ?? 'Request failed')
  }
  if (res.status === 204) return undefined as T
  return res.json()
}

export const api = {
  employees: {
    list: (params: { page: number; page_size: number; name?: string; country?: string }) => {
      const query = new URLSearchParams(
        Object.entries(params)
          .filter(([, v]) => v !== undefined && v !== '')
          .map(([k, v]) => [k, String(v)])
      )
      return request<{ data: EmployeePage }>(`/api/employees?${query}`)
    },
    get: (id: number) =>
      request<{ data: Employee }>(`/api/employees/${id}`),
    metrics: () =>
      request<{ data: SalaryMetrics }>('/api/employees/metrics'),
    delete: (id: number) =>
      request<void>(`/api/employees/${id}`, { method: 'DELETE' }),
    update: (id: number, data: EmployeeFormData) =>
      request<{ data: Employee }>(`/api/employees/${id}`, {
        method: 'PUT',
        body: JSON.stringify(data),
      }),
    create: (data: EmployeeFormData) =>
      request<{ data: Employee }>('/api/employees', {
        method: 'POST',
        body: JSON.stringify(data),
      }),
  },
}
