import { Routes, Route, Link } from 'react-router-dom'
import { useAuth } from './AuthContext.jsx'
import Home from './pages/Home.jsx'
import Login from './pages/Login.jsx'

export default function App() {
  const { user, loading, logout } = useAuth()

  if (loading) return null

  return (
    <>
      <nav className="navbar navbar-dark bg-dark px-3">
        <Link className="navbar-brand" to="/">Placement Portal</Link>
        {user ? (
          <div className="d-flex align-items-center gap-3">
            <span className="text-light">{user.username} ({user.role})</span>
            <button className="btn btn-outline-light btn-sm" onClick={logout}>
              Logout
            </button>
          </div>
        ) : (
          <Link className="btn btn-outline-light btn-sm" to="/login">Login</Link>
        )}
      </nav>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
      </Routes>
    </>
  )
}