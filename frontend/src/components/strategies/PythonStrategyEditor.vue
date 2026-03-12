<template>
  <section class="panel">
    <template v-if="mode === 'empty' || modelValue === null">
      <div class="empty-editor">
        <h2>选择一个策略</h2>
        <p>从左侧选择已有策略，或者新建第一条 Python 策略。</p>
      </div>
    </template>

    <template v-else>
      <header class="panel-header">
        <div>
          <h2>{{ mode === "draft" ? "新建 Python 策略" : "策略详情" }}</h2>
          <p>当前只管理 Python 策略资产，尚未接入回测执行。</p>
        </div>
      </header>

      <label class="field">
        <span>策略名称</span>
        <input :value="modelValue.name" @input="updateField('name', ($event.target as HTMLInputElement).value)" />
      </label>

      <label class="field">
        <span>策略说明</span>
        <input
          :value="modelValue.description"
          @input="updateField('description', ($event.target as HTMLInputElement).value)"
        />
      </label>

      <label class="field">
        <span>标签</span>
        <input :value="modelValue.tagsText" @input="updateField('tagsText', ($event.target as HTMLInputElement).value)" />
      </label>

      <label class="field">
        <span>参数说明</span>
        <input
          :value="modelValue.parameterSchemaText"
          @input="updateField('parameterSchemaText', ($event.target as HTMLInputElement).value)"
        />
      </label>

      <label class="field">
        <span>Python 代码</span>
        <textarea
          :value="modelValue.code"
          data-testid="python-code-editor"
          rows="14"
          @input="updateField('code', ($event.target as HTMLTextAreaElement).value)"
        />
      </label>

      <div class="actions">
        <button type="button" @click="$emit('save')">保存</button>
        <button v-if="mode === 'edit'" type="button" @click="$emit('delete')">删除</button>
        <button type="button" @click="$emit('reset')">恢复未保存修改</button>
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
.panel {
  border: 1px solid #d0d5dd;
  border-radius: 1rem;
  display: grid;
  gap: 1rem;
  padding: 1rem;
}

.panel-header h2,
.panel-header p,
.empty-editor h2,
.empty-editor p {
  margin: 0;
}

.panel-header p,
.empty-editor p {
  color: #475467;
  margin-top: 0.35rem;
}

.field {
  display: grid;
  gap: 0.35rem;
}

textarea {
  font-family: "SFMono-Regular", "Menlo", monospace;
  line-height: 1.4;
}

.actions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
}
</style>
