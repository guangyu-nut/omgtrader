<template>
  <section class="surface-card data-status-panel">
    <div class="surface-header">
      <div class="surface-header__copy">
        <p class="section-label">Data Status</p>
        <h2>数据状态</h2>
        <p class="subtle-copy">用覆盖范围和同步节奏判断本地行情是否足够支撑下一轮研究。</p>
      </div>
      <div class="status-pills">
        <span class="status-pill status-pill--positive">Ready Check</span>
      </div>
    </div>

    <div class="status-grid">
      <article class="status-grid__card">
        <span>最近更新时间</span>
        <strong>{{ lastUpdated }}</strong>
      </article>
      <article class="status-grid__card">
        <span>分钟线状态</span>
        <strong>待同步</strong>
      </article>
    </div>
  </section>
</template>

<script setup lang="ts">
defineProps<{
  lastUpdated: string;
}>();
</script>

<style scoped>
.data-status-panel {
  min-height: 100%;
}

.status-grid {
  display: grid;
  gap: 0.9rem;
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.status-grid__card {
  background: rgba(18, 32, 51, 0.03);
  border: 1px solid rgba(18, 32, 51, 0.06);
  border-radius: 1rem;
  display: grid;
  gap: 0.5rem;
  padding: 1rem;
}

.status-grid__card span {
  color: var(--text-muted);
  font-size: var(--text-sm);
}

.status-grid__card strong {
  font-family: var(--font-mono);
  font-size: 1.02rem;
}

@media (max-width: 640px) {
  .status-grid {
    grid-template-columns: 1fr;
  }
}
</style>
