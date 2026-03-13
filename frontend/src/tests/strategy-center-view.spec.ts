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

    expect(wrapper.text()).toContain("Python 策略工作台");
    expect(wrapper.text()).toContain("Alpha");
    expect(wrapper.get('[data-testid="python-code-editor"]').exists()).toBe(true);
    expect((wrapper.get("textarea").element as HTMLTextAreaElement).value).toContain("class Strategy");
  });

  it("filters the list with the search box", async () => {
    fetchMock.mockResolvedValueOnce({
      ok: true,
      json: async () => [
        {
          id: "ps-1",
          name: "Alpha",
          description: "动量",
          tags: ["轮动"],
          updated_at: "2026-03-12T10:00:00Z",
        },
        {
          id: "ps-2",
          name: "Beta",
          description: "均值回归",
          tags: ["反转"],
          updated_at: "2026-03-12T11:00:00Z",
        },
      ],
    });
    fetchMock.mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        id: "ps-1",
        name: "Alpha",
        description: "动量",
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

    await wrapper.get('input[placeholder="搜索策略"]').setValue("Beta");

    expect(wrapper.text()).toContain("Beta");
    expect(wrapper.text()).not.toContain("Alpha");
  });

  it("prompts before switching away from unsaved edits", async () => {
    vi.spyOn(window, "confirm").mockReturnValue(false);
    fetchMock
      .mockResolvedValueOnce({
        ok: true,
        json: async () => [
          {
            id: "ps-1",
            name: "Alpha",
            description: "动量",
            tags: ["轮动"],
            updated_at: "2026-03-12T10:00:00Z",
          },
          {
            id: "ps-2",
            name: "Beta",
            description: "反转",
            tags: ["反转"],
            updated_at: "2026-03-12T11:00:00Z",
          },
        ],
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          id: "ps-1",
          name: "Alpha",
          description: "动量",
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

    await wrapper.get('input[value="Alpha"]').setValue("Alpha Updated");
    await wrapper.get('button.list-item:not(.is-active)').trigger("click");
    await flushPromises();

    expect(window.confirm).toHaveBeenCalled();
    expect(fetchMock).toHaveBeenCalledTimes(2);
    expect((wrapper.get('input[value="Alpha Updated"]').element as HTMLInputElement).value).toBe("Alpha Updated");
  });

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

  it("confirms deletion and falls back to the empty state", async () => {
    vi.spyOn(window, "confirm").mockReturnValue(true);
    fetchMock
      .mockResolvedValueOnce({
        ok: true,
        json: async () => [
          {
            id: "ps-1",
            name: "Alpha",
            description: "动量",
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
          description: "动量",
          tags: ["轮动"],
          parameter_schema_text: "window: int",
          code: "class Strategy:\n    pass\n",
          created_at: "2026-03-12T10:00:00Z",
          updated_at: "2026-03-12T10:00:00Z",
        }),
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => null,
      });

    const wrapper = mount(StrategyCenterView);
    await flushPromises();
    await flushPromises();

    const deleteButton = wrapper
      .findAll("button")
      .find((candidate) => candidate.text() === "删除");

    expect(deleteButton).toBeDefined();

    await deleteButton!.trigger("click");
    await flushPromises();

    expect(window.confirm).toHaveBeenCalled();
    expect(wrapper.text()).toContain("创建第一条 Python 策略");
  });

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
});
