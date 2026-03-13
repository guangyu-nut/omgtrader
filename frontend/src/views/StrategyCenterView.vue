<template>
  <main class="page-shell strategy-center-view">
    <header class="page-header">
      <p class="eyebrow">Python Lab</p>
      <h1>Python 策略工作台</h1>
      <p class="page-intro">
        把 Python 策略当成研究资产来维护，先完成列表、详情和代码保存，再逐步接入执行能力。
      </p>
    </header>

    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>

    <section class="panel-grid panel-grid--three">
      <article class="surface-card surface-card--muted strategy-summary-card">
        <p class="section-label">Assets</p>
        <strong>{{ pythonStrategyStore.items.length }} 条策略资产</strong>
        <span>列表视图专注管理已保存的 Python 策略，适合作为研究入口。</span>
      </article>
      <article class="surface-card strategy-summary-card">
        <p class="section-label">Search</p>
        <strong>{{ filteredStrategies.length }} 条当前结果</strong>
        <span>通过搜索快速切换到目标策略，避免在资产列表里来回跳转。</span>
      </article>
      <article class="surface-card strategy-summary-card strategy-summary-card--signal">
        <p class="section-label">Mode</p>
        <strong>{{ editorMode === "draft" ? "Draft" : editorMode === "edit" ? "Editing" : "Idle" }}</strong>
        <span>代码编辑区保持独立深色终端语气，突出策略写作和参数说明。</span>
      </article>
    </section>

    <section class="layout">
      <PythonStrategyListPanel
        v-model:query="searchText"
        :items="filteredStrategies"
        :selected-id="pythonStrategyStore.selectedId"
        @create="startDraft"
        @select="selectStrategy"
      />
      <PythonStrategyEditor
        :model-value="editorState"
        :mode="editorMode"
        @delete="handleDelete"
        @reset="resetEditorState"
        @save="handleSave"
        @update:model-value="handleEditorChange"
      />
    </section>
  </main>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from "vue";

import type { PythonStrategyDetail, PythonStrategyPayload } from "../api/pythonStrategies";
import PythonStrategyEditor from "../components/strategies/PythonStrategyEditor.vue";
import PythonStrategyListPanel from "../components/strategies/PythonStrategyListPanel.vue";
import { pythonStrategyStore } from "../stores/pythonStrategies";


type EditorState = {
  id: string;
  name: string;
  description: string;
  tagsText: string;
  parameterSchemaText: string;
  code: string;
};


const DEFAULT_CODE = `class Strategy:
    def build_signals(self, context):
        return []
`;

const errorMessage = ref("");
const searchText = ref("");
const editorState = ref<EditorState | null>(null);
const savedSnapshot = ref("");

const editorMode = computed<"empty" | "draft" | "edit">(() => {
  if (editorState.value === null) {
    return "empty";
  }

  return editorState.value.id ? "edit" : "draft";
});

const filteredStrategies = computed(() => {
  const query = searchText.value.trim().toLowerCase();
  if (!query) {
    return pythonStrategyStore.items;
  }

  return pythonStrategyStore.items.filter((item) =>
    [item.name, item.description, item.tags.join(" ")].join(" ").toLowerCase().includes(query),
  );
});

onMounted(async () => {
  await loadInitialState();
});

async function loadInitialState() {
  errorMessage.value = "";

  try {
    const items = await pythonStrategyStore.loadList();
    if (items.length === 0) {
      pythonStrategyStore.clearSelection();
      setPersistedEditorState(null);
      return;
    }

    await selectStrategy(items[0].id, true);
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : "加载策略中心失败";
  }
}

async function selectStrategy(strategyId: string, force = false) {
  if (!force && !confirmDiscardChanges()) {
    return;
  }

  errorMessage.value = "";

  try {
    const strategy = await pythonStrategyStore.selectStrategy(strategyId);
    setPersistedEditorState(toEditorState(strategy));
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : "加载策略详情失败";
  }
}

function startDraft() {
  if (!confirmDiscardChanges()) {
    return;
  }

  pythonStrategyStore.clearSelection();
  setPersistedEditorState(createDraftState());
}

async function handleSave() {
  if (editorState.value === null) {
    return;
  }

  errorMessage.value = "";

  try {
    const saved = await pythonStrategyStore.saveStrategy(toPayload(editorState.value));
    setPersistedEditorState(toEditorState(saved));
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : "保存 Python 策略失败";
  }
}

async function handleDelete() {
  if (editorState.value === null || !editorState.value.id) {
    return;
  }

  if (!window.confirm("确定删除当前 Python 策略吗？")) {
    return;
  }

  errorMessage.value = "";

  try {
    const next = await pythonStrategyStore.removeStrategy(editorState.value.id);
    setPersistedEditorState(next ? toEditorState(next) : null);
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : "删除 Python 策略失败";
  }
}

async function resetEditorState() {
  if (editorState.value === null) {
    return;
  }

  if (!editorState.value.id) {
    setPersistedEditorState(createDraftState());
    return;
  }

  await selectStrategy(editorState.value.id, true);
}

function createDraftState(): EditorState {
  return {
    id: "",
    name: "My Python Strategy",
    description: "",
    tagsText: "",
    parameterSchemaText: "",
    code: DEFAULT_CODE,
  };
}

function toEditorState(strategy: PythonStrategyDetail): EditorState {
  return {
    id: strategy.id,
    name: strategy.name,
    description: strategy.description,
    tagsText: strategy.tags.join(", "),
    parameterSchemaText: strategy.parameter_schema_text,
    code: strategy.code,
  };
}

function toPayload(state: EditorState): PythonStrategyPayload & { id?: string } {
  return {
    id: state.id || undefined,
    name: state.name,
    description: state.description,
    tags: state.tagsText
      .split(",")
      .map((tag) => tag.trim())
      .filter(Boolean),
    parameter_schema_text: state.parameterSchemaText,
    code: state.code,
  };
}

function handleEditorChange(value: EditorState) {
  editorState.value = value;
}

function setPersistedEditorState(value: EditorState | null) {
  editorState.value = value;
  savedSnapshot.value = serializeEditorState(value);
}

function confirmDiscardChanges() {
  if (!isDirty()) {
    return true;
  }

  return window.confirm("当前策略有未保存修改，确定要离开吗？");
}

function isDirty() {
  return serializeEditorState(editorState.value) !== savedSnapshot.value;
}

function serializeEditorState(value: EditorState | null) {
  return JSON.stringify(value);
}
</script>

<style scoped>
.strategy-center-view {
  padding: var(--space-3) 0 var(--space-7);
}

.layout {
  display: grid;
  gap: var(--space-5);
  grid-template-columns: minmax(18rem, 24rem) minmax(0, 1fr);
}

.error {
  color: #b45309;
  margin: 0;
}

.strategy-summary-card {
  min-height: 10.5rem;
}

.strategy-summary-card strong {
  font-size: 1.15rem;
}

.strategy-summary-card span {
  color: var(--text-muted);
  font-size: var(--text-sm);
}

.strategy-summary-card--signal {
  background:
    linear-gradient(135deg, rgba(123, 176, 255, 0.16) 0%, rgba(16, 23, 36, 0.02) 60%),
    var(--bg-panel);
}

@media (max-width: 980px) {
  .layout {
    grid-template-columns: 1fr;
  }
}
</style>
