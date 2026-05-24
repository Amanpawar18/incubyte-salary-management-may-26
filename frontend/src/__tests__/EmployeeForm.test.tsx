import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { describe, it, expect, vi } from 'vitest'
import { EmployeeForm } from '../components/employees/EmployeeForm'

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
})
