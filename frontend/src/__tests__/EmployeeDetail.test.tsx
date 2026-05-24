import { render, screen } from '@testing-library/react'
import { describe, it, expect } from 'vitest'
import { EmployeeDetail } from '../components/employees/EmployeeDetail'
import type { Employee } from '../lib/api'

const employee: Employee = {
  id: 1,
  full_name: 'Alice Smith',
  job_title: 'Software Engineer',
  department: 'Engineering',
  country: 'India',
  salary: 80000,
  email: 'alice@company.com',
  created_at: '2026-01-01T00:00:00',
  updated_at: '2026-01-01T00:00:00',
}

describe('EmployeeDetail', () => {
  it('shows employee details when open', () => {
    render(<EmployeeDetail employee={employee} open={true} onClose={() => {}} />)
    expect(screen.getByText('Alice Smith')).toBeInTheDocument()
    expect(screen.getByText('Software Engineer')).toBeInTheDocument()
    expect(screen.getByText('alice@company.com')).toBeInTheDocument()
  })

  it('does not show details when closed', () => {
    render(<EmployeeDetail employee={employee} open={false} onClose={() => {}} />)
    expect(screen.queryByText('Alice Smith')).not.toBeInTheDocument()
  })
})
