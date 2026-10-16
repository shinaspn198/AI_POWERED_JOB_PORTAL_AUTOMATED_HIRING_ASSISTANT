"""
Day 60 - In-Memory High Performance LRU Cache with TTL

Features:
- O(1) get/set with OrderedDict
- Time-to-Live (TTL) expiration
- Memory bound limit (max items eviction)
- Thread-safe operations
- Hit/Miss telemetry
"""

import time
import threading
from collections import OrderedDict
from typing import Any, Optional, Tuple, Dict


class TTLCache:
    """Thread-safe LRU Cache with TTL expiration and item limit."""

    def __init__(self, maxsize: int = 1000, default_ttl_sec: float = 300.0):
        self.maxsize = maxsize
        self.default_ttl = default_ttl_sec
        self._cache: OrderedDict[str, Tuple[Any, float]] = OrderedDict()
        self._lock = threading.Lock()
        self.hits = 0
        self.misses = 0

    def get(self, key: str) -> Optional[Any]:
        """Retrieves item from cache if present and not expired."""
        with self._lock:
            if key not in self._cache:
                self.misses += 1
                return None

            value, expiry = self._cache[key]
            if time.time() > expiry:
                # Expired
                del self._cache[key]
                self.misses += 1
                return None

            # Move to end (most recently used)
            self._cache.move_to_end(key)
            self.hits += 1
            return value

    def set(self, key: str, value: Any, ttl_sec: Optional[float] = None) -> None:
        """Stores item in cache with TTL and enforces maxsize."""
        ttl = ttl_sec if ttl_sec is not None else self.default_ttl
        expiry = time.time() + ttl

        with self._lock:
            if key in self._cache:
                self._cache.move_to_end(key)
            self._cache[key] = (value, expiry)

            # Evict oldest if exceeding maxsize
            if len(self._cache) > self.maxsize:
                self._cache.popitem(last=False)

    def clear(self) -> None:
        """Empties cache."""
        with self._lock:
            self._cache.clear()
            self.hits = 0
            self.misses = 0

    def get_stats(self) -> Dict[str, Any]:
        """Returns cache telemetry."""
        with self._lock:
            total_lookups = self.hits + self.misses
            hit_ratio = round((self.hits / total_lookups) * 100, 2) if total_lookups > 0 else 0.0
            return {
                "size": len(self._cache),
                "maxsize": self.maxsize,
                "hits": self.hits,
                "misses": self.misses,
                "hit_ratio_percent": hit_ratio,
            }


# Global shared instance for model and scoring caches
GLOBAL_EVAL_CACHE = TTLCache(maxsize=2000, default_ttl_sec=600.0)
