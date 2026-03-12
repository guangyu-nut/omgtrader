import { expect, test } from "@playwright/test";

test("user can login, prepare research flow, run backtest, and view results", async ({ page }) => {
  await page.goto("/login");
  await page.getByLabel("用户名").fill("demo");
  await page.getByLabel("密码").fill("pass123456");
  await page.getByRole("button", { name: "登录" }).click();

  await expect(page.getByRole("heading", { name: "工作台" })).toBeVisible();

  await page.goto("/data-center");
  await expect(page.getByText("最近更新时间")).toBeVisible();
  await expect(page.getByText("000001.SZ")).toBeVisible();

  await page.goto("/strategy-center");
  await page.getByRole("button", { name: "保存股票池" }).click();
  await expect(page.getByText("股票池已创建")).toBeVisible();
  await page.getByRole("button", { name: "创建策略" }).click();
  await expect(page.getByText("策略已创建")).toBeVisible();

  await page.goto("/backtests");
  await page.getByRole("button", { name: "开始回测" }).click();

  await expect(page.getByRole("heading", { name: "累计收益" })).toBeVisible();
  await expect(page.getByRole("heading", { name: "策略总结" })).toBeVisible();
});
