from __future__ import annotations

from dataclasses import dataclass

from app.services.backtest_engine.execution import TradeFill


@dataclass(frozen=True, slots=True)
class PortfolioPosition:
    symbol: str
    entry_price: float
    exit_price: float
    return_pct: float


@dataclass(frozen=True, slots=True)
class PortfolioResult:
    positions: list[PortfolioPosition]
    equity_curve: list[float]


class PortfolioService:
    def build(self, *, fills: list[TradeFill], exit_prices: dict[str, float]) -> PortfolioResult:
        positions: list[PortfolioPosition] = []
        for fill in fills:
            if fill.status != "filled" or fill.price is None:
                continue

            exit_price = exit_prices.get(fill.symbol)
            if exit_price is None:
                continue

            net_return = (exit_price - fill.price - fill.commission) / fill.price
            positions.append(
                PortfolioPosition(
                    symbol=fill.symbol,
                    entry_price=fill.price,
                    exit_price=exit_price,
                    return_pct=net_return,
                )
            )

        portfolio_return = sum(position.return_pct for position in positions) / len(positions) if positions else 0.0
        return PortfolioResult(
            positions=positions,
            equity_curve=[1.0, 1.0 + portfolio_return],
        )
