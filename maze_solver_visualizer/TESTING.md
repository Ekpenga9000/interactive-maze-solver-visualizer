# Testing Quick Reference

## ❌ WRONG - Don't run test files directly:

```bash
python tests/test_dfs.py        # ❌ This will fail with import errors
python tests/test_bfs.py        # ❌ This will fail with import errors
```

## ✅ CORRECT - Use pytest or the test runner:

### Option 1: Using our custom test runner (recommended)

```bash
# Run all unit tests
python run_tests.py --unit

# Run specific test categories
python run_tests.py --integration
python run_tests.py --performance

# Run all tests
python run_tests.py --all

# Run with coverage
python run_tests.py --coverage
```

### Option 2: Using pytest directly

```bash
# Run specific test file
pytest tests/test_dfs.py -v
pytest tests/test_bfs.py -v
pytest tests/test_dijkstra.py -v

# Run multiple test files
pytest tests/test_dfs.py tests/test_bfs.py tests/test_dijkstra.py -v

# Run all unit tests
pytest tests/test_maze_generator.py tests/test_maze_solver.py tests/test_dfs.py tests/test_bfs.py tests/test_dijkstra.py -v

# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=. --cov-report=html
```

## Why the direct approach fails:

When you run `python tests/test_dfs.py`, Python doesn't properly set up the module path, so imports like `from algorithms.depth_first_search import DepthFirstSearch` fail because Python can't find the `algorithms` package.

pytest and our test runner properly configure the Python path and module resolution.

## Test Suite Summary:

- ✅ 112 unit tests passing
- 🧪 5 test files covering all algorithms and components
- 📊 Comprehensive coverage of maze generation, solving, and algorithms
- 🔧 Professional test structure with fixtures and configuration
