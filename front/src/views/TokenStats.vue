<template>
  <div class="token-stats-page">
    <el-card class="header-card">
      <h2>Token消耗统计</h2>
      <el-radio-group v-model="days" @change="loadStats">
        <el-radio-button :value="7">近7天</el-radio-button>
        <el-radio-button :value="30">近30天</el-radio-button>
        <el-radio-button :value="90">近90天</el-radio-button>
      </el-radio-group>
    </el-card>

    <el-row :gutter="20" class="stats-cards">
      <el-col :span="6">
        <el-card class="stat-card total-card">
          <div class="stat-value">{{ formatNumber(stats.total?.total_tokens || 0) }}</div>
          <div class="stat-label">总Token消耗</div>
          <div class="stat-detail">{{ stats.total?.total_calls || 0 }} 次调用</div>
        </el-card>
      </el-col>
      <el-col :span="9">
        <el-card class="stat-card generate-card">
          <div class="stat-header">
            <el-icon><search /></el-icon>
            <span>搜索题目</span>
          </div>
          <div class="stat-value">{{ formatNumber(stats.generate?.total_tokens || 0) }}</div>
          <div class="stat-detail">
            <span>输入: {{ formatNumber(stats.generate?.prompt_tokens || 0) }}</span>
            <span>输出: {{ formatNumber(stats.generate?.completion_tokens || 0) }}</span>
            <span>{{ stats.generate?.call_count || 0 }} 次</span>
          </div>
        </el-card>
      </el-col>
      <el-col :span="9">
        <el-card class="stat-card evaluate-card">
          <div class="stat-header">
            <el-icon><edit /></el-icon>
            <span>评判答案</span>
          </div>
          <div class="stat-value">{{ formatNumber(stats.evaluate?.total_tokens || 0) }}</div>
          <div class="stat-detail">
            <span>输入: {{ formatNumber(stats.evaluate?.prompt_tokens || 0) }}</span>
            <span>输出: {{ formatNumber(stats.evaluate?.completion_tokens || 0) }}</span>
            <span>{{ stats.evaluate?.call_count || 0 }} 次</span>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20">
      <el-col :span="16">
        <el-card>
          <template #header>
            <span>每日Token消耗趋势</span>
          </template>
          <div ref="dailyChart" class="chart-container"></div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card>
          <template #header>
            <span>消耗占比</span>
          </template>
          <div ref="typeChart" class="chart-container"></div>
        </el-card>
      </el-col>
    </el-row>

    <el-card class="recent-card">
      <template #header>
        <span>最近调用记录</span>
      </template>
      <el-table :data="stats.recent" stripe max-height="400">
        <el-table-column label="类型" width="100">
          <template #default="{ row }">
            <el-tag :type="row.api_type === 'generate' ? 'primary' : 'success'" size="small">
              {{ row.api_type === 'generate' ? '搜索题目' : '评判答案' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="model_name" label="模型" width="150" />
        <el-table-column label="输入Token" width="120">
          <template #default="{ row }">
            <span class="token-input">{{ row.prompt_tokens }}</span>
          </template>
        </el-table-column>
        <el-table-column label="输出Token" width="120">
          <template #default="{ row }">
            <span class="token-output">{{ row.completion_tokens }}</span>
          </template>
        </el-table-column>
        <el-table-column label="总Token" width="120">
          <template #default="{ row }">
            <span class="token-total">{{ row.total_tokens }}</span>
          </template>
        </el-table-column>
        <el-table-column label="调用时间">
          <template #default="{ row }">
            {{ formatTime(row.created_at) }}
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { getTokenStats } from '../api/ai'
import { Search, Edit } from '@element-plus/icons-vue'
import * as echarts from 'echarts'

const days = ref(30)
const stats = ref({})
const dailyChart = ref(null)
const typeChart = ref(null)
let dailyChartInstance = null
let typeChartInstance = null

const formatNumber = (num) => {
  if (num >= 10000) {
    return (num / 10000).toFixed(1) + '万'
  }
  return num.toLocaleString()
}

const formatTime = (timeStr) => {
  if (!timeStr) return '-'
  return new Date(timeStr).toLocaleString('zh-CN')
}

const loadStats = async () => {
  try {
    const res = await getTokenStats(days.value)
    stats.value = res.data
    await nextTick()
    renderCharts()
  } catch (error) {
    console.error(error)
  }
}

const renderCharts = () => {
  renderDailyChart()
  renderTypeChart()
}

const renderDailyChart = () => {
  if (!dailyChart.value) return

  if (!dailyChartInstance) {
    dailyChartInstance = echarts.init(dailyChart.value)
  }

  const dailyGenerate = stats.value.daily_generate || []
  const dailyEvaluate = stats.value.daily_evaluate || []

  const allDates = [...new Set([
    ...dailyGenerate.map(d => d.date),
    ...dailyEvaluate.map(d => d.date)
  ])].sort()

  const generateMap = {}
  dailyGenerate.forEach(d => { generateMap[d.date] = d.total_tokens })

  const evaluateMap = {}
  dailyEvaluate.forEach(d => { evaluateMap[d.date] = d.total_tokens })

  const option = {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      },
      formatter: function(params) {
        let result = params[0].axisValue + '<br/>'
        let total = 0
        params.forEach(p => {
          result += p.marker + p.seriesName + ': ' + (p.value || 0) + '<br/>'
          total += p.value || 0
        })
        result += '总计: ' + total
        return result
      }
    },
    legend: {
      data: ['搜索题目', '评判答案']
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: allDates,
      axisLabel: {
        rotate: 45
      }
    },
    yAxis: {
      type: 'value'
    },
    series: [
      {
        name: '搜索题目',
        type: 'bar',
        stack: 'total',
        data: allDates.map(d => generateMap[d] || 0),
        itemStyle: {
          color: '#409eff'
        }
      },
      {
        name: '评判答案',
        type: 'bar',
        stack: 'total',
        data: allDates.map(d => evaluateMap[d] || 0),
        itemStyle: {
          color: '#67c23a'
        }
      }
    ]
  }

  dailyChartInstance.setOption(option)
}

const renderTypeChart = () => {
  if (!typeChart.value) return

  if (!typeChartInstance) {
    typeChartInstance = echarts.init(typeChart.value)
  }

  const generateTokens = stats.value.generate?.total_tokens || 0
  const evaluateTokens = stats.value.evaluate?.total_tokens || 0

  const option = {
    tooltip: {
      trigger: 'item',
      formatter: function(params) {
        return params.name + '<br/>Token: ' + params.value + '<br/>占比: ' + params.percent + '%'
      }
    },
    legend: {
      orient: 'vertical',
      left: 'left'
    },
    series: [
      {
        name: 'Token消耗',
        type: 'pie',
        radius: ['40%', '70%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 10,
          borderColor: '#fff',
          borderWidth: 2
        },
        label: {
          show: true,
          formatter: '{b}\n{d}%'
        },
        data: [
          { value: generateTokens, name: '搜索题目', itemStyle: { color: '#409eff' } },
          { value: evaluateTokens, name: '评判答案', itemStyle: { color: '#67c23a' } }
        ]
      }
    ]
  }

  typeChartInstance.setOption(option)
}

onMounted(() => {
  loadStats()
  window.addEventListener('resize', () => {
    dailyChartInstance?.resize()
    typeChartInstance?.resize()
  })
})
</script>

<style scoped>
.token-stats-page {
  max-width: 1200px;
  margin: 0 auto;
}

.header-card {
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.header-card h2 {
  margin: 0;
}

.stats-cards {
  margin-bottom: 20px;
}

.stat-card {
  text-align: center;
  height: 140px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.stat-header {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  margin-bottom: 10px;
  font-size: 16px;
  font-weight: 500;
}

.stat-value {
  font-size: 28px;
  font-weight: bold;
  color: #303133;
}

.stat-label {
  color: #909399;
  margin-top: 5px;
}

.stat-detail {
  color: #909399;
  font-size: 12px;
  margin-top: 8px;
  display: flex;
  justify-content: center;
  gap: 15px;
}

.total-card .stat-value {
  color: #e6a23c;
}

.generate-card .stat-header {
  color: #409eff;
}

.generate-card .stat-value {
  color: #409eff;
}

.evaluate-card .stat-header {
  color: #67c23a;
}

.evaluate-card .stat-value {
  color: #67c23a;
}

.chart-container {
  height: 400px;
}

.recent-card {
  margin-top: 20px;
}

.token-input {
  color: #409eff;
}

.token-output {
  color: #67c23a;
}

.token-total {
  font-weight: bold;
  color: #e6a23c;
}
</style>
