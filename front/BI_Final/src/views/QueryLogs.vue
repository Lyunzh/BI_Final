<template>
   <div>
    <div class="query-bar">
      <v-card class="query-card" color="primary" dark>
        <v-row align="center" no-gutters>
          <v-col cols="12" md="3">
            <v-text-field v-model="keyword" label="SQL关键字" dense outlined color="white" />
          </v-col>
          <v-col cols="12" md="4">
            <v-menu v-model="menu" :close-on-content-click="false" transition="scale-transition" offset-y>
              <template #activator="{ on, attrs }">
                <v-text-field
                  v-model="dateRangeText"
                  label="时间范围"
                  readonly
                  v-bind="attrs"
                  v-on="on"
                  dense
                  outlined
                  color="white"
                />
              </template>
              <v-date-picker v-model="dateRange" range @change="menu = false" />
            </v-menu>
          </v-col>
          <v-col cols="12" md="2">
            <v-btn class="query-btn" color="white" text @click="query" :loading="loading">
              查询
            </v-btn>
          </v-col>
        </v-row>
      </v-card>
    </div>
    <v-card class="mt-4 content-card">
      <v-card-title>查询结果</v-card-title>
      <v-data-table :headers="tableHeaders" :items="tableData" dense />
    </v-card>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
const keyword = ref('')
const dateRange = ref([])
const menu = ref(false)
const loading = ref(false)
const tableData = ref([])
const tableHeaders = [
  { text: '查询时间', value: 'queryTime' },
  { text: 'SQL语句', value: 'sqlQuery' },
  { text: '耗时(ms)', value: 'duration' }
]
const dateRangeText = computed(() =>
  dateRange.value.length === 2 ? `${dateRange.value[0]} ~ ${dateRange.value[1]}` : ''
)

async function query() {
  loading.value = true
  setTimeout(() => {
    tableData.value = [
      { queryTime: '2023-06-01 10:00:00', sqlQuery: 'SELECT ...', duration: 120 },
      { queryTime: '2023-06-01 11:00:00', sqlQuery: 'SELECT ...', duration: 80 }
    ]
    loading.value = false
  }, 500)
}
</script>

<style scoped>
.query-bar {
  margin-top: 24px;
  margin-bottom: 16px;
}
.query-card {
  padding: 16px 24px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(33, 150, 243, 0.08);
}
.query-btn {
  width: 100%;
  font-weight: bold;
  font-size: 16px;
  background: #1976d2 !important;
  color: #fff !important;
  border-radius: 8px;
}
.content-card {
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(33, 150, 243, 0.08);
}
</style>