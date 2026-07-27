<script setup>

const blog_info = reactive({
    title: "",
    author: "",
    content: "",
})

// new.vue
const blog_post = async () => {
  try {
    await useCreate(blog_info)
    await navigateTo('/')
  } catch (error) {

  }
}

</script>

<template>
    <div class="page">
        <NuxtLink to="/" class="brand">
            <span class="brand-mark"><span class="brand-dot"></span></span>
            <span class="brand-name">Signal</span>
        </NuxtLink>

        <h1 class="page-title">New post</h1>
        <p class="page-subtitle">Share something you have learned or built.</p>

        <form class="post-form" @submit.prevent="blog_post">
            <div class="field">
                <label for="title">Title</label>
                <input v-model="blog_info.title" id="title" name="title" type="text" placeholder="Give your post a title" required />
            </div>

            <div class="field">
                <label for="author">Author</label>
                <input v-model="blog_info.author" id="author" name="author" type="text" placeholder="Your name (optional)" />
            </div>

            <div class="field">
                <label for="content">Content</label>
                <textarea v-model="blog_info.content" id="content" name="content" rows="10" placeholder="Write your post…" required></textarea>
            </div>

            <div class="form-actions">
                <NuxtLink to="/" class="btn btn-secondary">Cancel</NuxtLink>
                <button type="submit" class="btn btn-primary">Publish</button>
            </div>
        </form>
    </div>
</template>

<style scoped>
.page {
    max-width: 720px;
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

.page-title {
    font-family: var(--font-serif);
    font-size: clamp(26px, 5vw, 34px);
    font-weight: 600;
    margin: 0 0 6px 0;
    letter-spacing: -0.01em;
}

.page-subtitle {
    font-size: 15px;
    color: var(--color-text-muted);
    margin: 0 0 40px 0;
}

.post-form {
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
    resize: none;
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
    margin-top: 8px;
}

.btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 10px 20px;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 600;
    text-decoration: none;
    border: 1px solid transparent;
    cursor: pointer;
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

@media (max-width: 480px) {
    .page {
        padding: 40px 16px 72px;
    }

    .form-actions {
        flex-direction: column-reverse;
    }

    .btn {
        width: 100%;
    }
}
</style>
