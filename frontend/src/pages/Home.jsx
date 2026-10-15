import { useAuth } from '../AuthContext.jsx'

export default function Home() {
    const { user } = useAuth()

    return (
        <div className="container py-5">
            <h1>Campus Placement Portal</h1>
            <p className="text-muted">
                {user
                    ? `Logged in as ${user.username} (${user.role}).`
                    : 'Please log in to continue.'}
            </p>
        </div>
    )
}