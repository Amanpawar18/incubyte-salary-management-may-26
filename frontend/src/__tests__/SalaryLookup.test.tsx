import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { SalaryLookup } from '../components/employees/SalaryLookup'

const mockJobTitleMetrics = vi.fn()

vi.mock('../lib/api', () => ({
  api: {
    employees: {
      jobTitleMetrics: (...args: unknown[]) => mockJobTitleMetrics(...args),
    },
  },
}))

describe('SalaryLookup', () => {
  beforeEach(() => {
    mockJobTitleMetrics.mockReset()
  })

  it('renders job title and country inputs', () => {
    render(<SalaryLookup />)
    expect(screen.getByPlaceholderText(/job title/i)).toBeInTheDocument()
    expect(screen.getByPlaceholderText(/country/i)).toBeInTheDocument()
  })

  it('disables Look up button when inputs are empty', () => {
    render(<SalaryLookup />)
    expect(screen.getByRole('button', { name: /look up/i })).toBeDisabled()
  })

  it('shows average salary after successful lookup', async () => {
    mockJobTitleMetrics.mockResolvedValue({
      data: { job_title: 'Software Engineer', country: 'India', count: 42, average_salary: 95000 },
    })
    const user = userEvent.setup()
    render(<SalaryLookup />)
    await user.type(screen.getByPlaceholderText(/job title/i), 'Software Engineer')
    await user.type(screen.getByPlaceholderText(/country/i), 'India')
    await user.click(screen.getByRole('button', { name: /look up/i }))
    expect(await screen.findByText('$95,000')).toBeInTheDocument()
    expect(screen.getByText(/42 employee/i)).toBeInTheDocument()
  })

  it('shows not found message when API returns error', async () => {
    mockJobTitleMetrics.mockRejectedValue(new Error('No employees found'))
    const user = userEvent.setup()
    render(<SalaryLookup />)
    await user.type(screen.getByPlaceholderText(/job title/i), 'CEO')
    await user.type(screen.getByPlaceholderText(/country/i), 'Mars')
    await user.click(screen.getByRole('button', { name: /look up/i }))
    expect(await screen.findByText(/no employees found/i)).toBeInTheDocument()
  })
})
