import { expect, test } from "@playwright/test";

test("login page renders on local startup", async ({ page }) => {
  await page.goto("http://127.0.0.1:5173/login");
  await expect(page.getByRole("heading", { name: "登录" })).toBeVisible();
});
