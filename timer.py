import time


def logging_time(original_fn):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = original_fn(*args, **kwargs)
        end_time = time.time()

        return result

    return wrapper
