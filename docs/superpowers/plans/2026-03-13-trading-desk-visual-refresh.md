# Trading Desk Visual Refresh Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild the main product pages into a unified trading-desk visual system without changing routing, APIs, or core behavior.

**Architecture:** Introduce a small global style foundation for tokens, base controls, and shared surfaces, then restyle the app shell and page compositions on top of it. Keep business logic intact and use the existing page/component structure wherever possible so the visual rewrite stays controlled and regression-friendly.

**Tech Stack:** Vue 3, TypeScript, CSS, Vitest, Vue Test Utils

---

## Spec Reference

- Spec: `docs/superpowers/specs/2026-03-13-trading-desk-visual-refresh-design.md`

## File Structure Map

- `frontend/src/main.ts`
  - Imports the new global style layers before mounting the app
- `frontend/src/styles/tokens.css`
  - Design tokens for colors, spacing, radii, shadows, typography, and terminal surfaces
- `frontend/src/styles/base.css`
  - Global element styling for `body`, headings, buttons, inputs, textareas, tables, and shared layout utilities
- `frontend/src/styles/surfaces.css`
  - Shared shell, page, panel, badge, and terminal-panel classes used across pages
- `frontend/src/components/app/AppShell.vue`
  - Darker terminal-style navigation shell and brand/status area
- `frontend/src/views/LoginView.vue`
  - Trading-desk login entry composition
- `frontend/src/views/WorkbenchView.vue`
  - Research overview page shell and section rhythm
- `frontend/src/views/DataCenterView.vue`
  - Data operations page composition
- `frontend/src/views/BacktestCenterView.vue`
  - Backtest launch and task-queue composition
- `frontend/src/views/StrategyCenterView.vue`
  - Python strategy workspace composition with stronger visual hierarchy
- `frontend/src/views/ResultsView.vue`
  - Analysis-oriented result page composition
- `frontend/src/components/workbench/RecentRunsPanel.vue`
  - Workbench summary card styling
- `frontend/src/components/workbench/DataStatusPanel.vue`
  - Workbench data-status card styling
- `frontend/src/components/data/DataSourceForm.vue`
  - Data-source configuration card styling
- `frontend/src/components/data/SyncTaskTable.vue`
  - Sync task table styling
- `frontend/src/components/backtests/BacktestLaunchCard.vue`
  - Launch card styling
- `frontend/src/components/backtests/BacktestJobTable.vue`
  - Task queue table styling
- `frontend/src/components/strategies/PythonStrategyListPanel.vue`
  - Strategy directory styling
- `frontend/src/components/strategies/PythonStrategyEditor.vue`
  - Deep terminal editor styling
- `frontend/src/components/results/MetricsCards.vue`
  - Results metric card styling
- `frontend/src/components/results/RebalanceTable.vue`
  - Results table styling
- `frontend/src/components/results/AiInsightPanel.vue`
  - Results AI side-panel styling
- `frontend/src/tests/app-shell.spec.ts`
  - Shell structure regression
- `frontend/src/tests/login-view.spec.ts`
  - Login page structure and auth flow regression
- `frontend/src/tests/workbench-view.spec.ts`
  - Workbench structure regression
- `frontend/src/tests/data-center-view.spec.ts`
  - Data center structure regression
- `frontend/src/tests/backtest-center-view.spec.ts`
  - Backtest center structure regression
- `frontend/src/tests/strategy-center-view.spec.ts`
  - Strategy workspace regression
- `frontend/src/tests/results-view.spec.ts`
  - Result page structure regression

## Implementation Order

1. Create the shared theme foundation and rebuild the shell/login entry
2. Restyle the operational workflow pages: workbench, data center, backtest center
3. Turn strategy center and results page into the two visual focal points, then run regressions

## Chunk 1: Theme Foundation And Entry Experience

### Task 1: Add failing shell and login structure tests

**Files:**
- Modify: `frontend/src/tests/app-shell.spec.ts`
- Modify: `frontend/src/tests/login-view.spec.ts`

- [ ] **Step 1: Extend the shell and login tests for the new structure**

```ts
it("shows the terminal shell brand and local mode badge", async () => {
  await router.push("/workbench");
  const wrapper = mount(App, { global: { plugins: [router] } });
  await flushPromises();

  expect(wrapper.text()).toContain("OMGTrader");
  expect(wrapper.text()).toContain("Local Mode");
});
```

```ts
it("renders the trading desk login copy", async () => {
  const wrapper = mount(LoginView, { global: { plugins: [router] } });

  expect(wrapper.text()).toContain("A 股量化研究终端");
  expect(wrapper.text()).toContain("本地运行");
});
```

- [ ] **Step 2: Run the shell/login tests to verify failure**

Run: `cd frontend && npm test -- --run src/tests/app-shell.spec.ts src/tests/login-view.spec.ts`
Expected: FAIL because the current shell and login page do not render the new trading-desk structure

### Task 2: Implement the global theme layer, shell, and login redesign

**Files:**
- Create: `frontend/src/styles/tokens.css`
- Create: `frontend/src/styles/base.css`
- Create: `frontend/src/styles/surfaces.css`
- Modify: `frontend/src/main.ts`
- Modify: `frontend/src/components/app/AppShell.vue`
- Modify: `frontend/src/views/LoginView.vue`

- [ ] **Step 1: Add global tokens and base layers**

```css
:root {
  --bg-app: #f2f5fa;
  --bg-shell: #182233;
  --bg-panel: #fbfcfe;
  --bg-terminal: #101722;
  --text-primary: #122033;
  --text-muted: #60708a;
  --accent-signal: #ff8d4d;
  --accent-active: #6ea8ff;
  --border-subtle: #d7dee8;
  --radius-panel: 18px;
}
```

```ts
import "./styles/tokens.css";
import "./styles/base.css";
import "./styles/surfaces.css";
```

- [ ] **Step 2: Rebuild the app shell as a terminal navigation frame**

```vue
<aside class="app-shell-sidebar">
  <div class="brand-block">
    <p class="eyebrow">Local Mode</p>
    <h1>OMGTrader</h1>
    <p>A 股量化研究工作台</p>
  </div>
</aside>
```

- [ ] **Step 3: Redesign the login page as a product entry screen**

```vue
<main class="login-screen">
  <section class="login-hero">
    <p class="eyebrow">A 股量化研究终端</p>
    <h1>在本地完成数据、策略、回测与复盘。</h1>
  </section>
  <section class="login-card">
    <!-- existing form -->
  </section>
</main>
```

- [ ] **Step 4: Re-run the shell/login tests**

Run: `cd frontend && npm test -- --run src/tests/app-shell.spec.ts src/tests/login-view.spec.ts`
Expected: PASS

- [ ] **Step 5: Commit the theme foundation**

```bash
git add frontend/src/main.ts frontend/src/styles frontend/src/components/app/AppShell.vue frontend/src/views/LoginView.vue frontend/src/tests/app-shell.spec.ts frontend/src/tests/login-view.spec.ts
git commit -m "feat: add trading desk theme foundation"
```

## Chunk 2: Operational Workflow Pages

### Task 3: Add failing workbench, data center, and backtest center structure tests

**Files:**
- Modify: `frontend/src/tests/workbench-view.spec.ts`
- Modify: `frontend/src/tests/data-center-view.spec.ts`
- Modify: `frontend/src/tests/backtest-center-view.spec.ts`

- [ ] **Step 1: Rewrite the page tests around the new trading-desk structure**

```ts
it("shows the workbench overview cards", () => {
  const wrapper = mount(WorkbenchView);

  expect(wrapper.text()).toContain("研究总览");
  expect(wrapper.text()).toContain("最近回测");
});
```

```ts
it("shows the data operations sections", () => {
  const wrapper = mount(DataCenterView);

  expect(wrapper.text()).toContain("数据运行面板");
  expect(wrapper.text()).toContain("覆盖范围");
});
```

```ts
it("shows the backtest launch desk", () => {
  const wrapper = mount(BacktestCenterView);

  expect(wrapper.text()).toContain("任务发射台");
  expect(wrapper.text()).toContain("回测任务");
});
```

- [ ] **Step 2: Run the workflow-page tests to verify failure**

Run: `cd frontend && npm test -- --run src/tests/workbench-view.spec.ts src/tests/data-center-view.spec.ts src/tests/backtest-center-view.spec.ts`
Expected: FAIL because the current pages do not expose the new structure and copy

### Task 4: Restyle the workbench, data center, and backtest center

**Files:**
- Modify: `frontend/src/views/WorkbenchView.vue`
- Modify: `frontend/src/views/DataCenterView.vue`
- Modify: `frontend/src/views/BacktestCenterView.vue`
- Modify: `frontend/src/components/workbench/RecentRunsPanel.vue`
- Modify: `frontend/src/components/workbench/DataStatusPanel.vue`
- Modify: `frontend/src/components/data/DataSourceForm.vue`
- Modify: `frontend/src/components/data/SyncTaskTable.vue`
- Modify: `frontend/src/components/backtests/BacktestLaunchCard.vue`
- Modify: `frontend/src/components/backtests/BacktestJobTable.vue`

- [ ] **Step 1: Upgrade the workbench into a research overview page**

```vue
<header class="page-header page-header--dashboard">
  <p class="eyebrow">Research Overview</p>
  <h1>研究总览</h1>
  <p class="page-intro">快速查看数据就绪状态、最近回测和下一步入口。</p>
</header>
```

- [ ] **Step 2: Upgrade the data center into a data-operations layout**

```vue
<section class="workspace-grid workspace-grid--ops">
  <DataSourceForm class="surface-card" />
  <SyncTaskTable class="surface-card" />
</section>
```

- [ ] **Step 3: Upgrade the backtest center into a launch desk**

```vue
<header class="page-header">
  <p class="eyebrow">Execution Desk</p>
  <h1>任务发射台</h1>
</header>
```

- [ ] **Step 4: Re-run the workflow-page tests**

Run: `cd frontend && npm test -- --run src/tests/workbench-view.spec.ts src/tests/data-center-view.spec.ts src/tests/backtest-center-view.spec.ts`
Expected: PASS

- [ ] **Step 5: Commit the operational page refresh**

```bash
git add frontend/src/views/WorkbenchView.vue frontend/src/views/DataCenterView.vue frontend/src/views/BacktestCenterView.vue frontend/src/components/workbench/RecentRunsPanel.vue frontend/src/components/workbench/DataStatusPanel.vue frontend/src/components/data/DataSourceForm.vue frontend/src/components/data/SyncTaskTable.vue frontend/src/components/backtests/BacktestLaunchCard.vue frontend/src/components/backtests/BacktestJobTable.vue frontend/src/tests/workbench-view.spec.ts frontend/src/tests/data-center-view.spec.ts frontend/src/tests/backtest-center-view.spec.ts
git commit -m "feat: refresh operational workflow pages"
```

## Chunk 3: Strategy And Results Visual Focal Points

### Task 5: Add failing strategy center and results structure tests

**Files:**
- Modify: `frontend/src/tests/strategy-center-view.spec.ts`
- Modify: `frontend/src/tests/results-view.spec.ts`

- [ ] **Step 1: Extend the strategy and results tests with the new visual structure**

```ts
it("shows the terminal editor messaging for python strategies", async () => {
  const wrapper = mount(StrategyCenterView);
  await flushPromises();

  expect(wrapper.text()).toContain("Python 策略工作台");
  expect(wrapper.get('[data-testid="python-code-editor"]').exists()).toBe(true);
});
```

```ts
it("renders the results analysis layout", async () => {
  const wrapper = mount(ResultsView, { global: { plugins: [router] } });
  await flushPromises();

  expect(wrapper.text()).toContain("分析总览");
  expect(wrapper.text()).toContain("策略总结");
});
```

- [ ] **Step 2: Run the strategy/results tests to verify failure**

Run: `cd frontend && npm test -- --run src/tests/strategy-center-view.spec.ts src/tests/results-view.spec.ts`
Expected: FAIL because the current page structure and copy do not yet match the new analysis/terminal layouts

### Task 6: Restyle the strategy center and results page, then run full regressions

**Files:**
- Modify: `frontend/src/views/StrategyCenterView.vue`
- Modify: `frontend/src/components/strategies/PythonStrategyListPanel.vue`
- Modify: `frontend/src/components/strategies/PythonStrategyEditor.vue`
- Modify: `frontend/src/views/ResultsView.vue`
- Modify: `frontend/src/components/results/MetricsCards.vue`
- Modify: `frontend/src/components/results/RebalanceTable.vue`
- Modify: `frontend/src/components/results/AiInsightPanel.vue`

- [ ] **Step 1: Turn strategy center into the main terminal workspace**

```vue
<header class="page-header">
  <p class="eyebrow">Python Strategy Desk</p>
  <h1>Python 策略工作台</h1>
</header>
```

```vue
<label class="field field--terminal">
  <span>Python 代码</span>
  <textarea data-testid="python-code-editor" class="terminal-editor" />
</label>
```

- [ ] **Step 2: Turn results page into an analysis-oriented dashboard**

```vue
<header class="results-hero">
  <p class="eyebrow">Analysis Overview</p>
  <h1>分析总览</h1>
</header>
```

- [ ] **Step 3: Re-run the strategy/results tests**

Run: `cd frontend && npm test -- --run src/tests/strategy-center-view.spec.ts src/tests/results-view.spec.ts`
Expected: PASS

- [ ] **Step 4: Run the full frontend regression suite**

Run: `cd frontend && npm test -- --run`
Expected: PASS

- [ ] **Step 5: Run a local startup spot-check**

Run: `bash scripts/dev/start.sh`
Expected: Frontend and backend both start successfully so the refreshed pages can be manually reviewed in the browser

- [ ] **Step 6: Commit the final visual refresh**

```bash
git add frontend docs/superpowers/specs/2026-03-13-trading-desk-visual-refresh-design.md docs/superpowers/plans/2026-03-13-trading-desk-visual-refresh.md
git commit -m "feat: refresh trading desk visuals"
```
