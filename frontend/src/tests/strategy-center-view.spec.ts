import { flushPromises, mount } from "@vue/test-utils";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import StrategyCenterView from "../views/StrategyCenterView.vue";


const fetchMock = vi.fn();


describe("StrategyCenterView", () => {
  beforeEach(() => {
    fetchMock.mockReset();
    vi.stubGlobal("fetch", fetchMock);
    if (typeof window !== "undefined" && window.localStorage && typeof window.localStorage.clear === "function") {
      window.localStorage.clear();
    }
  });

  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("shows the empty state when there are no python strategies", async () => {
    fetchMock.mockResolvedValueOnce({
      ok: true,
      json: async () => [],
    });

    const wrapper = mount(StrategyCenterView);
    await flushPromises();

    expect(wrapper.text()).toContain("新建 Python 策略");
    expect(wrapper.text()).toContain("创建第一条 Python 策略");
  });

  it("loads an existing python strategy into the editor", async () => {
    fetchMock
      .mockResolvedValueOnce({
        ok: true,
        json: async () => [
          {
            id: "ps-1",
            name: "Alpha",
            description: "动量轮动",
            tags: ["轮动"],
            updated_at: "2026-03-12T10:00:00Z",
          },
        ],
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          id: "ps-1",
          name: "Alpha",
          description: "动量轮动",
          tags: ["轮动"],
          parameter_schema_text: "window: int",
          code: "class Strategy:\n    pass\n",
          created_at: "2026-03-12T10:00:00Z",
          updated_at: "2026-03-12T10:00:00Z",
        }),
      });

    const wrapper = mount(StrategyCenterView);
    await flushPromises();
    await flushPromises();

    expect(wrapper.text()).toContain("Alpha");
    expect((wrapper.get("textarea").element as HTMLTextAreaElement).value).toContain("class Strategy");
  });
});
