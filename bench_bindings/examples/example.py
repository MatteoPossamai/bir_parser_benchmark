import bench_bindings
import time

start = time.time()
result = bench_bindings.sum_as_string(1, 2)
end = time.time()

print("--- Python Bindings Benchmark ---")
print("Number of tests: 1")
print("Time taken (seconds): %s" % (end - start))