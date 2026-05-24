import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { describe, it, expect, vi } from 'vitest'
import { EmployeeForm } from '../components/employees/EmployeeForm'
import type { Employee } from '../lib/api'

const existingEmployee: Employee = {
  id: 1,
  full_name: 'Alice Smith',
  email: 'alice@company.com',
  job_title: 'Software Engineer',
  department: 'Engineering',
  country: 'India',
  salary: 80000,
  created_at: '2026-01-01T00:00:00',
  updated_at: '2026-01-01T00:00:00',
}

const noop = () => {}

describe('EmployeeForm', () => {
  it('renders all form fields when open', () => {
    render(<EmployeeForm open onClose={noop} onSubmit={noop} />)
    expect(screen.getByLabelText(/full name/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/email/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/job title/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/department/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/country/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/salary/i)).toBeInTheDocument()
  })

  it('shows validation error when full name is empty on submit', async () => {
    render(<EmployeeForm open onClose={noop} onSubmit={noop} />)
    fireEvent.click(screen.getByRole('button', { name: /save/i }))
    await waitFor(() => {
      expect(screen.getByText(/full name is required/i)).toBeInTheDocument()
    })
  })

  it('calls onSubmit with form data when all fields are valid', async () => {
    const onSubmit = vi.fn()
    render(<EmployeeForm open onClose={noop} onSubmit={onSubmit} />)

    fireEvent.change(screen.getByLabelText(/full name/i), { target: { value: 'Bob Jones' } })
    fireEvent.change(screen.getByLabelText(/email/i), { target: { value: 'bob@company.com' } })
    fireEvent.change(screen.getByLabelText(/job title/i), { target: { value: 'Designer' } })
    fireEvent.change(screen.getByLabelText(/department/i), { target: { value: 'Design' } })
    fireEvent.change(screen.getByLabelText(/country/i), { target: { value: 'Germany' } })
    fireEvent.change(screen.getByLabelText(/salary/i), { target: { value: '95000' } })
    fireEvent.click(screen.getByRole('button', { name: /save/i }))

    await waitFor(() => {
      expect(onSubmit).toHaveBeenCalledWith({
        full_name: 'Bob Jones',
        email: 'bob@company.com',
        job_title: 'Designer',
        department: 'Design',
        country: 'Germany',
        salary: 95000,
      })
    })
  })

  it('calls onClose when cancel is clicked', () => {
    const onClose = vi.fn()
    render(<EmployeeForm open onClose={onClose} onSubmit={noop} />)
    fireEvent.click(screen.getByRole('button', { name: /cancel/i }))
    expect(onClose).toHaveBeenCalled()
  })

  it('shows "Add Employee" title in create mode', () => {
    render(<EmployeeForm open onClose={noop} onSubmit={noop} />)
    expect(screen.getByText(/add employee/i)).toBeInTheDocument()
  })

  it('shows "Edit Employee" title when employee prop is provided', () => {
    render(<EmployeeForm open onClose={noop} onSubmit={noop} employee={existingEmployee} />)
    expect(screen.getByText(/edit employee/i)).toBeInTheDocument()
  })

  it('pre-fills all fields with employee data in edit mode', () => {
    render(<EmployeeForm open onClose={noop} onSubmit={noop} employee={existingEmployee} />)
    expect(screen.getByLabelText<HTMLInputElement>(/full name/i).value).toBe('Alice Smith')
    expect(screen.getByLabelText<HTMLInputElement>(/email/i).value).toBe('alice@company.com')
    expect(screen.getByLabelText<HTMLInputElement>(/job title/i).value).toBe('Software Engineer')
    expect(screen.getByLabelText<HTMLInputElement>(/department/i).value).toBe('Engineering')
    expect(screen.getByLabelText<HTMLInputElement>(/country/i).value).toBe('India')
    expect(screen.getByLabelText<HTMLInputElement>(/salary/i).value).toBe('80000')
  })

  it('calls onSubmit with updated data when edited form is submitted', async () => {
    const onSubmit = vi.fn()
    render(<EmployeeForm open onClose={noop} onSubmit={onSubmit} employee={existingEmployee} />)
    fireEvent.change(screen.getByLabelText(/salary/i), { target: { value: '95000' } })
    fireEvent.click(screen.getByRole('button', { name: /save/i }))
    await waitFor(() => {
      expect(onSubmit).toHaveBeenCalledWith(expect.objectContaining({ salary: 95000 }))
    })
  })

  it('still validates required fields in edit mode', async () => {
    render(<EmployeeForm open onClose={noop} onSubmit={noop} employee={existingEmployee} />)
    fireEvent.change(screen.getByLabelText(/full name/i), { target: { value: '' } })
    fireEvent.click(screen.getByRole('button', { name: /save/i }))
    await waitFor(() => {
      expect(screen.getByText(/full name is required/i)).toBeInTheDocument()
    })
  })
})
