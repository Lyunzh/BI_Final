<template>
<NavBar />
  
 <div class="app-header">
    <span class="app-title">新闻实时动态分析系统</span>
    <button class="clear-btn" @click="refreshAll">清除数据</button>
  </div>
  <router-view />
</template>

<script setup>
import NavBar from './components/NavBar.vue'
function refreshAll() {
  window.location.reload()
  alert('数据已清空！')
}
</script>
<style scoped>
.app-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #e3f2fd;
  padding: 18px 32px 10px 32px;
  border-bottom: 2px solid #1976d2;
}
.app-title {
  font-size: 2rem;
  font-weight: bold;
  color: #1976d2;
  letter-spacing: 2px;
}
.clear-btn {
  background: #1976d2;
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 8px 28px;
  font-size: 1.1rem;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s, box-shadow 0.2s;
  box-shadow: 0 2px 8px rgba(33, 150, 243, 0.08);
}
.clear-btn:hover {
  background: #1565c0;
  box-shadow: 0 4px 16px rgba(33, 150, 243, 0.18);
}
</style>