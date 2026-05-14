<template>
  <div class="login-page">
    <div class="login-left">
      <div class="login-left-content">
        <div class="brand">
          <div class="brand-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m18 16 4-4-4-4"/><path d="m6 8-4 4 4 4"/><path d="m14.5 4-5 16"/></svg>
          </div>
          <span class="brand-text">PyInterview</span>
        </div>
        <h1 class="hero-title">掌握 Python 面试<br /><span class="hero-highlight">从这里开始</span></h1>
        <p class="hero-desc">AI 驱动的在线答题系统，智能出题、自动评判，助你轻松备战技术面试。</p>
        <div class="hero-features">
          <div class="feature-item">
            <div class="feature-icon">
              <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22c5.523 0 10-4.477 10-10S17.523 2 12 2 2 6.477 2 12s4.477 10 10 10z"/><path d="m9 12 2 2 4-4"/></svg>
            </div>
            <span>AI 智能生成面试题目</span>
          </div>
          <div class="feature-item">
            <div class="feature-icon">
              <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22c5.523 0 10-4.477 10-10S17.523 2 12 2 2 6.477 2 12s4.477 10 10 10z"/><path d="m9 12 2 2 4-4"/></svg>
            </div>
            <span>自动评判 &amp; 详细反馈</span>
          </div>
          <div class="feature-item">
            <div class="feature-icon">
              <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22c5.523 0 10-4.477 10-10S17.523 2 12 2 2 6.477 2 12s4.477 10 10 10z"/><path d="m9 12 2 2 4-4"/></svg>
            </div>
            <span>多题型覆盖，全面练习</span>
          </div>
        </div>
      </div>
      <div class="login-left-decoration">
        <div class="deco-circle deco-circle-1"></div>
        <div class="deco-circle deco-circle-2"></div>
      </div>
    </div>

    <div class="login-right">
      <div class="login-form-wrapper">
        <div class="form-header">
          <h2 class="form-title">欢迎回来</h2>
          <p class="form-subtitle">登录你的账号继续学习</p>
        </div>
        <n-form ref="formRef" :model="formValue" :rules="rules" size="large" class="login-form">
          <n-form-item path="username" :show-label="false">
            <n-input
              v-model:value="formValue.username"
              placeholder="请输入用户名"
              :input-props="{ autocomplete: 'username' }"
            >
              <template #prefix>
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="var(--text-tertiary)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
              </template>
            </n-input>
          </n-form-item>
          <n-form-item path="password" :show-label="false">
            <n-input
              v-model:value="formValue.password"
              type="password"
              show-password-on="mousedown"
              placeholder="请输入密码"
              :input-props="{ autocomplete: 'current-password' }"
              @keyup.enter="handleLogin"
            >
              <template #prefix>
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="var(--text-tertiary)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="11" x="3" y="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
              </template>
            </n-input>
          </n-form-item>
          <n-button
            type="primary"
            block
            :loading="loading"
            @click="handleLogin"
            class="login-btn"
          >
            登 录
          </n-button>
        </n-form>
        <div class="form-footer">
          <span style="color: var(--text-tertiary);">还没有账号？</span>
          <router-link to="/register" class="register-link">立即注册</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue"
import { useRouter } from "vue-router"
import { useAuthStore } from "@/stores/auth"
import { useMessage } from "naive-ui"
import type { FormInst } from "naive-ui"

const router = useRouter()
const authStore = useAuthStore()
const message = useMessage()

const formRef = ref<FormInst | null>(null)
const loading = ref(false)
const formValue = ref({
  username: "",
  password: ""
})

const rules = {
  username: { required: true, message: "请输入用户名", trigger: "blur" },
  password: { required: true, message: "请输入密码", trigger: "blur" }
}

const handleLogin = async () => {
  formRef.value?.validate(async (errors) => {
    if (!errors) {
      loading.value = true
      try {
        await authStore.login(formValue.value)
        message.success("登录成功")
        router.push("/")
      } catch (e) {
        console.error(e)
      } finally {
        loading.value = false
      }
    }
  })
}
</script>

<style scoped>
.login-page {
  display: flex;
  height: 100vh;
  width: 100vw;
  overflow: hidden;
}

.login-left {
  position: relative;
  flex: 1;
  background: var(--bg);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  padding: 3rem;
}

.login-left-content {
  position: relative;
  z-index: 2;
  max-width: 480px;
}

.brand {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 2.5rem;
}

.brand-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 44px;
  height: 44px;
  background: var(--accent-subtle);
  border: 1px solid var(--border);
  border-radius: 12px;
  color: var(--accent);
}

.brand-text {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--text);
  letter-spacing: -0.02em;
}

.hero-title {
  font-size: 2.75rem;
  font-weight: 800;
  line-height: 1.2;
  color: var(--text);
  letter-spacing: -0.03em;
  margin-bottom: 1.25rem;
}

.hero-highlight {
  color: var(--accent);
}

.hero-desc {
  font-size: 1.05rem;
  line-height: 1.7;
  color: var(--text-secondary);
  margin-bottom: 2.5rem;
}

.hero-features {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: 12px;
  color: var(--text-secondary);
  font-size: 0.95rem;
}

.feature-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  background: var(--accent-subtle);
  border-radius: 8px;
  color: var(--accent);
  flex-shrink: 0;
}

.login-left-decoration {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.deco-circle {
  position: absolute;
  border-radius: 50%;
}

.deco-circle-1 {
  width: 500px;
  height: 500px;
  top: -100px;
  right: -150px;
  background: radial-gradient(circle, rgba(var(--accent-rgb), 0.06) 0%, transparent 70%);
}

.deco-circle-2 {
  width: 300px;
  height: 300px;
  bottom: -50px;
  left: -80px;
  background: radial-gradient(circle, rgba(var(--accent-secondary-rgb, 167, 139, 250), 0.06) 0%, transparent 70%);
}

.login-right {
  width: 480px;
  min-width: 420px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 3rem;
  background: var(--bg-elevated);
  border-left: 1px solid var(--border);
}

.login-form-wrapper {
  width: 100%;
  max-width: 360px;
}

.form-header {
  margin-bottom: 2rem;
}

.form-title {
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--text);
  letter-spacing: -0.02em;
  margin-bottom: 0.5rem;
}

.form-subtitle {
  font-size: 0.95rem;
  color: var(--text-tertiary);
}

.login-form :deep(.n-input) {
  border-radius: 8px;
  --n-color: #FFFFFF !important;
  --n-color-focus: #FFFFFF !important;
  --n-text-color: #0D1117 !important;
  --n-caret-color: #0D1117 !important;
  --n-placeholder-color: #9CA3AF !important;
}

.login-form :deep(.n-input .n-input__input-el) {
  height: 48px;
}

.login-form :deep(.n-input .n-input-wrapper) {
  padding: 0 14px;
}

.login-btn {
  height: 48px !important;
  border-radius: 8px !important;
  font-size: 1rem !important;
  font-weight: 600 !important;
  margin-top: 8px;
  transition: all 0.15s ease;
}

.login-btn:hover {
  transform: translateY(-1px);
}

.form-footer {
  text-align: center;
  margin-top: 1.75rem;
  font-size: 0.9rem;
}

.register-link {
  color: var(--accent);
  font-weight: 600;
  text-decoration: none;
  margin-left: 4px;
  transition: color 0.15s;
}

.register-link:hover {
  color: var(--accent-hover);
}

@media (max-width: 900px) {
  .login-left {
    display: none;
  }
  .login-right {
    width: 100%;
    min-width: unset;
    border-left: none;
  }
}
</style>
