import time

def st_time(func):
    """
        st decorator to calculate the total time of a func
    """

    def st_func(*args, **keyArgs):
        t1 = time.time()
        r = func(*args, **keyArgs)
        t2 = time.time()
        print("--- Python Benchmark ---")
        print("Number of tests: ", len(args[0]))
        print("Time taken (seconds): %s" % (t2 - t1))
        print("Average time per test (seconds): %s" % ((t2 - t1) / len(args[0])))
        return r

    return st_func