<template>
  <section class="surface-card data-source-form">
    <div class="surface-header">
      <div class="surface-header__copy">
        <p class="section-label">Source Config</p>
        <h2>添加数据源</h2>
        <p class="subtle-copy">先配置接入方式，再让同步任务去追踪拉取和更新状态。</p>
      </div>
      <div class="status-pills">
        <span class="status-pill">Free / Token</span>
      </div>
    </div>

    <label class="field-stack">
      <span class="field-label">名称</span>
      <input :value="name" @input="$emit('update:name', ($event.target as HTMLInputElement).value)" />
    </label>
    <label class="field-stack">
      <span class="field-label">类型</span>
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
.data-source-form {
  min-height: 100%;
}
</style>
