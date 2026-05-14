<template>
  <div class="result-page">
    <el-card v-if="loading" v-loading="true" style="min-height: 400px;"></el-card>

    <template v-else-if="result">
      <el-card class="result-summary">
        <div class="summary-content">
          <div class="score-circle">
            <el-progress type="circle" :percentage="scorePercentage" :width="150">
              <template #default>
                <span class="score-text">{{ result.total_score }}</span>
                <span class="score-unit">分</span>
              </template>
            </el-progress>
          </div>
          <div class="summary-info">
            <h2>{{ result.exam.title }}</h2>
            <div class="info-grid">
              <div class="info-item">
                <span class="label">总题数</span>
                <span class="value">{{ result.total_count }} 道</span>
              </div>
              <div class="info-item">
                <span class="label">正确数</span>
                <span class="value correct">{{ result.correct_count }} 道</span>
              </div>
              <div class="info-item">
                <span class="label">错误数</span>
                <span class="value wrong">{{ result.total_count - result.correct_count }} 道</span>
              </div>
              <div class="info-item">
                <span class="label">正确率</span>
                <span class="value">{{ scorePercentage }}%</span>
              </div>
            </div>
          </div>
        </div>
      </el-card>

      <el-card class="answers-list">
        <template #header>
          <span>答题详情</span>
        </template>

        <div v-for="(answer, index) in result.answers" :key="index" class="answer-item">
          <div class="answer-header">
            <span class="question-index">第 {{ index + 1 }} 题</span>
            <el-tag :type="answer.is_correct ? 'success' : 'danger'">
              {{ answer.is_correct ? '正确' : '错误' }}
            </el-tag>
            <span class="score">{{ answer.score }} 分</span>
          </div>

          <div class="question-content">{{ answer.question_content }}</div>

          <div class="answer-detail">
            <div class="your-answer" :class="{ wrong: !answer.is_correct }">
              <strong>你的答案：</strong>{{ answer.user_answer }}
            </div>
            <div v-if="!answer.is_correct" class="ai-feedback">
              <strong>AI反馈：</strong>
              <div class="feedback-content">{{ answer.ai_feedback }}</div>
            </div>
          </div>
        </div>
      </el-card>

      <div class="actions">
        <el-button @click="router.push('/exam')">再来一次</el-button>
        <el-button type="primary" @click="router.push('/')">返回首页</el-button>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getExamResult } from '../api/exam'

const route = useRoute()
const router = useRouter()
const result = ref(null)
const loading = ref(true)

const scorePercentage = computed(() => {
  if (!result.value) return 0
  const totalScore = result.value.total_count * 10
  return Math.round((result.value.total_score / totalScore) * 100)
})

onMounted(async () => {
  try {
    const res = await getExamResult(route.params.id)
    result.value = res.data
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.result-page {
  max-width: 900px;
  margin: 0 auto;
}

.result-summary {
  margin-bottom: 20px;
}

.summary-content {
  display: flex;
  align-items: center;
  gap: 40px;
}

.score-circle {
  flex-shrink: 0;
}

.score-text {
  font-size: 36px;
  font-weight: bold;
  color: #303133;
}

.score-unit {
  font-size: 14px;
  color: #909399;
}

.summary-info h2 {
  margin: 0 0 20px 0;
  color: #303133;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 15px;
}

.info-item {
  display: flex;
  flex-direction: column;
}

.info-item .label {
  color: #909399;
  font-size: 14px;
}

.info-item .value {
  font-size: 20px;
  font-weight: bold;
  color: #303133;
}

.info-item .value.correct {
  color: #67c23a;
}

.info-item .value.wrong {
  color: #f56c6c;
}

.answer-item {
  border-bottom: 1px solid #ebeef5;
  padding: 20px 0;
}

.answer-item:last-child {
  border-bottom: none;
}

.answer-header {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 15px;
}

.question-index {
  font-weight: bold;
}

.score {
  color: #909399;
}

.question-content {
  background: #f5f7fa;
  padding: 15px;
  border-radius: 4px;
  margin-bottom: 15px;
  white-space: pre-wrap;
}

.answer-detail {
  padding-left: 15px;
}

.your-answer {
  margin-bottom: 10px;
}

.your-answer.wrong {
  color: #f56c6c;
}

.ai-feedback {
  background: #fdf6ec;
  padding: 15px;
  border-radius: 4px;
  color: #e6a23c;
}

.feedback-content {
  margin-top: 10px;
  white-space: pre-wrap;
}

.actions {
  margin-top: 20px;
  display: flex;
  justify-content: center;
  gap: 15px;
}
</style>
