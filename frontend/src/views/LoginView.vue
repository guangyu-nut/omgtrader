<template>
  <main class="login-view">
    <section class="login-hero">
      <div class="status-pills">
        <span class="status-pill status-pill--active">本地运行</span>
        <span class="status-pill">轻量部署</span>
        <span class="status-pill status-pill--signal">Python 策略</span>
      </div>
      <p class="eyebrow">A 股量化研究终端</p>
      <h1>在本地完成数据、策略、回测与复盘。</h1>
      <p class="login-hero__intro">
        统一管理行情、Python 策略资产和回测结果，用更接近桌面研究终端的方式推进你的量化实验。
      </p>
      <div class="login-hero__signals">
        <article class="signal-card">
          <p class="section-label">Data Layer</p>
          <strong>日线 / 分钟线</strong>
          <span>内置数据接入、覆盖范围追踪、同步任务可视化。</span>
        </article>
        <article class="signal-card signal-card--terminal">
          <p class="section-label">Strategy Layer</p>
          <strong>Python 策略资产</strong>
          <span>先把策略写好、保存好，再逐步接入回测执行能力。</span>
        </article>
      </div>
    </section>

    <section class="login-card surface-card">
      <div class="login-card__header">
        <p class="eyebrow">Local Access</p>
        <h2>登录工作台</h2>
        <p class="subtle-copy">使用本地账户进入当前研究工作区。</p>
      </div>

      <form class="login-form" @submit.prevent="handleSubmit">
        <label class="field-stack">
          <span class="field-label">用户名</span>
          <input id="username" v-model="form.username" autocomplete="username" />
        </label>
        <label class="field-stack">
          <span class="field-label">密码</span>
          <input id="password" v-model="form.password" autocomplete="current-password" type="password" />
        </label>
        <button type="submit">登录</button>
        <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
      </form>
    </section>
  </main>
</template>

<script setup lang="ts">
import { reactive, ref } from "vue";

import { router } from "../router";
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
    await router.push("/workbench");
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : "登录失败";
  }
}
</script>

<style scoped>
.login-view {
  display: grid;
  grid-template-columns: minmax(0, 1.2fr) minmax(22rem, 26rem);
  gap: var(--space-6);
  min-height: 100vh;
  padding: clamp(1.25rem, 3vw, 2.5rem);
}

.login-hero {
  align-content: start;
  background:
    linear-gradient(145deg, rgba(255, 255, 255, 0.65) 0%, rgba(233, 239, 247, 0.85) 100%);
  border: 1px solid rgba(18, 32, 51, 0.08);
  border-radius: 1.8rem;
  box-shadow: var(--shadow-panel);
  display: grid;
  gap: var(--space-4);
  overflow: hidden;
  padding: clamp(1.6rem, 3vw, 2.8rem);
  position: relative;
}

.login-hero::after {
  content: "";
  inset: auto -6rem -6rem auto;
  position: absolute;
  width: 18rem;
  height: 18rem;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(255, 141, 77, 0.26), transparent 70%);
  pointer-events: none;
}

.login-hero h1 {
  font-size: clamp(2.35rem, 4vw, 4.5rem);
  letter-spacing: -0.05em;
  line-height: 0.95;
  margin: 0;
  max-width: 12ch;
}

.login-hero__intro {
  color: var(--text-secondary);
  margin: 0;
  max-width: 42rem;
}

.login-hero__signals {
  display: grid;
  gap: var(--space-4);
  grid-template-columns: repeat(2, minmax(0, 1fr));
  margin-top: auto;
}

.signal-card {
  background: rgba(255, 255, 255, 0.64);
  border: 1px solid rgba(18, 32, 51, 0.08);
  border-radius: 1.35rem;
  display: grid;
  gap: var(--space-2);
  min-height: 11rem;
  padding: var(--space-5);
}

.signal-card strong {
  font-size: 1.15rem;
}

.signal-card span {
  color: var(--text-muted);
  font-size: var(--text-sm);
  line-height: 1.7;
}

.signal-card--terminal {
  background:
    linear-gradient(180deg, rgba(30, 45, 68, 0.85) 0%, rgba(15, 23, 36, 0.96) 100%);
  border-color: rgba(173, 196, 229, 0.12);
  color: var(--text-on-dark);
}

.signal-card--terminal .section-label,
.signal-card--terminal span {
  color: var(--text-on-dark-muted);
}

.login-card {
  align-self: center;
  gap: var(--space-5);
  max-width: 26rem;
  width: 100%;
}

.login-card__header {
  display: grid;
  gap: var(--space-2);
}

.login-card__header h2 {
  font-size: 1.8rem;
  letter-spacing: -0.04em;
  margin: 0;
}

.login-form {
  display: grid;
  gap: var(--space-4);
}

.error {
  color: #b45309;
  font-size: var(--text-sm);
  margin: 0;
}

@media (max-width: 900px) {
  .login-view {
    grid-template-columns: 1fr;
  }

  .login-hero__signals {
    grid-template-columns: 1fr;
  }

  .login-card {
    max-width: none;
  }
}
</style>
