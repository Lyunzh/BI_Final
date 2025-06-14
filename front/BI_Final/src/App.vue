<template>
<NavBar />
  <router-view />
  <v-app>
    <v-app-bar color="primary" dark>
      <v-toolbar-title>新闻实时动态分析系统</v-toolbar-title>
      <v-spacer />
      <v-btn icon @click="refreshAll"><v-icon>mdi-refresh</v-icon></v-btn>
    </v-app-bar>
    <v-main>
      <v-container fluid>
        <router-view />
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import NavBar from './components/NavBar.vue'
function refreshAll() {
  window.location.reload()
}
</script>