<template>
  <div class="login-page">
    <div class="login-left">
      <div class="login-left-content">
        <div class="brand">
          <div class="brand-icon"><CodeIcon class="w-7 h-7" /></div>
          <span class="brand-text">PyInterview</span>
        </div>
        <h1 class="hero-title">加入我们<br /><span class="hero-highlight">开启练习之旅</span></h1>
        <p class="hero-desc">注册账号，即刻体验 AI 出题与智能评判，全方位提升面试能力。</p>
        <div class="hero-stats">
          <div class="stat-item"><span class="stat-number">1000+</span><span class="stat-label">精选题目</span></div>
          <div class="stat-divider"></div>
          <div class="stat-item"><span class="stat-number">4 种</span><span class="stat-label">题目类型</span></div>
          <div class="stat-divider"></div>
          <div class="stat-item"><span class="stat-number">AI</span><span class="stat-label">智能评判</span></div>
        </div>
      </div>
      <div class="login-left-decoration"><div class="deco-circle deco-circle-1"></div><div class="deco-circle deco-circle-2"></div></div>
    </div>

    <div class="login-right">
      <div class="login-form-wrapper">
        <div class="form-header">
          <h2 class="form-title">创建账号</h2>
          <p class="form-subtitle">填写信息，几秒即可完成注册</p>
        </div>
        <n-form ref="formRef" :model="formValue" :rules="rules" size="large" class="login-form">
          <n-form-item path="username" :show-label="false">
            <n-input v-model:value="formValue.username" placeholder="请输入用户名" :input-props="{ autocomplete: 'username' }">
              <template #prefix><UserIcon class="w-[18px] h-[18px]" style="color: #9CA3AF;" /></template>
            </n-input>
          </n-form-item>
          <n-form-item path="password" :show-label="false">
            <n-input v-model:value="formValue.password" type="password" show-password-on="mousedown" placeholder="请设置密码（至少6位）" :input-props="{ autocomplete: 'new-password' }" @keyup.enter="handleRegister">
              <template #prefix><LockIcon class="w-[18px] h-[18px]" style="color: #9CA3AF;" /></template>
            </n-input>
          </n-form-item>
          <n-button type="primary" block :loading="loading" @click="handleRegister" class="login-btn">注 册</n-button>
        </n-form>
        <div class="form-footer">
          <span style="color: #9CA3AF;">已有账号？</span>
          <router-link to="/login" class="register-link">立即登录</router-link>
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
import { CodeIcon, UserIcon, LockIcon } from "lucide-vue-next"

const router = useRouter()
const authStore = useAuthStore()
const message = useMessage()
const formRef = ref<FormInst | null>(null)
const loading = ref(false)
const formValue = ref({ username: "", password: "" })
const rules = { username: { required: true, message: "请输入用户名", trigger: "blur" }, password: { required: true, message: "请输入密码", trigger: "blur" } }

const handleRegister = async () => { formRef.value?.validate(async (errors) => { if (!errors) { loading.value = true; try { await authStore.register(formValue.value); message.success("注册成功"); router.push("/") } catch (e) { console.error(e) } finally { loading.value = false } } }) }
</script>

<style scoped>
.login-page { display: flex; height: 100vh; width: 100vw; overflow: hidden; }
.login-left { position: relative; flex: 1; background: #0D1117; display: flex; align-items: center; justify-content: center; overflow: hidden; padding: 3rem; }
.login-left-content { position: relative; z-index: 2; max-width: 480px; }
.brand { display: flex; align-items: center; gap: 10px; margin-bottom: 2.5rem; }
.brand-icon { display: flex; align-items: center; justify-content: center; width: 44px; height: 44px; background: linear-gradient(135deg, #2563EB, #7C3AED); border-radius: 12px; color: white; }
.brand-text { font-size: 1.25rem; font-weight: 700; color: #E6EDF3; letter-spacing: -0.02em; }
.hero-title { font-size: 2.75rem; font-weight: 800; line-height: 1.2; color: #E6EDF3; letter-spacing: -0.03em; margin-bottom: 1.25rem; }
.hero-highlight { color: #58A6FF; }
.hero-desc { font-size: 1.05rem; line-height: 1.7; color: #9CA3AF; margin-bottom: 2.5rem; }
.hero-stats { display: flex; align-items: center; gap: 24px; padding: 20px 24px; background: #161B22; border: 1px solid #30363D; border-radius: 12px; }
.stat-item { display: flex; flex-direction: column; gap: 4px; }
.stat-number { font-size: 1.25rem; font-weight: 700; color: #E6EDF3; }
.stat-label { font-size: 0.8rem; color: #9CA3AF; }
.stat-divider { width: 1px; height: 36px; background: #30363D; }
.login-left-decoration { position: absolute; inset: 0; pointer-events: none; }
.deco-circle { position: absolute; border-radius: 50%; }
.deco-circle-1 { width: 500px; height: 500px; top: -100px; right: -150px; background: radial-gradient(circle, rgba(88, 166, 255, 0.06) 0%, transparent 70%); }
.deco-circle-2 { width: 300px; height: 300px; bottom: -50px; left: -80px; background: radial-gradient(circle, rgba(167, 139, 250, 0.06) 0%, transparent 70%); }
.login-right { width: 480px; min-width: 420px; display: flex; align-items: center; justify-content: center; padding: 3rem; background: #F9FAFB; border-left: 1px solid #E5E7EB; }
.login-form-wrapper { width: 100%; max-width: 360px; }
.form-header { margin-bottom: 2rem; }
.form-title { font-size: 1.75rem; font-weight: 700; color: #111827; letter-spacing: -0.02em; margin-bottom: 0.5rem; }
.form-subtitle { font-size: 0.95rem; color: #9CA3AF; }
.login-form :deep(.n-input) { border-radius: 8px; }
.login-form :deep(.n-input .n-input__input-el) { height: 48px; }
.login-form :deep(.n-input .n-input-wrapper) { padding: 0 14px; }
.login-btn { height: 48px !important; border-radius: 8px !important; font-size: 1rem !important; font-weight: 600 !important; margin-top: 8px; transition: all 0.15s ease; }
.login-btn:hover { transform: translateY(-1px); }
.form-footer { text-align: center; margin-top: 1.75rem; font-size: 0.9rem; }
.register-link { color: #2563EB; font-weight: 600; text-decoration: none; margin-left: 4px; transition: color 0.15s; }
.register-link:hover { color: #1D4ED8; }
@media (max-width: 900px) { .login-left { display: none; } .login-right { width: 100%; min-width: unset; border-left: none; } }
</style>
