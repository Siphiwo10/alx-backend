#!/usr/bin/python3
"""MRU Caching System"""

from base_caching import BaseCaching


class MRUCache(BaseCaching):
    """MRUCache class that inherits from BaseCaching and implements
    a caching system with an MRU (Most Recently Used) eviction policy.
    """

    def __init__(self):
        """Initialize the MRUCache class."""
        super().__init__()
        self.mru_order = []

    def put(self, key, item):
        """Add an item in the cache.
        
        If the cache exceeds the MAX_ITEMS, it discards the most
        recently used item.
        """
        if key is None or item is None:
            return

        if key in self.cache_data:
            # Move the key to the end of the MRU order to mark it as recently used
            self.mru_order.remove(key)
        elif len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            # If cache is full, remove the most recently used item
            mru_key = self.mru_order.pop()
            del self.cache_data[mru_key]
            print(f"DISCARD: {mru_key}")

        # Add or update the cache and MRU order
        self.cache_data[key] = item
        self.mru_order.append(key)

    def get(self, key):
        """Get an item by key. If the key exists, it is marked as recently used."""
        if key is None or key not in self.cache_data:
            return None

        # Move accessed key to the end of MRU order
        self.mru_order.remove(key)
        self.mru_order.append(key)
        return self.cache_data[key]

