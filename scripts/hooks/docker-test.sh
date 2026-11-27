#!/usr/bin/env bash
set -e

# Run tests inside Docker before committing.

if [ ! -f "Dockerfile" ]; then
    exit 0
fi

# Only run when relevant files are staged.
STAGED=$(git diff --cached --name-only --diff-filter=AM |
    grep -E '(^src/|^tests/|^Dockerfile$|^pyproject\.toml$|^\.dockerignore$)' || true)

if [ -z "$STAGED" ]; then
    exit 0
fi

# Tests will be implemented in Module 5.
if [ ! -d "tests" ]; then
    echo "SKIPPED: tests/ does not exist yet (Module 5)."
    exit 0
fi

echo "Building Docker image and running tests..."

if ! docker build -t kata-tests-precommit . -q > /dev/null 2>&1; then
    echo "ERROR: Docker build failed."
    exit 1
fi

if ! docker run --rm kata-tests-precommit; then
    echo "ERROR: Tests failed inside Docker."
    exit 1
fi

echo "All tests passed."
