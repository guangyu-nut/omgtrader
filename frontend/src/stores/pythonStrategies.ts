import { reactive } from "vue";

import {
  createPythonStrategy,
  deletePythonStrategy,
  getPythonStrategy,
  listPythonStrategies,
  type PythonStrategyDetail,
  type PythonStrategyListItem,
  type PythonStrategyPayload,
  updatePythonStrategy,
} from "../api/pythonStrategies";


type PythonStrategiesState = {
  items: PythonStrategyListItem[];
  selectedId: string;
  selectedStrategy: PythonStrategyDetail | null;
};


const state = reactive<PythonStrategiesState>({
  items: [],
  selectedId: "",
  selectedStrategy: null,
});


async function loadList() {
  state.items = await listPythonStrategies();
  return state.items;
}

async function selectStrategy(strategyId: string) {
  state.selectedId = strategyId;
  state.selectedStrategy = await getPythonStrategy(strategyId);
  return state.selectedStrategy;
}

function clearSelection() {
  state.selectedId = "";
  state.selectedStrategy = null;
}

function restoreHighlight(id: string) {
  state.selectedId = id;
}

async function saveStrategy(payload: PythonStrategyPayload & { id?: string }) {
  const saved = payload.id
    ? await updatePythonStrategy(payload.id, payload)
    : await createPythonStrategy(payload);

  await loadList();
  state.selectedId = saved.id;
  state.selectedStrategy = saved;
  return saved;
}

async function removeStrategy(strategyId: string) {
  await deletePythonStrategy(strategyId);
  state.items = state.items.filter((item) => item.id !== strategyId);

  if (state.selectedId !== strategyId) {
    return state.selectedStrategy;
  }

  if (state.items.length === 0) {
    clearSelection();
    return null;
  }

  return selectStrategy(state.items[0].id);
}

function reset() {
  state.items = [];
  clearSelection();
}


export const pythonStrategyStore = {
  get items() {
    return state.items;
  },
  get selectedId() {
    return state.selectedId;
  },
  get selectedStrategy() {
    return state.selectedStrategy;
  },
  loadList,
  selectStrategy,
  clearSelection,
  restoreHighlight,
  saveStrategy,
  removeStrategy,
  reset,
};
