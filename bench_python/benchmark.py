import argparse
import timeit

from bir_parser import BIRParser
from time_decorator import st_time

@st_time
def benchmark_tests(lines: list[str], parser: BIRParser):
    for line in lines:
        parser.parse(line)
        
    

if __name__ == "__main__":
    # Get the args to find the test case's path
    parser = argparse.ArgumentParser(description='Benchmarking for Parser for BIR')
    parser.add_argument('--tests', action="store", dest='tests', default="./test_cases.txt")
    args = parser.parse_args()

    # Create the parser to do the parsing
    parser = BIRParser()
    
    # Collect tests
    tests = []
    
    # Open the file and test the code
    with open(args.tests, 'r') as f:
        lines = f.readlines()
        for line in lines:
            tests.append(line.strip())

    benchmark_tests(tests, parser)
    
