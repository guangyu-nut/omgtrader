# Design: 新建策略取消功能

**Date:** 2026-03-13
**Feature:** 在新建 Python 策略（draft 模式）时增加取消按钮，点击后回到上一个已选中的策略，若无则显示空状态。

---

## 背景

`StrategyCenterView.vue` 是 Python 策略工作台。点击"新建 Python 策略"按钮后进入 draft 模式，当前只有"保存"和"恢复未保存修改"两个操作，没有取消按钮。用户无法放弃新建并回到之前的状态。

---

## 目标

- draft 模式下，actions 区域展示"取消"按钮
- 点击取消：若之前有选中的策略，则恢复该策略的**已保存（干净）状态**；若无，则显示空状态（`editorMode === "empty"`）
- 若 draft 内容已修改，点取消前弹出确认对话框（与现有 `confirmDiscardChanges()` 行为一致）
- **取消动作本身**不触发额外的 API 请求（后续用户交互如点击列表项仍会正常发起请求）
- 已知限制：取消后恢复的是本地缓存的最后保存状态，不重新拉取，若策略在此期间被其他客户端修改则不会感知

---

## 改动文件

### 1. `frontend/src/stores/pythonStrategies.ts`

新增 `restoreHighlight(id: string)` 方法，仅设置 `state.selectedId`，用于恢复列表左侧的高亮状态。

**与 `clearSelection()` 的区别：** `clearSelection()` 同时清零 `selectedId` 和 `selectedStrategy`；`restoreHighlight` 仅写 `selectedId`，不触碰 `selectedStrategy`。两者不等价。

传入 `""` 时，效果是将 `selectedId` 写为空字符串（此时 store 已经处于 `selectedId === ""` 的状态，该调用不产生可见副作用，属于防御性状态同步）。

```ts
function restoreHighlight(id: string) {
  state.selectedId = id;
}

export const pythonStrategyStore = {
  // ...existing...
  restoreHighlight,
};
```

### 2. `frontend/src/views/StrategyCenterView.vue`

**新增 `cancelTarget` ref（本地类型，定义于同文件）：**

```ts
type CancelTarget = { editorState: EditorState | null; selectedId: string };
const cancelTarget = ref<CancelTarget | null>(null);
```

**修改 `startDraft()`：** 进入 draft 前保存当前**已保存的干净状态**。

关键设计决策：
- **捕获 `savedSnapshot` 而非 `editorState.value`。** 若用户进入 draft 前有未保存的修改，`confirmDiscardChanges()` 已提示放弃那些修改。取消 draft 后应恢复到最后一次保存的状态。`savedSnapshot` 始终由 `setPersistedEditorState` 维护，保存最后一次 save 时的序列化快照。
- **`startDraft()` 只能在 `onMounted` → `loadInitialState()` 完成后被触发**（用户需要与 UI 交互），而 `loadInitialState` 必然调用 `setPersistedEditorState`，因此 `savedSnapshot.value` 到达此处时已为合法 JSON（`"null"` 或对象串）。为防御性编码，仍用 `savedSnapshot.value ? JSON.parse(...) : null` 形式。
- **顺序重要：** `cancelTarget` 必须在 `clearSelection()` 之前赋值，否则 `selectedId` 已被清零。

```ts
function startDraft() {
  if (!confirmDiscardChanges()) return;
  // 顺序重要：先保存快照，再清除选中状态
  cancelTarget.value = {
    editorState: savedSnapshot.value ? (JSON.parse(savedSnapshot.value) as EditorState | null) : null,
    selectedId: pythonStrategyStore.selectedId,
  };
  pythonStrategyStore.clearSelection();
  setPersistedEditorState(createDraftState());
}
```

**新增 `handleCancelDraft()`：**

```ts
function handleCancelDraft() {
  if (!confirmDiscardChanges()) return;
  const target = cancelTarget.value;
  cancelTarget.value = null;
  // target 在此处必然有值（取消按钮只在 draft 模式出现，而进入 draft 必先调用 startDraft）
  // 以下 if 为防御性保护
  if (target) {
    pythonStrategyStore.restoreHighlight(target.selectedId);
    // 若 target.editorState 为 null，setPersistedEditorState(null) 将使 editorMode === "empty"
    setPersistedEditorState(target.editorState);
  }
}
```

**绑定事件：** 以下为 `<PythonStrategyEditor>` 组件标签的**完整替换**（在现有属性基础上增加 `@cancel`）：

```html
<PythonStrategyEditor
  :model-value="editorState"
  :mode="editorMode"
  @cancel="handleCancelDraft"
  @delete="handleDelete"
  @reset="resetEditorState"
  @save="handleSave"
  @update:model-value="handleEditorChange"
/>
```

### 3. `frontend/src/components/strategies/PythonStrategyEditor.vue`

**`defineEmits` 完整替换**（新增 `cancel`）：

```ts
const emit = defineEmits<{
  save: [];
  delete: [];
  reset: [];
  cancel: [];
  "update:modelValue": [value: EditorState];
}>();
```

**actions 区域完整 DOM 替换**（顺序：保存 → 取消（draft）/ 删除（edit）→ 恢复未保存修改）：

- "取消"和"删除"互斥：draft 模式显示取消，edit 模式显示删除
- "恢复未保存修改"在 draft 和 edit 模式下均显示（无 `v-if`，与现有行为保持一致）

```html
<div class="actions">
  <button type="button" @click="$emit('save')">保存</button>
  <button v-if="mode === 'draft'" class="button-secondary" type="button" @click="$emit('cancel')">
    取消
  </button>
  <button v-if="mode === 'edit'" class="button-danger" type="button" @click="$emit('delete')">删除</button>
  <button class="button-secondary" type="button" @click="$emit('reset')">恢复未保存修改</button>
</div>
```

---

## 数据流

```
用户点击"新建 Python 策略"
  → startDraft()
  → 先保存 cancelTarget（savedSnapshot 解析的干净状态 + selectedId），再 clearSelection()
  → setPersistedEditorState(createDraftState())
  → 进入 draft 模式，显示取消按钮

用户点击"取消"
  → PythonStrategyEditor emit cancel
  → handleCancelDraft()
  → confirmDiscardChanges()（draft 未修改则直接通过；已修改则弹确认框）
  → restoreHighlight(target.selectedId) + setPersistedEditorState(target.editorState)
  → cancelTarget 清空
```

---

## 边界情况

| 场景 | 行为 |
|------|------|
| 新建后未修改 draft 直接取消 | `isDirty()` 为 false，无确认框，直接恢复 |
| 新建后已修改 draft 后取消 | 弹出确认框；确认后恢复 cancelTarget 状态，拒绝则留在 draft |
| 取消后恢复的策略数据非最新 | 显示本地缓存的最后保存状态（已知限制，不发起重新拉取） |
| 有已选中策略时新建（含未保存修改），确认放弃后取消 draft | 恢复的是 savedSnapshot（干净状态），而非刚放弃的脏数据 |
| 无已选中策略时新建后取消 | `target.editorState` 为 null → `editorMode === "empty"` → 显示空状态 UI |
| 取消后再次新建 | cancelTarget 重新记录，流程正常 |
| draft 模式下 `resetEditorState()` | 仍保持原有行为（重置为空 draft），不清除 cancelTarget |
| 取消后用户点击列表项 | 正常触发 `selectStrategy()`，`selectedStrategy` 被刷新，恢复完整 store 状态 |

---

## 不涉及范围

- edit 模式（编辑已保存策略）无取消按钮，不在本次范围
- 不修改 `StrategyForm.vue`（Top N 等权轮动，独立旧组件）
- 不涉及后端变更
