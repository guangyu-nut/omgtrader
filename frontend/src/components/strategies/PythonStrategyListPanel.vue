<template>
  <section class="surface-card strategy-list-panel">
    <div class="surface-header strategy-list-panel__header">
      <div class="surface-header__copy">
        <p class="section-label">Strategy Directory</p>
        <h2>Python 策略</h2>
        <p class="subtle-copy">浏览、搜索并切换你的 Python 策略资产，右侧保持单页编辑工作流。</p>
      </div>
      <div class="status-pills">
        <span class="status-pill status-pill--active">{{ items.length }} Assets</span>
      </div>
      <button type="button" @click="$emit('create')">新建 Python 策略</button>
    </div>

    <label class="field-stack">
      <span class="field-label">搜索</span>
      <input
        :value="query"
        placeholder="搜索策略"
        @input="$emit('update:query', ($event.target as HTMLInputElement).value)"
      />
    </label>

    <div v-if="items.length === 0" class="empty-state">
      <div class="empty-state__copy">
        <strong>创建第一条 Python 策略</strong>
        <p>先保存一份策略说明和代码骨架，后续再把执行能力接上去。</p>
      </div>
    </div>

    <div v-else class="list">
      <button
        v-for="item in items"
        :key="item.id"
        :class="['list-item', { 'is-active': item.id === selectedId }]"
        type="button"
        @click="$emit('select', item.id)"
      >
        <div class="list-item__header">
          <strong>{{ item.name }}</strong>
          <span class="list-item__timestamp">{{ formatTimestamp(item.updated_at) }}</span>
        </div>
        <p>{{ item.description || "暂无说明" }}</p>
        <small>{{ item.tags.join(" / ") || "未打标签" }}</small>
      </button>
    </div>
  </section>
</template>

<script setup lang="ts">
import type { PythonStrategyListItem } from "../../api/pythonStrategies";

defineProps<{
  items: PythonStrategyListItem[];
  query: string;
  selectedId: string;
}>();

defineEmits<{
  create: [];
  select: [strategyId: string];
  "update:query": [value: string];
}>();

function formatTimestamp(value: string) {
  return value.replace("T", " ").slice(0, 16);
}
</script>

<style scoped>
.strategy-list-panel {
  display: grid;
  min-height: 100%;
}

.list {
  display: grid;
  gap: 0.9rem;
}

.list-item {
  align-items: start;
  background: rgba(18, 32, 51, 0.03);
  border: 1px solid rgba(18, 32, 51, 0.06);
  border-radius: 1rem;
  display: grid;
  gap: 0.4rem;
  min-height: 7.2rem;
  padding: 1rem;
  text-align: left;
}

.list-item.is-active {
  background:
    linear-gradient(135deg, rgba(123, 176, 255, 0.18) 0%, rgba(255, 141, 77, 0.08) 100%);
  border-color: rgba(59, 130, 246, 0.22);
  box-shadow: 0 0 0 1px rgba(59, 130, 246, 0.14) inset;
}

.list-item__header {
  display: flex;
  gap: var(--space-3);
  justify-content: space-between;
}

.list-item__timestamp {
  color: var(--text-muted);
  font-family: var(--font-mono);
  font-size: 0.72rem;
}

.list-item strong,
.list-item p,
.list-item small {
  margin: 0;
}

.list-item p,
.list-item small {
  color: var(--text-muted);
}

.empty-state__copy {
  display: grid;
  gap: var(--space-2);
}

.empty-state__copy strong,
.empty-state__copy p {
  margin: 0;
}

.empty-state__copy p {
  color: var(--text-muted);
}
</style>
