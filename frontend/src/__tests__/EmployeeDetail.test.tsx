import { render, screen, fireEvent } from '@testing-library/react'
import { describe, it, expect, vi } from 'vitest'
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
  it('shows all employee fields when open', () => {
    render(<EmployeeDetail employee={employee} open={true} onClose={() => {}} />)
    expect(screen.getByText('Alice Smith')).toBeInTheDocument()
    expect(screen.getByText('Software Engineer')).toBeInTheDocument()
    expect(screen.getByText('Engineering')).toBeInTheDocument()
    expect(screen.getByText('India')).toBeInTheDocument()
    expect(screen.getByText('alice@company.com')).toBeInTheDocument()
    expect(screen.getByText('$80,000')).toBeInTheDocument()
  })

  it('does not show details when closed', () => {
    render(<EmployeeDetail employee={employee} open={false} onClose={() => {}} />)
    expect(screen.queryByText('Alice Smith')).not.toBeInTheDocument()
  })

  it('does not show Edit button when onEdit is not provided', () => {
    render(<EmployeeDetail employee={employee} open={true} onClose={() => {}} />)
    expect(screen.queryByRole('button', { name: /edit/i })).not.toBeInTheDocument()
  })

  it('calls onEdit with employee when Edit button is clicked', () => {
    const onEdit = vi.fn()
    render(<EmployeeDetail employee={employee} open={true} onClose={() => {}} onEdit={onEdit} />)
    fireEvent.click(screen.getByRole('button', { name: /edit/i }))
    expect(onEdit).toHaveBeenCalledWith(employee)
  })

  it('calls onClose when sheet is dismissed', () => {
    const onClose = vi.fn()
    render(<EmployeeDetail employee={employee} open={true} onClose={onClose} />)
    fireEvent.keyDown(document, { key: 'Escape' })
    expect(onClose).toHaveBeenCalled()
  })

  it('shows Delete button when onDelete is provided', () => {
    render(<EmployeeDetail employee={employee} open={true} onClose={() => {}} onDelete={() => {}} />)
    expect(screen.getByRole('button', { name: /delete/i })).toBeInTheDocument()
  })

  it('does not show Delete button when onDelete is not provided', () => {
    render(<EmployeeDetail employee={employee} open={true} onClose={() => {}} />)
    expect(screen.queryByRole('button', { name: /delete/i })).not.toBeInTheDocument()
  })

  it('calls onDelete with employee id when Delete is clicked', () => {
    const onDelete = vi.fn()
    render(<EmployeeDetail employee={employee} open={true} onClose={() => {}} onDelete={onDelete} />)
    fireEvent.click(screen.getByRole('button', { name: /delete/i }))
    expect(onDelete).toHaveBeenCalledWith(employee.id)
  })
})
