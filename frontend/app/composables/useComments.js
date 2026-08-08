export function useComments(postId) {
  return useFetch(`/api/post/${postId}/comments`)
}

export function usePostComment(postId, content) {
  return $fetch(`/api/post/${postId}/comments`, {
    method: 'POST',
    body: { content },
  })
}

export function useDeleteComment(postId, commentId) {
  return $fetch(`/api/post/${postId}/comments/${commentId}`, {
    method: 'DELETE',
  })
}
