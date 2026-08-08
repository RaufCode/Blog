export default defineEventHandler(async (event) => {
    const config = useRuntimeConfig(event)
    const id = getRouterParam(event, 'id')
    const body = await readBody(event)

    try {
        return await $fetch(`${config.backendUrl}/posts/${id}`, {
            method: 'PUT',
            body,
            headers: authHeaders(event),
        })
    } catch (error) {
        throw createError({
            statusCode: error?.statusCode ?? 500,
            statusMessage: error?.data?.detail ?? "Unable to update post"
        })
    }
})
