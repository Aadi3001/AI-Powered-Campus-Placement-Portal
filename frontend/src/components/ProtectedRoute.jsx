import { Navigate } from 'react-router-dom'
import { useAuth } from '../AuthContext.jsx'

export default function ProtectedRoute({ roles, children }) {
    const { user, loading } = useAuth()

    if (loading) return null
    if (!user) return <Navigate to="/login" replace />

    if (roles && !roles.includes(user.role)) {
        return (
            <div className="container py-5">
                <div className="alert alert-warning">
                    This page is for {roles.join(' / ').toLowerCase()} accounts only.
                </div>
            </div>
        )
    }

    return children
}