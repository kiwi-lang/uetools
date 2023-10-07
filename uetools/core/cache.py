import hashlib
import pickle
import os
import hashlib
from threading import Thread

import pkg_resources


def _compute_version(data: bytes) -> str:
    sha = hashlib.sha256()
    sha.update(data)
    return sha.hexdigest()


thread_message = dict()


def get_cache_status(cache_key):
    return thread_message[cache_key]


def _load_cache(path):
    cached_result = None
    cached_version = None

    if os.path.exists(path):
        with open(path, 'rb') as file:
            try:
                data = file.read()
                cached_version = _compute_version(data)
                cached_result = pickle.loads(data)
            except:
                cached_result = None
                cached_version = None

    return cached_result, cached_version


def _save_cache(key, path, result, cached_version):
    global thread_message

    data = pickle.dumps(result)
    new_version = _compute_version(data)

    if cached_version is None or cached_version != new_version:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'wb') as file:
            file.write(data)

    if cached_version is None:
        thread_message[key] = "Generated command cache"
        
    elif cached_version != new_version:
        thread_message[key] = "Warning data was out of date"

    else:
        thread_message[key] = "Command cache was up to date"


def cache_to_local(cache_key):
    """Cache function evaluation to the filesystem
    
    When the function is called again the cache is update async
    """
    def argkey(args, kwargs):
        key = hashlib.sha256()

        for arg in args:
            key.update(str(arg).encode())

        for k, v in kwargs.items():
            key.update(str(k).encode())
            key.update(str(v).encode())

        return key.hexdigest()

    caches = dict()

    def _cache_to_local(fun):
        def wrapper(*args, **kwargs):
            nonlocal caches

            argk = argkey(args, kwargs)
            key = f'{cache_key}_{argk}'
            cached_result, cached_version = caches.get(key, (None, None))
            
            if cached_result is None:
                cache_file = pkg_resources.resource_filename(
                    __name__, f"data/{key}.pkl"
                )
                cached_result, cached_version = _load_cache(cache_file)
                caches[key] = cached_result, cached_version

            def _update_data():
                cached_result = fun(*args, **kwargs)

                _save_cache(
                    cache_key, 
                    cache_file, 
                    cached_result, 
                    cached_version
                )
                return cached_result

            def _background():
                worker = Thread(target=_update_data)
                worker.start()

            if cached_result is not None:
                # launch a async update
                _background()
                # return current cache
                return cached_result
            else:
                # Have to to it sync
                return _update_data()

        return wrapper

    return _cache_to_local
