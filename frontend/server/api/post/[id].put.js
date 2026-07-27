export default defineEventHandler(async (event) => {
    const config = useRuntimeConfig(event)
    const id = getRouterParam(event, 'id')
    const body = await readBody(event)

    try {
        return await $fetch(`${config.backendUrl}/posts/${id}`, {
            method: 'PUT',
            body,
        })
    } catch (error) {
        throw createError({
            statusCode: error?.statusCode ?? 500,
            statusMessage: "Unable to update post"
        })
    }
})
