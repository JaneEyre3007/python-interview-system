<template>
  <div class="home">
    <el-row :gutter="20">
      <el-col :span="24">
        <h1>欢迎使用Python面试在线答题系统</h1>
        <p class="subtitle">基于小米MiMo大模型，智能出题与判题</p>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="stats-row">
      <el-col :span="6">
        <el-card class="stat-card">
          <el-icon size="40" color="#409eff"><document /></el-icon>
          <div class="stat-info">
            <div class="stat-value">{{ stats.totalQuestions }}</div>
            <div class="stat-label">题库总量</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <el-icon size="40" color="#67c23a"><finished /></el-icon>
          <div class="stat-info">
            <div class="stat-value">{{ stats.completedExams }}</div>
            <div class="stat-label">已完成考试</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <el-icon size="40" color="#e6a23c"><star /></el-icon>
          <div class="stat-info">
            <div class="stat-value">{{ stats.avgScore }}</div>
            <div class="stat-label">平均得分</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <el-icon size="40" color="#f56c6c"><timer /></el-icon>
          <div class="stat-info">
            <div class="stat-value">{{ stats.totalTime }}</div>
            <div class="stat-label">学习时长(分)</div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="action-row">
      <el-col :span="12">
        <el-card class="action-card" @click="goToExam">
          <el-icon size="60" color="#409eff"><edit /></el-icon>
          <h3>开始答题</h3>
          <p>选择题目类型和难度，开始练习</p>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card class="action-card" @click="goToQuestions">
          <el-icon size="60" color="#67c23a"><collection /></el-icon>
          <h3>浏览题库</h3>
          <p>查看所有题目，支持AI生成新题</p>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getQuestions } from '../api/question'
import { getExamList } from '../api/exam'
import { Document, Finished, Star, Timer, Edit, Collection } from '@element-plus/icons-vue'

const router = useRouter()

const stats = ref({
  totalQuestions: 0,
  completedExams: 0,
  avgScore: 0,
  totalTime: 0
})

onMounted(async () => {
  try {
    const res = await getQuestions({ page_size: 1 })
    stats.value.totalQuestions = res.data.count || 0

    const examRes = await getExamList()
    const exams = examRes.data.results || []
    stats.value.completedExams = exams.filter(e => e.status === 'completed').length
  } catch (error) {
    console.error(error)
  }
})

const goToExam = () => router.push('/exam')
const goToQuestions = () => router.push('/questions')
</script>

<style scoped>
.home {
  max-width: 1200px;
  margin: 0 auto;
}

h1 {
  text-align: center;
  color: #303133;
  margin-bottom: 10px;
}

.subtitle {
  text-align: center;
  color: #909399;
  margin-bottom: 30px;
}

.stats-row {
  margin-bottom: 30px;
}

.stat-card {
  display: flex;
  align-items: center;
  padding: 20px;
}

.stat-card :deep(.el-card__body) {
  display: flex;
  align-items: center;
  gap: 15px;
  width: 100%;
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 28px;
  font-weight: bold;
  color: #303133;
}

.stat-label {
  color: #909399;
  font-size: 14px;
}

.action-row {
  margin-bottom: 30px;
}

.action-card {
  text-align: center;
  padding: 40px 20px;
  cursor: pointer;
  transition: transform 0.3s, box-shadow 0.3s;
}

.action-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
}

.action-card h3 {
  margin: 15px 0 10px;
  color: #303133;
}

.action-card p {
  color: #909399;
  margin: 0;
}
</style>
