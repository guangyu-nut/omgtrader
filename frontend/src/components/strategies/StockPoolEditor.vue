<template>
  <section class="panel">
    <h2>股票池</h2>
    <label class="field">
      <span>股票池名称</span>
      <input :value="name" @input="$emit('update:name', ($event.target as HTMLInputElement).value)" />
    </label>
    <label class="field">
      <span>股票代码</span>
      <textarea :value="symbolsText" rows="4" @input="$emit('update:symbolsText', ($event.target as HTMLTextAreaElement).value)" />
    </label>
    <button type="button" @click="$emit('submit')">保存股票池</button>
  </section>
</template>

<script setup lang="ts">
defineProps<{
  name: string;
  symbolsText: string;
}>();

defineEmits<{
  submit: [];
  "update:name": [value: string];
  "update:symbolsText": [value: string];
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
