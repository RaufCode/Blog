export default defineEventHandler(async (event) => {
    const config = useRuntimeConfig(event)
    const id = getRouterParam(event, 'id')

    try {
        return await $fetch(`${config.backendUrl}/posts/${id}`)
    } catch (error) {
        throw createError({
            statusCode: error?.statusCode ?? 500,
            statusMessage: "Unable to fetch post"
        })
    }
})
