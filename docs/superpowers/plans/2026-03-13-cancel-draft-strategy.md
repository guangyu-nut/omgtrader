# Cancel Draft Strategy Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在新建 Python 策略（draft 模式）时增加取消按钮，点击后回到上一个已选中的策略的干净状态，若无则显示空状态。

**Architecture:** 在 store 中新增 `restoreHighlight` 方法仅恢复列表高亮；在 `StrategyCenterView` 中用 `cancelTarget` ref 记录进入 draft 前的快照，取消时直接从快照恢复，无需 API 调用；在 `PythonStrategyEditor` 中新增取消按钮（仅 draft 模式可见）。

**Tech Stack:** Vue 3 Composition API、TypeScript、Vitest + @vue/test-utils

---

## Chunk 1: store 新增 restoreHighlight

**Files:**
- Modify: `frontend/src/stores/pythonStrategies.ts`

---

- [ ] **Step 1: 在 `pythonStrategies.ts` 中新增 `restoreHighlight` 函数并导出**

  在 `clearSelection` 函数下方（第 40-43 行后）插入：

  ```ts
  function restoreHighlight(id: string) {
    state.selectedId = id;
  }
  ```

  在导出对象（`export const pythonStrategyStore`）中加入 `restoreHighlight`：

  ```ts
  export const pythonStrategyStore = {
    get items() { return state.items; },
    get selectedId() { return state.selectedId; },
    get selectedStrategy() { return state.selectedStrategy; },
    loadList,
    selectStrategy,
    clearSelection,
    restoreHighlight,
    saveStrategy,
    removeStrategy,
    reset,
  };
  ```

- [ ] **Step 2: 确认 TypeScript 无报错**

  ```bash
  cd frontend && npx tsc --noEmit
  ```

  Expected: 无错误输出

- [ ] **Step 3: Commit**

  ```bash
  git add frontend/src/stores/pythonStrategies.ts
  git commit -m "feat: add restoreHighlight to pythonStrategyStore"
  ```

---

## Chunk 2: PythonStrategyEditor 新增取消按钮

**Files:**
- Modify: `frontend/src/components/strategies/PythonStrategyEditor.vue`

---

- [ ] **Step 1: 写失败测试**

  在 `frontend/src/tests/strategy-center-view.spec.ts` 末尾的 `describe` 块内新增：

  ```ts
  it("shows a cancel button in draft mode but not in edit mode", async () => {
    // edit mode: load a strategy
    fetchMock
      .mockResolvedValueOnce({
        ok: true,
        json: async () => [
          { id: "ps-1", name: "Alpha", description: "", tags: [], updated_at: "2026-03-12T10:00:00Z" },
        ],
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          id: "ps-1",
          name: "Alpha",
          description: "",
          tags: [],
          parameter_schema_text: "",
          code: "class Strategy:\n    pass\n",
          created_at: "2026-03-12T10:00:00Z",
          updated_at: "2026-03-12T10:00:00Z",
        }),
      });

    const wrapper = mount(StrategyCenterView);
    await flushPromises();
    await flushPromises();

    // edit mode: no cancel button
    const cancelInEdit = wrapper.findAll("button").find((b) => b.text() === "取消");
    expect(cancelInEdit).toBeUndefined();

    // enter draft mode (no API call needed)
    await wrapper.findAll("button").find((b) => b.text() === "新建 Python 策略")!.trigger("click");

    // draft mode: cancel button visible
    const cancelInDraft = wrapper.findAll("button").find((b) => b.text() === "取消");
    expect(cancelInDraft).toBeDefined();
  });
  ```

- [ ] **Step 2: 运行测试，确认失败**

  ```bash
  cd frontend && npx vitest run src/tests/strategy-center-view.spec.ts
  ```

  Expected: `shows a cancel button in draft mode but not in edit mode` — **FAIL**

- [ ] **Step 3: 在 `PythonStrategyEditor.vue` 中新增 cancel emit 和取消按钮**

  **3a. 在 `defineEmits` 中加入 `cancel: []`**（第 95-100 行，完整替换）：

  ```ts
  const emit = defineEmits<{
    save: [];
    delete: [];
    reset: [];
    cancel: [];
    "update:modelValue": [value: EditorState];
  }>();
  ```

  **3b. 替换 `actions` div**（第 71-75 行，完整替换）：

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

- [ ] **Step 4: 运行测试，确认通过**

  ```bash
  cd frontend && npx vitest run src/tests/strategy-center-view.spec.ts
  ```

  Expected: 全部 **PASS**（包含新增测试）

- [ ] **Step 5: Commit**

  ```bash
  git add frontend/src/components/strategies/PythonStrategyEditor.vue \
          frontend/src/tests/strategy-center-view.spec.ts
  git commit -m "feat: add cancel button to PythonStrategyEditor draft mode"
  ```

---

## Chunk 3: StrategyCenterView 接入取消逻辑

**Files:**
- Modify: `frontend/src/views/StrategyCenterView.vue`

---

- [ ] **Step 1: 写取消场景的失败测试（有已选中策略时取消）**

  在 `frontend/src/tests/strategy-center-view.spec.ts` 的 `describe` 块内新增：

  ```ts
  it("cancel in draft mode restores the previously selected strategy", async () => {
    fetchMock
      .mockResolvedValueOnce({
        ok: true,
        json: async () => [
          { id: "ps-1", name: "Alpha", description: "", tags: [], updated_at: "2026-03-12T10:00:00Z" },
        ],
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          id: "ps-1",
          name: "Alpha",
          description: "",
          tags: [],
          parameter_schema_text: "",
          code: "class Strategy:\n    pass\n",
          created_at: "2026-03-12T10:00:00Z",
          updated_at: "2026-03-12T10:00:00Z",
        }),
      });

    const wrapper = mount(StrategyCenterView);
    await flushPromises();
    await flushPromises();

    // enter draft mode
    await wrapper.findAll("button").find((b) => b.text() === "新建 Python 策略")!.trigger("click");
    expect(wrapper.text()).toContain("新建 Python 策略");

    // click cancel
    await wrapper.findAll("button").find((b) => b.text() === "取消")!.trigger("click");

    // should be back in edit mode showing Alpha
    expect(wrapper.text()).toContain("策略详情");
    expect((wrapper.get('input[value="Alpha"]').element as HTMLInputElement).value).toBe("Alpha");
    // no cancel button visible in edit mode
    expect(wrapper.findAll("button").find((b) => b.text() === "取消")).toBeUndefined();
  });
  ```

- [ ] **Step 2: 写无已选中策略时取消的失败测试**

  继续在同一 `describe` 块内新增：

  ```ts
  it("cancel in draft mode shows empty state when no prior strategy", async () => {
    fetchMock.mockResolvedValueOnce({
      ok: true,
      json: async () => [],
    });

    const wrapper = mount(StrategyCenterView);
    await flushPromises();

    // enter draft mode
    await wrapper.findAll("button").find((b) => b.text() === "新建 Python 策略")!.trigger("click");
    expect(wrapper.text()).toContain("新建 Python 策略");

    // click cancel
    await wrapper.findAll("button").find((b) => b.text() === "取消")!.trigger("click");

    // should show empty state
    expect(wrapper.text()).toContain("选择一个策略");
    expect(wrapper.findAll("button").find((b) => b.text() === "取消")).toBeUndefined();
  });
  ```

- [ ] **Step 3: 运行测试，确认两个新测试失败**

  ```bash
  cd frontend && npx vitest run src/tests/strategy-center-view.spec.ts
  ```

  Expected: 两个新测试 **FAIL**（旧测试仍 PASS）

- [ ] **Step 4: 在 `StrategyCenterView.vue` 中新增 cancelTarget ref 和类型定义**

  在 `script setup` 的 ref 声明区域（第 75-78 行附近），在现有 `const savedSnapshot = ref("")` 之后加入：

  ```ts
  type CancelTarget = { editorState: EditorState | null; selectedId: string };
  const cancelTarget = ref<CancelTarget | null>(null);
  ```

- [ ] **Step 5: 修改 `startDraft()` 保存 cancelTarget**

  将第 135-142 行的 `startDraft` 函数完整替换为：

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

- [ ] **Step 6: 新增 `handleCancelDraft()` 函数**

  在 `startDraft` 函数之后插入：

  ```ts
  function handleCancelDraft() {
    if (!confirmDiscardChanges()) return;
    const target = cancelTarget.value;
    cancelTarget.value = null;
    if (target) {
      pythonStrategyStore.restoreHighlight(target.selectedId);
      setPersistedEditorState(target.editorState);
    }
  }
  ```

- [ ] **Step 7: 在模板中绑定 `@cancel` 事件**

  将第 39-46 行的 `<PythonStrategyEditor>` 完整替换为：

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

- [ ] **Step 8: 运行所有测试，确认全部通过**

  ```bash
  cd frontend && npx vitest run src/tests/strategy-center-view.spec.ts
  ```

  Expected: 全部 **PASS**

- [ ] **Step 9: 运行完整测试套件**

  ```bash
  cd frontend && npx vitest run
  ```

  Expected: 全部 **PASS**，无回归

- [ ] **Step 10: 确认 TypeScript 无报错**

  ```bash
  cd frontend && npx tsc --noEmit
  ```

  Expected: 无错误输出

- [ ] **Step 11: Commit**

  ```bash
  git add frontend/src/views/StrategyCenterView.vue \
          frontend/src/tests/strategy-center-view.spec.ts
  git commit -m "feat: restore previous state on cancel draft strategy"
  ```
