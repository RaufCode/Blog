<script setup>
const { login } = useAuth()
const route = useRoute()

const credentials = reactive({
  email: '',
  password: '',
})

const isSubmitting = ref(false)
const errorMessage = ref('')
const showPassword = ref(false)

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

    <!-- ── Animated Background ── -->
    <div class="bg-canvas" aria-hidden="true">
      <div class="bg-orb bg-orb-1"></div>
      <div class="bg-orb bg-orb-2"></div>
      <div class="bg-orb bg-orb-3"></div>
      <div class="bg-grid"></div>
    </div>

    <!-- ── Topbar ── -->
    <header class="topbar">
      <div class="topbar-inner">
        <NuxtLink to="/" class="brand" aria-label="Back to Signal home">
          <div class="brand-icon">
            <svg width="16" height="16" viewBox="0 0 18 18" fill="none" aria-hidden="true">
              <path d="M5 9h8M5 6h5M5 12h6" stroke="white" stroke-width="1.8" stroke-linecap="round"/>
            </svg>
          </div>
          <span class="brand-name">Signal</span>
        </NuxtLink>

        <NuxtLink to="/" class="btn-back">
          <svg width="14" height="14" viewBox="0 0 14 14" fill="none" aria-hidden="true">
            <path d="M11 7H3M6 4L3 7l3 3" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          Back to home
        </NuxtLink>
      </div>
    </header>

    <!-- ── Auth Layout ── -->
    <main class="auth-layout">

      <!-- Left Panel -->
      <div class="auth-left" aria-hidden="true">
        <div class="left-content">
          <div class="left-tagline">
            <div class="tagline-eyebrow">
              <span class="eyebrow-dot"></span>
              Your signal awaits
            </div>
            <h2 class="tagline-title">Write with<br><span class="tagline-accent">purpose.</span></h2>
            <p class="tagline-desc">Join a community of writers sharing ideas that matter. Every post starts with a single sentence.</p>
          </div>

          <div class="left-features">
            <div class="feature-item">
              <div class="feature-icon">
                <svg width="14" height="14" viewBox="0 0 16 16" fill="none">
                  <path d="M2 8l4 4 8-8" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </div>
              <span>Publish instantly, no approval needed</span>
            </div>
            <div class="feature-item">
              <div class="feature-icon">
                <svg width="14" height="14" viewBox="0 0 16 16" fill="none">
                  <path d="M2 8l4 4 8-8" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </div>
              <span>AI-powered summaries for every post</span>
            </div>
            <div class="feature-item">
              <div class="feature-icon">
                <svg width="14" height="14" viewBox="0 0 16 16" fill="none">
                  <path d="M2 8l4 4 8-8" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </div>
              <span>Full editorial control, always</span>
            </div>
          </div>

          <!-- Decorative card stack -->
          <div class="card-stack">
            <div class="stack-card stack-card-3"></div>
            <div class="stack-card stack-card-2"></div>
            <div class="stack-card stack-card-1">
              <div class="stack-avatar"></div>
              <div class="stack-lines">
                <div class="stack-line stack-line-long"></div>
                <div class="stack-line stack-line-short"></div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Right Panel — Form -->
      <div class="auth-right">
        <div class="auth-card">

          <!-- Card header -->
          <div class="card-header">
            <div class="auth-eyebrow">
              <span class="eyebrow-dot"></span>
              Welcome back
            </div>
            <h1 class="auth-title">Sign in</h1>
            <p class="auth-subtitle">Continue your writing journey.</p>
          </div>

          <!-- Error card -->
          <div v-if="errorMessage" class="error-card" role="alert">
            <div class="error-icon">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" aria-hidden="true">
                <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2"/>
                <path d="M12 7v6M12 16.5h.01" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/>
              </svg>
            </div>
            <div class="error-content">
              <span class="error-title">Authentication Failed</span>
              <span class="error-message">{{ errorMessage }}</span>
            </div>
          </div>

          <!-- Form -->
          <form class="auth-form" @submit.prevent="handleSubmit" novalidate>

            <div class="field">
              <label for="email" class="field-label">Email address</label>
              <div class="field-wrap">
                <div class="field-icon">
                  <svg width="15" height="15" viewBox="0 0 16 16" fill="none" aria-hidden="true">
                    <rect x="1" y="3" width="14" height="10" rx="2" stroke="currentColor" stroke-width="1.4"/>
                    <path d="M1 6l7 4 7-4" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round"/>
                  </svg>
                </div>
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
            </div>

            <div class="field">
              <label for="password" class="field-label">Password</label>
              <div class="field-wrap">
                <div class="field-icon">
                  <svg width="15" height="15" viewBox="0 0 16 16" fill="none" aria-hidden="true">
                    <rect x="3" y="7" width="10" height="7" rx="1.5" stroke="currentColor" stroke-width="1.4"/>
                    <path d="M5 7V5a3 3 0 0 1 6 0v2" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/>
                  </svg>
                </div>
                <input
                  id="password"
                  v-model="credentials.password"
                  :type="showPassword ? 'text' : 'password'"
                  name="password"
                  autocomplete="current-password"
                  placeholder="••••••••"
                  required
                  class="field-input"
                />
                <button type="button" class="toggle-pw" @click="showPassword = !showPassword" :aria-label="showPassword ? 'Hide password' : 'Show password'">
                  <svg v-if="!showPassword" width="15" height="15" viewBox="0 0 16 16" fill="none">
                    <path d="M1 8s2.5-5 7-5 7 5 7 5-2.5 5-7 5-7-5-7-5Z" stroke="currentColor" stroke-width="1.4"/>
                    <circle cx="8" cy="8" r="2" stroke="currentColor" stroke-width="1.4"/>
                  </svg>
                  <svg v-else width="15" height="15" viewBox="0 0 16 16" fill="none">
                    <path d="M2 2l12 12M6.5 6.7A2 2 0 0 0 9.3 9.5M4 4.4C2.4 5.5 1 8 1 8s2.5 5 7 5c1.2 0 2.3-.3 3.3-.8M7 3.1C7.3 3 7.7 3 8 3c4.5 0 7 5 7 5s-.6 1.2-1.7 2.4" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/>
                  </svg>
                </button>
              </div>
            </div>

            <button
              type="submit"
              class="btn-submit"
              :disabled="isSubmitting || !credentials.email || !credentials.password"
              :aria-busy="isSubmitting"
            >
              <span class="btn-shimmer"></span>
              <svg v-if="isSubmitting" class="spinner" width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true">
                <circle cx="8" cy="8" r="6" stroke="currentColor" stroke-width="2" stroke-dasharray="28" stroke-dashoffset="14" stroke-linecap="round"/>
              </svg>
              <span>{{ isSubmitting ? 'Signing in…' : 'Sign in to Signal' }}</span>
              <svg v-if="!isSubmitting" width="14" height="14" viewBox="0 0 14 14" fill="none" aria-hidden="true">
                <path d="M3 7h8M8 4l3 3-3 3" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </button>

          </form>

          <!-- Divider -->
          <div class="divider" aria-hidden="true">
            <span class="divider-line"></span>
            <span class="divider-text">New here?</span>
            <span class="divider-line"></span>
          </div>

          <p class="auth-switch">
            <NuxtLink to="/signup" class="btn-switch">Create your account →</NuxtLink>
          </p>

        </div>
      </div>
    </main>

  </div>
</template>

<style scoped>
/* ── Page & Background ── */
.auth-page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  position: relative;
  overflow: hidden;
}

.bg-canvas {
  position: fixed;
  inset: 0;
  z-index: 0;
  pointer-events: none;
}

.bg-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.4;
}
.bg-orb-1 {
  width: 500px; height: 500px;
  background: radial-gradient(circle, rgba(124,92,252,0.3) 0%, transparent 70%);
  top: -150px; left: -100px;
  animation: orb-float-1 12s ease-in-out infinite;
}
.bg-orb-2 {
  width: 400px; height: 400px;
  background: radial-gradient(circle, rgba(99,102,241,0.2) 0%, transparent 70%);
  bottom: -100px; right: -80px;
  animation: orb-float-2 15s ease-in-out infinite;
}
.bg-orb-3 {
  width: 300px; height: 300px;
  background: radial-gradient(circle, rgba(167,139,250,0.15) 0%, transparent 70%);
  top: 50%; left: 50%;
  transform: translate(-50%, -50%);
  animation: orb-float-3 18s ease-in-out infinite;
}
.bg-grid {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(255,255,255,0.015) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,0.015) 1px, transparent 1px);
  background-size: 60px 60px;
}

@keyframes orb-float-1 {
  0%, 100% { transform: translate(0, 0) scale(1); }
  33% { transform: translate(40px, 30px) scale(1.05); }
  66% { transform: translate(-20px, 50px) scale(0.95); }
}
@keyframes orb-float-2 {
  0%, 100% { transform: translate(0, 0) scale(1); }
  50% { transform: translate(-30px, -40px) scale(1.08); }
}
@keyframes orb-float-3 {
  0%, 100% { transform: translate(-50%, -50%) scale(1); opacity: 0.15; }
  50% { transform: translate(-50%, -50%) scale(1.3); opacity: 0.08; }
}

/* ── Topbar ── */
.topbar {
  height: var(--nav-h);
  border-bottom: 1px solid var(--border);
  background: rgba(13, 13, 16, 0.6);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  position: sticky;
  top: 0;
  z-index: 100;
}

.topbar-inner {
  max-width: var(--max-w-wide);
  margin: 0 auto;
  padding: 0 28px;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.brand {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  font-weight: 800;
  font-size: 16px;
  letter-spacing: -0.03em;
  color: var(--text-primary);
  transition: opacity var(--duration-fast);
  text-decoration: none;
}
.brand:hover { opacity: 0.8; }

.brand-icon {
  width: 30px;
  height: 30px;
  border-radius: 8px;
  background: linear-gradient(135deg, var(--accent), #a78bfa);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px var(--accent-glow);
}
.brand-name { color: var(--text-primary); }

.btn-back {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  font-weight: 600;
  color: var(--text-secondary);
  background: rgba(255,255,255,0.04);
  border: 1px solid var(--border);
  padding: 7px 16px;
  border-radius: var(--radius-full);
  transition: all var(--duration-fast);
  text-decoration: none;
}
.btn-back:hover {
  background: rgba(255,255,255,0.08);
  color: var(--text-primary);
  border-color: rgba(255,255,255,0.12);
}

/* ── Layout ── */
.auth-layout {
  flex: 1;
  display: grid;
  grid-template-columns: 1fr 1fr;
  position: relative;
  z-index: 1;
}

/* ── Left Panel ── */
.auth-left {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 60px 48px;
  border-right: 1px solid var(--border);
  position: relative;
  overflow: hidden;
}

.left-content {
  max-width: 400px;
  width: 100%;
}

.tagline-eyebrow {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: var(--accent);
  margin-bottom: 20px;
}
.eyebrow-dot {
  display: inline-block;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--accent);
  box-shadow: 0 0 8px var(--accent);
  animation: dot-pulse 2s ease-in-out infinite;
}
@keyframes dot-pulse {
  0%, 100% { box-shadow: 0 0 6px var(--accent); }
  50% { box-shadow: 0 0 14px var(--accent), 0 0 24px var(--accent-glow); }
}

.tagline-title {
  font-family: var(--font-serif);
  font-size: clamp(36px, 4vw, 52px);
  font-weight: 700;
  line-height: 1.1;
  letter-spacing: -0.03em;
  color: var(--text-primary);
  margin-bottom: 20px;
}
.tagline-accent {
  background: linear-gradient(135deg, var(--accent), #a78bfa, #60a5fa);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
.tagline-desc {
  font-size: 15px;
  color: var(--text-secondary);
  line-height: 1.7;
  margin-bottom: 36px;
  max-width: 36ch;
}

.left-features {
  display: flex;
  flex-direction: column;
  gap: 14px;
  margin-bottom: 48px;
}
.feature-item {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 14px;
  color: var(--text-secondary);
}
.feature-icon {
  width: 24px;
  height: 24px;
  border-radius: 6px;
  background: var(--accent-subtle);
  border: 1px solid rgba(124,92,252,0.25);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--accent);
  flex-shrink: 0;
}

/* ── Decorative card stack ── */
.card-stack {
  position: relative;
  height: 90px;
}
.stack-card {
  position: absolute;
  border-radius: 12px;
  border: 1px solid var(--border);
}
.stack-card-3 {
  bottom: 0; left: 20px;
  width: 280px; height: 64px;
  background: var(--bg-elevated);
  transform: rotate(-3deg);
  opacity: 0.3;
}
.stack-card-2 {
  bottom: 6px; left: 10px;
  width: 280px; height: 64px;
  background: var(--bg-surface);
  transform: rotate(-1.5deg);
  opacity: 0.6;
}
.stack-card-1 {
  bottom: 12px; left: 0;
  width: 280px; height: 64px;
  background: var(--bg-elevated);
  border-color: rgba(124,92,252,0.2);
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 0 16px;
}
.stack-avatar {
  width: 34px; height: 34px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--accent), #a78bfa);
  flex-shrink: 0;
}
.stack-lines {
  display: flex;
  flex-direction: column;
  gap: 8px;
  flex: 1;
}
.stack-line {
  height: 8px;
  border-radius: 4px;
  background: var(--bg-overlay);
}
.stack-line-long { width: 80%; }
.stack-line-short { width: 50%; }

/* ── Right Panel ── */
.auth-right {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 60px 48px;
}

.auth-card {
  width: 100%;
  max-width: 420px;
  animation: fadeUp var(--duration-slow) var(--ease-out) both;
}

.card-header {
  margin-bottom: 32px;
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
  margin-bottom: 12px;
}

.auth-title {
  font-family: var(--font-serif);
  font-size: clamp(28px, 4vw, 36px);
  font-weight: 700;
  letter-spacing: -0.02em;
  color: var(--text-primary);
  margin-bottom: 8px;
  line-height: 1.1;
}

.auth-subtitle {
  font-size: 15px;
  color: var(--text-secondary);
  line-height: 1.6;
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

/* ── Form ── */
.auth-form {
  display: flex;
  flex-direction: column;
  gap: 18px;
  margin-bottom: 28px;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 7px;
}

.field-label {
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--text-tertiary);
  transition: color var(--duration-fast);
}
.field:focus-within .field-label {
  color: var(--accent);
}

.field-wrap {
  position: relative;
  display: flex;
  align-items: center;
}

.field-icon {
  position: absolute;
  left: 14px;
  color: var(--text-tertiary);
  display: flex;
  align-items: center;
  justify-content: center;
  pointer-events: none;
  transition: color var(--duration-fast);
}
.field:focus-within .field-icon {
  color: var(--accent);
}

.field-input {
  font-family: var(--font-sans);
  font-size: 14.5px;
  padding: 13px 44px 13px 42px;
  background: rgba(255,255,255,0.03);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  color: var(--text-primary);
  transition: border-color var(--duration-fast), box-shadow var(--duration-fast), background var(--duration-fast);
  width: 100%;
  -webkit-appearance: none;
}
.field-input::placeholder { color: var(--text-tertiary); }
.field-input:hover { border-color: rgba(255,255,255,0.1); background: rgba(255,255,255,0.04); }
.field-input:focus {
  outline: none;
  border-color: var(--accent);
  background: rgba(124,92,252,0.05);
  box-shadow: 0 0 0 3px var(--accent-glow), 0 1px 6px rgba(0,0,0,0.2);
}

.toggle-pw {
  position: absolute;
  right: 12px;
  background: none;
  border: none;
  cursor: pointer;
  color: var(--text-tertiary);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 4px;
  border-radius: 4px;
  transition: color var(--duration-fast), background var(--duration-fast);
}
.toggle-pw:hover { color: var(--text-primary); background: rgba(255,255,255,0.06); }

/* ── Submit Button ── */
.btn-submit {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  margin-top: 6px;
  padding: 14px 22px;
  background: linear-gradient(135deg, var(--accent) 0%, #6366f1 100%);
  color: white;
  font-size: 14px;
  font-weight: 700;
  border: none;
  border-radius: var(--radius-md);
  cursor: pointer;
  letter-spacing: 0.02em;
  overflow: hidden;
  transition: transform var(--duration-fast), box-shadow var(--duration-fast), opacity var(--duration-fast);
  width: 100%;
}
.btn-shimmer {
  position: absolute;
  inset: 0;
  background: linear-gradient(105deg, transparent 40%, rgba(255,255,255,0.15) 50%, transparent 60%);
  background-size: 200% 100%;
  animation: shimmer-btn 3s ease-in-out infinite;
}
@keyframes shimmer-btn {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
.btn-submit:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 8px 30px var(--accent-glow), 0 4px 12px rgba(0,0,0,0.3);
}
.btn-submit:active:not(:disabled) { transform: translateY(0); }
.btn-submit:disabled { opacity: 0.45; cursor: not-allowed; }

.spinner { animation: spin 0.7s linear infinite; flex-shrink: 0; }

/* ── Divider ── */
.divider {
  display: flex;
  align-items: center;
  gap: 14px;
  margin-bottom: 20px;
}
.divider-line {
  flex: 1;
  height: 1px;
  background: var(--border);
}
.divider-text {
  font-size: 12px;
  color: var(--text-tertiary);
  white-space: nowrap;
  font-weight: 500;
}

/* ── Switch ── */
.auth-switch {
  text-align: center;
}
.btn-switch {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  padding: 12px 22px;
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
  background: rgba(255,255,255,0.04);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  transition: all var(--duration-fast);
  text-decoration: none;
}
.btn-switch:hover {
  background: rgba(255,255,255,0.07);
  border-color: rgba(255,255,255,0.12);
  color: var(--accent);
}

/* ── Responsive ── */
@media (max-width: 900px) {
  .auth-left { display: none; }
  .auth-layout { grid-template-columns: 1fr; }
}
@media (max-width: 640px) {
  .topbar { padding: 0 18px; }
  .auth-right { padding: 40px 24px; }
}
</style>
