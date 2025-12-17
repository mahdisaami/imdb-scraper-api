import asyncio
import random


async def rate_limit():
    await asyncio.sleep(random.uniform(1, 2))  # Simple rate limiting: wait for 1 second between requests