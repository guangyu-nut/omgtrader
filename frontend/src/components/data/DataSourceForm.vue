<template>
  <section class="panel">
    <h2>添加数据源</h2>
    <label class="field">
      <span>名称</span>
      <input :value="name" @input="$emit('update:name', ($event.target as HTMLInputElement).value)" />
    </label>
    <label class="field">
      <span>类型</span>
      <select :value="providerType" @change="$emit('update:providerType', ($event.target as HTMLSelectElement).value)">
        <option value="free">免费源</option>
        <option value="token">Token 源</option>
      </select>
    </label>
    <button type="button" @click="$emit('submit')">保存数据源</button>
  </section>
</template>

<script setup lang="ts">
defineProps<{
  name: string;
  providerType: string;
}>();

defineEmits<{
  submit: [];
  "update:name": [value: string];
  "update:providerType": [value: string];
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
