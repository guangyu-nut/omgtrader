<template>
  <section class="panel">
    <h2>发起回测</h2>
    <label class="field">
      <span>策略实例 ID</span>
      <input
        :value="strategyInstanceId"
        placeholder="输入策略实例 ID"
        @input="$emit('update:strategyInstanceId', ($event.target as HTMLInputElement).value)"
      />
    </label>
    <button type="button" @click="$emit('launch')">开始回测</button>
  </section>
</template>

<script setup lang="ts">
defineProps<{
  strategyInstanceId: string;
}>();

defineEmits<{
  launch: [];
  "update:strategyInstanceId": [value: string];
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
