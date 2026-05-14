<template>
  <div class="ai-config-page">
    <el-card>
      <template #header>
        <div class="card-header">
          <h2>AI模型配置</h2>
          <el-tag :type="config.is_active ? 'success' : 'info'">
            {{ config.is_active ? '已启用' : '未启用' }}
          </el-tag>
        </div>
      </template>

      <el-alert
        title="配置说明"
        type="info"
        description="您可以配置自己的AI模型API。支持OpenAI兼容接口（如MiMo、通义千问、智谱AI等）。配置后将使用您的个人API调用模型。"
        :closable="false"
        show-icon
        style="margin-bottom: 20px;"
      />

      <el-form :model="form" :rules="rules" ref="formRef" label-width="120px">
        <el-form-item label="提供商" prop="provider">
          <el-select v-model="form.provider" placeholder="选择提供商">
            <el-option label="OpenAI兼容接口" value="openai" />
            <el-option label="自定义" value="custom" />
          </el-select>
        </el-form-item>

        <el-form-item label="API Key" prop="api_key">
          <el-input
            v-model="form.api_key"
            type="password"
            show-password
            placeholder="请输入API Key"
          />
        </el-form-item>

        <el-form-item label="API地址" prop="api_url">
          <el-input v-model="form.api_url" placeholder="如：https://api.openai.com/v1/chat/completions" />
          <div class="form-tip">
            <p>常用API地址：</p>
            <p>- MiMo: https://token-plan-cn.xiaomimimo.com/v1/chat/completions</p>
            <p>- OpenAI: https://api.openai.com/v1/chat/completions</p>
            <p>- 通义千问: https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions</p>
            <p>- 智谱AI: https://open.bigmodel.cn/api/paas/v4/chat/completions</p>
          </div>
        </el-form-item>

        <el-form-item label="模型名称" prop="model_name">
          <el-input v-model="form.model_name" placeholder="如：mimo-v2.5-pro、gpt-4o、qwen-turbo" />
          <div class="form-tip">
            <p>常用模型：</p>
            <p>- MiMo: mimo-v2.5-pro</p>
            <p>- OpenAI: gpt-4o、gpt-4o-mini、gpt-3.5-turbo</p>
            <p>- 通义千问: qwen-turbo、qwen-plus、qwen-max</p>
            <p>- 智谱AI: glm-4、glm-4-flash</p>
          </div>
        </el-form-item>

        <el-form-item label="启用">
          <el-switch v-model="form.is_active" />
          <span class="form-tip" style="margin-left: 10px;">启用后将使用您的个人API配置</span>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" :loading="saving" @click="handleSave">保存配置</el-button>
          <el-button type="danger" :loading="deleting" @click="handleDelete" :disabled="!config.is_active">
            删除配置
          </el-button>
          <el-button @click="loadConfig">重新加载</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { getAIConfig, saveAIConfig, deleteAIConfig } from '../api/user'
import { ElMessage, ElMessageBox } from 'element-plus'

const formRef = ref()
const saving = ref(false)
const deleting = ref(false)
const config = ref({})

const form = reactive({
  provider: 'openai',
  api_key: '',
  api_url: '',
  model_name: '',
  is_active: false
})

const rules = {
  api_key: [{ required: true, message: '请输入API Key', trigger: 'blur' }],
  api_url: [{ required: true, message: '请输入API地址', trigger: 'blur' }],
  model_name: [{ required: true, message: '请输入模型名称', trigger: 'blur' }]
}

const loadConfig = async () => {
  try {
    const res = await getAIConfig()
    config.value = res.data
    form.provider = res.data.provider || 'openai'
    form.api_url = res.data.api_url || ''
    form.model_name = res.data.model_name || ''
    form.is_active = res.data.is_active || false
    form.api_key = ''  // 始终清空api_key，因为GET返回的是掩码
  } catch (error) {
    console.error(error)
  }
}

const handleSave = async () => {
  await formRef.value.validate()
  saving.value = true
  try {
    await saveAIConfig(form)
    ElMessage.success('配置保存成功')
    loadConfig()
  } catch (error) {
    console.error(error)
  } finally {
    saving.value = false
  }
}

const handleDelete = async () => {
  try {
    await ElMessageBox.confirm('确定要删除AI配置吗？删除后需要重新配置才能使用AI功能。', '确认删除', {
      type: 'warning'
    })
    deleting.value = true
    await deleteAIConfig()
    ElMessage.success('配置已删除')
    form.api_key = ''
    form.api_url = ''
    form.model_name = ''
    form.is_active = false
    loadConfig()
  } catch (error) {
    if (error !== 'cancel') {
      console.error(error)
    }
  } finally {
    deleting.value = false
  }
}

onMounted(() => {
  loadConfig()
})
</script>

<style scoped>
.ai-config-page {
  max-width: 800px;
  margin: 0 auto;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.card-header h2 {
  margin: 0;
}

.form-tip {
  color: #909399;
  font-size: 12px;
  margin-top: 5px;
  line-height: 1.8;
}

.form-tip p {
  margin: 0;
}
</style>
