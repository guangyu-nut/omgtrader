import { describe, expect, it } from "vitest";

import { router } from "../router";

describe("router", () => {
  it("registers the login route", () => {
    expect(router.resolve("/login").name).toBe("login");
  });
});
