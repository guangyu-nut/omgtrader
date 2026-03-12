<template>
  <section class="panel">
    <div class="panel-header">
      <div>
        <h2>Python 策略</h2>
        <p>浏览与管理你的 Python 策略资产。</p>
      </div>
      <button type="button" @click="$emit('create')">新建 Python 策略</button>
    </div>

    <label class="field">
      <span>搜索</span>
      <input
        :value="query"
        placeholder="搜索策略"
        @input="$emit('update:query', ($event.target as HTMLInputElement).value)"
      />
    </label>

    <div v-if="items.length === 0" class="empty-state">
      <p>创建第一条 Python 策略</p>
    </div>

    <div v-else class="list">
      <button
        v-for="item in items"
        :key="item.id"
        :class="['list-item', { 'is-active': item.id === selectedId }]"
        type="button"
        @click="$emit('select', item.id)"
      >
        <strong>{{ item.name }}</strong>
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
</script>

<style scoped>
.panel {
  border: 1px solid #d0d5dd;
  border-radius: 1rem;
  display: grid;
  gap: 1rem;
  padding: 1rem;
}

.panel-header {
  display: flex;
  gap: 1rem;
  justify-content: space-between;
}

.panel-header h2,
.panel-header p {
  margin: 0;
}

.panel-header p {
  color: #475467;
  font-size: 0.9rem;
  margin-top: 0.35rem;
}

.field {
  display: grid;
  gap: 0.35rem;
}

.list {
  display: grid;
  gap: 0.75rem;
}

.list-item {
  background: #ffffff;
  border: 1px solid #d0d5dd;
  border-radius: 0.9rem;
  display: grid;
  gap: 0.35rem;
  padding: 0.85rem;
  text-align: left;
}

.list-item.is-active {
  border-color: #0f62fe;
  box-shadow: 0 0 0 1px #0f62fe inset;
}

.list-item strong,
.list-item p,
.list-item small {
  margin: 0;
}

.list-item p,
.list-item small,
.empty-state {
  color: #475467;
}
</style>
