import pandas as pd
import os
import sqlite3
from time import time

# 12 hours
CACHE_EXPIRY_TIME = 12 * 60 *60
# debug - make cache expiry after 1 second
# CACHE_EXPIRY_TIME = 1

class CacheManager():
    def __init__(self, cache_directory, use_cache):
        self.use_cache = use_cache
        if self.use_cache:
            if cache_directory is None:
                cache_directory = os.path.join(os.path.expanduser("~"), "fl-data-dl-cache")

            # create the directory if it doesn't exist
            if not os.path.exists(cache_directory):
                os.makedirs(cache_directory)

        self.cache_directory = cache_directory
        
    def save_data(self, data_frame, *keys):
        if self.use_cache:
            key = self._create_key(keys)
            cache_file_path = os.path.join(self.cache_directory, key)
            data_frame.to_csv(cache_file_path, index=False)
            print("saving cache  - {}".format(key))
            
    def get_data(self, *keys, expires=True):
        if self.use_cache:
            key = self._create_key(keys)
            cache_file_path = os.path.join(self.cache_directory, key)

            use_cache = False
            # does the file exist?
            if os.path.isfile(cache_file_path):
                # does the cache expire?
                if expires:
                    # is the cache file less than 12 hours old?
                    if time() - os.path.getmtime(cache_file_path) < CACHE_EXPIRY_TIME:
                        use_cache = True
                else:
                    use_cache = True

            if use_cache:
                print("reading cache - {}".format(key))
                return pd.read_csv(cache_file_path)
        
    def _create_key(self, ids):
        return "_".join(map(str, ids))
