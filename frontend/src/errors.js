// Turns the API's validation errors into one readable sentence
export function errorText(err, fallback) {
    const data = err.response?.data
    if (data && typeof data === 'object') {
        return Object.values(data).flat().join(' ')
    }
    return fallback
}