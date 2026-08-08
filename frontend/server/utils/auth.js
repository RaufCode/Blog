export function authHeaders(event) {
  const token = getCookie(event, 'auth_token')
  return token ? { Authorization: `Bearer ${token}` } : {}
}
