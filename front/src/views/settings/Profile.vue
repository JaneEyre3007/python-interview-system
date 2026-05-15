<template>
  <div class="max-w-md mx-auto space-y-5 animate-in">
    <div class="text-center">
      <div class="w-12 h-12 rounded-xl flex items-center justify-center mx-auto mb-3" style="background: #EFF6FF; color: #2563EB;">
        <SettingsIcon class="w-6 h-6" />
      </div>
      <h1 class="text-xl font-bold" style="color: #111827;">个人设置</h1>
      <p class="text-xs mt-1" style="color: #9CA3AF;">修改密码 · 管理账户</p>
    </div>

    <!-- User Info Card -->
    <div class="p-6 rounded-xl space-y-4" style="background: #FFFFFF; border: 1px solid #E5E7EB;">
      <div class="flex items-center gap-3 pb-4" style="border-bottom: 1px solid #E5E7EB;">
        <div class="w-10 h-10 rounded-full flex items-center justify-center text-white font-bold text-sm"
          style="background: linear-gradient(135deg, #2563EB, #7C3AED);">
          {{ authStore.user?.username?.[0]?.toUpperCase() }}
        </div>
        <div>
          <p class="text-sm font-semibold" style="color: #111827;">{{ authStore.user?.username }}</p>
        </div>
      </div>

      <n-form :model="form" label-placement="top" size="small">
        <n-form-item label="原密码">
          <n-input v-model:value="form.oldPassword" type="password" placeholder="输入当前密码" />
        </n-form-item>
        <n-form-item label="新密码">
          <n-input v-model:value="form.newPassword" type="password" placeholder="输入新密码（至少6位）" />
        </n-form-item>
        <n-form-item label="确认新密码">
          <n-input v-model:value="form.confirmPassword" type="password" placeholder="再次输入新密码" />
        </n-form-item>

        <n-button type="primary" block :loading="loading" @click="handleChangePassword" class="!rounded-lg !font-semibold !h-10">
          <template #icon><LockIcon class="w-4 h-4" /></template>
          修改密码
        </n-button>
      </n-form>
    </div>

    <!-- Logout -->
    <div class="p-6 rounded-xl" style="background: #FFFFFF; border: 1px solid #E5E7EB;">
      <n-button type="error" block @click="handleLogout" class="!rounded-lg !font-semibold !h-10">
        <template #icon><LogOutIcon class="w-4 h-4" /></template>
        退出登录
      </n-button>
    </div>

  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from "vue"
import { useRouter } from "vue-router"
import { useAuthStore } from "@/stores/auth"
import { useMessage } from "naive-ui"
import { SettingsIcon, LockIcon, LogOutIcon } from "lucide-vue-next"
import api from "@/api"

const router = useRouter()
const authStore = useAuthStore()
const message = useMessage()
const loading = ref(false)

const form = reactive({
  oldPassword: "",
  newPassword: "",
  confirmPassword: "",
})

const handleChangePassword = async () => {
  if (!form.oldPassword || !form.newPassword || !form.confirmPassword) {
    message.warning("请填写完整")
    return
  }
  if (form.newPassword !== form.confirmPassword) {
    message.warning("两次新密码不一致")
    return
  }
  if (form.newPassword.length < 6) {
    message.warning("新密码至少6位")
    return
  }
  loading.value = true
  try {
    await api.post("/users/change-password/", {
      old_password: form.oldPassword,
      new_password: form.newPassword,
    })
    message.success("密码已修改，请重新登录")
    authStore.logout()
    router.push("/login")
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

const handleLogout = () => {
  authStore.logout()
  router.push("/login")
}
</script>
