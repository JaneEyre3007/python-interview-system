<template>
  <div class="max-w-xl mx-auto space-y-5 animate-in">
    <div class="text-center">
      <div class="w-12 h-12 rounded-xl flex items-center justify-center mx-auto mb-3" style="background: #EFF6FF; color: #2563EB;"><SettingsIcon class="w-6 h-6" /></div>
      <h1 class="text-xl font-bold" style="color: #111827;">AI 模型配置</h1>
      <p class="text-xs mt-1" style="color: #9CA3AF;">配置 AI 提供商和 API 凭据</p>
    </div>

    <div class="p-6 rounded-xl space-y-5" style="background: #FFFFFF; border: 1px solid #E5E7EB;">
      <div class="flex items-start gap-2.5 p-3 rounded-lg" style="background: #EFF6FF; border: 1px solid #E5E7EB;">
        <div class="p-1.5 rounded-md shrink-0 mt-0.5" style="background: #2563EB; color: #FFFFFF;"><InfoIcon class="w-3.5 h-3.5" /></div>
        <div>
          <p class="text-xs font-medium mb-0.5" style="color: #2563EB;">支持 OpenAI 兼容接口</p>
          <p class="text-[11px] leading-relaxed" style="color: #4B5563;">API Key 会加密存储。支持 MiMo、通义千问、智谱等兼容提供商。</p>
        </div>
      </div>

      <n-form :model="config" label-placement="top" size="small">
        <n-form-item label="提供商"><n-select v-model:value="config.provider" :options="providerOptions" /></n-form-item>
        <n-form-item label="API 地址"><n-input v-model:value="config.api_url" placeholder="https://api.openai.com/v1" /></n-form-item>
        <n-form-item label="API Key"><n-input v-model:value="config.api_key" type="password" show-password-on="mousedown" placeholder="sk-..." /></n-form-item>
        <n-form-item label="模型名称"><n-input v-model:value="config.model_name" placeholder="gpt-3.5-turbo / gpt-4 / deepseek-chat" /></n-form-item>

        <div class="flex items-center justify-between p-3.5 rounded-lg" style="background: #F9FAFB; border: 1px solid #E5E7EB;">
          <div>
            <p class="text-sm font-medium" style="color: #111827;">启用 AI 功能</p>
            <p class="text-[11px] mt-0.5" style="color: #9CA3AF;">开启后可使用 AI 出题和自动评判</p>
          </div>
          <n-switch v-model:value="config.is_active" />
        </div>

        <div class="flex items-center gap-2.5 p-3 rounded-lg" :style="{ background: config.is_active ? '#ECFDF5' : '#F9FAFB', border: `1px solid ${config.is_active ? '#059669' : '#E5E7EB'}` }">
          <div class="w-2 h-2 rounded-full shrink-0" :style="{ background: config.is_active ? '#059669' : '#9CA3AF' }"></div>
          <p class="text-xs font-medium" :style="{ color: config.is_active ? '#059669' : '#9CA3AF' }">{{ config.is_active ? 'AI 功能已启用' : 'AI 功能已禁用' }}</p>
        </div>

        <div class="flex gap-2">
          <n-button type="primary" block class="!rounded-lg !font-semibold !h-10" :loading="loading" @click="handleSave"><template #icon><SaveIcon class="w-4 h-4" /></template>保存配置</n-button>
          <n-button quaternary type="error" @click="handleDelete" :disabled="!config.api_url"><template #icon><TrashIcon class="w-3.5 h-3.5" /></template>清除</n-button>
        </div>
      </n-form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, reactive } from "vue"
import { InfoIcon, SaveIcon, TrashIcon, SettingsIcon } from "lucide-vue-next"
import { useMessage, useDialog } from "naive-ui"
import api from "@/api"

const message = useMessage()
const dialog = useDialog()
const loading = ref(false)
const config = reactive({ provider: "openai", api_key: "", api_url: "https://api.openai.com/v1", model_name: "gpt-3.5-turbo", is_active: true })
const providerOptions = [{ label: "OpenAI 兼容", value: "openai" }, { label: "自定义", value: "custom" }]

onMounted(async () => { try { const d: any = await api.get("/users/ai-config/"); if (d && d.provider) { Object.assign(config, d); config.api_key = "" } } catch (e) { console.error(e) } })
const handleSave = async () => { if (!config.api_url.trim()) { message.warning("请输入 API 地址"); return } loading.value = true; try { await api.post("/users/ai-config/", { ...config }); message.success("配置已保存") } catch (e) { console.error(e) } finally { loading.value = false } }
const handleDelete = () => { dialog.warning({ title: "确认清除", content: "确定要删除 AI 配置吗？清除后 AI 功能将不可用。", positiveText: "确定清除", negativeText: "取消", onPositiveClick: async () => { try { await api.delete("/users/ai-config/"); message.success("配置已删除"); Object.assign(config, { provider: "openai", api_key: "", api_url: "https://api.openai.com/v1", model_name: "gpt-3.5-turbo", is_active: false }) } catch (e) { console.error(e) } } }) }
</script>
