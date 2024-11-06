#!/usr/bin/python3
"""LFU Caching System"""

from base_caching import BaseCaching


class LFUCache(BaseCaching):
    """LFUCache class that inherits from BaseCaching and implements
    a caching system with an LFU (Least Frequently Used) eviction policy.
    """

    def __init__(self):
        """Initialize the LFUCache class."""
        super().__init__()
        self.usage_frequency = {}  # Dictionary to keep track of usage frequency
        self.usage_order = []      # List to maintain insertion order for LRU handling

    def put(self, key, item):
        """Add an item in the cache.
        
        If the cache exceeds MAX_ITEMS, discard the least frequently used item.
        If multiple items have the same frequency, discard the least recently used.
        """
        if key is None or item is None:
            return

        if key in self.cache_data:
            # Update the item and increment the usage frequency
            self.cache_data[key] = item
            self.usage_frequency[key] += 1
        else:
            # If cache exceeds capacity, remove the LFU (or LRU if ties)
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                # Find the item with the lowest frequency and remove it
                min_freq = min(self.usage_frequency.values())
                lfu_keys = [k for k in self.usage_order if self.usage_frequency[k] == min_freq]
                
                # Discard the LRU among the LFU items
                lfu_key = lfu_keys[0]
                self.usage_order.remove(lfu_key)
                del self.cache_data[lfu_key]
                del self.usage_frequency[lfu_key]
                print(f"DISCARD: {lfu_key}")

            # Insert the new key with initial frequency 1
            self.cache_data[key] = item
            self.usage_frequency[key] = 1
            self.usage_order.append(key)

        # Update the usage order to mark the key as recently used
        if key in self.usage_order:
            self.usage_order.remove(key)
        self.usage_order.append(key)

    def get(self, key):
        """Get an item by key. If the key exists, it increments its usage frequency."""
        if key is None or key not in self.cache_data:
            return None

        # Increment frequency and update usage order
        self.usage_frequency[key] += 1
        self.usage_order.remove(key)
        self.usage_order.append(key)
        
        return self.cache_data[key]

