<script setup>
const { login } = useAuth()
const route = useRoute()

const credentials = reactive({
  email: '',
  password: '',
})

const isSubmitting = ref(false)
const errorMessage = ref('')

async function handleSubmit() {
  isSubmitting.value = true
  errorMessage.value = ''
  try {
    await login(credentials)
    await navigateTo(route.query.redirect?.toString() || '/')
  } catch (error) {
    errorMessage.value = error?.data?.statusMessage || 'Invalid email or password.'
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <div class="auth-page">

    <!-- ── Topbar ── -->
    <header class="topbar">
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
    </header>

    <!-- ── Auth Card ── -->
    <main class="auth-container">
      <div class="auth-glow" aria-hidden="true"></div>

      <div class="auth-card">
        <div class="auth-eyebrow">
          <span class="eyebrow-dot" aria-hidden="true"></span>
          Welcome back
        </div>
        <h1 class="auth-title">Sign in</h1>
        <p class="auth-subtitle">Sign in to write, edit, and manage your posts.</p>

        <div v-if="errorMessage" class="error-banner" role="alert">
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true">
            <circle cx="8" cy="8" r="7" stroke="currentColor" stroke-width="1.4"/>
            <path d="M8 5v3.5M8 11h.01" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>
          </svg>
          {{ errorMessage }}
        </div>

        <form class="auth-form" @submit.prevent="handleSubmit" novalidate>
          <div class="field">
            <label for="email" class="field-label">Email</label>
            <input
              id="email"
              v-model="credentials.email"
              type="email"
              name="email"
              autocomplete="email"
              placeholder="you@example.com"
              required
              class="field-input"
            />
          </div>

          <div class="field">
            <label for="password" class="field-label">Password</label>
            <input
              id="password"
              v-model="credentials.password"
              type="password"
              name="password"
              autocomplete="current-password"
              placeholder="••••••••"
              required
              class="field-input"
            />
          </div>

          <button
            type="submit"
            class="btn-submit"
            :disabled="isSubmitting || !credentials.email || !credentials.password"
            :aria-busy="isSubmitting"
          >
            <svg v-if="isSubmitting" class="spinner" width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true">
              <circle cx="8" cy="8" r="6" stroke="currentColor" stroke-width="2" stroke-dasharray="28" stroke-dashoffset="14" stroke-linecap="round"/>
            </svg>
            {{ isSubmitting ? 'Signing in…' : 'Sign in' }}
          </button>
        </form>

        <p class="auth-switch">
          Don't have an account? <NuxtLink to="/signup" class="inline-link">Create one</NuxtLink>
        </p>
      </div>
    </main>

  </div>
</template>

<style scoped>
.auth-page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  animation: fadeUp var(--duration-slow) var(--ease-out) both;
}

/* ── Topbar ── */
.topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  height: var(--nav-h);
  border-bottom: 1px solid var(--border);
  background: rgba(13, 13, 16, 0.85);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  position: sticky;
  top: 0;
  z-index: 100;
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

/* ── Auth Container ── */
.auth-container {
  flex: 1;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 48px 24px;
  overflow: hidden;
}

.auth-glow {
  position: absolute;
  top: -100px;
  left: 50%;
  transform: translateX(-50%);
  width: 560px;
  height: 340px;
  background: radial-gradient(ellipse, rgba(124,92,252,0.16) 0%, transparent 70%);
  pointer-events: none;
}

.auth-card {
  position: relative;
  width: 100%;
  max-width: 420px;
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 40px 36px;
  box-shadow: var(--shadow-lg);
}

.auth-eyebrow {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: var(--accent);
  margin-bottom: 14px;
}

.eyebrow-dot {
  display: inline-block;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--accent);
}

.auth-title {
  font-family: var(--font-serif);
  font-size: clamp(26px, 4vw, 32px);
  font-weight: 700;
  letter-spacing: -0.02em;
  color: var(--text-primary);
  margin-bottom: 8px;
}

.auth-subtitle {
  font-size: 14px;
  color: var(--text-secondary);
  line-height: 1.6;
  margin-bottom: 28px;
}

/* ── Error Banner ── */
.error-banner {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 16px;
  background: rgba(240, 96, 96, 0.08);
  border: 1px solid rgba(240, 96, 96, 0.2);
  border-radius: var(--radius-md);
  color: var(--color-error);
  font-size: 13px;
  font-weight: 500;
  margin-bottom: 22px;
}

/* ── Form ── */
.auth-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.field-label {
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--text-tertiary);
}

.field-input {
  font-family: var(--font-sans);
  font-size: 15px;
  padding: 13px 15px;
  background: var(--bg-elevated);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  color: var(--text-primary);
  transition: border-color var(--duration-fast), box-shadow var(--duration-fast);
  width: 100%;
  -webkit-appearance: none;
}

.field-input::placeholder { color: var(--text-tertiary); }

.field-input:hover { border-color: rgba(255,255,255,0.12); }

.field-input:focus {
  outline: none;
  border-color: var(--accent);
  box-shadow: var(--shadow-accent);
}

.btn-submit {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  margin-top: 4px;
  padding: 13px 22px;
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
.btn-submit:hover:not(:disabled) {
  background: var(--accent-hover);
  transform: translateY(-1px);
  box-shadow: 0 4px 20px var(--accent-glow);
}
.btn-submit:active:not(:disabled) { transform: translateY(0); }
.btn-submit:disabled { opacity: 0.4; cursor: not-allowed; }

.spinner { animation: spin 0.7s linear infinite; flex-shrink: 0; }

.auth-switch {
  margin-top: 24px;
  text-align: center;
  font-size: 13px;
  color: var(--text-secondary);
}

.inline-link {
  color: var(--accent);
  font-weight: 600;
  text-decoration: underline;
  text-underline-offset: 2px;
}

/* ── Responsive ── */
@media (max-width: 640px) {
  .topbar { padding: 0 16px; }
  .auth-container { padding: 32px 16px; }
  .auth-card { padding: 32px 24px; }
}
</style>
