import pandas as pd
import os
import sqlite3
from datetime import datetime

class CacheManager():
    def __init__(self, cache_directory, use_cache):
        self.use_cache = use_cache
        if self.use_cache:
            if cache_directory is None:
                cache_directory = os.path.join(os.path.expanduser("~"), "fl-data-dl-cache")

            # create the directory if it doesn't exist
            if not os.path.exists(cache_directory):
                os.makedirs(cache_directory)

            print("using cache   - {}".format(cache_directory))

        self.cache_directory = cache_directory
        
    def save_data(self, data_frame, *keys):
        if self.use_cache:
            key = self._create_key(keys)
            cache_file_path = os.path.join(self.cache_directory, key)
            data_frame.to_csv(cache_file_path, index=False)
            print("saving cache  - {}".format(key))
            
    def get_data(self, *keys, expiry=None):
        if self.use_cache:
            key = self._create_key(keys)
            cache_file_path = os.path.join(self.cache_directory, key)

            use_cache = False
            # does the file exist?
            if os.path.isfile(cache_file_path):
                # does the cache expire?
                if expiry is not None:
                    # is the cached file older than the expiry datetime?
                    file_age = datetime.fromtimestamp(os.path.getmtime(cache_file_path))
                    if expiry < file_age:
                        use_cache = True
                else:
                    use_cache = True

            if use_cache:
                print("reading cache - {}".format(key))
                return pd.read_csv(cache_file_path)

    def _create_key(self, ids):
        return "_".join(map(str, ids))
