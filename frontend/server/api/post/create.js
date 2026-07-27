export default defineEventHandler(async (event) => {
    const config = useRuntimeConfig(event)
    const body = await readBody(event)

    try {
        return await $fetch(`${config.backendUrl}/posts/`, {
            method: 'POST',
            body,
        })
    } catch (error) {
        throw createError({
            statusCode: error?.statusCode ?? 500,
            statusMessage: "Unable to fetch posts"
        },
        )
    }

})