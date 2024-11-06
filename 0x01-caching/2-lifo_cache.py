#!/usr/bin/env python3
"""Inherits from BaseCaching"""


from base_caching import BaseCaching


class LIFOCache(BaseCaching):
    """
    dictionary and `MAX_ITEMS` constant.
    """

    def __init__(self):
        """
        Initializes the `LIFOCache` instance.
        """
        super().__init__()  # Call the parent class constructor

    def put(self, key, item):
        """
        Adds a key-value pair to the cache, followin.
        """
        if key is None or item is None:
            return

        if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            # LIFO eviction: remove the most recently added item
            discarded_key = list(self.cache_data.keys())[-1]
            del self.cache_data[discarded_key]
            print("DISCARD: {}".format(discarded_key))

        self.cache_data[key] = item

    def get(self, key):
        """
        Retrieves key (Any): The key to look up.
        """
        return self.cache_data.get(key)
