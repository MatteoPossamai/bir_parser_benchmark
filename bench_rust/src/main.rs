pub mod parser;
use std::time::SystemTime;

use pilator::parser::Parser;

fn main() {
    let mut parser = pilator::parser::naive_parser::NaiveParser::new();

    for regex in parser::get_regex_for_bench() {
        parser.add_regex(regex);
    }

    let start = SystemTime::now();

    // Parse the regexes
    for _ in 0..27{
        let res = parser.parse("(BExp_Const (bv))", None);
        println!("{:?}", res);
    }

    let end = SystemTime::now();
    let time = end.duration_since(start).unwrap();

    println!("--- Rust Benchmark ---");
    println!("Number of tests: {}", parser::get_regex_for_bench().len());
    println!("Time taken (seconds): {}", time.as_secs());
    println!("Average time per test (seconds): {}", time.as_secs() / parser::get_regex_for_bench().len() as u64);
}
