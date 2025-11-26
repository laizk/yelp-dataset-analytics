#!/bin/bash
set -e

echo "🚀 Running dbt build (seed + run + test)..."
dbt build

exec "$@"
