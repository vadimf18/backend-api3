#!/usr/bin/env bash
set -e

echo " Running pre-test checks..."
python /app/app/tests_pre_start.py

echo " Running test suite..."
bash ./scripts/test.sh "$@"

echo "Tests completed successfully"
