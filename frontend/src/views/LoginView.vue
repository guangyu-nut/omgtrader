<template>
  <main class="login-view">
    <h1>登录</h1>
    <form class="login-form" @submit.prevent="handleSubmit">
      <label class="field">
        <span>用户名</span>
        <input id="username" v-model="form.username" autocomplete="username" />
      </label>
      <label class="field">
        <span>密码</span>
        <input id="password" v-model="form.password" autocomplete="current-password" type="password" />
      </label>
      <button type="submit">登录</button>
      <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
    </form>
  </main>
</template>

<script setup lang="ts">
import { reactive, ref } from "vue";

import { authStore } from "../stores/auth";

const errorMessage = ref("");
const form = reactive({
  password: "",
  username: "",
});

async function handleSubmit() {
  errorMessage.value = "";

  try {
    await authStore.login({
      password: form.password,
      username: form.username,
    });
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : "登录失败";
  }
}
</script>

<style scoped>
.login-view {
  display: grid;
  gap: 0.75rem;
  padding: 2rem;
}

.login-form {
  display: grid;
  gap: 1rem;
  max-width: 20rem;
}

.field {
  display: grid;
  gap: 0.35rem;
}

.error {
  color: #b42318;
}
</style>
