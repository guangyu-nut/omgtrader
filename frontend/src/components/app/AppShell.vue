<template>
  <div class="app-shell">
    <aside class="app-shell-sidebar" data-testid="app-sidebar">
      <div class="app-shell-brand">
        <p class="eyebrow app-shell-eyebrow">Local Mode</p>
        <h1>OMGTrader</h1>
        <p class="app-shell-summary">A 股量化研究工作台</p>
        <div class="status-pills">
          <span class="status-pill">macOS Workspace</span>
          <span class="status-pill status-pill--signal">Single User</span>
        </div>
      </div>

      <nav class="app-shell-nav">
        <RouterLink
          v-for="item in navItems"
          :key="item.name"
          :class="['app-shell-link', { 'is-active': route.name === item.name }]"
          :data-route-name="item.name"
          :to="item.to"
        >
          <span class="app-shell-link__label">{{ item.label }}</span>
          <span class="app-shell-link__meta">{{ item.meta }}</span>
        </RouterLink>
      </nav>

      <div class="app-shell-status">
        <p class="section-label">Research Node</p>
        <strong>本地研究环境</strong>
        <span>所有数据、策略与结果均保存在当前工作区。</span>
      </div>
    </aside>

    <section class="app-shell-content">
      <div class="app-shell-content__inner">
        <slot />
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { useRoute } from "vue-router";

const route = useRoute();

const navItems = [
  { label: "工作台", meta: "Overview", name: "workbench", to: "/workbench" },
  { label: "数据中心", meta: "Data Ops", name: "data-center", to: "/data-center" },
  { label: "策略中心", meta: "Python Lab", name: "strategy-center", to: "/strategy-center" },
  { label: "回测中心", meta: "Launch Desk", name: "backtests", to: "/backtests" },
];
</script>

<style scoped>
.app-shell {
  display: grid;
  grid-template-columns: minmax(16rem, 18.5rem) minmax(0, 1fr);
  gap: var(--space-5);
  min-height: 100vh;
  padding: var(--space-5);
}

.app-shell-sidebar {
  background:
    linear-gradient(180deg, rgba(32, 47, 72, 0.94) 0%, rgba(18, 28, 44, 0.98) 100%);
  border: 1px solid rgba(173, 196, 229, 0.14);
  border-radius: 1.75rem;
  box-shadow: var(--shadow-shell);
  display: grid;
  align-content: start;
  gap: var(--space-6);
  grid-template-rows: auto auto 1fr;
  overflow: hidden;
  padding: var(--space-6);
  position: sticky;
  top: 0;
}

.app-shell-brand {
  display: grid;
  gap: var(--space-3);
}

.app-shell-eyebrow {
  color: var(--accent-active);
}

.app-shell-brand h1 {
  color: var(--text-on-dark);
  font-size: 1.6rem;
  letter-spacing: -0.04em;
  margin: 0;
}

.app-shell-summary {
  color: var(--text-on-dark-muted);
  font-size: var(--text-sm);
  margin: 0;
}

.app-shell-nav {
  display: grid;
  gap: 0.7rem;
}

.app-shell-link {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(173, 196, 229, 0.08);
  border-radius: 1.2rem;
  display: grid;
  gap: 0.15rem;
  padding: 0.95rem 1rem;
  text-decoration: none;
  transition:
    transform 160ms ease,
    border-color 160ms ease,
    background 160ms ease;
}

.app-shell-link:hover {
  border-color: rgba(123, 176, 255, 0.26);
  transform: translateX(2px);
}

.app-shell-link__label {
  color: var(--text-on-dark);
  font-size: 0.98rem;
  font-weight: 700;
}

.app-shell-link__meta {
  color: var(--text-on-dark-muted);
  font-family: var(--font-mono);
  font-size: 0.74rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.app-shell-link.is-active {
  background:
    linear-gradient(135deg, rgba(123, 176, 255, 0.22) 0%, rgba(255, 141, 77, 0.1) 100%);
  border-color: rgba(123, 176, 255, 0.36);
  box-shadow: inset 0 0 0 1px rgba(123, 176, 255, 0.18);
}

.app-shell-status {
  align-self: end;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(173, 196, 229, 0.08);
  border-radius: 1.25rem;
  color: var(--text-on-dark-muted);
  display: grid;
  gap: var(--space-2);
  padding: var(--space-4);
}

.app-shell-status strong {
  color: var(--text-on-dark);
  font-size: var(--text-sm);
}

.app-shell-status span {
  font-size: 0.82rem;
  line-height: 1.6;
}

.app-shell-content {
  min-width: 0;
  padding: var(--space-4) 0;
}

.app-shell-content__inner {
  margin: 0 auto;
  max-width: 96rem;
  min-height: calc(100vh - (2 * var(--space-5)));
}

@media (max-width: 900px) {
  .app-shell {
    grid-template-columns: 1fr;
    padding: var(--space-3);
  }

  .app-shell-sidebar {
    gap: var(--space-4);
    position: static;
  }

  .app-shell-nav {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .app-shell-status {
    display: none;
  }
}
</style>
