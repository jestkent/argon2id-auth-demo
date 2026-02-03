import time
from collections import defaultdict, deque

class SimpleRateLimiter:
    """
    Allows max_requests in window_seconds per key.
    In production, use Redis or a gateway rate limiter.
    """
    def __init__(self, max_requests: int = 10, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.hits = defaultdict(deque)

    def allow(self, key: str) -> bool:
        now = time.time()
        q = self.hits[key]

        while q and (now - q[0]) > self.window_seconds:
            q.popleft()

        if len(q) >= self.max_requests:
            return False

        q.append(now)
        return True
