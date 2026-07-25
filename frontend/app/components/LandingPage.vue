<script setup>
const {data: posts, error, pending, status, refresh} = await usePosts()

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
</script>

<template>
    <div class="page">
        <header class="brand">
            <span class="brand-mark"><span class="brand-dot"></span></span>
            <span class="brand-name">Signal</span>
        </header>

        <h1 class="page-title">Notes on building software</h1>
        <p class="page-subtitle">A compiled reading of every post on Signal — engineering, product and career writing.</p>

        <p v-if="pending" class="state-message">Loading posts…</p>
        <p v-else-if="error" class="state-message state-message--error">Couldn't load posts. Please try again later.</p>
        <p v-else-if="!posts || !posts.length" class="state-message">No posts yet.</p>
        <template v-else>
            <NuxtLink v-for="post in posts" :key="post.id" :to="`/post/${post.id}`" class="post">
                <h2 class="post-title">{{ post.title }}</h2>
                <div class="post-meta">
                    <span class="avatar">{{ initials(post.author) }}</span>
                    <span class="author">{{ post.author || "anonymous" }}</span>
                    <span class="meta-sep">·</span>
                    <span class="date">{{ formatDate(post.created_at) }}</span>
                    <span class="meta-sep">·</span>
                    <span class="read-time">{{ readTime(post.content) }}</span>
                </div>
                <p class="post-body">{{ post.content }}</p>
            </NuxtLink>
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

.brand {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 20px;
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

.page-title {
    font-family: var(--font-serif);
    font-size: clamp(26px, 5vw, 34px);
    font-weight: 600;
    margin: 0 0 6px 0;
    letter-spacing: -0.01em;
}

.page-subtitle {
    font-size: 15px;
    line-height: 1.65;
    color: var(--color-text-muted);
    max-width: 58ch;
    margin: 0 0 44px 0;
}

.state-message {
    font-size: 15px;
    color: var(--color-text-muted);
}

.state-message--error {
    color: var(--color-error);
}

.post {
    display: block;
    padding-top: 36px;
    margin-top: 36px;
    border-top: 1px solid var(--color-border);
    color: inherit;
    text-decoration: none;
}

.post:first-of-type {
    padding-top: 0;
    margin-top: 0;
    border-top: none;
}

.post:hover .post-title {
    color: var(--color-accent);
}

.post-title {
    font-family: var(--font-serif);
    font-size: clamp(20px, 4vw, 26px);
    font-weight: 700;
    line-height: 1.2;
    margin: 0 0 14px 0;
    letter-spacing: -0.01em;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

.post-meta {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 22px;
    padding-bottom: 18px;
    border-bottom: 1px solid var(--color-border);
    flex-wrap: wrap;
}

.avatar {
    width: 24px;
    height: 24px;
    border-radius: 50%;
    background: var(--color-accent);
    color: white;
    font-size: 10px;
    font-weight: 700;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}

.author {
    font-size: 13px;
    font-weight: 600;
    max-width: 160px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.meta-sep,
.date,
.read-time {
    font-size: 13px;
    color: var(--color-text-faint);
}

.post-body {
    font-size: 15px;
    line-height: 1.8;
    color: var(--color-body);
    max-width: 66ch;
    white-space: pre-wrap;
    margin: 0;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

@media (max-width: 480px) {
    .page {
        padding: 40px 16px 72px;
    }
}
</style>
