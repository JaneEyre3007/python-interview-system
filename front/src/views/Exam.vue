<template>
  <div class="exam-page">
    <el-card v-if="loading" v-loading="true" style="min-height: 400px;"></el-card>

    <template v-else-if="exam">
      <el-card class="exam-header">
        <div class="header-content">
          <h2>{{ exam.title }}</h2>
          <div class="exam-info">
            <span>总分：{{ exam.total_score }}分</span>
            <span>题目数：{{ examQuestions.length }}道</span>
            <el-tag :type="exam.status === 'in_progress' ? 'warning' : 'info'">
              {{ exam.status === 'in_progress' ? '进行中' : '待开始' }}
            </el-tag>
          </div>
        </div>
      </el-card>

      <el-row :gutter="20">
        <el-col :span="18">
          <el-card class="question-card">
            <template v-if="exam.status === 'pending'">
              <div class="start-exam">
                <h3>准备开始考试</h3>
                <p>共 {{ examQuestions.length }} 道题目，总分 {{ exam.total_score }} 分</p>
                <el-button type="primary" size="large" @click="handleStart">开始答题</el-button>
              </div>
            </template>

            <template v-else-if="exam.status === 'in_progress' && currentQuestion">
              <div class="question-content">
                <div class="question-header">
                  <el-tag :type="getTypeTag(currentQuestion.question.type)">
                    {{ getTypeLabel(currentQuestion.question.type) }}
                  </el-tag>
                  <span class="question-index">第 {{ currentIndex + 1 }} / {{ examQuestions.length }} 题</span>
                </div>
                <div class="question-text">{{ currentQuestion.question.content }}</div>

                <template v-if="currentQuestion.question.type === 'choice'">
                  <div class="options">
                    <el-radio-group v-model="userAnswer">
                      <el-radio
                        v-for="(value, key) in currentQuestion.question.options"
                        :key="key"
                        :value="key"
                        class="option-item"
                      >
                        {{ key }}. {{ value }}
                      </el-radio>
                    </el-radio-group>
                  </div>
                </template>

                <template v-else>
                  <el-input
                    v-model="userAnswer"
                    type="textarea"
                    :rows="4"
                    placeholder="请输入你的答案"
                  />
                </template>

                <div class="question-actions">
                  <el-button @click="prevQuestion" :disabled="currentIndex === 0">上一题</el-button>
                  <el-tag v-if="isAnswered" type="success" size="large">已作答</el-tag>
                  <el-tag v-else-if="submitting" type="warning" size="large">保存中...</el-tag>
                  <el-button
                    v-if="currentIndex < examQuestions.length - 1"
                    type="primary"
                    @click="nextQuestion"
                  >
                    下一题
                  </el-button>
                  <el-button
                    v-else
                    type="danger"
                    @click="handleFinish"
                  >
                    完成考试
                  </el-button>
                </div>
              </div>
            </template>
          </el-card>
        </el-col>

        <el-col :span="6">
          <el-card class="answer-sheet">
            <template #header>
              <span>答题卡</span>
            </template>
            <div class="sheet-grid">
              <div
                v-for="(item, index) in examQuestions"
                :key="index"
                :class="['sheet-item', {
                  'current': index === currentIndex,
                  'answered': item.question.id in answeredQuestions
                }]"
                @click="goToQuestion(index)"
              >
                {{ index + 1 }}
              </div>
            </div>
            <div class="sheet-legend">
              <span><span class="legend-dot answered"></span> 已答</span>
              <span><span class="legend-dot current"></span> 当前</span>
              <span><span class="legend-dot"></span> 未答</span>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { startExam, submitAnswer, finishExam, getExamResult } from '../api/exam'
import { ElMessage, ElMessageBox } from 'element-plus'

const route = useRoute()
const router = useRouter()
const exam = ref(null)
const examQuestions = ref([])
const loading = ref(true)
const currentIndex = ref(0)
const userAnswer = ref('')
const submitting = ref(false)
const answeredQuestions = ref({})
let debounceTimer = null

const typeMap = {
  choice: { label: '选择题', tag: '' },
  fill: { label: '填空题', tag: 'success' },
  code: { label: '编程题', tag: 'warning' },
  short: { label: '简答题', tag: 'info' }
}

const getTypeLabel = (type) => typeMap[type]?.label || type
const getTypeTag = (type) => typeMap[type]?.tag || ''

const currentQuestion = computed(() => {
  return examQuestions.value[currentIndex.value] || null
})

const isAnswered = computed(() => {
  if (!currentQuestion.value) return false
  return currentQuestion.value.question.id in answeredQuestions.value
})

watch(userAnswer, (newVal) => {
  if (!currentQuestion.value || exam.value?.status !== 'in_progress') return
  if (isAnswered.value) return
  if (!newVal || !newVal.trim()) return

  if (currentQuestion.value.question.type === 'choice') {
    saveAnswer(newVal)
  } else {
    clearTimeout(debounceTimer)
    debounceTimer = setTimeout(() => {
      saveAnswer(newVal)
    }, 1000)
  }
})

const saveAnswer = async (answer) => {
  if (!currentQuestion.value || submitting.value) return
  submitting.value = true
  try {
    await submitAnswer(exam.value.id, {
      question_id: currentQuestion.value.question.id,
      answer: answer
    })
    answeredQuestions.value[currentQuestion.value.question.id] = answer
    ElMessage.success('答案已自动保存')
  } catch (error) {
    console.error(error)
  } finally {
    submitting.value = false
  }
}

const loadExam = async () => {
  loading.value = true
  try {
    const res = await getExamResult(route.params.id)
    exam.value = res.data.exam
    examQuestions.value = res.data.exam.questions || []

    if (res.data.answers) {
      const answered = {}
      res.data.answers.forEach(a => {
        answered[a.question] = a.user_answer
      })
      answeredQuestions.value = answered
    }
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
}

const handleStart = async () => {
  try {
    await startExam(exam.value.id)
    exam.value.status = 'in_progress'
    ElMessage.success('考试已开始')
  } catch (error) {
    console.error(error)
  }
}

const prevQuestion = () => {
  if (currentIndex.value > 0) {
    currentIndex.value--
    loadCurrentAnswer()
  }
}

const nextQuestion = () => {
  if (currentIndex.value < examQuestions.value.length - 1) {
    currentIndex.value++
    loadCurrentAnswer()
  }
}

const goToQuestion = (index) => {
  currentIndex.value = index
  loadCurrentAnswer()
}

const loadCurrentAnswer = () => {
  const q = currentQuestion.value
  if (q && q.question.id in answeredQuestions.value) {
    userAnswer.value = answeredQuestions.value[q.question.id]
  } else {
    userAnswer.value = ''
  }
}

const handleFinish = async () => {
  try {
    await ElMessageBox.confirm('确定要完成考试吗？', '提示', {
      type: 'warning'
    })
    const res = await finishExam(exam.value.id)
    ElMessage.success(`考试完成！得分：${res.data.total_score}`)
    router.push(`/result/${exam.value.id}`)
  } catch (error) {
    if (error !== 'cancel') {
      console.error(error)
    }
  }
}

onMounted(() => {
  loadExam()
})
</script>

<style scoped>
.exam-page {
  max-width: 1200px;
  margin: 0 auto;
}

.exam-header {
  margin-bottom: 20px;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.exam-info {
  display: flex;
  gap: 20px;
  align-items: center;
  color: #666;
}

.start-exam {
  text-align: center;
  padding: 60px 20px;
}

.start-exam h3 {
  margin-bottom: 15px;
}

.start-exam p {
  color: #666;
  margin-bottom: 30px;
}

.question-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.question-index {
  color: #909399;
}

.question-text {
  font-size: 16px;
  line-height: 1.8;
  margin-bottom: 20px;
  white-space: pre-wrap;
}

.options {
  margin-bottom: 20px;
}

.option-item {
  display: block;
  margin-bottom: 15px;
  padding: 10px 15px;
  background: #f5f7fa;
  border-radius: 4px;
}

.question-actions {
  margin-top: 30px;
  display: flex;
  gap: 10px;
  justify-content: center;
}

.answer-sheet {
  position: sticky;
  top: 80px;
}

.sheet-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 8px;
}

.sheet-item {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.sheet-item.current {
  background: #409eff;
  color: white;
  border-color: #409eff;
}

.sheet-item.answered {
  background: #67c23a;
  color: white;
  border-color: #67c23a;
}

.sheet-legend {
  margin-top: 15px;
  display: flex;
  gap: 15px;
  justify-content: center;
  font-size: 12px;
  color: #909399;
}

.legend-dot {
  display: inline-block;
  width: 12px;
  height: 12px;
  border-radius: 2px;
  margin-right: 4px;
  vertical-align: middle;
}

.legend-dot.answered {
  background: #67c23a;
}

.legend-dot.current {
  background: #409eff;
}
</style>
