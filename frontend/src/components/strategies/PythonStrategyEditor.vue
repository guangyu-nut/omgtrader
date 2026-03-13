<template>
  <section class="surface-card strategy-editor">
    <template v-if="mode === 'empty' || modelValue === null">
      <div class="empty-editor">
        <p class="section-label">Editor Idle</p>
        <h2>选择一个策略</h2>
        <p>从左侧选择已有策略，或者新建第一条 Python 策略。</p>
      </div>
    </template>

    <template v-else>
      <header class="surface-header">
        <div class="surface-header__copy">
          <p class="section-label">Editor Workspace</p>
          <h2>{{ mode === "draft" ? "新建 Python 策略" : "策略详情" }}</h2>
          <p class="subtle-copy">当前只管理 Python 策略资产，尚未接入回测执行。</p>
        </div>
        <div class="status-pills">
          <span class="status-pill">{{ mode === "draft" ? "Draft" : "Saved Asset" }}</span>
          <span class="status-pill status-pill--signal">Code First</span>
        </div>
      </header>

      <div class="meta-grid">
        <label class="field-stack">
          <span class="field-label">策略名称</span>
          <input :value="modelValue.name" @input="updateField('name', ($event.target as HTMLInputElement).value)" />
        </label>

        <label class="field-stack">
          <span class="field-label">标签</span>
          <input :value="modelValue.tagsText" @input="updateField('tagsText', ($event.target as HTMLInputElement).value)" />
        </label>

        <label class="field-stack meta-grid__wide">
          <span class="field-label">策略说明</span>
          <input
            :value="modelValue.description"
            @input="updateField('description', ($event.target as HTMLInputElement).value)"
          />
        </label>

        <label class="field-stack meta-grid__wide">
          <span class="field-label">参数说明</span>
          <input
            :value="modelValue.parameterSchemaText"
            @input="updateField('parameterSchemaText', ($event.target as HTMLInputElement).value)"
          />
        </label>
      </div>

      <section class="terminal-surface code-block">
        <div class="code-block__header">
          <div>
            <p class="section-label code-block__label">Python Source</p>
            <h3>Python 代码</h3>
          </div>
          <span class="code-block__hint">研究终端模式</span>
        </div>
        <label class="field-stack code-block__editor">
          <span class="sr-only">Python 代码</span>
          <textarea
            :value="modelValue.code"
            data-testid="python-code-editor"
            rows="16"
            @input="updateField('code', ($event.target as HTMLTextAreaElement).value)"
          />
        </label>
      </section>

      <div class="actions">
        <button type="button" @click="$emit('save')">保存</button>
        <button v-if="mode === 'edit'" class="button-danger" type="button" @click="$emit('delete')">删除</button>
        <button class="button-secondary" type="button" @click="$emit('reset')">恢复未保存修改</button>
      </div>
    </template>
  </section>
</template>

<script setup lang="ts">
type EditorState = {
  id: string;
  name: string;
  description: string;
  tagsText: string;
  parameterSchemaText: string;
  code: string;
};

const props = defineProps<{
  modelValue: EditorState | null;
  mode: "empty" | "draft" | "edit";
}>();

const emit = defineEmits<{
  save: [];
  delete: [];
  reset: [];
  "update:modelValue": [value: EditorState];
}>();

function updateField<K extends keyof EditorState>(key: K, value: EditorState[K]) {
  if (props.modelValue === null) {
    return;
  }

  emit("update:modelValue", {
    ...props.modelValue,
    [key]: value,
  });
}
</script>

<style scoped>
.strategy-editor {
  min-height: 100%;
}

.empty-editor {
  align-content: center;
  background:
    linear-gradient(135deg, rgba(123, 176, 255, 0.12) 0%, rgba(255, 141, 77, 0.08) 100%);
  border: 1px dashed rgba(59, 130, 246, 0.2);
  border-radius: 1.3rem;
  display: grid;
  gap: var(--space-3);
  min-height: 22rem;
  padding: var(--space-6);
  text-align: center;
}

.empty-editor h2,
.empty-editor p {
  margin: 0;
}

.empty-editor p:last-child {
  color: var(--text-muted);
}

.meta-grid {
  display: grid;
  gap: var(--space-4);
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.meta-grid__wide {
  grid-column: 1 / -1;
}

.code-block {
  display: grid;
  gap: var(--space-4);
}

.code-block__header {
  align-items: center;
  display: flex;
  gap: var(--space-3);
  justify-content: space-between;
}

.code-block__header h3 {
  margin: 0;
}

.code-block__label {
  color: var(--accent-active);
}

.code-block__hint {
  color: var(--text-on-dark-muted);
  font-family: var(--font-mono);
  font-size: 0.78rem;
  text-transform: uppercase;
}

.code-block__editor :deep(textarea) {
  background: rgba(7, 13, 22, 0.76);
  border-color: rgba(123, 176, 255, 0.16);
  color: var(--text-on-dark);
  font-family: var(--font-mono);
  line-height: 1.65;
  min-height: 21rem;
}

.actions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
}

.sr-only {
  border: 0;
  clip: rect(0 0 0 0);
  height: 1px;
  margin: -1px;
  overflow: hidden;
  padding: 0;
  position: absolute;
  width: 1px;
}

@media (max-width: 900px) {
  .meta-grid {
    grid-template-columns: 1fr;
  }

  .meta-grid__wide {
    grid-column: auto;
  }
}
</style>
