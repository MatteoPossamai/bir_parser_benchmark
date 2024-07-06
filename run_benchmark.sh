#!/bin/bash
echo "===== BENCHMARK TESTS FOR BIR PARSER ====="

# Python benchmark
echo
python3 ./bench_python/benchmark.py $1

# Rust benchmark
echo
cd bench_rust
cargo build --release > /dev/null 2>&1
./target/release/bench_rust

# Bindings benchmark
echo 
cd ../bench_bindings
python examples/example.py

# --- Python Benchmark ---
# Number of tests:  27
# Time taken (seconds): 0.06189894676208496
# Average time per test (seconds): 0.0022925535837809243

# --- Python Bindings Benchmark ---
# Number of tests: 1
# Time taken (seconds): 1.1205673217773438e-05