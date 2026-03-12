# Global Sidebar Navigation Design

**Date:** 2026-03-12
**Status:** Approved for implementation

## Goal

Add a single app-level left sidebar so the core research workflow is always reachable from one place, instead of relying on scattered per-page buttons.

## Scope

This change covers:

- A shared application shell for non-login pages
- A fixed left sidebar with four entries:
  - `工作台`
  - `数据中心`
  - `策略中心`
  - `回测中心`
- Active-route highlighting for those entries
- Reusing the same shell on the results page
- Removing redundant top-of-page navigation buttons from core pages

This change does not cover:

- A dedicated `结果中心` list page
- Mobile drawer behavior beyond preserving usable stacked layout
- Any backend or API changes

## Design

### Layout model

`/login` stays standalone.

All other product pages render inside a shared `AppShell` layout:

- Left column: persistent navigation
- Right column: current page content

### Navigation behavior

The sidebar exposes the four fixed workflow entries only:

- `工作台`
- `数据中心`
- `策略中心`
- `回测中心`

The current route is highlighted.

`/results/:jobId` uses the same shell but is not shown as a fixed navigation item, because result viewing remains contextual to a launched backtest.

### Routing approach

Route metadata marks which pages should use the shared shell.

The app root decides whether to wrap the current page in `AppShell`, which keeps page-level logic simple and prevents every view from owning its own layout.

### View cleanup

`WorkbenchView` / `DataCenterView` / `StrategyCenterView` / `BacktestCenterView` should keep their page title and local content, but remove duplicated top navigation buttons.

## Testing

Frontend tests should prove:

- Login page renders without sidebar shell
- A shell-enabled route renders the four sidebar entries
- The active navigation item is visually marked

## Success Criteria

- A user can reach all four core modules from the left sidebar
- Navigation is consistent across core pages
- Login remains visually separate
- Existing frontend tests continue to pass
