<template>
  <div class="app">
    <aside class="sidebar">
      <div class="sidebar-logo">
        <h1>{{ t('nav.companyName') }}</h1>
        <span class="subtitle">{{ t('nav.subtitle') }}</span>
      </div>

      <nav class="sidebar-nav" aria-label="Main">
        <router-link
          to="/"
          :class="{ active: $route.path === '/' }"
          :aria-current="$route.path === '/' ? 'page' : null"
        >
          <svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">
            <rect x="3" y="3" width="7" height="7" rx="1.5" />
            <rect x="14" y="3" width="7" height="7" rx="1.5" />
            <rect x="3" y="14" width="7" height="7" rx="1.5" />
            <rect x="14" y="14" width="7" height="7" rx="1.5" />
          </svg>
          <span class="nav-label">{{ t('nav.overview') }}</span>
        </router-link>

        <router-link
          to="/inventory"
          :class="{ active: $route.path === '/inventory' }"
          :aria-current="$route.path === '/inventory' ? 'page' : null"
        >
          <svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">
            <path d="M21 8 12 3 3 8v8l9 5 9-5V8Z" />
            <path d="M3 8l9 5 9-5" />
            <path d="M12 13v8" />
          </svg>
          <span class="nav-label">{{ t('nav.inventory') }}</span>
        </router-link>

        <router-link
          to="/orders"
          :class="{ active: $route.path === '/orders' }"
          :aria-current="$route.path === '/orders' ? 'page' : null"
        >
          <svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">
            <rect x="5" y="4" width="14" height="17" rx="2" />
            <path d="M9 4V3h6v1" />
            <path d="M9 10h6M9 14h6M9 18h3" />
          </svg>
          <span class="nav-label">{{ t('nav.orders') }}</span>
        </router-link>

        <router-link
          to="/spending"
          :class="{ active: $route.path === '/spending' }"
          :aria-current="$route.path === '/spending' ? 'page' : null"
        >
          <svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">
            <rect x="3" y="6" width="18" height="12" rx="2" />
            <circle cx="12" cy="12" r="2.5" />
            <path d="M3 10h2M19 14h2" />
          </svg>
          <span class="nav-label">{{ t('nav.finance') }}</span>
        </router-link>

        <router-link
          to="/demand"
          :class="{ active: $route.path === '/demand' }"
          :aria-current="$route.path === '/demand' ? 'page' : null"
        >
          <svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">
            <path d="M3 17l6-6 4 4 8-8" />
            <path d="M15 7h6v6" />
          </svg>
          <span class="nav-label">{{ t('nav.demandForecast') }}</span>
        </router-link>

        <router-link
          to="/reports"
          :class="{ active: $route.path === '/reports' }"
          :aria-current="$route.path === '/reports' ? 'page' : null"
        >
          <svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">
            <path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8l-5-5Z" />
            <path d="M14 3v5h5" />
            <path d="M9 13h6M9 17h6" />
          </svg>
          <span class="nav-label">{{ t('nav.reports') }}</span>
        </router-link>
      </nav>

      <div class="sidebar-bottom">
        <LanguageSwitcher />
        <ProfileMenu
          @show-profile-details="showProfileDetails = true"
          @show-tasks="showTasks = true"
        />
      </div>
    </aside>

    <div class="shell">
      <header class="topbar">
        <h2 class="topbar-title">{{ pageTitle }}</h2>
        <FilterBar />
      </header>
      <main class="main-content">
        <router-view />
      </main>
    </div>

    <ProfileDetailsModal
      :is-open="showProfileDetails"
      @close="showProfileDetails = false"
    />

    <TasksModal
      :is-open="showTasks"
      :tasks="tasks"
      @close="showTasks = false"
      @add-task="addTask"
      @delete-task="deleteTask"
      @toggle-task="toggleTask"
    />
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { api } from './api'
import { useAuth } from './composables/useAuth'
import { useI18n } from './composables/useI18n'
import FilterBar from './components/FilterBar.vue'
import ProfileMenu from './components/ProfileMenu.vue'
import ProfileDetailsModal from './components/ProfileDetailsModal.vue'
import TasksModal from './components/TasksModal.vue'
import LanguageSwitcher from './components/LanguageSwitcher.vue'

export default {
  name: 'App',
  components: {
    FilterBar,
    ProfileMenu,
    ProfileDetailsModal,
    TasksModal,
    LanguageSwitcher
  },
  setup() {
    const { currentUser } = useAuth()
    const { t } = useI18n()
    const route = useRoute()
    const showProfileDetails = ref(false)
    const showTasks = ref(false)
    const apiTasks = ref([])

    // Top-bar title derived from the current route; reuses the same nav.* keys
    // as the sidebar so the title follows the active locale. Unknown paths
    // fall back to the Overview label.
    const pageTitle = computed(() => ({
      '/': t('nav.overview'),
      '/inventory': t('nav.inventory'),
      '/orders': t('nav.orders'),
      '/spending': t('nav.finance'),
      '/demand': t('nav.demandForecast'),
      '/reports': t('nav.reports')
    }[route.path] || t('nav.overview')))

    // Merge mock tasks from currentUser with API tasks
    const tasks = computed(() => {
      return [...currentUser.value.tasks, ...apiTasks.value]
    })

    const loadTasks = async () => {
      try {
        apiTasks.value = await api.getTasks()
      } catch (err) {
        console.error('Failed to load tasks:', err)
      }
    }

    const addTask = async (taskData) => {
      try {
        const newTask = await api.createTask(taskData)
        // Add new task to the beginning of the array
        apiTasks.value.unshift(newTask)
      } catch (err) {
        console.error('Failed to add task:', err)
      }
    }

    const deleteTask = async (taskId) => {
      try {
        // Check if it's a mock task (from currentUser)
        const isMockTask = currentUser.value.tasks.some(t => t.id === taskId)

        if (isMockTask) {
          // Remove from mock tasks
          const index = currentUser.value.tasks.findIndex(t => t.id === taskId)
          if (index !== -1) {
            currentUser.value.tasks.splice(index, 1)
          }
        } else {
          // Remove from API tasks
          await api.deleteTask(taskId)
          apiTasks.value = apiTasks.value.filter(t => t.id !== taskId)
        }
      } catch (err) {
        console.error('Failed to delete task:', err)
      }
    }

    const toggleTask = async (taskId) => {
      try {
        // Check if it's a mock task (from currentUser)
        const mockTask = currentUser.value.tasks.find(t => t.id === taskId)

        if (mockTask) {
          // Toggle mock task status
          mockTask.status = mockTask.status === 'pending' ? 'completed' : 'pending'
        } else {
          // Toggle API task
          const updatedTask = await api.toggleTask(taskId)
          const index = apiTasks.value.findIndex(t => t.id === taskId)
          if (index !== -1) {
            apiTasks.value[index] = updatedTask
          }
        }
      } catch (err) {
        console.error('Failed to toggle task:', err)
      }
    }

    onMounted(loadTasks)

    return {
      t,
      pageTitle,
      showProfileDetails,
      showTasks,
      tasks,
      addTask,
      deleteTask,
      toggleTask
    }
  }
}
</script>

<style>
/* ---------- Design tokens ---------- */
:root {
  --sidebar-w: 240px;
  --sidebar-bg: #0f172a;
  --sidebar-fg: #94a3b8;
  --sidebar-active: rgba(59, 130, 246, .15);
  --accent: #3b82f6;
  --content-bg: #f8fafc;
  --card-bg: #fff;
  --border: #e2e8f0;
  --text: #0f172a;
  --muted: #64748b;
  --radius: 12px;
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-5: 24px;
  --space-6: 32px;
}

/* ---------- Reset ---------- */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
  background: var(--content-bg);
  color: var(--text);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* ---------- App shell ---------- */
.app {
  display: flex;
  min-height: 100vh;
}

.sidebar {
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  width: var(--sidebar-w);
  background: var(--sidebar-bg);
  color: var(--sidebar-fg);
  display: flex;
  flex-direction: column;
  padding: var(--space-5) var(--space-3);
  z-index: 110;
  overflow: visible;
}

.sidebar-logo {
  padding: 0 var(--space-3) var(--space-5);
}

.sidebar-logo h1 {
  color: #fff;
  font-size: 1rem;
  font-weight: 700;
  letter-spacing: -.01em;
}

.sidebar-logo .subtitle {
  display: block;
  font-size: .75rem;
  color: var(--sidebar-fg);
  margin-top: 2px;
}

.sidebar-nav {
  display: flex;
  flex-direction: column;
  gap: 2px;
  flex: 1;
}

.sidebar-nav a {
  position: relative;
  display: flex;
  align-items: center;
  gap: var(--space-3);
  height: 40px;
  padding: 0 var(--space-3);
  border-radius: 10px;
  color: var(--sidebar-fg);
  text-decoration: none;
  font-size: .875rem;
  font-weight: 500;
  transition: background .15s, color .15s;
}

.sidebar-nav a svg {
  width: 20px;
  height: 20px;
  flex: none;
}

.sidebar-nav a:hover {
  background: rgba(255, 255, 255, .06);
  color: #fff;
}

.sidebar-nav a.active {
  background: var(--sidebar-active);
  color: #fff;
}

/* Blue rail flush with the sidebar edge (offset = sidebar horizontal padding) */
.sidebar-nav a.active::before {
  content: '';
  position: absolute;
  left: -12px;
  top: 8px;
  bottom: 8px;
  width: 3px;
  border-radius: 0 3px 3px 0;
  background: var(--accent);
}

.sidebar-nav a:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
}

.sidebar-bottom {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: var(--space-2);
  padding-top: var(--space-4);
  border-top: 1px solid rgba(255, 255, 255, .08);
}

/*
 * LanguageSwitcher / ProfileMenu ship white, light-theme scoped styles.
 * The selectors below are one level deeper than the components' own
 * `.x[data-v-*]` rules so they win on specificity regardless of CSS order.
 */
.sidebar .sidebar-bottom .language-button,
.sidebar .sidebar-bottom .profile-button {
  color: #e2e8f0;
  border-color: rgba(255, 255, 255, .12);
  background: transparent;
}

.sidebar .sidebar-bottom .language-button:hover,
.sidebar .sidebar-bottom .profile-button:hover {
  background: rgba(255, 255, 255, .06);
  border-color: rgba(255, 255, 255, .2);
}

.sidebar .sidebar-bottom .language-button:focus-visible,
.sidebar .sidebar-bottom .profile-button:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
}

.sidebar .sidebar-bottom .globe-icon,
.sidebar .sidebar-bottom .chevron {
  color: var(--sidebar-fg);
}

.sidebar .sidebar-bottom .profile-name {
  color: #e2e8f0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.sidebar .sidebar-bottom .profile-menu {
  min-width: 0;
}

/* Dropdowns sit at the viewport bottom here, so open them upward and anchor
 * to the left edge; the panels stay white (component styles untouched). */
.sidebar .sidebar-bottom .dropdown-menu {
  top: auto;
  bottom: calc(100% + var(--space-2));
  left: 0;
  right: auto;
}

.shell {
  flex: 1;
  margin-left: var(--sidebar-w);
  min-width: 0;
  display: flex;
  flex-direction: column;
}

.topbar {
  position: sticky;
  top: 0;
  z-index: 100;
  min-height: 64px;
  background: #fff;
  border-bottom: 1px solid var(--border);
  display: flex;
  align-items: center;
  gap: var(--space-5);
  padding: var(--space-2) var(--space-6);
  flex-wrap: wrap;
}

.topbar-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--text);
  letter-spacing: -.02em;
  white-space: nowrap;
}

.topbar .filters-bar {
  margin-left: auto;
}

.main-content {
  flex: 1;
  width: 100%;
  max-width: 1400px;
  padding: var(--space-6);
}

/* Views still render their own .page-header; the top bar shows the title
 * once, so hide the in-view duplicate. Prefixed with .shell so it out-ranks
 * scoped view rules such as Dashboard's `.page-header { display: flex }`. */
.shell .main-content > * > .page-header {
  display: none;
}

/* ---------- Shared page pieces ---------- */
.page-header {
  margin-bottom: 1.5rem;
}

.page-header h2 {
  font-size: 1.875rem;
  font-weight: 700;
  color: #0f172a;
  margin-bottom: 0.375rem;
  letter-spacing: -0.025em;
}

.page-header p {
  color: #64748b;
  font-size: 0.938rem;
}

.section-title {
  font-size: .8125rem;
  font-weight: 600;
  color: var(--muted);
  text-transform: uppercase;
  letter-spacing: .06em;
  margin: var(--space-5) 0 var(--space-3);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.25rem;
  margin-bottom: 1.5rem;
}

.card,
.stat-card,
.kpi-card {
  border-radius: var(--radius);
  padding: var(--space-5);
  border: 1px solid var(--border);
  background: var(--card-bg);
  box-shadow: 0 1px 2px rgba(15, 23, 42, .04);
}

.stat-card {
  transition: all 0.2s ease;
}

.stat-card:hover {
  border-color: #cbd5e1;
  box-shadow: 0 4px 12px rgba(15, 23, 42, .06);
}

.stat-label {
  color: #64748b;
  font-size: 0.875rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 0.625rem;
}

.stat-value {
  font-size: 2.25rem;
  font-weight: 700;
  color: #0f172a;
  letter-spacing: -0.025em;
}

.stat-card.warning .stat-value {
  color: #ea580c;
}

.stat-card.success .stat-value {
  color: #059669;
}

.stat-card.danger .stat-value {
  color: #dc2626;
}

.stat-card.info .stat-value {
  color: #2563eb;
}

.card {
  margin-bottom: 1.25rem;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding-bottom: 0.875rem;
  border-bottom: 1px solid #e2e8f0;
}

.card-title {
  font-size: 1.125rem;
  font-weight: 700;
  color: #0f172a;
  letter-spacing: -0.025em;
}

.table-container {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

thead {
  background: #f8fafc;
  border-top: 1px solid #e2e8f0;
  border-bottom: 1px solid #e2e8f0;
}

th {
  text-align: left;
  padding: 0.5rem 0.75rem;
  font-weight: 600;
  color: #475569;
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

td {
  padding: 0.5rem 0.75rem;
  border-top: 1px solid #f1f5f9;
  color: #334155;
  font-size: 0.875rem;
}

tbody tr {
  transition: background-color 0.15s ease;
}

tbody tr:hover {
  background: #f8fafc;
}

.badge {
  display: inline-block;
  padding: 0.313rem 0.75rem;
  border-radius: 6px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.025em;
}

.badge.success {
  background: #d1fae5;
  color: #065f46;
}

.badge.warning {
  background: #fed7aa;
  color: #92400e;
}

.badge.danger {
  background: #fecaca;
  color: #991b1b;
}

.badge.info {
  background: #dbeafe;
  color: #1e40af;
}

.badge.increasing {
  background: #d1fae5;
  color: #065f46;
}

.badge.decreasing {
  background: #fecaca;
  color: #991b1b;
}

.badge.stable {
  background: #e0e7ff;
  color: #3730a3;
}

.badge.high {
  background: #fecaca;
  color: #991b1b;
}

.badge.medium {
  background: #fed7aa;
  color: #92400e;
}

.badge.low {
  background: #dbeafe;
  color: #1e40af;
}

.loading {
  text-align: center;
  padding: 3rem;
  color: #64748b;
  font-size: 0.938rem;
}

.error {
  background: #fef2f2;
  border: 1px solid #fecaca;
  color: #991b1b;
  padding: 1rem;
  border-radius: 8px;
  margin: 1rem 0;
  font-size: 0.938rem;
}

/* ---------- Responsive ---------- */
@media (max-width: 1024px) {
  :root {
    --sidebar-w: 64px;
  }

  .sidebar {
    padding: var(--space-4) var(--space-2);
  }

  .sidebar-logo .subtitle,
  .sidebar-nav .nav-label {
    display: none;
  }

  .sidebar-logo {
    padding: 0 0 var(--space-4);
  }

  .sidebar-logo h1 {
    font-size: .75rem;
    text-align: center;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  .sidebar-nav a {
    justify-content: center;
    padding: 0;
  }

  .sidebar-nav a.active::before {
    left: -8px;
  }

  .sidebar-bottom {
    flex-direction: column;
  }

  /* Icon-only rail: collapse the two bottom buttons to their icon/avatar */
  .sidebar .sidebar-bottom .language-label,
  .sidebar .sidebar-bottom .profile-name,
  .sidebar .sidebar-bottom .chevron {
    display: none;
  }

  .sidebar .sidebar-bottom .language-button,
  .sidebar .sidebar-bottom .profile-button {
    padding: var(--space-2);
  }
}

@media (max-width: 768px) {
  .app {
    flex-direction: column;
  }

  .sidebar {
    position: static;
    width: 100%;
    flex-direction: row;
    align-items: center;
    padding: var(--space-2) var(--space-3);
  }

  .sidebar-logo {
    padding: 0 var(--space-3) 0 0;
  }

  .sidebar-nav {
    flex-direction: row;
    gap: 4px;
  }

  .sidebar-nav a.active::before {
    display: none;
  }

  .sidebar-bottom {
    flex-direction: row;
    border: 0;
    padding: 0;
    margin-left: auto;
  }

  /* Sidebar is a top drawer here: dropdowns open downward again */
  .sidebar .sidebar-bottom .dropdown-menu {
    top: calc(100% + var(--space-2));
    bottom: auto;
    right: 0;
    left: auto;
  }

  .shell {
    margin-left: 0;
  }

  .main-content {
    padding: var(--space-4);
  }
}
</style>
