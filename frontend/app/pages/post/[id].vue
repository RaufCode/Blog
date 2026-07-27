<script setup>
definePageMeta({
  validate (route) {
    // Check if the id is made up of digits
    return typeof route.params.id === 'string' && /^\d+$/.test(route.params.id)
  },
})
const route = useRoute()
const { data: post, pending, error } = await usePost(route.params.id)

const isEditing = ref(false)
const editForm = reactive({
  title: '',
  author: '',
  content: '',
})

function startEdit() {
  editForm.title = post.value.title
  editForm.author = post.value.author || ''
  editForm.content = post.value.content
  isEditing.value = true
}

const delete_post = async () => {
    if (!confirm('Delete this post? This cannot be undone.')) {
        return
    }
    try {
        await useDelete(post.value.id)
        await navigateTo('/')
    } catch (error) {

    }
}

function cancelEdit() {
  isEditing.value = false
}

async function saveEdit() {
  try {
    const { data } = await useUpdate(post.value.id, {
      title: editForm.title,
      author: editForm.author,
      content: editForm.content,
    })
    post.value = data.value
    isEditing.value = false
  } catch (error) {

  }
}

function initials(author) {
  const name = author || 'anonymous'
  return name.trim().split(/\s+/).map(w => w[0]).join('').slice(0, 2).toUpperCase()
}

function readTime(content) {
  const words = (content || '').trim().split(/\s+/).filter(Boolean).length
  return Math.max(1, Math.round(words / 200)) + ' min read'
}

function formatDate(value) {
  return new Date(value).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
}

function paragraphs(content) {
  return (content || '')
    .split(/\n{2,}/)
    .map(paragraph => paragraph.trim())
    .filter(Boolean)
}
</script>

<template>
    <div class="page">
        <header class="topbar">
            <NuxtLink to="/" class="brand">
                <span class="brand-mark"><span class="brand-dot"></span></span>
                <span class="brand-name">Signal</span>
            </NuxtLink>
            <div v-if="post && !isEditing" class="post-actions">
                <button type="button" class="btn btn-secondary" @click="startEdit">Edit</button>
                <button @click="delete_post" type="button" class="btn btn-danger">Delete</button>
            </div>
        </header>

        <p v-if="pending" class="state-message">Loading…</p>
        <p v-else-if="error" class="state-message state-message--error">Couldn't load this post.</p>

        <template v-else-if="post">
            <form v-if="isEditing" class="edit-form" @submit.prevent="saveEdit">
                <div class="field">
                    <label for="edit-title">Title</label>
                    <input id="edit-title" v-model="editForm.title" type="text" required />
                </div>
                <div class="field">
                    <label for="edit-author">Author</label>
                    <input id="edit-author" v-model="editForm.author" type="text" placeholder="Optional" />
                </div>
                <div class="field">
                    <label for="edit-content">Content</label>
                    <textarea id="edit-content" v-model="editForm.content" rows="14" required></textarea>
                </div>
                <div class="form-actions">
                    <button type="button" class="btn btn-secondary" @click="cancelEdit">Cancel</button>
                    <button type="submit" class="btn btn-primary">Save</button>
                </div>
            </form>

            <article v-else class="post">
                <h1 class="post-title">{{ post.title }}</h1>
                <div class="post-meta">
                    <span class="avatar">{{ initials(post.author) }}</span>
                    <span class="author">{{ post.author || "anonymous" }}</span>
                    <span class="meta-sep">·</span>
                    <span class="date">{{ formatDate(post.created_at) }}</span>
                    <span class="meta-sep">·</span>
                    <span class="read-time">{{ readTime(post.content) }}</span>
                </div>
                <div class="post-body">
                    <p v-for="(paragraph, index) in paragraphs(post.content)" :key="index">{{ paragraph }}</p>
                </div>
            </article>
        </template>
    </div>
</template>

<style scoped>
.page {
    max-width: 760px;
    margin: 0 auto;
    padding: 56px 24px 96px;
    font-family: var(--font-sans);
    color: var(--color-text);
}

.topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
    margin-bottom: 40px;
}

.brand {
    display: inline-flex;
    align-items: center;
    gap: 10px;
    color: inherit;
    text-decoration: none;
}

.post-actions {
    display: flex;
    gap: 10px;
}

.brand-mark {
    width: 26px;
    height: 26px;
    border-radius: 7px;
    background: var(--color-accent);
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}

.brand-dot {
    width: 10px;
    height: 10px;
    background: var(--color-accent-contrast);
    border-radius: 3px;
}

.brand-name {
    font-weight: 800;
    font-size: 18px;
    letter-spacing: -0.02em;
}

.state-message {
    font-size: 15px;
    color: var(--color-text-muted);
}

.state-message--error {
    color: var(--color-error);
}

.post {
    max-width: 68ch;
    margin: 0 auto;
}

.post-title {
    font-family: var(--font-serif);
    font-size: clamp(28px, 5vw, 40px);
    font-weight: 700;
    line-height: 1.2;
    margin: 0 0 20px 0;
    letter-spacing: -0.01em;
}

.post-meta {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 36px;
    padding-bottom: 24px;
    border-bottom: 1px solid var(--color-border);
    flex-wrap: wrap;
}

.avatar {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    background: var(--color-accent);
    color: white;
    font-size: 11px;
    font-weight: 700;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}

.author {
    font-size: 14px;
    font-weight: 600;
}

.meta-sep,
.date,
.read-time {
    font-size: 14px;
    color: var(--color-text-faint);
}

.post-body {
    font-size: 17px;
    line-height: 1.85;
    color: var(--color-body);
}

.post-body p {
    margin: 0;
}

.post-body p + p {
    margin-top: 1.35em;
}

.btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 8px 16px;
    border-radius: 8px;
    font-size: 13px;
    font-weight: 600;
    text-decoration: none;
    border: 1px solid transparent;
    cursor: pointer;
    white-space: nowrap;
}

.btn-primary {
    background: var(--color-accent);
    color: var(--color-accent-contrast);
}

.btn-primary:hover {
    opacity: 0.9;
}

.btn-secondary {
    background: transparent;
    color: var(--color-text-muted);
    border-color: var(--color-border);
}

.btn-danger {
    background: transparent;
    color: var(--color-error);
    border-color: var(--color-border);
}

.edit-form {
    max-width: 68ch;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    gap: 24px;
}

.field {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.field label {
    font-size: 13px;
    font-weight: 600;
    color: var(--color-text-muted);
}

.field input,
.field textarea {
    font-family: var(--font-sans);
    font-size: 15px;
    line-height: 1.6;
    padding: 12px 14px;
    border: 1px solid var(--color-border);
    border-radius: 8px;
    background: oklch(1 0 0);
    color: var(--color-text);
    resize: vertical;
}

.field input:focus,
.field textarea:focus {
    outline: none;
    border-color: var(--color-accent);
}

.form-actions {
    display: flex;
    justify-content: flex-end;
    gap: 12px;
}

@media (max-width: 480px) {
    .page {
        padding: 40px 16px 72px;
    }

    .topbar {
        flex-wrap: wrap;
    }
}
</style>
