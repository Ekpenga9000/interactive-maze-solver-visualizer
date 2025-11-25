"""
Setup script for Maze Solver & Visualizer
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="maze-solver-visualizer",
    version="1.0.0",
    author="CS5001 Student",
    author_email="your.email@example.com",
    description="A Python application that generates random mazes and solves them using various pathfinding algorithms",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/maze-solver-visualizer",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Education",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.12",
        "Topic :: Education",
        "Topic :: Games/Entertainment :: Puzzle Games",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: pygame",
    ],
    python_requires=">=3.12",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0",
            "black>=23.0",
            "flake8>=6.0",
            "mypy>=1.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "maze-solver=main:main",
        ],
    },
    project_urls={
        "Bug Tracker": "https://github.com/yourusername/maze-solver-visualizer/issues",
        "Documentation": "https://github.com/yourusername/maze-solver-visualizer#readme",
        "Source Code": "https://github.com/yourusername/maze-solver-visualizer",
    },
)