<script setup>
definePageMeta({
  validate(route) {
    return typeof route.params.id === 'string' && /^\d+$/.test(route.params.id)
  },
})

const route = useRoute()
const { data: post, pending, error } = await usePost(route.params.id)
const { data: comments } = await useComments(route.params.id)
const { isAuthenticated, user } = useAuth()

const isOwner = computed(() =>
  isAuthenticated.value &&
  !!post.value &&
  post.value.user_id != null &&
  String(post.value.user_id) === String(user.value?.sub)
)

const isEditing = ref(false)
const editForm = reactive({ title: '', author: '', content: '' })

function startEdit() {
  if (!isOwner.value) return
  editForm.title = post.value.title
  editForm.author = post.value.author || ''
  editForm.content = post.value.content
  isEditing.value = true
}
function cancelEdit() { isEditing.value = false }

async function saveEdit() {
  try {
    const { data } = await useUpdate(post.value.id, {
      title: editForm.title,
      author: editForm.author,
      content: editForm.content,
    })
    post.value = data.value
    isEditing.value = false
  } catch {}
}

const summary = ref('')
const summarizing = ref(false)
const summarizeError = ref(false)
async function summarize() {
  summarizing.value = true
  summarizeError.value = false
  try {
    const data = await useSummarize(post.value.id)
    summary.value = data?.summary || ''
  } catch {
    summarizeError.value = true
  } finally {
    summarizing.value = false
  }
}

const showDeleteConfirm = ref(false)
const deleting = ref(false)
async function confirmDelete() {
  if (!isOwner.value) return
  deleting.value = true
  try {
    await useDelete(post.value.id)
    await navigateTo('/')
  } catch {
    deleting.value = false
    showDeleteConfirm.value = false
  }
}

const newComment = ref('')
const postingComment = ref(false)
const commentError = ref(false)
async function submitComment() {
  if (!newComment.value.trim()) return
  postingComment.value = true
  commentError.value = false
  try {
    const created = await usePostComment(post.value.id, newComment.value.trim())
    comments.value = [...(comments.value || []), created]
    newComment.value = ''
  } catch {
    commentError.value = true
  } finally {
    postingComment.value = false
  }
}

const deletingCommentId = ref(null)
async function removeComment(commentId) {
  deletingCommentId.value = commentId
  try {
    await useDeleteComment(post.value.id, commentId)
    comments.value = (comments.value || []).filter((c) => c.id !== commentId)
  } catch {
    // leave the comment in place if deletion failed
  } finally {
    deletingCommentId.value = null
  }
}

function commentAuthorName(comment) {
  return `${comment.author.first_name} ${comment.author.last_name}`.trim()
}
function canDeleteComment(comment) {
  if (!isAuthenticated.value) return false
  if (isOwner.value) return true
  return String(comment.author.id) === String(user.value?.sub)
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
  return new Date(value).toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' })
}
function paragraphs(content) {
  return (content || '').split(/\n{2,}/).map(p => p.trim()).filter(Boolean)
}

const scrolled = ref(false)
if (import.meta.client) {
  window.addEventListener('scroll', () => { scrolled.value = window.scrollY > 20 }, { passive: true })
}
</script>

<template>
  <div class="page">

    <!-- Navbar -->
    <header class="nav" :class="{ 'nav--scrolled': scrolled }">
      <div class="nav-inner">
        <NuxtLink to="/" class="brand">
          <svg width="18" height="18" viewBox="0 0 18 18" fill="none" aria-hidden="true">
            <rect width="18" height="18" rx="5" fill="var(--accent)"/>
            <path d="M5 9h8M5 6h5M5 12h6" stroke="white" stroke-width="1.6" stroke-linecap="round"/>
          </svg>
          <span>Signal</span>
        </NuxtLink>

        <div v-if="post && !isEditing" class="post-actions">
          <button class="btn btn-summarize" :disabled="summarizing" @click="summarize">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" aria-hidden="true">
              <path d="M11 2.5c.18 0 .34.12.39.29l1.06 3.53a4.5 4.5 0 0 0 3.02 3.02l3.53 1.06c.17.05.29.21.29.39s-.12.34-.29.39l-3.53 1.06a4.5 4.5 0 0 0-3.02 3.02l-1.06 3.53a.41.41 0 0 1-.78 0l-1.06-3.53a4.5 4.5 0 0 0-3.02-3.02l-3.53-1.06a.41.41 0 0 1 0-.78l3.53-1.06a4.5 4.5 0 0 0 3.02-3.02l1.06-3.53c.05-.17.21-.29.39-.29Z" fill="currentColor"/>
            </svg>
            {{ summarizing ? 'Summarizing…' : 'AI Summary' }}
            <span v-if="summarizing" class="spinner-dot"></span>
          </button>
          <template v-if="isAuthenticated">
            <button class="btn btn-edit" @click="startEdit">
              <svg width="13" height="13" viewBox="0 0 14 14" fill="none" aria-hidden="true">
                <path d="M9.5 2.5l2 2L4 12H2v-2L9.5 2.5Z" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round"/>
              </svg>
              Edit
            </button>
            <button class="btn btn-danger" @click="showDeleteConfirm = true">
              <svg width="13" height="13" viewBox="0 0 14 14" fill="none" aria-hidden="true">
                <path d="M2 4h10M5 4V2.5h4V4M5.5 6.5v4M8.5 6.5v4M3 4l.8 7.5h6.4L11 4" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              Delete
            </button>
          </template>
          <NuxtLink v-else :to="`/login?redirect=/post/${post.id}`" class="btn btn-edit">
            Sign in to edit
          </NuxtLink>
        </div>

        <div v-if="isEditing" class="edit-actions">
          <button class="btn btn-cancel-edit" @click="cancelEdit">Cancel</button>
          <button class="btn btn-save" type="button" @click="saveEdit">Save changes</button>
        </div>
      </div>
    </header>

    <!-- Loading -->
    <div v-if="pending" class="state-loading" aria-busy="true" aria-label="Loading post">
      <div class="loading-bar"></div>
      <div class="skeleton-post">
        <div class="sk sk-title"></div>
        <div class="sk sk-meta"></div>
        <div class="sk sk-line"></div>
        <div class="sk sk-line"></div>
        <div class="sk sk-line short"></div>
      </div>
    </div>

    <!-- Error -->
    <div v-else-if="error" class="error-card full-page-error" role="alert">
      <div class="error-icon">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" aria-hidden="true">
          <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2"/>
          <path d="M12 7v6M12 16.5h.01" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/>
        </svg>
      </div>
      <div class="error-content">
        <span class="error-title">Couldn't load this post</span>
        <span class="error-message">The post you're looking for might have been removed or is temporarily unavailable. <br><br> <NuxtLink to="/" class="inline-link">← Go back home</NuxtLink></span>
      </div>
    </div>

    <!-- Post Content -->
    <template v-else-if="post">

      <!-- Edit Form -->
      <main v-if="isEditing" class="edit-container">
        <div class="edit-eyebrow">Editing post</div>
        <form class="edit-form" @submit.prevent="saveEdit">
          <div class="field">
            <label for="edit-title" class="field-label">Title</label>
            <input id="edit-title" v-model="editForm.title" type="text" required class="field-input"/>
          </div>
          <div class="field">
            <label for="edit-author" class="field-label">Author <span class="optional">optional</span></label>
            <input id="edit-author" v-model="editForm.author" type="text" class="field-input"/>
          </div>
          <div class="field">
            <label for="edit-content" class="field-label">Content</label>
            <textarea id="edit-content" v-model="editForm.content" rows="18" required class="field-textarea"></textarea>
          </div>
          <div class="form-actions">
            <button type="button" class="btn btn-cancel-edit" @click="cancelEdit">Cancel</button>
            <button type="submit" class="btn btn-save">Save changes</button>
          </div>
        </form>
      </main>

      <!-- Article View -->
      <main v-else class="article-container">

        <!-- Article header -->
        <header class="article-header">
          <NuxtLink to="/" class="back-link">
            <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
              <path d="M11 7H3M6 4L3 7l3 3" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            All posts
          </NuxtLink>
          <h1 class="article-title">{{ post.title }}</h1>
          <div class="article-meta">
            <span class="avatar">{{ initials(post.author) }}</span>
            <span class="meta-author">{{ post.author || 'anonymous' }}</span>
            <span class="meta-dot" aria-hidden="true"></span>
            <time :datetime="post.created_at" class="meta-date">{{ formatDate(post.created_at) }}</time>
            <span class="meta-dot" aria-hidden="true"></span>
            <span class="meta-read">{{ readTime(post.content) }}</span>
          </div>
        </header>

        <!-- Divider -->
        <div class="article-divider" aria-hidden="true"></div>

        <!-- Summarize error -->
        <div v-if="summarizeError" class="error-card" role="alert">
          <div class="error-icon">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" aria-hidden="true">
              <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2"/>
              <path d="M12 7v6M12 16.5h.01" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/>
            </svg>
          </div>
          <div class="error-content">
            <span class="error-title">Summary Failed</span>
            <span class="error-message">Couldn't generate a summary. Please try again.</span>
          </div>
        </div>

        <!-- AI Summary -->
        <div v-if="summary" class="summary-card">
          <div class="summary-card-glow"></div>
          <div class="summary-card-content">
            <div class="summary-header">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" aria-hidden="true">
                <path d="M11 2.5c.18 0 .34.12.39.29l1.06 3.53a4.5 4.5 0 0 0 3.02 3.02l3.53 1.06c.17.05.29.21.29.39s-.12.34-.29.39l-3.53 1.06a4.5 4.5 0 0 0-3.02 3.02l-1.06 3.53a.41.41 0 0 1-.78 0l-1.06-3.53a4.5 4.5 0 0 0-3.02-3.02l-3.53-1.06a.41.41 0 0 1 0-.78l3.53-1.06a4.5 4.5 0 0 0 3.02-3.02l1.06-3.53c.05-.17.21-.29.39-.29Z" fill="url(#summary-grad)"/>
                <defs>
                  <linearGradient id="summary-grad" x1="0" y1="0" x2="24" y2="24" gradientUnits="userSpaceOnUse">
                    <stop stop-color="#7c5cfc" />
                    <stop offset="1" stop-color="#a78bfa" />
                  </linearGradient>
                </defs>
              </svg>
              AI Executive Summary
            </div>
            <p class="summary-text">{{ summary }}</p>
          </div>
        </div>

        <!-- Body -->
        <article class="article-body">
          <p v-for="(para, i) in paragraphs(post.content)" :key="i">{{ para }}</p>
        </article>

        <!-- End decoration -->
        <div class="article-end" aria-hidden="true">
          <span class="end-line"></span>
          <span class="end-icon">
            <svg width="16" height="16" viewBox="0 0 18 18" fill="none">
              <rect width="18" height="18" rx="5" fill="var(--accent)" opacity="0.3"/>
              <path d="M5 9h8M5 6h5M5 12h6" stroke="var(--accent)" stroke-width="1.6" stroke-linecap="round"/>
            </svg>
          </span>
          <span class="end-line"></span>
        </div>

        <!-- Back CTA -->
        <div class="article-footer">
          <NuxtLink to="/" class="back-cta">
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
              <path d="M13 8H3M6 4L2 8l4 4" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            Back to all posts
          </NuxtLink>
        </div>

      </main>
    </template>

    <!-- Delete Confirm Modal -->
    <Teleport to="body">
      <div v-if="showDeleteConfirm" class="modal-backdrop" @click.self="showDeleteConfirm = false" role="dialog" aria-modal="true" aria-labelledby="delete-dialog-title">
        <div class="modal">
          <div class="modal-icon" aria-hidden="true">
            <svg width="22" height="22" viewBox="0 0 22 22" fill="none">
              <path d="M3 6h16M8 6V4h6v2M9.5 10v6M12.5 10v6M4 6l1.2 12h11.6L18 6" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          <h2 id="delete-dialog-title" class="modal-title">Delete this post?</h2>
          <p class="modal-body">This action cannot be undone. The post will be permanently removed.</p>
          <div class="modal-actions">
            <button class="btn btn-modal-cancel" @click="showDeleteConfirm = false">Cancel</button>
            <button class="btn btn-modal-delete" :disabled="deleting" @click="confirmDelete">
              <svg v-if="deleting" class="spinner" width="14" height="14" viewBox="0 0 16 16" fill="none">
                <circle cx="8" cy="8" r="6" stroke="currentColor" stroke-width="2" stroke-dasharray="28" stroke-dashoffset="14" stroke-linecap="round"/>
              </svg>
              {{ deleting ? 'Deleting…' : 'Yes, delete' }}
            </button>
          </div>
        </div>
      </div>
    </Teleport>

  </div>
</template>

<style scoped>
.page { min-height: 100vh; display: flex; flex-direction: column; animation: fadeUp var(--duration-slow) var(--ease-out) both; }

/* Navbar */
.nav { position: sticky; top: 0; z-index: 100; height: var(--nav-h); border-bottom: 1px solid transparent; transition: background var(--duration-base) var(--ease-out), border-color var(--duration-base) var(--ease-out), box-shadow var(--duration-base) var(--ease-out); }
.nav--scrolled { background: rgba(13,13,16,0.88); backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px); border-color: var(--border); box-shadow: 0 1px 24px rgba(0,0,0,0.4); }
.nav-inner { max-width: var(--max-w-wide); margin: 0 auto; padding: 0 24px; height: 100%; display: flex; align-items: center; justify-content: space-between; gap: 16px; }

.brand { display: inline-flex; align-items: center; gap: 9px; font-weight: 800; font-size: 16px; letter-spacing: -0.03em; color: var(--text-primary); transition: opacity var(--duration-fast); }
.brand:hover { opacity: 0.8; }

.post-actions, .edit-actions { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }

/* Buttons */
.btn { display: inline-flex; align-items: center; gap: 6px; padding: 7px 14px; border-radius: var(--radius-full); font-size: 13px; font-weight: 600; border: 1px solid var(--border); background: var(--bg-elevated); color: var(--text-secondary); cursor: pointer; transition: background var(--duration-fast), color var(--duration-fast), border-color var(--duration-fast), transform var(--duration-fast), box-shadow var(--duration-fast); white-space: nowrap; }
.btn:hover { background: var(--bg-overlay); color: var(--text-primary); border-color: rgba(255,255,255,0.12); }

.btn-summarize { color: var(--accent); border-color: rgba(124,92,252,0.3); background: var(--accent-subtle); }
.btn-summarize:hover:not(:disabled) { background: rgba(124,92,252,0.18); border-color: var(--accent); box-shadow: 0 0 16px var(--accent-glow); }
.btn-summarize:disabled { opacity: 0.5; cursor: not-allowed; }

.btn-edit:hover { color: var(--text-primary); }

.btn-danger { color: var(--color-error); border-color: rgba(240,96,96,0.25); }
.btn-danger:hover { background: rgba(240,96,96,0.1); border-color: var(--color-error); color: var(--color-error); }

.btn-save { background: var(--accent); color: white; border-color: transparent; }
.btn-save:hover { background: var(--accent-hover); transform: translateY(-1px); box-shadow: 0 4px 16px var(--accent-glow); border-color: transparent; }

.btn-cancel-edit { color: var(--text-secondary); }

.spinner-dot { width: 6px; height: 6px; border-radius: 50%; background: currentColor; animation: pulse-glow 1s ease-in-out infinite; }
.spinner { animation: spin 0.7s linear infinite; }

/* Loading */
.state-loading { max-width: 720px; margin: 0 auto; padding: 48px 24px; }
.loading-bar { height: 2px; background: linear-gradient(90deg, transparent, var(--accent), transparent); background-size: 200% 100%; animation: shimmer 1.2s ease-in-out infinite; border-radius: 99px; margin-bottom: 48px; }
.skeleton-post { display: flex; flex-direction: column; gap: 16px; }
.sk { border-radius: 6px; background: linear-gradient(90deg, var(--bg-elevated) 25%, var(--bg-overlay) 50%, var(--bg-elevated) 75%); background-size: 400px 100%; animation: shimmer 1.4s ease-in-out infinite; }
.sk-title { height: 36px; width: 75%; }
.sk-meta { height: 14px; width: 45%; margin-bottom: 8px; }
.sk-line { height: 14px; width: 100%; }
.sk-line.short { width: 65%; }

/* ── Error Card ── */
.error-card {
  display: flex;
  align-items: flex-start;
  gap: 14px;
  padding: 16px;
  background: rgba(240, 96, 96, 0.05);
  border: 1px solid rgba(240, 96, 96, 0.2);
  border-radius: var(--radius-md);
  box-shadow: 0 8px 24px rgba(240, 96, 96, 0.1), inset 0 1px 0 rgba(255, 255, 255, 0.05);
  position: relative;
  overflow: hidden;
  margin-bottom: 24px;
  animation: error-shake 0.4s cubic-bezier(0.36, 0.07, 0.19, 0.97) both;
}
.full-page-error { max-width: 720px; margin: 80px auto; }
.error-card::before {
  content: "";
  position: absolute;
  top: 0; left: 0; bottom: 0;
  width: 4px;
  background: var(--color-error);
  box-shadow: 0 0 12px var(--color-error);
}
.error-icon {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background: rgba(240, 96, 96, 0.15);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-error);
  flex-shrink: 0;
}
.error-content {
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.error-title {
  font-size: 14px;
  font-weight: 700;
  color: var(--color-error);
}
.error-message {
  font-size: 14px;
  color: var(--text-secondary);
  line-height: 1.5;
}
.inline-link {
  color: var(--accent);
  font-weight: 600;
  text-decoration: underline;
}
@keyframes error-shake {
  10%, 90% { transform: translate3d(-1px, 0, 0); }
  20%, 80% { transform: translate3d(2px, 0, 0); }
  30%, 50%, 70% { transform: translate3d(-3px, 0, 0); }
  40%, 60% { transform: translate3d(3px, 0, 0); }
}

/* Article */
.article-container { flex: 1; max-width: 720px; width: 100%; margin: 0 auto; padding: 48px 24px 80px; }

.article-header { margin-bottom: 32px; }

.back-link { display: inline-flex; align-items: center; gap: 6px; font-size: 13px; font-weight: 600; color: var(--text-tertiary); margin-bottom: 28px; transition: color var(--duration-fast); }
.back-link:hover { color: var(--accent); }

.article-title { font-family: var(--font-serif); font-size: clamp(28px, 5vw, 44px); font-weight: 700; line-height: 1.15; letter-spacing: -0.02em; color: var(--text-primary); margin-bottom: 20px; }

.article-meta { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }
.avatar { width: 28px; height: 28px; border-radius: 50%; background: linear-gradient(135deg, var(--accent), #a78bfa); color: white; font-size: 11px; font-weight: 700; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.meta-author { font-size: 14px; font-weight: 600; color: var(--text-secondary); }
.meta-dot { width: 3px; height: 3px; border-radius: 50%; background: var(--text-tertiary); flex-shrink: 0; }
.meta-date, .meta-read { font-size: 13px; color: var(--text-tertiary); }

.article-divider { height: 1px; background: linear-gradient(90deg, transparent, var(--border) 20%, var(--border) 80%, transparent); margin-bottom: 36px; }

/* AI Summary */
.summary-card { position: relative; margin-bottom: 40px; border-radius: var(--radius-lg); background: var(--bg-surface); border: 1px solid transparent; box-shadow: 0 4px 20px rgba(0,0,0,0.2); z-index: 1; }
.summary-card::before { content: ""; position: absolute; inset: -1px; border-radius: calc(var(--radius-lg) + 1px); background: linear-gradient(135deg, rgba(124,92,252,0.5), rgba(167,139,250,0.2), rgba(124,92,252,0.1)); z-index: -1; pointer-events: none; }
.summary-card-glow { position: absolute; inset: 0; border-radius: var(--radius-lg); background: radial-gradient(circle at top left, rgba(124,92,252,0.15) 0%, transparent 60%); z-index: 0; pointer-events: none; overflow: hidden; }
.summary-card-glow::after { content: ""; position: absolute; top: 0; left: -100%; width: 50%; height: 100%; background: linear-gradient(90deg, transparent, rgba(255,255,255,0.05), transparent); animation: summary-shimmer 4s ease-in-out infinite; }
@keyframes summary-shimmer { 0% { left: -100%; } 50%, 100% { left: 200%; } }
.summary-card-content { position: relative; z-index: 1; padding: 24px 28px; }
.summary-header { display: flex; align-items: center; gap: 8px; font-size: 11.5px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; background: linear-gradient(135deg, #a78bfa, #c4b5fd); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; margin-bottom: 12px; }
.summary-text { font-size: 15.5px; line-height: 1.75; color: var(--text-primary); text-shadow: 0 1px 2px rgba(0,0,0,0.4); }



/* Article body */
.article-body { font-family: var(--font-serif); font-size: 19px; line-height: 1.85; color: var(--text-secondary); }
.article-body p { margin: 0; }
.article-body p + p { margin-top: 1.4em; }

/* End + Back */
.article-end { display: flex; align-items: center; gap: 16px; margin: 56px 0 40px; }
.end-line { flex: 1; height: 1px; background: var(--border); }
.end-icon { display: flex; align-items: center; }

.article-footer { text-align: center; }
.back-cta { display: inline-flex; align-items: center; gap: 8px; font-size: 14px; font-weight: 600; color: var(--text-secondary); background: var(--bg-elevated); border: 1px solid var(--border); padding: 10px 20px; border-radius: var(--radius-full); transition: background var(--duration-fast), color var(--duration-fast), border-color var(--duration-fast), transform var(--duration-fast); }
.back-cta:hover { background: var(--bg-overlay); color: var(--text-primary); border-color: rgba(255,255,255,0.12); transform: translateX(-2px); }

/* Edit Container */
.edit-container { flex: 1; max-width: 680px; width: 100%; margin: 0 auto; padding: 48px 24px 80px; }
.edit-eyebrow { font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; color: var(--accent); margin-bottom: 28px; }
.edit-form { display: flex; flex-direction: column; gap: 24px; }
.field { display: flex; flex-direction: column; gap: 8px; }
.field-label { font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: var(--text-tertiary); display: flex; align-items: center; gap: 6px; }
.optional { font-size: 10px; font-weight: 600; text-transform: none; background: var(--bg-elevated); border: 1px solid var(--border); padding: 2px 7px; border-radius: var(--radius-full); }
.field-input, .field-textarea { font-family: var(--font-sans); font-size: 15px; line-height: 1.65; padding: 13px 16px; background: var(--bg-surface); border: 1px solid var(--border); border-radius: var(--radius-md); color: var(--text-primary); transition: border-color var(--duration-fast), box-shadow var(--duration-fast), background var(--duration-fast); width: 100%; }
.field-input::placeholder, .field-textarea::placeholder { color: var(--text-tertiary); }
.field-input:focus, .field-textarea:focus { outline: none; border-color: var(--accent); background: var(--bg-elevated); box-shadow: var(--shadow-accent); }
.field-textarea { resize: none; min-height: 300px; }
.form-actions { display: flex; justify-content: flex-end; gap: 12px; padding-top: 8px; }

/* Delete Modal */
.modal-backdrop { position: fixed; inset: 0; background: rgba(0,0,0,0.7); backdrop-filter: blur(6px); -webkit-backdrop-filter: blur(6px); z-index: 1000; display: flex; align-items: center; justify-content: center; padding: 24px; animation: fadeIn var(--duration-base) var(--ease-out) both; }
.modal { background: var(--bg-surface); border: 1px solid var(--border); border-radius: var(--radius-lg); padding: 32px; max-width: 400px; width: 100%; box-shadow: var(--shadow-lg); animation: fadeUp var(--duration-base) var(--ease-out) both; }
.modal-icon { width: 44px; height: 44px; border-radius: var(--radius-md); background: rgba(240,96,96,0.1); border: 1px solid rgba(240,96,96,0.2); display: flex; align-items: center; justify-content: center; color: var(--color-error); margin-bottom: 16px; }
.modal-title { font-size: 18px; font-weight: 700; color: var(--text-primary); margin-bottom: 8px; }
.modal-body { font-size: 14px; color: var(--text-secondary); line-height: 1.6; margin-bottom: 24px; }
.modal-actions { display: flex; gap: 10px; justify-content: flex-end; }
.btn-modal-cancel { background: var(--bg-elevated); border: 1px solid var(--border); color: var(--text-secondary); border-radius: var(--radius-full); padding: 9px 18px; font-size: 14px; font-weight: 600; cursor: pointer; transition: background var(--duration-fast), color var(--duration-fast); }
.btn-modal-cancel:hover { background: var(--bg-overlay); color: var(--text-primary); }
.btn-modal-delete { display: inline-flex; align-items: center; gap: 7px; background: var(--color-error); color: white; border: 1px solid transparent; border-radius: var(--radius-full); padding: 9px 18px; font-size: 14px; font-weight: 700; cursor: pointer; transition: opacity var(--duration-fast), transform var(--duration-fast); }
.btn-modal-delete:hover:not(:disabled) { opacity: 0.88; transform: translateY(-1px); }
.btn-modal-delete:disabled { opacity: 0.5; cursor: not-allowed; }

@media (max-width: 640px) {
  .nav-inner { padding: 0 16px; }
  .post-actions { gap: 6px; }
  .btn { padding: 6px 10px; font-size: 12px; }
  .article-container, .edit-container { padding: 32px 16px 64px; }
  .article-title { font-size: clamp(24px, 7vw, 36px); }
  .article-body { font-size: 17px; }
  .form-actions { flex-direction: column-reverse; }
}
</style>
