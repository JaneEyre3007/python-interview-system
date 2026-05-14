<template>
  <div class="exam-setup">
    <el-card class="setup-card">
      <template #header>
        <h2>创建新考试</h2>
      </template>
      <el-form :model="form" :rules="rules" ref="formRef" label-width="120px">
        <el-form-item label="试卷标题" prop="title">
          <el-input v-model="form.title" placeholder="如：Python基础测试" />
        </el-form-item>
        <el-form-item label="题目数量" prop="question_count">
          <el-slider v-model="form.question_count" :min="1" :max="maxCount" :step="1" show-input />
          <span class="count-hint">题库共 {{ maxCount }} 道题</span>
        </el-form-item>
        <el-form-item label="题目类型">
          <el-radio-group v-model="form.question_type">
            <el-radio-button value="mixed">混合</el-radio-button>
            <el-radio-button value="choice">选择题</el-radio-button>
            <el-radio-button value="fill">填空题</el-radio-button>
            <el-radio-button value="code">编程题</el-radio-button>
            <el-radio-button value="short">简答题</el-radio-button>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="难度">
          <el-radio-group v-model="form.difficulty">
            <el-radio-button value="mixed">混合</el-radio-button>
            <el-radio-button value="easy">简单</el-radio-button>
            <el-radio-button value="medium">中等</el-radio-button>
            <el-radio-button value="hard">困难</el-radio-button>
          </el-radio-group>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :loading="loading" @click="handleCreate">
            开始考试
          </el-button>
          <el-button @click="router.push('/')">返回首页</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { createExam } from '../api/exam'
import { getQuestions } from '../api/question'
import { ElMessage } from 'element-plus'

const router = useRouter()
const formRef = ref()
const loading = ref(false)
const maxCount = ref(10)

const form = reactive({
  title: 'Python面试练习',
  question_count: 10,
  question_type: 'mixed',
  difficulty: 'mixed'
})

const rules = {
  title: [{ required: true, message: '请输入试卷标题', trigger: 'blur' }]
}

onMounted(async () => {
  try {
    const res = await getQuestions({ page_size: 1 })
    const total = res.data.count || 0
    maxCount.value = total > 0 ? total : 10
    form.question_count = total > 0 ? Math.min(total, 30) : 10
  } catch (error) {
    console.error(error)
  }
})

const handleCreate = async () => {
  await formRef.value.validate()
  loading.value = true
  try {
    const res = await createExam(form)
    ElMessage.success('试卷创建成功')
    router.push(`/exam/${res.data.id}`)
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.exam-setup {
  max-width: 800px;
  margin: 0 auto;
}

.setup-card {
  padding: 20px;
}

.setup-card :deep(.el-card__header) {
  text-align: center;
}

.setup-card :deep(.el-card__header h2) {
  margin: 0;
  color: #303133;
}

.count-hint {
  color: #909399;
  font-size: 12px;
  margin-left: 10px;
}
</style>
