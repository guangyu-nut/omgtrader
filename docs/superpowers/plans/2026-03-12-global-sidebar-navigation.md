# Global Sidebar Navigation Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add an app-level left sidebar shell that exposes the core product routes from every non-login page.

**Architecture:** Keep routing unchanged at the page level, but add route metadata and a shared `AppShell` wrapper in `App.vue`. The shell owns the persistent left navigation while individual pages keep only page-specific content.

**Tech Stack:** Vue 3, Vue Router, Vitest, Vue Test Utils

---

## File Structure Map

- `frontend/src/App.vue`
  - Root app shell switcher
- `frontend/src/router.ts`
  - Route metadata for shell-enabled pages
- `frontend/src/components/app/AppShell.vue`
  - Shared left-sidebar layout
- `frontend/src/tests/app-shell.spec.ts`
  - Shell visibility and active-link tests
- `frontend/src/views/WorkbenchView.vue`
  - Remove duplicated top nav
- `frontend/src/views/DataCenterView.vue`
  - Remove duplicated top nav
- `frontend/src/views/StrategyCenterView.vue`
  - Remove duplicated top nav
- `frontend/src/views/BacktestCenterView.vue`
  - Remove duplicated top nav

## Chunk 1: Shared App Shell

### Task 1: Add failing shell behavior tests

**Files:**
- Create: `frontend/src/tests/app-shell.spec.ts`

- [ ] **Step 1: Write the failing shell tests**

```ts
it("shows the sidebar on shell routes", async () => {
  await router.push("/workbench");
  const wrapper = mount(App, { global: { plugins: [router] } });
  expect(wrapper.text()).toContain("策略中心");
});
```

```ts
it("hides the sidebar on login", async () => {
  await router.push("/login");
  const wrapper = mount(App, { global: { plugins: [router] } });
  expect(wrapper.text()).not.toContain("数据中心");
});
```

- [ ] **Step 2: Run the shell tests to verify failure**

Run: `cd frontend && npm test -- --run src/tests/app-shell.spec.ts`
Expected: FAIL because the shared shell does not exist yet

- [ ] **Step 3: Implement the app shell**

Files:
- Modify: `frontend/src/App.vue`
- Modify: `frontend/src/router.ts`
- Create: `frontend/src/components/app/AppShell.vue`

- [ ] **Step 4: Re-run the shell tests**

Run: `cd frontend && npm test -- --run src/tests/app-shell.spec.ts`
Expected: PASS

## Chunk 2: Page Cleanup And Regression

### Task 2: Remove duplicated local nav from shell pages

**Files:**
- Modify: `frontend/src/views/WorkbenchView.vue`
- Modify: `frontend/src/views/DataCenterView.vue`
- Modify: `frontend/src/views/StrategyCenterView.vue`
- Modify: `frontend/src/views/BacktestCenterView.vue`

- [ ] **Step 1: Simplify page headers**

Keep page titles and content, remove duplicate top navigation buttons now covered by `AppShell`.

- [ ] **Step 2: Run focused frontend regression**

Run: `cd frontend && npm test -- --run src/tests/app-shell.spec.ts src/tests/workbench-view.spec.ts src/tests/data-center-view.spec.ts src/tests/strategy-center-view.spec.ts src/tests/backtest-center-view.spec.ts src/tests/login-view.spec.ts src/tests/router.spec.ts`
Expected: PASS

- [ ] **Step 3: Commit**

```bash
git add frontend docs/superpowers/specs/2026-03-12-global-sidebar-navigation-design.md docs/superpowers/plans/2026-03-12-global-sidebar-navigation.md
git commit -m "feat: add app sidebar shell"
```
