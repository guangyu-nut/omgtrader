# Python 策略中心重构设计

**Date:** 2026-03-12
**Status:** Approved for implementation planning

## Goal

将当前以参数化表单为主的 `策略中心`，重构为一个以 `Python 策略资产管理` 为核心的研究工作台页面。

这次改造的目标是让用户可以在系统内维护自己的 Python 策略清单，并完成完整的新增、查看、编辑、删除流程。

## Scope

This change covers:

- 将 `策略中心` 主页面改为左右分栏工作台
- 左侧展示现有 Python 策略列表及摘要信息
- 右侧展示当前选中策略的详情和编辑表单
- 支持 Python 策略的新增、列表、详情、更新、删除
- 新增独立的 `PythonStrategy` 后端资源与数据库表
- 提供基础代码模板，降低新建策略时的空白状态压力

This change does not cover:

- Python 策略执行、回测接入或运行日志
- 浏览器 IDE 体验，如 Monaco、代码补全、诊断、lint
- 代码版本历史、发布状态、回滚能力
- 对现有 `回测中心` 的主流程改造
- 旧参数化策略资产的数据迁移或删除

## Current State

当前 `策略中心` 是一个简单的表单页：

- 可以创建股票池
- 可以创建参数化策略实例
- 没有策略列表
- 没有详情查看
- 没有更新和删除能力
- 不支持 Python 策略资产

因此，这次改造不是增量补按钮，而是把 `策略中心` 的主视角从“参数化策略创建”切换为“Python 策略资产管理”。

## Design

### Layout Model

`策略中心` 保持现有路由 `/strategy-center`，但页面内容改为单页工作台布局：

- 左栏：`Python 策略列表`
- 右栏：`策略详情 / 编辑器`

页面不额外拆成“列表页”和“详情页”，避免用户在策略浏览和编辑之间频繁跳转。

### Left Panel

左栏包含：

- 页面标题 `策略中心`
- `新建 Python 策略` 按钮
- 关键字搜索框
- 策略列表

每条策略显示以下摘要：

- 策略名称
- 一行说明
- 标签
- 最近更新时间

列表默认按 `updated_at` 倒序排列，便于优先看到最近维护的策略。

### Right Panel

右栏有三种状态：

1. `空状态`
   - 当前没有任何策略时，提示用户创建第一条 Python 策略
2. `未选中状态`
   - 已存在策略但未选中时，引导用户从左侧选择策略
3. `编辑状态`
   - 选中某条策略后，显示完整的可编辑表单

编辑表单包含：

- `name`
- `description`
- `tags`
- `parameter_schema_text`
- `code`

操作区包含：

- `保存`
- `删除`
- `恢复未保存修改`

### New Strategy Flow

点击 `新建 Python 策略` 后：

- 左侧列表高亮一个新建中的临时项
- 右侧进入可编辑状态
- 代码区预填基础 Python 模板
- 只有用户点击 `保存` 后，才真正创建数据库记录，避免产生空白策略脏数据

基础模板只负责提供结构感，不承担执行约束。模板内容应足够简单，让用户能看懂这是“未来会被回测系统消费的 Python 策略定义”。

### Search Behavior

搜索框用于前端本地过滤当前已加载的策略列表。

搜索匹配以下字段：

- `name`
- `description`
- `tags`

这次不做服务端分页与复杂筛选。若未来策略数量明显增大，再补服务端查询能力。

### Unsaved Changes Behavior

如果用户已修改当前策略但尚未保存：

- 切换到其他策略前，需要明确提示存在未保存修改
- 用户可以选择继续切换或留在当前编辑状态
- 点击 `恢复未保存修改` 时，右侧内容回退到最近一次保存结果

### Delete Behavior

删除必须二次确认。

删除成功后：

- 左侧列表移除对应策略
- 若列表仍有其它策略，自动选中下一条策略
- 若没有剩余策略，右侧回到空状态

## Data Model

新增独立资源 `PythonStrategy`，字段如下：

- `id`
- `user_id`
- `name`
- `description`
- `tags_text`
- `parameter_schema_text`
- `code`
- `created_at`
- `updated_at`

### Field Semantics

- `name`
  - 必填，列表主标题
- `description`
  - 可为空字符串，用于描述策略逻辑、适用场景与限制
- `tags_text`
  - 简单文本存储，前端以标签数组方式编辑和展示
- `parameter_schema_text`
  - 自然语言或轻结构化文本，用于说明策略未来需要哪些输入参数
- `code`
  - Python 代码正文

### Validation Rules

- `name` 不能为空
- `code` 不能为空
- `description` 允许为空字符串，但接口返回时保持稳定字段结构
- `tags` 总数不做复杂限制，但空标签需要在写入前清理
- `parameter_schema_text` 允许为空字符串

这次不做：

- Python 语法执行校验
- 运行入口函数签名校验
- JSON Schema 级参数定义

## API Design

在现有 `strategies` 模块下新增一组 Python 策略接口：

- `GET /api/strategies/python`
- `GET /api/strategies/python/{id}`
- `POST /api/strategies/python`
- `PUT /api/strategies/python/{id}`
- `DELETE /api/strategies/python/{id}`

### Response Shapes

列表接口返回轻量摘要项：

- `id`
- `name`
- `description`
- `tags`
- `updated_at`

详情接口返回完整字段：

- `id`
- `name`
- `description`
- `tags`
- `parameter_schema_text`
- `code`
- `created_at`
- `updated_at`

### Error Handling

需要明确支持以下错误响应：

- 未登录时返回认证失败
- 请求不存在的策略时返回 `404`
- 试图访问其他用户策略时返回 `404` 或等价隐藏策略存在性的结果
- 提交空名称或空代码时返回 `422`
- 删除已不存在的策略时返回 `404`

## Integration Boundaries

### Relationship With Existing Strategy Assets

现有的 `StrategyInstance` 与 `StockPool` 模型暂时保留，用于支撑当前回测主流程。

但在前端 `策略中心` 主页面中：

- 不再展示参数化策略创建表单
- 不再把旧参数化策略作为主要入口
- 页面主语义切换为 `Python 策略资产中心`

### Relationship With Backtest Center

`回测中心` 这次不接 Python 策略执行。

这意味着：

- 当前回测入口保持原状
- Python 策略资产只完成保存和管理，不参与执行
- 若用户从产品上进入 `回测中心`，仍会看到旧回测流程

这是明确的阶段性分层，而不是遗漏。后续若要接入 Python 执行，需要单独设计执行接口、运行沙箱和结果映射。

## Frontend Units

建议拆成以下前端单元：

- `StrategyCenterView`
  - 页面容器，管理列表加载、当前选中项、保存状态和删除后的选中逻辑
- `PythonStrategyListPanel`
  - 左侧列表、搜索、新建入口
- `PythonStrategyEditor`
  - 右侧详情与编辑表单

这种拆分可以保证列表逻辑、编辑逻辑和页面编排彼此独立，后续接入更强编辑器时不需要重写整页。

## Backend Units

建议在 `backend/app/modules/strategies/` 下新增或扩展以下边界：

- `models.py`
  - 新增 `PythonStrategy`
- `schemas.py`
  - 新增 create / update / list / read schema
- `repository.py`
  - 新增列表、详情、创建、更新、删除数据访问方法
- `service.py`
  - 负责输入清理、用户隔离、默认模板填充
- `router.py`
  - 暴露 Python 策略 CRUD API

各单元职责应保持单一，不要把默认模板字符串、标签解析和 HTTP 错误映射杂糅在同一层。

## Migration Strategy

数据库新增一条 migration，用于创建 `python_strategies` 表。

本次 migration 不做：

- 旧参数化策略向 Python 策略的数据迁移
- 删除或重命名现有策略相关表

这样可以降低对当前稳定回测链路的冲击。

## Testing

### Backend

后端测试需要覆盖：

- 创建 Python 策略成功
- 获取列表成功并按更新时间返回
- 获取单条策略详情成功
- 更新策略成功
- 删除策略成功
- 非当前用户不可访问他人策略
- 非法 payload 返回校验错误

### Frontend

前端测试需要覆盖：

- 页面首次加载时正确展示空状态或首条策略
- 列表能展示策略摘要
- 点击新建后进入编辑状态并带默认代码模板
- 保存成功后列表和右侧详情同步更新
- 删除成功后正确切换到下一状态
- 搜索可以过滤列表
- 存在未保存修改时切换策略会出现提示

## Success Criteria

- 用户进入 `策略中心` 后，看到的是 Python 策略列表而非参数化表单
- 用户可以完成 Python 策略的新增、查看、编辑、删除
- 页面能稳定展示名称、说明、标签、参数说明和代码
- 后端提供完整且隔离良好的 Python 策略 CRUD 能力
- 现有回测中心流程不因这次改造而失效
