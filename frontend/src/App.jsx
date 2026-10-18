import { Routes, Route, Link } from 'react-router-dom'
import { useAuth } from './AuthContext.jsx'
import ProtectedRoute from './components/ProtectedRoute.jsx'
import Home from './pages/Home.jsx'
import Login from './pages/Login.jsx'
import Register from './pages/Register.jsx'
import Jobs from './pages/student/Jobs.jsx'
import Applications from './pages/student/Applications.jsx'
import Profile from './pages/student/Profile.jsx'
import MyJobs from './pages/recruiter/MyJobs.jsx'
import Applicants from './pages/recruiter/Applicants.jsx'
import RecruiterProfile from './pages/recruiter/Profile.jsx'

export default function App() {
  const { user, loading, logout } = useAuth()

  if (loading) return null

  return (
    <>
      <nav className="navbar navbar-dark bg-dark px-3">
        <div className="d-flex align-items-center gap-3">
          <Link className="navbar-brand" to="/">Placement Portal</Link>
          {user?.role === 'STUDENT' && (
            <>
              <Link className="text-light text-decoration-none" to="/student/jobs">Jobs</Link>
              <Link className="text-light text-decoration-none" to="/student/applications">
                My applications
              </Link>
              <Link className="text-light text-decoration-none" to="/student/profile">Profile</Link>
            </>
          )}
          {user?.role === 'RECRUITER' && (
            <>
              <Link className="text-light text-decoration-none" to="/recruiter/jobs">My jobs</Link>
              <Link className="text-light text-decoration-none" to="/recruiter/profile">Profile</Link>
            </>
          )}
        </div>
        {user ? (
          <div className="d-flex align-items-center gap-3">
            <span className="text-light">{user.username} ({user.role})</span>
            <button className="btn btn-outline-light btn-sm" onClick={logout}>
              Logout
            </button>
          </div>
        ) : (
          <div className="d-flex gap-2">
            <Link className="btn btn-outline-light btn-sm" to="/login">Login</Link>
            <Link className="btn btn-light btn-sm" to="/register">Register</Link>
          </div>
        )}
      </nav>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route
          path="/student/jobs"
          element={
            <ProtectedRoute roles={['STUDENT']}>
              <Jobs />
            </ProtectedRoute>
          }
        />
        <Route
          path="/student/applications"
          element={
            <ProtectedRoute roles={['STUDENT']}>
              <Applications />
            </ProtectedRoute>
          }
        />
        <Route
          path="/student/profile"
          element={
            <ProtectedRoute roles={['STUDENT']}>
              <Profile />
            </ProtectedRoute>
          }
        />
        <Route
          path="/recruiter/jobs"
          element={
            <ProtectedRoute roles={['RECRUITER']}>
              <MyJobs />
            </ProtectedRoute>
          }
        />
        <Route
          path="/recruiter/jobs/:jobId/applicants"
          element={
            <ProtectedRoute roles={['RECRUITER']}>
              <Applicants />
            </ProtectedRoute>
          }
        />
        <Route
          path="/recruiter/profile"
          element={
            <ProtectedRoute roles={['RECRUITER']}>
              <RecruiterProfile />
            </ProtectedRoute>
          }
        />
      </Routes>
    </>
  )
}