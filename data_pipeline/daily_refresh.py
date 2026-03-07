"""Daily EOD data refresh job."""


async def refresh_eod_data():
    """Pull end-of-day data and warm caches.

    Tasks:
    - Fetch closing prices for all tracked symbols
    - Update technical indicators
    - Warm quote cache for next day
    """
    raise NotImplementedError("daily_refresh not yet implemented")


if __name__ == "__main__":
    import asyncio
    asyncio.run(refresh_eod_data())
