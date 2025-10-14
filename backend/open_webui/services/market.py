from open_webui.services.markets import MARKETS, DEFAULT_MARKET

def locale_by_market(market: str) -> str:
	"""
	Get locale by market, fallback if not supported.
	"""
	market_lower = market.lower()
	return MARKETS[market_lower] if market_lower in MARKETS else DEFAULT_MARKET
