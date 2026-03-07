"""Quarterly filings refresh job."""


async def refresh_quarterly_data():
    """Pull quarterly filings and shareholding patterns.

    Tasks:
    - Check for new BSE quarterly filings
    - Update shareholding patterns
    - Refresh fundamentals cache
    """
    raise NotImplementedError("quarterly_filings not yet implemented")


if __name__ == "__main__":
    import asyncio
    asyncio.run(refresh_quarterly_data())
