export default defineEventHandler(async (event) => {
    const config = useRuntimeConfig(event)

    try {
        return await $fetch(`${config.backendUrl}/posts`)
    } catch (error) {
        throw createError({
            statusCode: error?.statusCode ?? 500,
            statusMessage: "Unable to fetch posts"
        },
        )
    }

})