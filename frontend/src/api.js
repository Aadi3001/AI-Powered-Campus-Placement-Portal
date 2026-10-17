import axios from 'axios'

const API_URL = 'http://127.0.0.1:8000/api'

// Endpoints that work without being logged in
const PUBLIC_URLS = ['/token/', '/register/']

const api = axios.create({ baseURL: API_URL })

// Attach the access token to every request except the public ones
api.interceptors.request.use((config) => {
    const token = localStorage.getItem('access')
    if (token && !PUBLIC_URLS.includes(config.url)) {
        config.headers.Authorization = `Bearer ${token}`
    }
    return config
})

// If a request fails with 401, try once to get a new access token
// using the refresh token. If that also fails, log the user out.
api.interceptors.response.use(
    (response) => response,
    async (error) => {
        const original = error.config
        const status = error.response?.status

        // Errors on public endpoints (like a wrong password) are shown by the page itself
        if (status !== 401 || PUBLIC_URLS.includes(original.url)) {
            return Promise.reject(error)
        }

        const refresh = localStorage.getItem('refresh')
        if (refresh && !original._retried) {
            original._retried = true
            try {
                const { data } = await axios.post(`${API_URL}/token/refresh/`, { refresh })
                localStorage.setItem('access', data.access)
                original.headers.Authorization = `Bearer ${data.access}`
                return api(original)
            } catch {
                // refresh token is also invalid or expired: fall through to logout
            }
        }

        localStorage.removeItem('access')
        localStorage.removeItem('refresh')
        window.location.href = '/login'
        return Promise.reject(error)
    },
)

export default api