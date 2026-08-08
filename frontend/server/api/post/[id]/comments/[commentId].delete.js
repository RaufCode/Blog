export default defineEventHandler(async (event) => {
    const config = useRuntimeConfig(event)
    const id = getRouterParam(event, 'id')
    const commentId = getRouterParam(event, 'commentId')

    try {
        return await $fetch(`${config.backendUrl}/posts/${id}/comments/${commentId}`, {
            method: 'DELETE',
            headers: authHeaders(event),
        })
    } catch (error) {
        throw createError({
            statusCode: error?.statusCode ?? 500,
            statusMessage: error?.data?.detail ?? "Unable to delete comment"
        })
    }
})
