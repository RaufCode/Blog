export function decodeJwtPayload(token) {
  const payload = token.split('.')[1]
  const json = Buffer.from(payload, 'base64url').toString('utf-8')
  return JSON.parse(json)
}
