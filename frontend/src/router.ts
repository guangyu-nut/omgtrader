import { createRouter, createWebHistory } from "vue-router";

export const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: "/",
      redirect: "/login",
    },
    {
      path: "/login",
      name: "login",
      component: () => import("./views/LoginView.vue"),
      meta: {
        shell: false,
      },
    },
    {
      path: "/workbench",
      name: "workbench",
      component: () => import("./views/WorkbenchView.vue"),
      meta: {
        shell: true,
      },
    },
    {
      path: "/backtests",
      name: "backtests",
      component: () => import("./views/BacktestCenterView.vue"),
      meta: {
        shell: true,
      },
    },
    {
      path: "/data-center",
      name: "data-center",
      component: () => import("./views/DataCenterView.vue"),
      meta: {
        shell: true,
      },
    },
    {
      path: "/strategy-center",
      name: "strategy-center",
      component: () => import("./views/StrategyCenterView.vue"),
      meta: {
        shell: true,
      },
    },
    {
      path: "/results/:jobId",
      name: "results",
      component: () => import("./views/ResultsView.vue"),
      meta: {
        shell: true,
      },
    },
  ],
});
