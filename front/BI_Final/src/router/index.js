import { createRouter, createWebHistory } from 'vue-router'
import NewsLifecycle from '../views/NewsLifecycle.vue'
import CategoryStats from '../views/CategoryStats.vue'
import UserInterest from '../views/UserInterest.vue'
import NewsRecommend from '../views/NewsRecommend.vue'
import QueryLogs from '../views/QueryLogs.vue'
import AdvancedQuery from '../views/AdvancedQuery.vue'

const routes = [
  { path: '/', redirect: '/news-lifecycle' },
  { path: '/news-lifecycle', component: NewsLifecycle },
  { path: '/category-stats', component: CategoryStats },
  { path: '/user-interest', component: UserInterest },
  { path: '/news-recommend', component: NewsRecommend },
  { path: '/query-logs', component: QueryLogs },
  { path: '/advanced-query', component: AdvancedQuery },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router