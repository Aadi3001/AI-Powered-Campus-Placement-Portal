import { useEffect, useState } from 'react'
import api from '../../api.js'
import { errorText } from '../../errors.js'

const EMPTY_COMPANY = { name: '', website: '', industry: '', description: '' }

export default function RecruiterProfile() {
  const [form, setForm] = useState(null)
  const [companies, setCompanies] = useState([])
  const [newCompany, setNewCompany] = useState(EMPTY_COMPANY)
  const [showNewCompany, setShowNewCompany] = useState(false)
  const [loading, setLoading] = useState(true)
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState('')
  const [message, setMessage] = useState('')

  useEffect(() => {
    Promise.all([api.get('/recruiter/profile/'), api.get('/recruiter/companies/')])
      .then(([profileRes, companiesRes]) => {
        const p = profileRes.data
        setCompanies(companiesRes.data)
        setForm({
          full_name: p.full_name ?? '',
          designation: p.designation ?? '',
          phone_number: p.phone_number ?? '',
          company: p.company ?? '',
        })
      })
      .catch(() => setError('Could not load your profile.'))
      .finally(() => setLoading(false))
  }, [])

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value })
  const handleCompanyChange = (e) =>
    setNewCompany({ ...newCompany, [e.target.name]: e.target.value })

  const saveProfile = async (e) => {
    e.preventDefault()
    setError('')
    setMessage('')
    setBusy(true)
    try {
      await api.patch('/recruiter/profile/', { ...form, company: form.company || null })
      setMessage('Profile saved.')
    } catch (err) {
      setError(errorText(err, 'Could not save your profile.'))
    } finally {
      setBusy(false)
    }
  }

  const createCompany = async (e) => {
    e.preventDefault()
    setError('')
    setMessage('')
    setBusy(true)
    try {
      const res = await api.post('/recruiter/companies/', newCompany)
      setCompanies((prev) => [...prev, res.data])
      setForm((f) => ({ ...f, company: res.data.id }))
      setNewCompany(EMPTY_COMPANY)
      setShowNewCompany(false)
      setMessage('Company created and selected. Click "Save profile" to keep it.')
    } catch (err) {
      setError(errorText(err, 'Could not create the company.'))
    } finally {
      setBusy(false)
    }
  }

  if (loading) return <div className="container py-5">Loading...</div>
  if (!form) {
    return (
      <div className="container py-5">
        <div className="alert alert-danger">{error}</div>
      </div>
    )
  }

  return (
    <div className="container py-4" style={{ maxWidth: 640 }}>
      <h1 className="mb-4">My profile</h1>
      {message && <div className="alert alert-success">{message}</div>}
      {error && <div className="alert alert-danger">{error}</div>}

      <form onSubmit={saveProfile} className="card card-body mb-4">
        {[
          ['full_name', 'Full name'],
          ['designation', 'Designation (for example HR Manager)'],
          ['phone_number', 'Phone number'],
        ].map(([name, label]) => (
          <div className="mb-3" key={name}>
            <label className="form-label" htmlFor={name}>{label}</label>
            <input
              id={name}
              name={name}
              className="form-control"
              value={form[name]}
              onChange={handleChange}
            />
          </div>
        ))}
        <div className="mb-3">
          <label className="form-label" htmlFor="company">Company</label>
          <select
            id="company"
            name="company"
            className="form-select"
            value={form.company}
            onChange={handleChange}
          >
            <option value="">Select a company</option>
            {companies.map((c) => (
              <option key={c.id} value={c.id}>{c.name}</option>
            ))}
          </select>
          <button
            type="button"
            className="btn btn-link btn-sm px-0"
            onClick={() => setShowNewCompany(!showNewCompany)}
          >
            {showNewCompany ? 'Cancel' : "My company isn't listed: create it"}
          </button>
        </div>
        <button className="btn btn-primary" disabled={busy}>Save profile</button>
      </form>

      {showNewCompany && (
        <form onSubmit={createCompany} className="card card-body">
          <h5 className="mb-3">New company</h5>
          {[
            ['name', 'Company name', true],
            ['website', 'Website (https://...)', false],
            ['industry', 'Industry', false],
            ['description', 'Short description', false],
          ].map(([name, label, required]) => (
            <div className="mb-3" key={name}>
              <label className="form-label" htmlFor={`company-${name}`}>{label}</label>
              <input
                id={`company-${name}`}
                name={name}
                className="form-control"
                value={newCompany[name]}
                onChange={handleCompanyChange}
                required={required}
              />
            </div>
          ))}
          <button className="btn btn-outline-primary" disabled={busy}>
            Create company
          </button>
        </form>
      )}
    </div>
  )
}