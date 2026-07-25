export function usePosts() {
  return useFetch('/api/post/')
}


// GET detailed post
export function usePost(id) {
  return useFetch(`/api/post/${id}`)
}
