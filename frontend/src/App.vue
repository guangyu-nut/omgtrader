<template>
  <RouterView v-slot="{ Component }">
    <AppShell v-if="showShell" data-testid="shell-container">
      <component :is="Component" />
    </AppShell>
    <component :is="Component" v-else />
  </RouterView>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { useRoute } from "vue-router";

import AppShell from "./components/app/AppShell.vue";

const route = useRoute();
const showShell = computed(() => route.meta.shell === true);
</script>
