#!/usr/bin/env python3
"""
Test runner for SBARDS Project
"""

import os
import sys
import unittest
import argparse
import time
from datetime import datetime

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='SBARDS Project Test Runner')

    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose output')
    parser.add_argument('--pattern', '-p', help='Pattern to match test names (e.g. "TestOrchestrator")')
    parser.add_argument('--list', '-l', action='store_true', help='List available tests without running them')

    return parser.parse_args()

def discover_tests(pattern=None):
    """Discover all tests in the tests directory"""
    test_dir = os.path.join(os.path.dirname(__file__), 'tests')

    if not os.path.exists(test_dir):
        print(f"Error: Test directory not found: {test_dir}")
        return None

    loader = unittest.TestLoader()

    # Discover all tests
    all_tests = loader.discover(test_dir)

    # If pattern is specified, filter tests
    if pattern:
        filtered_suite = unittest.TestSuite()

        def add_matching_tests(suite):
            for test in suite:
                if isinstance(test, unittest.TestSuite):
                    # Recursively process test suites
                    add_matching_tests(test)
                else:
                    # Check if test name matches pattern
                    if pattern.lower() in test.id().lower():
                        filtered_suite.addTest(test)

        add_matching_tests(all_tests)
        return filtered_suite

    return all_tests

def list_tests(suite):
    """List all tests in the test suite"""
    if not suite:
        return

    tests = []

    def get_test_cases(test_suite):
        if isinstance(test_suite, unittest.TestSuite):
            for test in test_suite:
                get_test_cases(test)
        else:
            tests.append(test_suite)

    get_test_cases(suite)

    print("\nAvailable Tests:")
    print("===============")

    for i, test in enumerate(tests, 1):
        test_name = test.id()
        print(f"{i}. {test_name}")

    print(f"\nTotal: {len(tests)} tests")

def run_tests(suite, verbose=False):
    """Run the test suite"""
    if not suite:
        return False

    # Create a test runner
    runner = unittest.TextTestRunner(verbosity=2 if verbose else 1)

    # Run the tests
    print("\nRunning Tests:")
    print("=============")

    start_time = time.time()
    result = runner.run(suite)
    end_time = time.time()

    # Print summary
    print("\nTest Summary:")
    print("============")
    print(f"Ran {result.testsRun} tests in {end_time - start_time:.2f} seconds")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")

    # Return True if all tests passed
    return len(result.failures) == 0 and len(result.errors) == 0

def main():
    """Main function"""
    args = parse_arguments()

    print("\n" + "=" * 60)
    print("SBARDS Project Test Runner".center(60))
    print("=" * 60)
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Python: {sys.version}")
    print("=" * 60)

    # Discover tests
    test_suite = discover_tests(args.pattern)

    if args.list:
        list_tests(test_suite)
        return 0

    # Run tests
    success = run_tests(test_suite, args.verbose)

    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
