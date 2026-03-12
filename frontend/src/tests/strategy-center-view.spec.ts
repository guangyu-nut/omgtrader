import { mount } from "@vue/test-utils";
import { describe, expect, it } from "vitest";

import StrategyCenterView from "../views/StrategyCenterView.vue";

describe("StrategyCenterView", () => {
  it("creates a top-n equal weight strategy", () => {
    const wrapper = mount(StrategyCenterView);

    expect(wrapper.text()).toContain("Top N 等权轮动");
  });
});
