<template>
  <main class="page">
    <header class="page-header">
      <h1>策略中心</h1>
      <p>用列表方式管理 Python 策略资产，后续再接入执行能力。</p>
    </header>

    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>

    <section class="layout">
      <PythonStrategyListPanel
        v-model:query="searchText"
        :items="filteredStrategies"
        :selected-id="pythonStrategyStore.selectedId"
        @create="startDraft"
        @select="selectStrategy"
      />
      <PythonStrategyEditor
        v-model="editorState"
        :mode="editorMode"
        @delete="handleDelete"
        @reset="resetEditorState"
        @save="handleSave"
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
      editorState.value = null;
      return;
    }

    await selectStrategy(items[0].id);
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : "加载策略中心失败";
  }
}

async function selectStrategy(strategyId: string) {
  errorMessage.value = "";

  try {
    const strategy = await pythonStrategyStore.selectStrategy(strategyId);
    editorState.value = toEditorState(strategy);
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : "加载策略详情失败";
  }
}

function startDraft() {
  pythonStrategyStore.clearSelection();
  editorState.value = createDraftState();
}

async function handleSave() {
  if (editorState.value === null) {
    return;
  }

  errorMessage.value = "";

  try {
    const saved = await pythonStrategyStore.saveStrategy(toPayload(editorState.value));
    editorState.value = toEditorState(saved);
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : "保存 Python 策略失败";
  }
}

async function handleDelete() {
  if (editorState.value === null || !editorState.value.id) {
    return;
  }

  errorMessage.value = "";

  try {
    const next = await pythonStrategyStore.removeStrategy(editorState.value.id);
    editorState.value = next ? toEditorState(next) : null;
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : "删除 Python 策略失败";
  }
}

async function resetEditorState() {
  if (editorState.value === null) {
    return;
  }

  if (!editorState.value.id) {
    editorState.value = createDraftState();
    return;
  }

  await selectStrategy(editorState.value.id);
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
</script>

<style scoped>
.page {
  display: grid;
  gap: 1rem;
  padding: 2rem;
}

.page-header {
  display: grid;
  gap: 0.5rem;
}

.page-header h1,
.page-header p {
  margin: 0;
}

.page-header p {
  color: #475467;
}

.layout {
  display: grid;
  gap: 1rem;
  grid-template-columns: minmax(18rem, 24rem) minmax(0, 1fr);
}

.error {
  color: #b42318;
}

@media (max-width: 980px) {
  .layout {
    grid-template-columns: 1fr;
  }
}
</style>
