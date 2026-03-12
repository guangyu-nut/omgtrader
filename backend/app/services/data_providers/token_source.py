class TokenSourceProvider:
    def fetch_symbol_bars(self, symbol_code: str) -> dict:
        raise NotImplementedError("Token source provider is not implemented yet")
