import os
import ujson

import utils

class JSONDB:
    def __init__(self, path):
        # the database is going to be a directory with files inside
        if not path.endswith('.db/'):
            path = path + '.db/'
        # save the base path
        self._base_path = path
        # create the folder if it does not exist
        if not utils.is_dir(path):
            for d in path.split('/'):
                try:
                    os.mkdir(d)
                    os.chdir(d)
                except:
                    pass
        os.chdir('/')
        if not utils.is_dir(path):
            raise Exception('JSONDB cannot create the structure of directories')

        # to work with a collection first we will have to cache it
        self._cache = {}

    def _abs_path(self, path):
        return self._base_path + '/'

    def cache(self, collections=None):
        with open(self._abs_path(collection)) as f:
            self._cache[collection] = ujson.load(f)

    def clear_cache(self, collections=None):
        pass

    def flush(self, collections=None):
        if collections is None:
            collections = self._cache.keys()
        for coll in list(collections):
            with open(self._abs_path(collection), 'w') as f:
                ujson.dump(self._cache[collection], f)

    def create_collection(self, name):
        # a collection is gonna be a new file
        pass
