<template>
  <div class="app-shell">
    <aside class="sidebar" data-testid="app-sidebar">
      <div class="brand">
        <h1>OMGTrader</h1>
        <p>A 股量化研究工作台</p>
      </div>

      <nav class="nav">
        <RouterLink
          v-for="item in navItems"
          :key="item.name"
          :class="['nav-link', { 'is-active': route.name === item.name }]"
          :data-route-name="item.name"
          :to="item.to"
        >
          {{ item.label }}
        </RouterLink>
      </nav>
    </aside>

    <section class="content">
      <slot />
    </section>
  </div>
</template>

<script setup lang="ts">
import { useRoute } from "vue-router";

const route = useRoute();

const navItems = [
  { label: "工作台", name: "workbench", to: "/workbench" },
  { label: "数据中心", name: "data-center", to: "/data-center" },
  { label: "策略中心", name: "strategy-center", to: "/strategy-center" },
  { label: "回测中心", name: "backtests", to: "/backtests" },
];
</script>

<style scoped>
.app-shell {
  display: grid;
  grid-template-columns: 240px minmax(0, 1fr);
  min-height: 100vh;
}

.sidebar {
  background: linear-gradient(180deg, #f5f8ff 0%, #eef4f7 100%);
  border-right: 1px solid #d0d5dd;
  display: grid;
  align-content: start;
  gap: 1.5rem;
  padding: 1.5rem 1rem;
}

.brand {
  display: grid;
  gap: 0.35rem;
}

.brand h1,
.brand p {
  margin: 0;
}

.brand h1 {
  font-size: 1.1rem;
}

.brand p {
  color: #475467;
  font-size: 0.9rem;
}

.nav {
  display: grid;
  gap: 0.5rem;
}

.nav-link {
  border-radius: 0.75rem;
  color: #344054;
  padding: 0.75rem 0.9rem;
  text-decoration: none;
}

.nav-link.is-active {
  background: #0f62fe;
  color: #ffffff;
}

.content {
  min-width: 0;
}

@media (max-width: 900px) {
  .app-shell {
    grid-template-columns: 1fr;
  }

  .sidebar {
    border-bottom: 1px solid #d0d5dd;
    border-right: none;
  }

  .nav {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}
</style>
