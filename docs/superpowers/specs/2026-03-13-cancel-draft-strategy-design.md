# Design: 新建策略取消功能

**Date:** 2026-03-13
**Feature:** 在新建 Python 策略（draft 模式）时增加取消按钮，点击后回到上一个已选中的策略，若无则显示空状态。

---

## 背景

`StrategyCenterView.vue` 是 Python 策略工作台。点击"新建 Python 策略"按钮后进入 draft 模式，当前只有"保存"和"恢复未保存修改"两个操作，没有取消按钮。用户无法放弃新建并回到之前的状态。

---

## 目标

- draft 模式下，actions 区域展示"取消"按钮
- 点击取消：若之前有选中的策略，则恢复该策略；若无，则显示空状态
- 不触发额外的 API 请求

---

## 改动文件

### 1. `frontend/src/stores/pythonStrategies.ts`

新增 `restoreSelectedId(id: string)` 方法，直接设置 `state.selectedId`，不调用 API。用于取消 draft 时恢复列表高亮。

导出该方法到 `pythonStrategyStore`。

### 2. `frontend/src/views/StrategyCenterView.vue`

**新增 `cancelTarget` ref：**

```ts
type CancelTarget = { editorState: EditorState | null; selectedId: string };
const cancelTarget = ref<CancelTarget | null>(null);
```

**修改 `startDraft()`：** 进入 draft 前保存当前状态：

```ts
function startDraft() {
  if (!confirmDiscardChanges()) return;
  cancelTarget.value = {
    editorState: editorState.value,
    selectedId: pythonStrategyStore.selectedId,
  };
  pythonStrategyStore.clearSelection();
  setPersistedEditorState(createDraftState());
}
```

**新增 `handleCancelDraft()`：**

```ts
function handleCancelDraft() {
  const target = cancelTarget.value;
  cancelTarget.value = null;
  if (target) {
    pythonStrategyStore.restoreSelectedId(target.selectedId);
    setPersistedEditorState(target.editorState);
  } else {
    setPersistedEditorState(null);
  }
}
```

**绑定事件：** 给 `PythonStrategyEditor` 添加 `@cancel="handleCancelDraft"`。

### 3. `frontend/src/components/strategies/PythonStrategyEditor.vue`

**新增 emit：**

```ts
const emit = defineEmits<{
  save: [];
  delete: [];
  reset: [];
  cancel: [];
  "update:modelValue": [value: EditorState];
}>();
```

**新增取消按钮**（仅 draft 模式）：

```html
<button v-if="mode === 'draft'" class="button-secondary" type="button" @click="$emit('cancel')">
  取消
</button>
```

放在 `actions` 区域，位于"保存"按钮之后。

---

## 数据流

```
用户点击"新建 Python 策略"
  → startDraft() 保存 cancelTarget
  → clearSelection() + setPersistedEditorState(createDraftState())
  → 进入 draft 模式，显示取消按钮

用户点击"取消"
  → PythonStrategyEditor emit cancel
  → handleCancelDraft()
  → 若 cancelTarget 有值：restoreSelectedId + setPersistedEditorState(target.editorState)
  → 若无：setPersistedEditorState(null)
  → cancelTarget 清空
```

---

## 边界情况

| 场景 | 行为 |
|------|------|
| 有已选中策略时新建后取消 | 恢复该策略的编辑器状态及列表高亮 |
| 无已选中策略时新建后取消 | 显示空状态（编辑器空白） |
| 取消后再次新建 | cancelTarget 重新记录，流程正常 |
| draft 模式下 `resetEditorState()` | 仍保持原有行为（重置为空 draft），不清除 cancelTarget |

---

## 不涉及范围

- edit 模式（编辑已保存策略）无取消按钮，不在本次范围
- 不修改 `StrategyForm.vue`（Top N 等权轮动，独立旧组件）
- 不涉及后端变更
