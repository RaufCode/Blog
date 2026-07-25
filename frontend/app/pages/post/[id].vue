<script setup>
definePageMeta({
  validate (route) {
    // Check if the id is made up of digits
    return typeof route.params.id === 'string' && /^\d+$/.test(route.params.id)
  },
})
const route = useRoute()
const { data: post, pending, error } = await usePost(route.params.id)

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
        <NuxtLink to="/" class="brand">
            <span class="brand-mark"><span class="brand-dot"></span></span>
            <span class="brand-name">Signal</span>
        </NuxtLink>

        <p v-if="pending" class="state-message">Loading…</p>
        <p v-else-if="error" class="state-message state-message--error">Couldn't load this post.</p>
        <article v-else-if="post" class="post">
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

.brand {
    display: inline-flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 40px;
    color: inherit;
    text-decoration: none;
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

@media (max-width: 480px) {
    .page {
        padding: 40px 16px 72px;
    }
}
</style>
