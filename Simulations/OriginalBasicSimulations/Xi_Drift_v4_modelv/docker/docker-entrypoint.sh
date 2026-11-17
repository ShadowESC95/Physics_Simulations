#!/bin/bash
set -e

# Activate virtualenv if needed
if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
fi

echo "🚀 Launching Physics Simulation"

# Run from config (default fallback)
if [ "$1" == "" ]; then
    python cli.py --config configs/default.yml
else
    exec "$@"
fi
