<template>
  <section class="surface-card backtest-launch-card">
    <div class="surface-header">
      <div class="surface-header__copy">
        <p class="section-label">Launch Action</p>
        <h2>发起回测</h2>
        <p class="subtle-copy">当前仍使用策略实例 ID 发起旧回测链路，适合作为视觉重构阶段的稳定入口。</p>
      </div>
      <div class="status-pills">
        <span class="status-pill status-pill--signal">Legacy Input</span>
      </div>
    </div>

    <label class="field-stack">
      <span class="field-label">策略实例 ID</span>
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
.backtest-launch-card {
  min-height: 100%;
}
</style>
