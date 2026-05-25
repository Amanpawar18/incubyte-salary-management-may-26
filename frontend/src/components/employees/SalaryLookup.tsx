import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { api, type JobTitleMetrics } from '@/lib/api'

export function SalaryLookup() {
  const [jobTitle, setJobTitle] = useState('')
  const [country, setCountry] = useState('')
  const [result, setResult] = useState<JobTitleMetrics | null>(null)
  const [notFound, setNotFound] = useState(false)
  const [loading, setLoading] = useState(false)

  async function handleLookup() {
    setLoading(true)
    setNotFound(false)
    setResult(null)
    try {
      const res = await api.employees.jobTitleMetrics({ job_title: jobTitle.trim(), country: country.trim() })
      setResult(res.data)
    } catch {
      setNotFound(true)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="rounded-xl border bg-background shadow-sm p-4 space-y-3">
      <p className="text-sm font-medium">Salary by Job Title & Country</p>
      <Input
        placeholder="Job title (e.g. Software Engineer)"
        value={jobTitle}
        onChange={e => setJobTitle(e.target.value)}
        onKeyDown={e => e.key === 'Enter' && handleLookup()}
      />
      <Input
        placeholder="Country (e.g. India)"
        value={country}
        onChange={e => setCountry(e.target.value)}
        onKeyDown={e => e.key === 'Enter' && handleLookup()}
      />
      <Button
        size="sm"
        className="w-full"
        onClick={handleLookup}
        disabled={loading || !jobTitle.trim() || !country.trim()}
      >
        {loading ? 'Looking up…' : 'Look up'}
      </Button>
      {result && (
        <div className="rounded-lg bg-muted/50 px-3 py-2 space-y-1">
          <p className="text-xs text-muted-foreground">
            {result.count} employee{result.count !== 1 ? 's' : ''}
          </p>
          <p className="text-xl font-semibold">${result.average_salary.toLocaleString('en-US')}</p>
          <p className="text-xs text-muted-foreground">
            avg for {result.job_title} in {result.country}
          </p>
        </div>
      )}
      {notFound && (
        <p className="text-sm text-muted-foreground text-center">No employees found for this combination.</p>
      )}
    </div>
  )
}
