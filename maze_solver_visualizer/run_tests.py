#!/usr/bin/env python3
"""
Test Runner Script for Maze Solver Visualizer
Provides convenient commands for running different test suites (standalone Python tests)
"""
import sys
import subprocess
import argparse
from pathlib import Path
import os


def run_python_test(test_file, description):
    """Run a standalone Python test file"""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: python3 {test_file}")
    print('='*60)
    
    try:
        result = subprocess.run([sys.executable, test_file], capture_output=True, text=True)
        
        if result.stdout:
            print(result.stdout)
            
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
            
        if result.returncode == 0:
            print(f"✅ {description} completed successfully!")
        else:
            print(f"❌ {description} failed with return code {result.returncode}")
            
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ Error running {description}: {e}")
        return False


def get_test_files():
    """Get all available standalone test files"""
    test_files = {
        'unit': [
            ('tests/test_algorithms.py', 'Algorithm Base Classes'),
            ('tests/test_bfs.py', 'Breadth-First Search'),
            ('tests/test_dfs.py', 'Depth-First Search'), 
            ('tests/test_dijkstra.py', 'Dijkstra Algorithm'),
            ('tests/test_explicit_graph.py', 'Explicit Graph'),
            ('tests/test_maze_generator.py', 'Maze Generator'),
            ('tests/test_maze_solver.py', 'Maze Solver'),
            ('tests/test_visualizer.py', 'Maze Visualizer'),
        ],
        'integration': [
            ('tests/test_compatibility.py', 'Backward Compatibility'),
        ],
        'all': []  # Will be populated with all tests
    }
    
    # Add all tests to 'all' category
    test_files['all'] = test_files['unit'] + test_files['integration']
    
    return test_files


def main():
    parser = argparse.ArgumentParser(description="Run standalone tests for Maze Solver Visualizer")
    parser.add_argument('--all', action='store_true', help='Run all tests')
    parser.add_argument('--unit', action='store_true', help='Run unit tests only')
    parser.add_argument('--integration', action='store_true', help='Run integration tests only') 
    parser.add_argument('--list', action='store_true', help='List available test files')
    parser.add_argument('--summary', action='store_true', help='Show summary of test results')
    parser.add_argument('--fast', action='store_true', help='Run core tests only (algorithms, generator, solver)')
    
    args = parser.parse_args()
    
    # Change to script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    test_files = get_test_files()
    
    if args.list:
        print("Available test files:")
        for category, files in test_files.items():
            if category != 'all':
                print(f"\n{category.title()} Tests:")
                for file_path, description in files:
                    print(f"  {file_path} - {description}")
        return 0
    
    success = True
    total_tests = 0
    passed_tests = 0
    
    # Determine which tests to run
    if args.fast:
        selected_tests = [
            ('tests/test_algorithms.py', 'Algorithm Base Classes'),
            ('tests/test_bfs.py', 'Breadth-First Search'),
            ('tests/test_dfs.py', 'Depth-First Search'),
            ('tests/test_dijkstra.py', 'Dijkstra Algorithm'),
            ('tests/test_maze_generator.py', 'Maze Generator'),
            ('tests/test_maze_solver.py', 'Maze Solver'),
        ]
    elif args.unit:
        selected_tests = test_files['unit']
    elif args.integration:
        selected_tests = test_files['integration']
    elif args.all or not any([args.unit, args.integration, args.fast]):
        selected_tests = test_files['all']
    else:
        selected_tests = test_files['all']
    
    # Run selected tests
    results = []
    for test_file, description in selected_tests:
        if Path(test_file).exists():
            test_success = run_python_test(test_file, description)
            results.append((description, test_success))
            success &= test_success
        else:
            print(f"⚠️  Warning: {test_file} not found, skipping...")
            results.append((description, False))
            success = False
    
    # Summary
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print('='*60)
    
    if args.summary or len(results) > 3:
        for description, test_success in results:
            status = "✅ PASS" if test_success else "❌ FAIL"
            print(f"{status} {description}")
    
    passed_count = sum(1 for _, success in results if success)
    total_count = len(results)
    
    print(f"\nResults: {passed_count}/{total_count} test files passed")
    
    if success:
        print("🎉 All requested tests completed successfully!")
        print("✅ Full test suite passed")
    else:
        print("❌ Some tests failed")
        print("🔍 Check the output above for details")
    
    print('='*60)
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())