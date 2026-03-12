<template>
  <section class="panel">
    <h2>策略总结</h2>
    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
    <template v-else-if="insight">
      <p>{{ insight.summary }}</p>
      <ul>
        <li v-for="risk in insight.risks" :key="risk">{{ risk }}</li>
      </ul>
    </template>
    <p v-else>AI 正在生成解读...</p>
  </section>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";

import { generateInsight, type AiInsight } from "../../api/ai";

const props = defineProps<{
  jobId: string;
}>();

const errorMessage = ref("");
const insight = ref<AiInsight | null>(null);

onMounted(async () => {
  try {
    insight.value = await generateInsight(props.jobId);
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : "生成 AI 解读失败";
  }
});
</script>

<style scoped>
.panel {
  border: 1px solid #d0d5dd;
  border-radius: 0.75rem;
  display: grid;
  gap: 0.75rem;
  padding: 1rem;
}

.error {
  color: #b42318;
}
</style>
