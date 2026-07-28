export function useAuth() {
  const user = useCookie('auth_user', { default: () => null })

  const isAuthenticated = computed(() => !!user.value)

  async function login(credentials) {
    const { user: loggedInUser } = await $fetch('/api/auth/login', {
      method: 'POST',
      body: credentials,
    })
    user.value = loggedInUser
    return loggedInUser
  }

  async function signup(data) {
    const { user: newUser } = await $fetch('/api/auth/signup', {
      method: 'POST',
      body: data,
    })
    user.value = newUser
    return newUser
  }

  async function logout() {
    await $fetch('/api/auth/logout', { method: 'POST' })
    user.value = null
  }

  return { user, isAuthenticated, login, signup, logout }
}
