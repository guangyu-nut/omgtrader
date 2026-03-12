from __future__ import annotations

from dataclasses import dataclass

from fastapi import HTTPException

from app.modules.ai_assistant.repository import AiAssistantRepository


@dataclass(frozen=True, slots=True)
class InsightOutput:
    summary: str
    risks: list[str]


class LocalInsightProvider:
    def generate(self, *, strategy_name: str, total_return: float | None, max_drawdown: float | None) -> InsightOutput:
        total_return_pct = 0.0 if total_return is None else total_return * 100
        drawdown_pct = 0.0 if max_drawdown is None else max_drawdown * 100
        summary = (
            f"策略 {strategy_name} 本次回测累计收益约 {total_return_pct:.2f}%，"
            f"最大回撤约 {drawdown_pct:.2f}%。"
        )
        risks = [
            "建议继续验证不同股票池下的稳健性。",
            "建议补充更多调仓周期和手续费场景对比。",
        ]
        return InsightOutput(summary=summary, risks=risks)


class AiAssistantService:
    def __init__(
        self,
        repository: AiAssistantRepository,
        *,
        provider: LocalInsightProvider | None = None,
    ) -> None:
        self._repository = repository
        self._provider = provider or LocalInsightProvider()

    def generate_backtest_insight(self, *, job_id: str, current_user_id: str):
        job, metric, strategy = self._repository.get_backtest_context(job_id=job_id)
        if job is None or strategy is None or strategy.created_by_user_id != current_user_id:
            raise HTTPException(status_code=404, detail="backtest result not found")

        output = self._provider.generate(
            strategy_name=strategy.name,
            total_return=metric.total_return if metric is not None else None,
            max_drawdown=metric.max_drawdown if metric is not None else None,
        )
        return self._repository.save_insight(
            job_id=job_id,
            summary=output.summary,
            risks=output.risks,
        )
