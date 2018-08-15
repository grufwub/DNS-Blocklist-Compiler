from functools import wraps
import threading

def synchronized(lock_attr_name):
    def _synched(func):
        @wraps(func)
        def _synchronizer(self, *args, **kws):
            lock = self.__getattribute__(lock_attr_name)
            lock.acquire()
            try:
                return func(self, *args, **kws)
            finally:
                lock.release()
        return _synchronizer
    return _synched

class SafeCollection:
    # have some class functions here
    def __init__(self, ordered):
        self.IS_ORDERED = ordered
        self.LOCK = threading.RLock()

class SafeDictionary(SafeCollection):
    def __init__(self, ordered = False):
        SafeCollection.__init__(self, ordered)
        self.__DICT = dict()
    
    @synchronized('LOCK')
    def __getitem__(self, key):
        return self.__DICT[key]
    
    @synchronized('LOCK')
    def pop_item(self, key):
        return self.__DICT.pop(key, None)

    @synchronized('LOCK')
    def length(self):
        return len(self.__DICT)
    
class SafeList(SafeCollection):
    def __init__(self, ordered = False):
        SafeCollection.__init__(self, ordered)
        self.__LIST = list()

    @synchronized('LOCK')
    def append(self, item):
        self.__LIST.append(item)

    @synchronized('LOCK')
    def extend(self, items):
        self.__LIST.extend(items)

    @synchronized('LOCK')
    def __getitem__(self, indices):
        return self.__LIST[indices]

    @synchronized('LOCK')
    def pop_item(self, index):
        return self.__LIST.pop(index)

    @synchronized('LOCK')
    def pop_items(self, indices):
        return_item = list()
        for index in indices:
            return_item.append(self.__LIST.pop(index))
        return return_item

    @synchronized('LOCK')
    def pop_start(self):
        return self.pop_item(0)

    @synchronized('LOCK')
    def pop_end(self):
        return self.__LIST.pop(len(this.__LEN) - 1)

    @synchronized('LOCK')
    def length(self):
        return len(self.__LIST)
    
        
            
