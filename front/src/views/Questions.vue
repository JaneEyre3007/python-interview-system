<template>
  <div class="questions-page">
    <el-card class="filter-card">
      <el-row :gutter="20">
        <el-col :span="6">
          <el-select v-model="filter.type" placeholder="题目类型" clearable @change="loadQuestions">
            <el-option label="选择题" value="choice" />
            <el-option label="填空题" value="fill" />
            <el-option label="编程题" value="code" />
            <el-option label="简答题" value="short" />
          </el-select>
        </el-col>
        <el-col :span="6">
          <el-select v-model="filter.difficulty" placeholder="难度" clearable @change="loadQuestions">
            <el-option label="简单" value="easy" />
            <el-option label="中等" value="medium" />
            <el-option label="困难" value="hard" />
          </el-select>
        </el-col>
        <el-col :span="12">
          <el-button type="primary" @click="showGenerateDialog = true">
            <el-icon><magic-stick /></el-icon>
            AI搜索题目
          </el-button>
          <el-button type="danger" :disabled="selectedIds.length === 0" @click="handleBatchDelete">
            <el-icon><delete /></el-icon>
            批量删除 ({{ selectedIds.length }})
          </el-button>
        </el-col>
      </el-row>
    </el-card>

    <el-card v-loading="loading">
      <el-table :data="questions" stripe @selection-change="handleSelectionChange">
        <el-table-column type="selection" width="55" />
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column label="类型" width="100">
          <template #default="{ row }">
            <el-tag :type="getTypeTag(row.type)">{{ getTypeLabel(row.type) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="难度" width="100">
          <template #default="{ row }">
            <el-tag :type="getDifficultyTag(row.difficulty)">{{ getDifficultyLabel(row.difficulty) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="content" label="题目内容" show-overflow-tooltip />
        <el-table-column label="来源" width="100">
          <template #default="{ row }">
            <el-tag v-if="row.created_by_ai" type="success">AI生成</el-tag>
            <el-tag v-else type="info">手动添加</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150">
          <template #default="{ row }">
            <el-button type="primary" link @click="viewQuestion(row)">查看</el-button>
            <el-button type="danger" link @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-pagination
        v-model:current-page="pagination.page"
        :page-size="pagination.pageSize"
        :total="pagination.total"
        layout="total, prev, pager, next"
        @current-change="loadQuestions"
        style="margin-top: 20px; justify-content: center;"
      />
    </el-card>

    <el-dialog v-model="showDetail" title="题目详情" width="600px">
      <div v-if="currentQuestion">
        <p><strong>题目类型：</strong>{{ getTypeLabel(currentQuestion.type) }}</p>
        <p><strong>难度：</strong>{{ getDifficultyLabel(currentQuestion.difficulty) }}</p>
        <p><strong>题目内容：</strong></p>
        <div class="question-content">{{ currentQuestion.content }}</div>
        <template v-if="currentQuestion.type === 'choice' && currentQuestion.options">
          <p><strong>选项：</strong></p>
          <div v-for="(value, key) in currentQuestion.options" :key="key" class="option-item">
            {{ key }}. {{ value }}
          </div>
        </template>
        <p><strong>正确答案：</strong>{{ currentQuestion.answer }}</p>
        <p v-if="currentQuestion.explanation"><strong>解析：</strong>{{ currentQuestion.explanation }}</p>
      </div>
    </el-dialog>

    <el-dialog v-model="showGenerateDialog" title="AI搜索题目" width="500px">
      <el-form :model="generateForm" label-width="100px">
        <el-form-item label="主题">
          <el-input v-model="generateForm.topic" placeholder="如：Python基础、Django、爬虫" />
        </el-form-item>
        <el-form-item label="题目类型">
          <el-select v-model="generateForm.type">
            <el-option label="选择题" value="choice" />
            <el-option label="填空题" value="fill" />
            <el-option label="编程题" value="code" />
            <el-option label="简答题" value="short" />
          </el-select>
        </el-form-item>
        <el-form-item label="难度">
          <el-select v-model="generateForm.difficulty">
            <el-option label="简单" value="easy" />
            <el-option label="中等" value="medium" />
            <el-option label="困难" value="hard" />
          </el-select>
        </el-form-item>
        <el-form-item label="数量">
          <el-input-number v-model="generateForm.count" :min="1" :max="10" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showGenerateDialog = false">取消</el-button>
        <el-button type="primary" :loading="generating" @click="handleGenerate">搜索</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { getQuestions, deleteQuestion, batchDeleteQuestions } from '../api/question'
import { generateQuestions } from '../api/ai'
import { ElMessage, ElMessageBox } from 'element-plus'
import { MagicStick, Delete } from '@element-plus/icons-vue'

const loading = ref(false)
const generating = ref(false)
const questions = ref([])
const showDetail = ref(false)
const showGenerateDialog = ref(false)
const currentQuestion = ref(null)
const selectedIds = ref([])

const filter = reactive({
  type: '',
  difficulty: ''
})

const pagination = reactive({
  page: 1,
  pageSize: 10,
  total: 0
})

const generateForm = reactive({
  topic: 'Python基础',
  type: 'choice',
  difficulty: 'medium',
  count: 3
})

const typeMap = {
  choice: { label: '选择题', tag: '' },
  fill: { label: '填空题', tag: 'success' },
  code: { label: '编程题', tag: 'warning' },
  short: { label: '简答题', tag: 'info' }
}

const difficultyMap = {
  easy: { label: '简单', tag: 'success' },
  medium: { label: '中等', tag: 'warning' },
  hard: { label: '困难', tag: 'danger' }
}

const getTypeLabel = (type) => typeMap[type]?.label || type
const getTypeTag = (type) => typeMap[type]?.tag || ''
const getDifficultyLabel = (diff) => difficultyMap[diff]?.label || diff
const getDifficultyTag = (diff) => difficultyMap[diff]?.tag || ''

const handleSelectionChange = (selection) => {
  selectedIds.value = selection.map(item => item.id)
}

const loadQuestions = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.page,
      page_size: pagination.pageSize
    }
    if (filter.type) params.type = filter.type
    if (filter.difficulty) params.difficulty = filter.difficulty

    const res = await getQuestions(params)
    questions.value = res.data.results || []
    pagination.total = res.data.count || 0
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
}

const viewQuestion = (question) => {
  currentQuestion.value = question
  showDetail.value = true
}

const handleDelete = async (question) => {
  try {
    await ElMessageBox.confirm(`确定要删除这道题目吗？`, '确认删除', {
      type: 'warning'
    })
    await deleteQuestion(question.id)
    ElMessage.success('删除成功')
    loadQuestions()
  } catch (error) {
    if (error !== 'cancel') {
      console.error(error)
    }
  }
}

const handleBatchDelete = async () => {
  try {
    await ElMessageBox.confirm(`确定要删除选中的 ${selectedIds.value.length} 道题目吗？`, '确认批量删除', {
      type: 'warning'
    })
    const res = await batchDeleteQuestions(selectedIds.value)
    ElMessage.success(res.data.message)
    selectedIds.value = []
    loadQuestions()
  } catch (error) {
    if (error !== 'cancel') {
      console.error(error)
    }
  }
}

const handleGenerate = async () => {
  generating.value = true
  try {
    const res = await generateQuestions(generateForm)
    ElMessage.success(res.data.message)
    showGenerateDialog.value = false
    loadQuestions()
  } catch (error) {
    console.error(error)
  } finally {
    generating.value = false
  }
}

onMounted(() => {
  loadQuestions()
})
</script>

<style scoped>
.questions-page {
  max-width: 1200px;
  margin: 0 auto;
}

.filter-card {
  margin-bottom: 20px;
}

.question-content {
  background: #f5f7fa;
  padding: 15px;
  border-radius: 4px;
  margin: 10px 0;
  white-space: pre-wrap;
}

.option-item {
  padding: 8px 15px;
  margin: 5px 0;
  background: #f5f7fa;
  border-radius: 4px;
}
</style>
