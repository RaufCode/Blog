<script setup>
const { user, isAuthenticated, logout } = useAuth()
const route = useRoute()

const isAccountMenuOpen = ref(false)
const showWriteLink = computed(() => route.path !== '/new')

function initialsFor(firstName, lastName) {
  return `${firstName?.[0] ?? ''}${lastName?.[0] ?? ''}`.toUpperCase() || '?'
}

async function handleLogout() {
  isAccountMenuOpen.value = false
  await logout()
  await navigateTo('/')
}

const scrolled = ref(false)
if (import.meta.client) {
  window.addEventListener('scroll', () => {
    scrolled.value = window.scrollY > 20
  }, { passive: true })
}
</script>

<template>
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
        <slot name="actions" />

        <NuxtLink
          v-if="showWriteLink"
          to="/new"
          class="icon-btn icon-btn-accent"
          title="Write a new post"
          aria-label="Write a new post"
        >
          <svg width="15" height="15" viewBox="0 0 14 14" fill="none" aria-hidden="true">
            <path d="M7 1v12M1 7h12" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>
          </svg>
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
</template>

<style scoped>
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

.icon-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 34px;
  height: 34px;
  flex-shrink: 0;
  border-radius: 50%;
  border: 1px solid var(--border);
  background: var(--bg-elevated);
  color: var(--text-secondary);
  cursor: pointer;
  transition: background var(--duration-fast), color var(--duration-fast), border-color var(--duration-fast), transform var(--duration-fast), box-shadow var(--duration-fast);
}
.icon-btn:hover {
  background: var(--bg-overlay);
  color: var(--text-primary);
  border-color: rgba(255,255,255,0.12);
}
.icon-btn:active { transform: translateY(0); }

.icon-btn-accent {
  background: var(--accent);
  border-color: transparent;
  color: var(--accent-contrast);
}
.icon-btn-accent:hover {
  background: var(--accent-hover);
  color: var(--accent-contrast);
  border-color: transparent;
  transform: translateY(-1px);
  box-shadow: 0 4px 16px var(--accent-glow);
}
.icon-btn-accent:active { transform: translateY(0); }

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
  white-space: nowrap;
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
  flex-shrink: 0;
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

@media (max-width: 640px) {
  .nav-inner { padding: 0 16px; }
}
</style>
