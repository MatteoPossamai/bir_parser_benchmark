pub mod parser;
use std::time::SystemTime;

fn main() {
    let mut parser = pilator::parser::naive_parser::NaiveParser::new();

    for regex in parser::get_regex_for_bench() {
        println!("{:?}", regex);
    }

    let start = SystemTime::now();

    for _ in 0..1000 {
        
    }

    let end = SystemTime::now();
    let time = end.duration_since(start).unwrap();

    println!("--- Rust Benchmark ---");
    println!("Number of tests: {}", parser::get_regex_for_bench().len());
    println!("Time taken (seconds): {}", time.as_secs());
    // println!("Average time per test (seconds): {}", time.as_secs() / parser::get_regex_for_bench().len() as u64);
}
