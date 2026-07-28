export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig(event)
  const body = await readBody(event)

  let result
  try {
    result = await $fetch(`${config.backendUrl}/users/login`, {
      method: 'POST',
      body,
    })
  } catch (error) {
    throw createError({
      statusCode: error?.statusCode ?? 500,
      statusMessage: error?.data?.detail ?? 'Invalid email or password',
    })
  }

  const user = decodeJwtPayload(result.access_token)

  setCookie(event, 'auth_token', result.access_token, {
    httpOnly: true,
    sameSite: 'lax',
    path: '/',
    maxAge: 60 * 60,
  })
  setCookie(event, 'auth_user', JSON.stringify(user), {
    httpOnly: false,
    sameSite: 'lax',
    path: '/',
    maxAge: 60 * 60,
  })

  return { user }
})
