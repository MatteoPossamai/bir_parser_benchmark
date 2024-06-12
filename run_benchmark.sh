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