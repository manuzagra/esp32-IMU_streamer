import os
import ujson

import utils


# collection =
# {
# 0: {'ssid': 'asdasd', 'password': 'jujujo'}
# 1: {'ssid': 'asdasd', 'password': 'jujujo', 'autoconnect': False}
# 2: {'ssid': 'asdasd', 'password': 'jujujo'}
# 3: {'ssid': 'asdasd', 'password': 'jujujo', 'autoconnect': True}
# 4: {'ssid': 'asdasd', 'password': 'jujujo', 'name': 'house'}
# }



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
        self.flush(collections)
        for coll in list(collections):
            del self._cache[coll]

    def flush(self, collections=None):
        if collections is None:
            collections = self._cache.keys()
        for coll in list(collections):
            with open(self._abs_path(collection), 'w') as f:
                ujson.dump(self._cache[collection], f)

    def create_collection(self, collection, cache=True):
        # a collection is gonna be a new file
        with open(self._abs_path(collection), 'w') as f:
            pass
        if cache:
            self._cache[collection] = {'next_id': 0}

    def drop_collection(self, collection):
        self.clear_cache(collection)
        or.remove(self._abs_path(collection))

    def insert(self, collection, document):
        self._cache[collection][self._cache[collection][next_id]] = document
        self._cache[collection][next_id] += 1

    # this decorator convert expresion into a exception free function
    # it is needed because no all the documents contain the same information
    def _safe_expression(exp):
        def s_exp(*args, **kwargs):
            try:
                return exp(*args, **kwargs)
            except:
                return False
        return s_exp

    def find(self, collection, expression, fields=None):
        expression = self._safe_expression(expression)
        if fields:
            def get_fields(doc):
                available_fields = set(fields).intersection(set(doc.keys()))
                return {k:v for k, v in doc.items() if k in available_fields}
        else:
            get_fields = lambda doc: doc
        return [get_fields(doc) for id, doc in self._cache[collection].items() if expression(doc)]

    def update(self, collection, selection_criteria, update_function):
        selection_criteria = self._safe_expression(selection_criteria)
        update_function = self._safe_expression(update_function)
        [update_function(d) for id, doc in self._cache[collection].items() if selection_criteria(doc)]

    def delete(self, collection, expression):
        def delete_doc(id):
            del self._cache[collection][id]
        temp = self._cache[collection].items()
        [delete_doc(id) for id, doc in temp if expression(doc)]
