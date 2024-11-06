#!/usr/bin/python3
"""LRU Caching System"""

from base_caching import BaseCaching


class LRUCache(BaseCaching):
    """LRUCache class that inherits from BaseCaching and implements
    a caching system with an LRU (Least Recently Used) eviction policy.
    """

    def __init__(self):
        """Initialize the LRUCache class."""
        super().__init__()
        self.lru_order = []

    def put(self, key, item):
        """Add an item in the cache.
        If the cache exceeds the MAX_ITEMS, it discards the least
        recently used item.
        """
        if key is None or item is None:
            return

        if key in self.cache_data:
            # Move the key to the end of the LRU order to mark it as recentl
            self.lru_order.remove(key)
        elif len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            # If cache is full, remove the least recently used item
            lru_key = self.lru_order.pop(0)
            del self.cache_data[lru_key]
            print(f"DISCARD: {lru_key}")

        # Add or update the cache and LRU order
        self.cache_data[key] = item
        self.lru_order.append(key)

    def get(self, key):
        """Get an item by key. If the key exists, it is marked as recently"""
        if key is None or key not in self.cache_data:
            return None

        # Move accessed key to the end of LRU order
        self.lru_order.remove(key)
        self.lru_order.append(key)
        return self.cache_data[key]
