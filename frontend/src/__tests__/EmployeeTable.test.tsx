import { render, screen, fireEvent } from '@testing-library/react'
import { describe, it, expect, vi } from 'vitest'
import { EmployeeTable } from '../components/employees/EmployeeTable'
import type { Employee } from '../lib/api'

const makeEmployee = (overrides: Partial<Employee> = {}): Employee => ({
  id: 1,
  full_name: 'Alice Smith',
  job_title: 'Software Engineer',
  department: 'Engineering',
  country: 'India',
  salary: 80000,
  email: 'alice@company.com',
  created_at: '2026-01-01T00:00:00',
  updated_at: '2026-01-01T00:00:00',
  ...overrides,
})

const noop = () => {}

describe('EmployeeTable', () => {
  it('shows empty state when no employees', () => {
    render(
      <EmployeeTable items={[]} total={0} page={1} pageSize={20} onPageChange={noop} />
    )
    expect(screen.getByText(/no employees/i)).toBeInTheDocument()
  })

  it('renders a row for each employee', () => {
    const employees = [
      makeEmployee({ id: 1, full_name: 'Alice Smith' }),
      makeEmployee({ id: 2, full_name: 'Bob Jones', email: 'bob@company.com' }),
    ]
    render(
      <EmployeeTable items={employees} total={2} page={1} pageSize={20} onPageChange={noop} />
    )
    expect(screen.getByText('Alice Smith')).toBeInTheDocument()
    expect(screen.getByText('Bob Jones')).toBeInTheDocument()
  })

  it('shows pagination info', () => {
    render(
      <EmployeeTable items={[makeEmployee()]} total={50} page={1} pageSize={20} onPageChange={noop} />
    )
    expect(screen.getByText(/1.*20.*50/)).toBeInTheDocument()
  })

  it('calls onPageChange with next page when Next is clicked', () => {
    const onPageChange = vi.fn()
    render(
      <EmployeeTable items={[makeEmployee()]} total={50} page={1} pageSize={20} onPageChange={onPageChange} />
    )
    fireEvent.click(screen.getByRole('button', { name: /next/i }))
    expect(onPageChange).toHaveBeenCalledWith(2)
  })

  it('disables Prev button on first page', () => {
    render(
      <EmployeeTable items={[makeEmployee()]} total={50} page={1} pageSize={20} onPageChange={noop} />
    )
    expect(screen.getByRole('button', { name: /prev/i })).toBeDisabled()
  })

  it('disables Next button on last page', () => {
    render(
      <EmployeeTable items={[makeEmployee()]} total={20} page={1} pageSize={20} onPageChange={noop} />
    )
    expect(screen.getByRole('button', { name: /next/i })).toBeDisabled()
  })
})
