<script setup>
definePageMeta({ middleware: 'auth' })

const blog_info = reactive({
  title: '',
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
    <AppHeader />

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

      <!-- Error card -->
      <div v-if="submitError" class="error-card" role="alert">
        <div class="error-icon">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" aria-hidden="true">
            <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2"/>
            <path d="M12 7v6M12 16.5h.01" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/>
          </svg>
        </div>
        <div class="error-content">
          <span class="error-title">Publishing Failed</span>
          <span class="error-message">Something went wrong. Please try again.</span>
        </div>
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
@keyframes error-shake {
  10%, 90% { transform: translate3d(-1px, 0, 0); }
  20%, 80% { transform: translate3d(2px, 0, 0); }
  30%, 50%, 70% { transform: translate3d(-3px, 0, 0); }
  40%, 60% { transform: translate3d(3px, 0, 0); }
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
  .page-header { padding: 48px 16px 40px; }
  .form-container { padding: 0 16px 48px; }
  .form-actions { flex-direction: column-reverse; }
  .btn-cancel,
  .btn-publish { width: 100%; }
}
</style>
