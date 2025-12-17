import asyncio


class ProxyRouter:
    def __init__(self, proxies):
        self.proxies = proxies
        self.lock = asyncio.Lock()
        self.index = 0

    async def get_proxy(self):
        async with self.lock:
            proxy = self.proxies[self.index]
            self.index = (self.index + 1) % len(self.proxies)
            return proxy
