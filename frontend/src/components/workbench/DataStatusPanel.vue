<template>
  <section class="panel">
    <h2>数据状态</h2>
    <p>最近更新时间</p>
    <p>{{ lastUpdated }}</p>
  </section>
</template>

<script setup lang="ts">
defineProps<{
  lastUpdated: string;
}>();
</script>

<style scoped>
.panel {
  border: 1px solid #d0d5dd;
  border-radius: 0.75rem;
  display: grid;
  gap: 0.5rem;
  padding: 1rem;
}
</style>
