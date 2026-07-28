<script setup>
definePageMeta({ middleware: 'auth' })

const { user } = useAuth()

const blog_info = reactive({
  title: '',
  author: `${user.value?.first_name ?? ''} ${user.value?.last_name ?? ''}`.trim(),
  content: '',
})

const isSubmitting = ref(false)
const submitError = ref(false)

const charCount = computed(() => blog_info.content.length)
const wordCount = computed(() => {
  return blog_info.content.trim().split(/\s+/).filter(Boolean).length
})
const readTime = computed(() => Math.max(1, Math.round(wordCount.value / 200)) + ' min read')

const blog_post = async () => {
  isSubmitting.value = true
  submitError.value = false
  try {
    await useCreate(blog_info)
    await navigateTo('/')
  } catch (error) {
    submitError.value = true
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <div class="page">

    <!-- ── Topbar ── -->
    <header class="topbar">
      <div class="topbar-inner">
        <NuxtLink to="/" class="brand" aria-label="Back to Signal home">
          <svg width="18" height="18" viewBox="0 0 18 18" fill="none" aria-hidden="true">
            <rect width="18" height="18" rx="5" fill="var(--accent)"/>
            <path d="M5 9h8M5 6h5M5 12h6" stroke="white" stroke-width="1.6" stroke-linecap="round"/>
          </svg>
          <span class="brand-name">Signal</span>
        </NuxtLink>

        <NuxtLink to="/" class="btn-back">
          <svg width="14" height="14" viewBox="0 0 14 14" fill="none" aria-hidden="true">
            <path d="M11 7H3M6 4L3 7l3 3" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          Back
        </NuxtLink>
      </div>
    </header>

    <!-- ── Page Header ── -->
    <div class="page-header">
      <div class="page-header-glow" aria-hidden="true"></div>
      <div class="page-eyebrow">
        <span class="eyebrow-dot" aria-hidden="true"></span>
        New post
      </div>
      <h1 class="page-title">Share what you've learned</h1>
      <p class="page-subtitle">Write your thoughts, document your process, or share an idea worth spreading.</p>
    </div>

    <!-- ── Form ── -->
    <main class="form-container">

      <!-- Error Banner -->
      <div v-if="submitError" class="error-banner" role="alert">
        <svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true">
          <circle cx="8" cy="8" r="7" stroke="currentColor" stroke-width="1.4"/>
          <path d="M8 5v3.5M8 11h.01" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>
        </svg>
        Something went wrong. Please try again.
      </div>

      <form class="post-form" @submit.prevent="blog_post" novalidate>

        <!-- Title -->
        <div class="field">
          <label for="title" class="field-label">Title <span class="required" aria-label="required">*</span></label>
          <input
            id="title"
            v-model="blog_info.title"
            name="title"
            type="text"
            autocomplete="off"
            placeholder="Give your post a compelling title"
            required
            class="field-input"
            :class="{ 'has-value': blog_info.title }"
          />
          <p class="field-hint">A great title is concise, specific, and sparks curiosity.</p>
        </div>

        <!-- Author -->
        <div class="field">
          <label for="author" class="field-label">
            Author
            <span class="optional-badge">optional</span>
          </label>
          <input
            id="author"
            v-model="blog_info.author"
            name="author"
            type="text"
            autocomplete="name"
            placeholder="Your name"
            class="field-input"
            :class="{ 'has-value': blog_info.author }"
          />
        </div>

        <!-- Content -->
        <div class="field">
          <div class="field-label-row">
            <label for="content" class="field-label">Content <span class="required" aria-label="required">*</span></label>
            <div class="content-stats" v-if="blog_info.content">
              <span>{{ wordCount }} words</span>
              <span class="stat-sep" aria-hidden="true">·</span>
              <span>{{ readTime }}</span>
            </div>
          </div>
          <textarea
            id="content"
            v-model="blog_info.content"
            name="content"
            rows="16"
            placeholder="Write your post… Start with the most important idea."
            required
            class="field-textarea"
            :class="{ 'has-value': blog_info.content }"
          ></textarea>
          <p class="field-hint">Use double line breaks to separate paragraphs.</p>
        </div>

        <!-- Actions -->
        <div class="form-actions">
          <NuxtLink to="/" class="btn-cancel">Discard</NuxtLink>
          <button
            type="submit"
            class="btn-publish"
            :disabled="isSubmitting || !blog_info.title.trim() || !blog_info.content.trim()"
            :aria-busy="isSubmitting"
          >
            <svg v-if="isSubmitting" class="spinner" width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true">
              <circle cx="8" cy="8" r="6" stroke="currentColor" stroke-width="2" stroke-dasharray="28" stroke-dashoffset="14" stroke-linecap="round"/>
            </svg>
            <svg v-else width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true">
              <path d="M2 8l4 4 8-8" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            {{ isSubmitting ? 'Publishing…' : 'Publish post' }}
          </button>
        </div>

      </form>
    </main>

    <!-- ── Footer ── -->
    <footer class="footer">
      <p class="footer-tip">
        <svg width="12" height="12" viewBox="0 0 12 12" fill="none" aria-hidden="true">
          <circle cx="6" cy="6" r="5" stroke="currentColor" stroke-width="1.2"/>
          <path d="M6 5.5v3M6 4h.01" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/>
        </svg>
        Your post will be public immediately after publishing.
      </p>
    </footer>

  </div>
</template>

<style scoped>
/* ── Layout ──────────────────────────────────────────────────── */
.page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  animation: fadeUp var(--duration-slow) var(--ease-out) both;
}

/* ── Topbar ──────────────────────────────────────────────────── */
.topbar {
  height: var(--nav-h);
  border-bottom: 1px solid var(--border);
  background: rgba(13, 13, 16, 0.85);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  position: sticky;
  top: 0;
  z-index: 100;
}

.topbar-inner {
  max-width: var(--max-w-wide);
  margin: 0 auto;
  padding: 0 24px;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.brand {
  display: inline-flex;
  align-items: center;
  gap: 9px;
  font-weight: 800;
  font-size: 16px;
  letter-spacing: -0.03em;
  color: var(--text-primary);
  transition: opacity var(--duration-fast);
}
.brand:hover { opacity: 0.8; }

.brand-name { color: var(--text-primary); }

.btn-back {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  font-weight: 600;
  color: var(--text-secondary);
  background: var(--bg-elevated);
  border: 1px solid var(--border);
  padding: 7px 14px;
  border-radius: var(--radius-full);
  transition: background var(--duration-fast), color var(--duration-fast), border-color var(--duration-fast);
}
.btn-back:hover {
  background: var(--bg-overlay);
  color: var(--text-primary);
  border-color: rgba(255,255,255,0.12);
}

/* ── Page Header ─────────────────────────────────────────────── */
.page-header {
  position: relative;
  overflow: hidden;
  text-align: center;
  padding: 64px 24px 52px;
}

.page-header-glow {
  position: absolute;
  top: -80px;
  left: 50%;
  transform: translateX(-50%);
  width: 500px;
  height: 300px;
  background: radial-gradient(ellipse, rgba(124,92,252,0.15) 0%, transparent 70%);
  pointer-events: none;
}

.page-eyebrow {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: var(--accent);
  margin-bottom: 16px;
}

.eyebrow-dot {
  display: inline-block;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--accent);
}

.page-title {
  font-family: var(--font-serif);
  font-size: clamp(28px, 5vw, 42px);
  font-weight: 700;
  letter-spacing: -0.02em;
  line-height: 1.15;
  color: var(--text-primary);
  margin-bottom: 12px;
}

.page-subtitle {
  font-size: 15px;
  color: var(--text-secondary);
  max-width: 46ch;
  margin: 0 auto;
  line-height: 1.65;
}

/* ── Form Container ──────────────────────────────────────────── */
.form-container {
  flex: 1;
  max-width: 680px;
  width: 100%;
  margin: 0 auto;
  padding: 0 24px 48px;
}

/* ── Error Banner ────────────────────────────────────────────── */
.error-banner {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 14px 18px;
  background: rgba(240, 96, 96, 0.08);
  border: 1px solid rgba(240, 96, 96, 0.2);
  border-radius: var(--radius-md);
  color: var(--color-error);
  font-size: 14px;
  font-weight: 500;
  margin-bottom: 28px;
}

/* ── Form ────────────────────────────────────────────────────── */
.post-form {
  display: flex;
  flex-direction: column;
  gap: 28px;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.field-label-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.field-label {
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--text-tertiary);
  display: flex;
  align-items: center;
  gap: 6px;
}

.required {
  color: var(--accent);
}

.optional-badge {
  font-size: 10px;
  font-weight: 600;
  text-transform: none;
  letter-spacing: 0.02em;
  color: var(--text-tertiary);
  background: var(--bg-elevated);
  border: 1px solid var(--border);
  padding: 2px 7px;
  border-radius: var(--radius-full);
}

.content-stats {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 11px;
  font-weight: 500;
  color: var(--text-tertiary);
}

.stat-sep {
  opacity: 0.5;
}

.field-input,
.field-textarea {
  font-family: var(--font-sans);
  font-size: 15px;
  line-height: 1.65;
  padding: 14px 16px;
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  color: var(--text-primary);
  transition: border-color var(--duration-fast), box-shadow var(--duration-fast), background var(--duration-fast);
  width: 100%;
  -webkit-appearance: none;
}

.field-input::placeholder,
.field-textarea::placeholder {
  color: var(--text-tertiary);
}

.field-input:hover,
.field-textarea:hover {
  border-color: rgba(255,255,255,0.12);
}

.field-input:focus,
.field-textarea:focus {
  outline: none;
  border-color: var(--accent);
  background: var(--bg-elevated);
  box-shadow: var(--shadow-accent);
}

.field-textarea {
  resize: none;
  min-height: 280px;
  font-size: 15px;
  line-height: 1.8;
}

.field-hint {
  font-size: 12px;
  color: var(--text-tertiary);
  line-height: 1.5;
}

/* ── Form Actions ────────────────────────────────────────────── */
.form-actions {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 12px;
  padding-top: 8px;
}

.btn-cancel {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 11px 22px;
  background: var(--bg-elevated);
  border: 1px solid var(--border);
  border-radius: var(--radius-full);
  color: var(--text-secondary);
  font-size: 14px;
  font-weight: 600;
  transition: background var(--duration-fast), color var(--duration-fast), border-color var(--duration-fast);
}
.btn-cancel:hover {
  background: var(--bg-overlay);
  color: var(--text-primary);
  border-color: rgba(255,255,255,0.12);
}

.btn-publish {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 11px 26px;
  background: var(--accent);
  color: var(--accent-contrast);
  font-size: 14px;
  font-weight: 700;
  border: 1px solid transparent;
  border-radius: var(--radius-full);
  cursor: pointer;
  letter-spacing: 0.01em;
  transition: background var(--duration-fast), transform var(--duration-fast), box-shadow var(--duration-fast), opacity var(--duration-fast);
}
.btn-publish:hover:not(:disabled) {
  background: var(--accent-hover);
  transform: translateY(-1px);
  box-shadow: 0 4px 20px var(--accent-glow);
}
.btn-publish:active:not(:disabled) { transform: translateY(0); }
.btn-publish:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

/* Spinner animation */
.spinner {
  animation: spin 0.7s linear infinite;
  flex-shrink: 0;
}

/* ── Footer ──────────────────────────────────────────────────── */
.footer {
  border-top: 1px solid var(--border);
  padding: 16px 24px;
  text-align: center;
}

.footer-tip {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  font-size: 12px;
  color: var(--text-tertiary);
}

/* ── Responsive ──────────────────────────────────────────────── */
@media (max-width: 640px) {
  .topbar { padding: 0 16px; }
  .page-header { padding: 48px 16px 40px; }
  .form-container { padding: 0 16px 48px; }
  .form-actions { flex-direction: column-reverse; }
  .btn-cancel,
  .btn-publish { width: 100%; }
}
</style>
