#!/usr/bin/env python3
"""
Test Runner Script for Maze Solver Visualizer
Provides convenient commands for running different test suites
"""
import sys
import subprocess
import argparse
from pathlib import Path


def run_command(command, description):
    """Run a command and handle output"""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {' '.join(command)}")
    print('='*60)
    
    try:
        result = subprocess.run(command, capture_output=True, text=True)
        
        if result.stdout:
            print("STDOUT:")
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


def main():
    parser = argparse.ArgumentParser(description="Run tests for Maze Solver Visualizer")
    parser.add_argument('--all', action='store_true', help='Run all tests')
    parser.add_argument('--unit', action='store_true', help='Run unit tests only')
    parser.add_argument('--integration', action='store_true', help='Run integration tests only')
    parser.add_argument('--performance', action='store_true', help='Run performance tests only')
    parser.add_argument('--coverage', action='store_true', help='Run tests with coverage report')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    parser.add_argument('--fast', action='store_true', help='Run fast tests only (exclude slow ones)')
    
    args = parser.parse_args()
    
    # Determine pytest executable
    pytest_cmd = 'pytest'
    
    # Base pytest arguments
    base_args = []
    if args.verbose:
        base_args.append('-v')
    else:
        base_args.append('-v')  # Always use verbose for better output
        
    # Add coverage if requested
    if args.coverage:
        base_args.extend(['--cov=.', '--cov-report=html', '--cov-report=term'])
        
    # Exclude slow tests if fast flag is used
    if args.fast:
        base_args.extend(['-m', 'not slow'])
        
    success = True
    
    if args.all or (not any([args.unit, args.integration, args.performance])):
        # Run all tests
        command = [pytest_cmd] + base_args + ['tests/']
        success &= run_command(command, "All Tests")
        
    else:
        if args.unit:
            # Run unit tests
            unit_files = [
                'tests/test_maze_generator.py',
                'tests/test_maze_solver.py',
                'tests/test_dfs.py',
                'tests/test_bfs.py',
                'tests/test_dijkstra.py'
            ]
            command = [pytest_cmd] + base_args + unit_files
            success &= run_command(command, "Unit Tests")
            
        if args.integration:
            # Run integration tests
            command = [pytest_cmd] + base_args + ['tests/test_integration.py']
            success &= run_command(command, "Integration Tests")
            
        if args.performance:
            # Run performance tests
            command = [pytest_cmd] + base_args + ['tests/test_performance.py']
            success &= run_command(command, "Performance Tests")
    
    # Final summary
    print(f"\n{'='*60}")
    if success:
        print("🎉 All requested tests completed successfully!")
        print("✅ Test suite passed")
    else:
        print("❌ Some tests failed")
        print("🔍 Check the output above for details")
    print('='*60)
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())