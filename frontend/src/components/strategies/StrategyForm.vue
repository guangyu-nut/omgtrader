<template>
  <section class="panel">
    <h2>Top N 等权轮动</h2>
    <label class="field">
      <span>策略名称</span>
      <input :value="name" @input="$emit('update:name', ($event.target as HTMLInputElement).value)" />
    </label>
    <label class="field">
      <span>持仓数量</span>
      <input :value="holdCount" min="1" type="number" @input="$emit('update:holdCount', Number(($event.target as HTMLInputElement).value))" />
    </label>
    <button type="button" @click="$emit('submit')">创建策略</button>
  </section>
</template>

<script setup lang="ts">
defineProps<{
  holdCount: number;
  name: string;
}>();

defineEmits<{
  submit: [];
  "update:holdCount": [value: number];
  "update:name": [value: string];
}>();
</script>

<style scoped>
.panel {
  border: 1px solid #d0d5dd;
  border-radius: 0.75rem;
  display: grid;
  gap: 0.75rem;
  padding: 1rem;
}

.field {
  display: grid;
  gap: 0.35rem;
}
</style>
