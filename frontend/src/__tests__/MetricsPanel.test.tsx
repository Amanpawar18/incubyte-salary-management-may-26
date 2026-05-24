import { render, screen } from '@testing-library/react'
import { describe, it, expect } from 'vitest'
import { MetricsPanel } from '../components/employees/MetricsPanel'
import type { SalaryMetrics } from '../lib/api'

const metrics: SalaryMetrics = {
  total: 5,
  average_salary: 90000,
  min_salary: 60000,
  max_salary: 120000,
  by_department: [
    { department: 'Engineering', count: 3, average_salary: 100000 },
    { department: 'Design', count: 2, average_salary: 75000 },
  ],
  by_country: [
    { country: 'India', count: 3, average_salary: 80000 },
    { country: 'Germany', count: 2, average_salary: 105000 },
  ],
}

const emptyMetrics: SalaryMetrics = {
  total: 0,
  average_salary: 0,
  min_salary: null,
  max_salary: null,
  by_department: [],
  by_country: [],
}

describe('MetricsPanel', () => {
  it('shows total employee count', () => {
    render(<MetricsPanel metrics={metrics} />)
    expect(screen.getByText('5')).toBeInTheDocument()
  })

  it('shows formatted average salary', () => {
    render(<MetricsPanel metrics={metrics} />)
    expect(screen.getByText('$90,000')).toBeInTheDocument()
  })

  it('shows formatted min and max salary', () => {
    render(<MetricsPanel metrics={metrics} />)
    expect(screen.getByText('$60,000')).toBeInTheDocument()
    expect(screen.getByText('$120,000')).toBeInTheDocument()
  })

  it('shows department breakdown', () => {
    render(<MetricsPanel metrics={metrics} />)
    expect(screen.getByText('Engineering')).toBeInTheDocument()
    expect(screen.getByText('Design')).toBeInTheDocument()
  })

  it('shows country breakdown', () => {
    render(<MetricsPanel metrics={metrics} />)
    expect(screen.getByText('India')).toBeInTheDocument()
    expect(screen.getByText('Germany')).toBeInTheDocument()
  })

  it('shows dashes for min/max when no employees', () => {
    render(<MetricsPanel metrics={emptyMetrics} />)
    expect(screen.getAllByText('—')).toHaveLength(2)
  })

  it('shows zero average when no employees', () => {
    render(<MetricsPanel metrics={emptyMetrics} />)
    expect(screen.getByText('$0')).toBeInTheDocument()
  })
})
