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
    },
    {
      path: "/workbench",
      name: "workbench",
      component: () => import("./views/WorkbenchView.vue"),
    },
    {
      path: "/backtests",
      name: "backtests",
      component: () => import("./views/BacktestCenterView.vue"),
    },
    {
      path: "/data-center",
      name: "data-center",
      component: () => import("./views/DataCenterView.vue"),
    },
    {
      path: "/strategy-center",
      name: "strategy-center",
      component: () => import("./views/StrategyCenterView.vue"),
    },
    {
      path: "/results/:jobId",
      name: "results",
      component: () => import("./views/ResultsView.vue"),
    },
  ],
});
