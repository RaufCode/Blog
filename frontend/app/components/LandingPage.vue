<script setup>
const { data: posts, error, pending, refresh } = await usePosts()
const { user, isAuthenticated, logout } = useAuth()

const isAccountMenuOpen = ref(false)

function initialsFor(firstName, lastName) {
  return `${firstName?.[0] ?? ''}${lastName?.[0] ?? ''}`.toUpperCase() || '?'
}

async function handleLogout() {
  isAccountMenuOpen.value = false
  await logout()
  await navigateTo('/')
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

function excerpt(content, maxLen = 160) {
  const stripped = (content || '').replace(/\s+/g, ' ').trim()
  return stripped.length > maxLen ? stripped.slice(0, maxLen).trimEnd() + '…' : stripped
}

// Sticky nav scroll behavior
const scrolled = ref(false)
if (import.meta.client) {
  window.addEventListener('scroll', () => {
    scrolled.value = window.scrollY > 20
  }, { passive: true })
}
</script>

<template>
  <div class="page">

    <!-- ── Navbar ── -->
    <header class="nav" :class="{ 'nav--scrolled': scrolled }">
      <div class="nav-inner">
        <NuxtLink to="/" class="brand">
          <span class="brand-icon" aria-hidden="true">
            <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
              <rect width="18" height="18" rx="5" fill="var(--accent)"/>
              <path d="M5 9h8M5 6h5M5 12h6" stroke="white" stroke-width="1.6" stroke-linecap="round"/>
            </svg>
          </span>
          <span class="brand-name">Signal</span>
        </NuxtLink>

        <nav class="nav-links" aria-label="Site navigation">
          <span class="nav-badge">{{ posts?.length ?? 0 }} posts</span>
          <NuxtLink to="/new" class="btn-nav">
            <svg width="14" height="14" viewBox="0 0 14 14" fill="none" aria-hidden="true">
              <path d="M7 1v12M1 7h12" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>
            </svg>
            Write
          </NuxtLink>

          <template v-if="isAuthenticated">
            <div class="account-menu">
              <button
                class="account-trigger"
                type="button"
                @click="isAccountMenuOpen = !isAccountMenuOpen"
                :aria-expanded="isAccountMenuOpen"
              >
                <span class="account-avatar" aria-hidden="true">
                  {{ initialsFor(user.first_name, user.last_name) }}
                </span>
              </button>

              <div v-if="isAccountMenuOpen" class="account-dropdown" @mouseleave="isAccountMenuOpen = false">
                <p class="account-name">{{ user.first_name }} {{ user.last_name }}</p>
                <p class="account-email">{{ user.email }}</p>
                <button class="account-logout" type="button" @click="handleLogout">Sign out</button>
              </div>
            </div>
          </template>
          <template v-else>
            <NuxtLink to="/login" class="btn-nav-ghost">Sign in</NuxtLink>
          </template>
        </nav>
      </div>
    </header>

    <!-- ── Hero ── -->
    <section class="hero">
      <div class="hero-glow" aria-hidden="true"></div>
      <div class="hero-content">
        <div class="hero-eyebrow">
          <span class="eyebrow-dot" aria-hidden="true"></span>
          Engineering · Product · Career
        </div>
        <h1 class="hero-title">Notes on building<br><em>great software</em></h1>
        <p class="hero-subtitle">
          A curated collection of essays, learnings, and ideas from the intersection of engineering, product thinking, and the human side of building things.
        </p>
        <NuxtLink to="/new" class="btn-hero">
          Start writing
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true">
            <path d="M3 8h10M9 4l4 4-4 4" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </NuxtLink>
      </div>
    </section>

    <!-- ── Posts Feed ── -->
    <main class="feed-section">
      <div class="feed-header">
        <h2 class="feed-title">Latest posts</h2>
        <button v-if="!pending && !error" class="btn-refresh" @click="refresh" title="Refresh posts" aria-label="Refresh posts">
          <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
            <path d="M13 2.5v4h-4" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M1.5 7A5.5 5.5 0 0 1 12.5 4.5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>
            <path d="M1 11.5v-4h4" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M12.5 7A5.5 5.5 0 0 1 1.5 9.5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>
          </svg>
        </button>
      </div>

      <!-- Loading skeleton -->
      <div v-if="pending" class="skeleton-list" aria-label="Loading posts" aria-busy="true">
        <div v-for="n in 4" :key="n" class="skeleton-card">
          <div class="skeleton-title"></div>
          <div class="skeleton-meta"></div>
          <div class="skeleton-body"></div>
          <div class="skeleton-body short"></div>
        </div>
      </div>

      <!-- Error -->
      <div v-else-if="error" class="error-card" role="alert">
        <div class="error-icon">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" aria-hidden="true">
            <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2"/>
            <path d="M12 7v6M12 16.5h.01" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/>
          </svg>
        </div>
        <div class="error-content">
          <span class="error-title">Couldn't load posts</span>
          <span class="error-message">Something went wrong. <button class="inline-link" @click="refresh">Try again</button></span>
        </div>
      </div>

      <!-- Empty -->
      <div v-else-if="!posts?.length" class="state-empty">
        <div class="state-empty-icon" aria-hidden="true">
          <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
            <rect x="4" y="6" width="24" height="20" rx="4" stroke="currentColor" stroke-width="1.5"/>
            <path d="M10 12h12M10 16h8M10 20h6" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
          </svg>
        </div>
        <p class="state-empty-title">No posts yet</p>
        <p class="state-empty-body">Be the first to share what you've learned or built.</p>
        <NuxtLink to="/new" class="btn-primary">Write the first post</NuxtLink>
      </div>

      <!-- Post list -->
      <ol v-else class="post-list" role="list">
        <li v-for="(post, index) in posts" :key="post.id" class="post-item" :style="`--delay:${index * 60}ms`">
          <NuxtLink :to="`/post/${post.id}`" class="post-card" :aria-label="`Read: ${post.title}`">
            <div class="post-card-inner">
              <div class="post-top">
                <div class="post-meta">
                  <span class="avatar" :title="post.author || 'anonymous'" aria-hidden="true">{{ initials(post.author) }}</span>
                  <span class="meta-author">{{ post.author || 'anonymous' }}</span>
                  <span class="meta-dot" aria-hidden="true"></span>
                  <time class="meta-date" :datetime="post.created_at">{{ formatDate(post.created_at) }}</time>
                  <span class="meta-dot" aria-hidden="true"></span>
                  <span class="meta-read">{{ readTime(post.content) }}</span>
                </div>
                <span class="post-arrow" aria-hidden="true">
                  <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                    <path d="M3 8h10M9 4l4 4-4 4" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </span>
              </div>
              <h3 class="post-title">{{ post.title }}</h3>
              <p class="post-excerpt">{{ excerpt(post.content) }}</p>
            </div>
            <div class="post-card-glow" aria-hidden="true"></div>
          </NuxtLink>
        </li>
      </ol>
    </main>

    <!-- ── Footer ── -->
    <footer class="footer">
      <div class="footer-inner">
        <NuxtLink to="/" class="footer-brand">
          <span aria-hidden="true">
            <svg width="14" height="14" viewBox="0 0 18 18" fill="none">
              <rect width="18" height="18" rx="5" fill="var(--accent)"/>
              <path d="M5 9h8M5 6h5M5 12h6" stroke="white" stroke-width="1.6" stroke-linecap="round"/>
            </svg>
          </span>
          Signal
        </NuxtLink>
        <p class="footer-copy">Built to share ideas. Designed to be read.</p>
      </div>
    </footer>

  </div>
</template>

<style scoped>
/* ── Layout ────────────────────────────────────────────────── */
.page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* ── Navbar ────────────────────────────────────────────────── */
.nav {
  position: sticky;
  top: 0;
  z-index: 100;
  height: var(--nav-h);
  transition: background var(--duration-base) var(--ease-out),
              border-color var(--duration-base) var(--ease-out),
              box-shadow var(--duration-base) var(--ease-out);
  border-bottom: 1px solid transparent;
}

.nav--scrolled {
  background: rgba(13, 13, 16, 0.85);
  backdrop-filter: blur(16px) saturate(1.4);
  -webkit-backdrop-filter: blur(16px) saturate(1.4);
  border-color: var(--border);
  box-shadow: 0 1px 32px rgba(0,0,0,0.3);
}

.nav-inner {
  max-width: var(--max-w-wide);
  margin: 0 auto;
  padding: 0 24px;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
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

.brand-icon {
  display: flex;
  align-items: center;
  justify-content: center;
}

.brand-name { color: var(--text-primary); }

.nav-links {
  display: flex;
  align-items: center;
  gap: 12px;
}

.nav-badge {
  font-size: 12px;
  font-weight: 500;
  color: var(--text-tertiary);
  background: var(--bg-elevated);
  border: 1px solid var(--border);
  padding: 3px 10px;
  border-radius: var(--radius-full);
  letter-spacing: 0.01em;
}

.btn-nav {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  background: var(--accent);
  color: var(--accent-contrast);
  font-size: 13px;
  font-weight: 600;
  border-radius: var(--radius-full);
  transition: background var(--duration-fast), transform var(--duration-fast), box-shadow var(--duration-fast);
  letter-spacing: 0.01em;
}
.btn-nav:hover {
  background: var(--accent-hover);
  transform: translateY(-1px);
  box-shadow: 0 4px 16px var(--accent-glow);
}
.btn-nav:active { transform: translateY(0); }

.btn-nav-ghost {
  display: inline-flex;
  align-items: center;
  padding: 8px 16px;
  background: var(--bg-elevated);
  border: 1px solid var(--border);
  color: var(--text-secondary);
  font-size: 13px;
  font-weight: 600;
  border-radius: var(--radius-full);
  transition: background var(--duration-fast), color var(--duration-fast), border-color var(--duration-fast);
}
.btn-nav-ghost:hover {
  background: var(--bg-overlay);
  color: var(--text-primary);
  border-color: rgba(255,255,255,0.12);
}

.account-menu {
  position: relative;
}

.account-trigger {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
  background: none;
  border: none;
  cursor: pointer;
}

.account-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--accent) 0%, #a78bfa 100%);
  color: white;
  font-size: 12px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: box-shadow var(--duration-fast);
}
.account-trigger:hover .account-avatar,
.account-trigger[aria-expanded="true"] .account-avatar {
  box-shadow: 0 0 0 3px var(--accent-glow);
}

.account-dropdown {
  position: absolute;
  top: calc(100% + 10px);
  right: 0;
  min-width: 200px;
  background: var(--bg-elevated);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: 14px 16px;
  box-shadow: var(--shadow-md);
  z-index: 110;
  animation: fadeUp var(--duration-fast) var(--ease-out) both;
}

.account-name {
  font-size: 13px;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 2px;
}

.account-email {
  font-size: 12px;
  color: var(--text-tertiary);
  margin-bottom: 12px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.account-logout {
  width: 100%;
  text-align: left;
  padding: 8px 10px;
  margin: 0 -10px;
  background: none;
  border: none;
  border-radius: var(--radius-sm);
  color: var(--color-error);
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: background var(--duration-fast);
}
.account-logout:hover {
  background: rgba(240, 96, 96, 0.1);
}

/* ── Hero ──────────────────────────────────────────────────── */
.hero {
  position: relative;
  overflow: hidden;
  padding: 96px 24px 80px;
  text-align: center;
  animation: fadeUp var(--duration-slow) var(--ease-out) both;
}

.hero-glow {
  position: absolute;
  top: -120px;
  left: 50%;
  transform: translateX(-50%);
  width: 700px;
  height: 500px;
  background: radial-gradient(ellipse at center, rgba(124,92,252,0.18) 0%, transparent 70%);
  pointer-events: none;
  animation: fadeIn 1.2s ease both 0.2s;
}

.hero-content {
  position: relative;
  max-width: 640px;
  margin: 0 auto;
}

.hero-eyebrow {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: var(--accent);
  margin-bottom: 24px;
  animation: fadeUp var(--duration-slow) var(--ease-out) both 100ms;
}

.eyebrow-dot {
  display: inline-block;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--accent);
  animation: pulse-glow 2.5s ease-in-out infinite;
}

.hero-title {
  font-family: var(--font-serif);
  font-size: clamp(38px, 6vw, 64px);
  font-weight: 700;
  line-height: 1.1;
  letter-spacing: -0.02em;
  color: var(--text-primary);
  margin-bottom: 20px;
  animation: fadeUp var(--duration-slow) var(--ease-out) both 200ms;
}

.hero-title em {
  font-style: italic;
  background: linear-gradient(135deg, var(--accent) 0%, #a78bfa 50%, #c4b5fd 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-subtitle {
  font-size: 17px;
  line-height: 1.7;
  color: var(--text-secondary);
  max-width: 52ch;
  margin: 0 auto 36px;
  font-weight: 400;
  animation: fadeUp var(--duration-slow) var(--ease-out) both 300ms;
}

.btn-hero {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 13px 28px;
  background: var(--accent);
  color: var(--accent-contrast);
  font-size: 15px;
  font-weight: 700;
  border-radius: var(--radius-full);
  letter-spacing: 0.01em;
  transition: background var(--duration-fast), transform var(--duration-base) var(--ease-out), box-shadow var(--duration-base) var(--ease-out);
  animation: fadeUp var(--duration-slow) var(--ease-out) both 400ms;
}
.btn-hero:hover {
  background: var(--accent-hover);
  transform: translateY(-2px);
  box-shadow: 0 8px 32px var(--accent-glow);
}
.btn-hero:active { transform: translateY(0); }

/* ── Feed Section ──────────────────────────────────────────── */
.feed-section {
  flex: 1;
  max-width: var(--max-w-prose);
  width: 100%;
  margin: 0 auto;
  padding: 0 24px 80px;
}

.feed-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 32px;
  padding-bottom: 16px;
  border-bottom: 1px solid var(--border);
}

.feed-title {
  font-family: var(--font-sans);
  font-size: 13px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--text-tertiary);
}

.btn-refresh {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 30px;
  height: 30px;
  border-radius: var(--radius-md);
  background: var(--bg-elevated);
  border: 1px solid var(--border);
  color: var(--text-tertiary);
  cursor: pointer;
  transition: color var(--duration-fast), background var(--duration-fast), border-color var(--duration-fast);
}
.btn-refresh:hover {
  color: var(--text-primary);
  background: var(--bg-overlay);
  border-color: rgba(255,255,255,0.12);
}

/* ── Skeleton Loading ──────────────────────────────────────── */
.skeleton-list { display: flex; flex-direction: column; gap: 24px; }

.skeleton-card {
  padding: 28px;
  border-radius: var(--radius-lg);
  background: var(--bg-surface);
  border: 1px solid var(--border);
}

.skeleton-title,
.skeleton-meta,
.skeleton-body {
  border-radius: 6px;
  background: linear-gradient(90deg, var(--bg-elevated) 25%, var(--bg-overlay) 50%, var(--bg-elevated) 75%);
  background-size: 400px 100%;
  animation: shimmer 1.4s ease-in-out infinite;
}

.skeleton-title  { height: 24px; width: 70%; margin-bottom: 14px; }
.skeleton-meta   { height: 14px; width: 40%; margin-bottom: 18px; }
.skeleton-body   { height: 14px; width: 100%; margin-bottom: 8px; }
.skeleton-body.short { width: 60%; }

/* ── Error / Empty States ──────────────────────────────────── */
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

.inline-link {
  background: none;
  border: none;
  color: inherit;
  font: inherit;
  font-weight: 700;
  text-decoration: underline;
  cursor: pointer;
}

.state-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 64px 24px;
  gap: 12px;
}

.state-empty-icon {
  width: 56px;
  height: 56px;
  border-radius: var(--radius-lg);
  background: var(--bg-elevated);
  border: 1px solid var(--border);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-tertiary);
  margin-bottom: 8px;
}

.state-empty-title {
  font-size: 18px;
  font-weight: 700;
  color: var(--text-primary);
}

.state-empty-body {
  font-size: 14px;
  color: var(--text-secondary);
  max-width: 36ch;
  margin-bottom: 8px;
}

.btn-primary {
  display: inline-flex;
  align-items: center;
  padding: 10px 22px;
  background: var(--accent);
  color: var(--accent-contrast);
  font-size: 14px;
  font-weight: 700;
  border-radius: var(--radius-full);
  transition: background var(--duration-fast), transform var(--duration-fast), box-shadow var(--duration-fast);
}
.btn-primary:hover {
  background: var(--accent-hover);
  transform: translateY(-1px);
  box-shadow: 0 4px 16px var(--accent-glow);
}

/* ── Post List ─────────────────────────────────────────────── */
.post-list {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.post-item {
  animation: fadeUp var(--duration-slow) var(--ease-out) both var(--delay, 0ms);
}

.post-card {
  display: block;
  position: relative;
  overflow: hidden;
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  transition: border-color var(--duration-base) var(--ease-out),
              transform var(--duration-base) var(--ease-out),
              box-shadow var(--duration-base) var(--ease-out);
  cursor: pointer;
}

.post-card:hover {
  border-color: rgba(124, 92, 252, 0.35);
  transform: translateY(-3px);
  box-shadow: var(--shadow-lg), 0 0 0 1px var(--accent-subtle);
}

.post-card-glow {
  position: absolute;
  top: -60px;
  right: -60px;
  width: 180px;
  height: 180px;
  border-radius: 50%;
  background: radial-gradient(ellipse at center, var(--accent-glow) 0%, transparent 70%);
  opacity: 0;
  transition: opacity var(--duration-slow) var(--ease-out);
  pointer-events: none;
}
.post-card:hover .post-card-glow { opacity: 1; }

.post-card-inner {
  padding: 28px 28px 24px;
}

.post-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 14px;
}

.post-meta {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.avatar {
  width: 26px;
  height: 26px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--accent) 0%, #a78bfa 100%);
  color: white;
  font-size: 10px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  letter-spacing: 0;
}

.meta-author {
  font-size: 13px;
  font-weight: 600;
  color: var(--text-secondary);
  max-width: 140px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.meta-dot {
  width: 3px;
  height: 3px;
  border-radius: 50%;
  background: var(--text-tertiary);
  flex-shrink: 0;
}

.meta-date,
.meta-read {
  font-size: 12px;
  color: var(--text-tertiary);
  white-space: nowrap;
}

.post-arrow {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: var(--bg-elevated);
  color: var(--text-tertiary);
  flex-shrink: 0;
  transition: background var(--duration-fast), color var(--duration-fast), transform var(--duration-base) var(--ease-out);
}
.post-card:hover .post-arrow {
  background: var(--accent-subtle);
  color: var(--accent);
  transform: translateX(3px);
}

.post-title {
  font-family: var(--font-serif);
  font-size: clamp(18px, 3vw, 22px);
  font-weight: 700;
  line-height: 1.3;
  letter-spacing: -0.01em;
  color: var(--text-primary);
  margin-bottom: 10px;
  transition: color var(--duration-fast);
}
.post-card:hover .post-title { color: #c4b5fd; }

.post-excerpt {
  font-size: 14px;
  line-height: 1.7;
  color: var(--text-secondary);
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* ── Footer ────────────────────────────────────────────────── */
.footer {
  border-top: 1px solid var(--border);
  padding: 24px;
}

.footer-inner {
  max-width: var(--max-w-wide);
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  flex-wrap: wrap;
}

.footer-brand {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  font-weight: 700;
  color: var(--text-secondary);
  letter-spacing: -0.01em;
  transition: color var(--duration-fast);
}
.footer-brand:hover { color: var(--text-primary); }

.footer-copy {
  font-size: 12px;
  color: var(--text-tertiary);
}

/* ── Responsive ────────────────────────────────────────────── */
@media (max-width: 640px) {
  .hero { padding: 72px 20px 60px; }
  .hero-title { font-size: clamp(30px, 9vw, 44px); }
  .hero-subtitle { font-size: 15px; }
  .feed-section { padding: 0 16px 64px; }
  .post-card-inner { padding: 20px 20px 18px; }
  .nav-inner { padding: 0 16px; }
  .nav-badge { display: none; }
}
</style>
