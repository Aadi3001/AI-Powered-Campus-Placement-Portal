import { createContext, useContext, useEffect, useState } from 'react'
import api from './api.js'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
    const [user, setUser] = useState(null)
    // We only need to wait for the server if a token is already stored
    const [loading, setLoading] = useState(() => Boolean(localStorage.getItem('access')))

    // On first load, if we already have a token, ask the API who we are
    useEffect(() => {
        if (!localStorage.getItem('access')) return
        api.get('/me/')
            .then((res) => setUser(res.data))
            .catch(() => setUser(null))
            .finally(() => setLoading(false))
    }, [])

    const login = async (username, password) => {
        const { data } = await api.post('/token/', { username, password })
        localStorage.setItem('access', data.access)
        localStorage.setItem('refresh', data.refresh)
        const me = await api.get('/me/')
        setUser(me.data)
        return me.data
    }

    const logout = () => {
        localStorage.removeItem('access')
        localStorage.removeItem('refresh')
        setUser(null)
    }

    return (
        <AuthContext.Provider value={{ user, loading, login, logout }}>
            {children}
        </AuthContext.Provider>
    )
}

// eslint-disable-next-line react-refresh/only-export-components
export function useAuth() {
    return useContext(AuthContext)
}