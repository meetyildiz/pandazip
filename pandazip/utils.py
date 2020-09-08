import gc
import time


def measure_time_mem(func):
    def wrapped_reduce(self, data, *args, **kwargs):
        # pre
        mem_usage_orig = data.memory_usage().sum() / 1024 ** 2

        start_time = time.time()
        # exec
        ret = func(self, data, *args, **kwargs)
        # post
        mem_usage_new = ret.memory_usage().sum() / 1024 ** 2

        end_time = time.time()
        """
        print(f'reduced data from {mem_usage_orig:.4f} MB '
              f'to {mem_usage_new:.4f} MB '
              f'in {(end_time - start_time):.2f} seconds')
        """
        gc.collect()
        return ret

    return wrapped_reduce