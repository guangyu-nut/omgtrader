# Python Strategy Center Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild the strategy center into a Python-strategy asset workspace with full CRUD, while keeping the existing backtest flow intact.

**Architecture:** Add a new `python_strategies` resource inside the existing backend `strategies` module instead of overloading the current parameterized `StrategyInstance` model. On the frontend, replace the current form-only strategy page with a split-panel workspace backed by a dedicated Python strategy API/store so the old backtest flow can remain untouched.

**Tech Stack:** FastAPI, SQLAlchemy, Alembic, Pydantic, pytest, Vue 3, TypeScript, Vitest, Vue Test Utils

---

## Spec Reference

- Spec: `docs/superpowers/specs/2026-03-12-python-strategy-center-design.md`

## File Structure Map

- `backend/alembic/versions/0006_add_python_strategies_table.py`
  - Adds the `python_strategies` table without changing old strategy tables
- `backend/app/modules/strategies/models.py`
  - Declares the new `PythonStrategy` ORM model alongside existing models
- `backend/app/modules/strategies/schemas.py`
  - Adds create, update, list, and detail schemas for Python strategies
- `backend/app/modules/strategies/repository.py`
  - Adds user-scoped CRUD queries for Python strategies
- `backend/app/modules/strategies/service.py`
  - Normalizes tags and orchestrates Python strategy CRUD behavior
- `backend/app/modules/strategies/router.py`
  - Exposes `/api/strategies/python*` endpoints
- `backend/tests/modules/strategies/test_python_strategies_api.py`
  - Covers create, list, detail, update, delete, and user isolation
- `backend/tests/test_migrations.py`
  - Verifies the new table exists after migration
- `frontend/src/api/pythonStrategies.ts`
  - Typed frontend client for Python strategy CRUD requests
- `frontend/src/stores/pythonStrategies.ts`
  - Holds loaded strategy summaries, selected strategy state, and CRUD helpers
- `frontend/src/components/strategies/PythonStrategyListPanel.vue`
  - Left-side search and strategy list UI
- `frontend/src/components/strategies/PythonStrategyEditor.vue`
  - Right-side detail and editing UI for one strategy
- `frontend/src/views/StrategyCenterView.vue`
  - Page container that coordinates loading, selection, draft creation, and guardrails
- `frontend/src/tests/strategy-center-view.spec.ts`
  - View-level tests for empty state, list behavior, save/delete flows, search, and unsaved-change prompts

## Implementation Order

1. Add backend schema and Python strategy CRUD APIs
2. Replace the strategy center page with a Python-strategy split-panel workspace
3. Add search, unsaved-change prompts, delete behavior, and regressions

## Chunk 1: Backend Python Strategy Resource

### Task 1: Add database support for Python strategies

**Files:**
- Create: `backend/alembic/versions/0006_add_python_strategies_table.py`
- Modify: `backend/app/modules/strategies/models.py`
- Modify: `backend/tests/test_migrations.py`

- [ ] **Step 1: Extend the migration test with the new table assertion**

```python
def test_initial_migration_creates_core_tables(db_engine):
    tables = set(inspect(db_engine).get_table_names())

    assert "python_strategies" in tables
```

- [ ] **Step 2: Run the migration test before adding the schema**

Run: `backend/.venv/bin/pytest backend/tests/test_migrations.py -v`
Expected: FAIL because `python_strategies` does not exist yet

- [ ] **Step 3: Add the ORM model and migration**

```python
class PythonStrategy(Base):
    __tablename__ = "python_strategies"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    description: Mapped[str] = mapped_column(String(), nullable=False, default="")
    tags_text: Mapped[str] = mapped_column(String(), nullable=False, default="")
    parameter_schema_text: Mapped[str] = mapped_column(String(), nullable=False, default="")
    code: Mapped[str] = mapped_column(String(), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(), nullable=False, default=lambda: datetime.now(UTC))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(),
        nullable=False,
        default=lambda: datetime.now(UTC),
    )
```

- [ ] **Step 4: Re-run the migration test**

Run: `backend/.venv/bin/pytest backend/tests/test_migrations.py -v`
Expected: PASS

- [ ] **Step 5: Commit the schema foundation**

```bash
git add backend/app/modules/strategies/models.py backend/alembic/versions/0006_add_python_strategies_table.py backend/tests/test_migrations.py
git commit -m "feat: add python strategy schema"
```

### Task 2: Implement Python strategy CRUD endpoints

**Files:**
- Modify: `backend/app/modules/strategies/schemas.py`
- Modify: `backend/app/modules/strategies/repository.py`
- Modify: `backend/app/modules/strategies/service.py`
- Modify: `backend/app/modules/strategies/router.py`
- Create: `backend/tests/modules/strategies/test_python_strategies_api.py`

- [ ] **Step 1: Write the failing Python strategy API tests**

```python
def test_create_and_list_python_strategies(client, auth_headers):
    create_response = client.post(
        "/api/strategies/python",
        headers=auth_headers,
        json={
            "name": "RSI Rotation",
            "description": "RSI 轮动策略",
            "tags": ["轮动", "RSI"],
            "parameter_schema_text": "lookback: int",
            "code": "class Strategy:\n    pass\n",
        },
    )

    list_response = client.get("/api/strategies/python", headers=auth_headers)

    assert create_response.status_code == 201
    assert list_response.status_code == 200
    assert list_response.json()[0]["name"] == "RSI Rotation"
```

```python
def test_update_and_delete_python_strategy(client, auth_headers):
    created = client.post(
        "/api/strategies/python",
        headers=auth_headers,
        json={"name": "Draft", "description": "", "tags": [], "parameter_schema_text": "", "code": "print('x')"},
    ).json()

    update_response = client.put(
        f"/api/strategies/python/{created['id']}",
        headers=auth_headers,
        json={
            "name": "Momentum Draft",
            "description": "更新后的说明",
            "tags": ["动量"],
            "parameter_schema_text": "window: int",
            "code": "print('updated')",
        },
    )
    delete_response = client.delete(f"/api/strategies/python/{created['id']}", headers=auth_headers)

    assert update_response.status_code == 200
    assert delete_response.status_code == 204
```

- [ ] **Step 2: Run the Python strategy API tests**

Run: `backend/.venv/bin/pytest backend/tests/modules/strategies/test_python_strategies_api.py -v`
Expected: FAIL because the Python strategy schemas, repository methods, service methods, and routes do not exist yet

- [ ] **Step 3: Implement the minimal CRUD backend**

```python
class PythonStrategyCreate(BaseModel):
    name: str
    description: str = ""
    tags: list[str] = Field(default_factory=list)
    parameter_schema_text: str = ""
    code: str
```

```python
@router.get("/python", response_model=list[PythonStrategyListItem])
def list_python_strategies(...):
    return service.list_python_strategies(current_user)
```

```python
def _serialize_tags(tags: list[str]) -> str:
    return ",".join(tag for tag in (item.strip() for item in tags) if tag)
```

- [ ] **Step 4: Re-run the Python strategy API tests**

Run: `backend/.venv/bin/pytest backend/tests/modules/strategies/test_python_strategies_api.py -v`
Expected: PASS

- [ ] **Step 5: Run compatibility regressions for the old strategy and backtest flow**

Run: `backend/.venv/bin/pytest backend/tests/modules/strategies/test_strategy_instances_api.py backend/tests/modules/backtests/test_backtest_jobs_api.py -v`
Expected: PASS to confirm the old parameterized strategy and backtest flow still work

- [ ] **Step 6: Commit the Python strategy APIs**

```bash
git add backend/app/modules/strategies backend/tests/modules/strategies/test_python_strategies_api.py
git commit -m "feat: add python strategy CRUD APIs"
```

## Chunk 2: Frontend Python Strategy Workspace

### Task 3: Replace the strategy center smoke test with Python workspace tests

**Files:**
- Modify: `frontend/src/tests/strategy-center-view.spec.ts`

- [ ] **Step 1: Rewrite the strategy center view tests around Python strategies**

```ts
it("shows the empty state when there are no python strategies", async () => {
  listPythonStrategies.mockResolvedValue([]);

  const wrapper = mount(StrategyCenterView);
  await flushPromises();

  expect(wrapper.text()).toContain("新建 Python 策略");
  expect(wrapper.text()).toContain("创建第一条 Python 策略");
});
```

```ts
it("loads an existing python strategy into the editor", async () => {
  listPythonStrategies.mockResolvedValue([
    { id: "ps-1", name: "Alpha", description: "动量轮动", tags: ["轮动"], updated_at: "2026-03-12T10:00:00Z" },
  ]);
  getPythonStrategy.mockResolvedValue({
    id: "ps-1",
    name: "Alpha",
    description: "动量轮动",
    tags: ["轮动"],
    parameter_schema_text: "window: int",
    code: "class Strategy:\n    pass\n",
    created_at: "2026-03-12T10:00:00Z",
    updated_at: "2026-03-12T10:00:00Z",
  });

  const wrapper = mount(StrategyCenterView);
  await flushPromises();

  expect(wrapper.text()).toContain("Alpha");
  expect(wrapper.find("textarea").element.value).toContain("class Strategy");
});
```

- [ ] **Step 2: Run the strategy center tests before the new workspace exists**

Run: `cd frontend && npm test -- --run src/tests/strategy-center-view.spec.ts`
Expected: FAIL because the new Python strategy API/store contract and split-panel UI do not exist yet

### Task 4: Implement the Python strategy data layer and split-panel UI

**Files:**
- Create: `frontend/src/api/pythonStrategies.ts`
- Create: `frontend/src/stores/pythonStrategies.ts`
- Create: `frontend/src/components/strategies/PythonStrategyListPanel.vue`
- Create: `frontend/src/components/strategies/PythonStrategyEditor.vue`
- Modify: `frontend/src/views/StrategyCenterView.vue`

- [ ] **Step 1: Add the typed frontend API client**

```ts
export async function listPythonStrategies(): Promise<PythonStrategyListItem[]> {
  const response = await fetch(`${API_BASE_URL}/api/strategies/python`, {
    headers: buildHeaders(),
  });

  if (!response.ok) {
    throw new Error("加载 Python 策略失败");
  }

  return (await response.json()) as PythonStrategyListItem[];
}
```

- [ ] **Step 2: Add the Python strategy store**

```ts
const state = reactive({
  items: [] as PythonStrategyListItem[],
  selectedId: "",
});

export const pythonStrategyStore = {
  async loadList() {
    state.items = await listPythonStrategies();
  },
};
```

- [ ] **Step 3: Rebuild the strategy center page as a split-panel workspace**

```vue
<section class="layout">
  <PythonStrategyListPanel
    :items="filteredStrategies"
    :selected-id="selectedId"
    @create="startDraft"
    @select="selectStrategy"
  />
  <PythonStrategyEditor
    :model-value="editorState"
    :mode="editorMode"
    @save="handleSave"
    @delete="handleDelete"
    @reset="resetDraft"
  />
</section>
```

- [ ] **Step 4: Re-run the strategy center tests**

Run: `cd frontend && npm test -- --run src/tests/strategy-center-view.spec.ts`
Expected: PASS

- [ ] **Step 5: Commit the new strategy workspace**

```bash
git add frontend/src/api/pythonStrategies.ts frontend/src/stores/pythonStrategies.ts frontend/src/components/strategies/PythonStrategyListPanel.vue frontend/src/components/strategies/PythonStrategyEditor.vue frontend/src/views/StrategyCenterView.vue frontend/src/tests/strategy-center-view.spec.ts
git commit -m "feat: rebuild strategy center for python assets"
```

## Chunk 3: Guardrails And Regression

### Task 5: Add search, unsaved-change, and delete-flow behavior

**Files:**
- Modify: `frontend/src/tests/strategy-center-view.spec.ts`
- Modify: `frontend/src/components/strategies/PythonStrategyListPanel.vue`
- Modify: `frontend/src/components/strategies/PythonStrategyEditor.vue`
- Modify: `frontend/src/views/StrategyCenterView.vue`

- [ ] **Step 1: Extend the strategy center tests with UX guardrails**

```ts
it("filters the list with the search box", async () => {
  listPythonStrategies.mockResolvedValue([
    { id: "ps-1", name: "Alpha", description: "动量", tags: ["轮动"], updated_at: "2026-03-12T10:00:00Z" },
    { id: "ps-2", name: "Beta", description: "均值回归", tags: ["反转"], updated_at: "2026-03-12T11:00:00Z" },
  ]);

  const wrapper = mount(StrategyCenterView);
  await flushPromises();
  await wrapper.get('input[placeholder="搜索策略"]').setValue("Beta");

  expect(wrapper.text()).toContain("Beta");
  expect(wrapper.text()).not.toContain("Alpha");
});
```

```ts
it("prompts before switching away from unsaved edits", async () => {
  vi.spyOn(window, "confirm").mockReturnValue(false);
  // mount, edit current strategy, click another list item
  expect(window.confirm).toHaveBeenCalled();
});
```

```ts
it("deletes a strategy and falls back to the empty state", async () => {
  vi.spyOn(window, "confirm").mockReturnValue(true);
  deletePythonStrategy.mockResolvedValue(undefined);
  // mount, delete current strategy
  expect(wrapper.text()).toContain("创建第一条 Python 策略");
});
```

- [ ] **Step 2: Run the focused UX tests before implementing the guardrails**

Run: `cd frontend && npm test -- --run src/tests/strategy-center-view.spec.ts`
Expected: FAIL because search, unsaved-change prompts, and delete transitions are not complete yet

- [ ] **Step 3: Implement the remaining guardrails**

```ts
function confirmDiscardChanges() {
  if (!isDirty.value) {
    return true;
  }

  return window.confirm("当前策略有未保存修改，确定要离开吗？");
}
```

```ts
const filteredStrategies = computed(() =>
  state.items.filter((item) => [item.name, item.description, item.tags.join(" ")].join(" ").includes(searchText.value)),
);
```

- [ ] **Step 4: Re-run the focused UX tests**

Run: `cd frontend && npm test -- --run src/tests/strategy-center-view.spec.ts`
Expected: PASS

### Task 6: Run regression suites and lock the feature checkpoint

**Files:**
- No additional source files required

- [ ] **Step 1: Run the full backend suite**

Run: `backend/.venv/bin/pytest backend/tests -v`
Expected: PASS

- [ ] **Step 2: Run the full frontend suite**

Run: `cd frontend && npm test -- --run`
Expected: PASS

- [ ] **Step 3: Commit the final feature polish**

```bash
git add frontend backend docs/superpowers/specs/2026-03-12-python-strategy-center-design.md docs/superpowers/plans/2026-03-12-python-strategy-center.md
git commit -m "feat: finish python strategy center"
```
