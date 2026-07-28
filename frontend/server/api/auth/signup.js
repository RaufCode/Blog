export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig(event)
  const body = await readBody(event)

  try {
    await $fetch(`${config.backendUrl}/users/`, {
      method: 'POST',
      body,
    })
  } catch (error) {
    throw createError({
      statusCode: error?.statusCode ?? 500,
      statusMessage: error?.data?.detail ?? 'Unable to create account',
    })
  }

  let result
  try {
    result = await $fetch(`${config.backendUrl}/users/login`, {
      method: 'POST',
      body: { email: body.email, password: body.password },
    })
  } catch (error) {
    throw createError({
      statusCode: error?.statusCode ?? 500,
      statusMessage: 'Account created, but sign-in failed. Please sign in.',
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
