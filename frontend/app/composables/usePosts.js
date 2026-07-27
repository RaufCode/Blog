export function usePosts() {
  return useFetch('/api/post/')
}


// GET detailed post
export function usePost(id) {
  return useFetch(`/api/post/${id}`)
}


export function useCreate(blog_info) {
  return useFetch(`/api/post/create`, {
    method: 'POST',
    body: blog_info,
  })
}

export function useDelete(id) {
  return useFetch(`/api/post/${id}`, {
    method: 'DELETE',
    body: id,
  })
}

export function useUpdate(id, blog_info) {
  return useFetch(`/api/post/${id}`, {
    method: 'PUT',
    body: blog_info,
  })
}


export function useSummarize(id) {
  return $fetch(`/api/${id}/summarize`, {
    method: 'POST',
  })
}

