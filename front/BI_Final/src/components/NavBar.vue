<template>
  <nav class="nav-bar">
    <RouterLink
      v-for="item in navItems"
      :key="item.path"
      :to="item.path"
      class="nav-block"
      :class="{ active: $route.path === item.path }"
    >
      {{ item.label }}
    </RouterLink>
  </nav>
</template>

<script setup>
import { useRoute } from 'vue-router'
const $route = useRoute()
const navItems = [
  { path: '/news-lifecycle', label: '新闻生命周期' },
  { path: '/category-stats', label: '分类变化统计' },
  { path: '/user-interest', label: '用户兴趣画像' },
  { path: '/news-recommend', label: '实时新闻推荐' },
  { path: '/query-logs', label: '查询日志' },
  { path: '/advanced-query', label: '高级多条件查询' }
]
</script>

<style scoped>
.nav-bar {
  display: flex;
  justify-content: center;
  align-items: center;
  background: #f5faff;
  padding: 0.5rem 0;
  border-bottom: 1.5px solid #e3eaf5;
  gap: 18px;
}
.nav-block {
  background: #e3f2fd;
  color: #1976d2;
  font-size: 18px;
  font-weight: 500;
  padding: 10px 28px;
  border-radius: 8px;
  text-decoration: none;
  transition: background 0.2s, color 0.2s, box-shadow 0.2s;
  box-shadow: 0 1px 4px rgba(33, 150, 243, 0.06);
  letter-spacing: 1px;
}
.nav-block:hover,
.nav-block.active {
  background: #1976d2;
  color: #fff;
  box-shadow: 0 2px 8px rgba(33, 150, 243, 0.12);
}
</style>