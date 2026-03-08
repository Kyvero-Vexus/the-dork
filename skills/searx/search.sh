#!/bin/bash
#
# SearX Search - public SearXNG clearnet fallback
#
# Usage:
#   search.sh "<query>"                  # auto-select + rotate
#   search.sh "<query>" <instance_url>   # fixed instance
#
# WARNING: SearX is NOT anonymous. Queries go over clearnet.
# Use DorXNG for anonymous search.
#

set -e

QUERY="$1"
INSTANCE="$2"

if [ -z "$QUERY" ]; then
    echo "Usage: search.sh \"<query>\" [instance_url]"
    echo ""
    echo "Examples:"
    echo "  search.sh \"SearXNG docs\""
    echo "  search.sh \"query\" https://searx.tiekoetter.com"
    echo ""
    echo "Find current instances at: https://searx.space/"
    echo ""
    echo "WARNING: SearX is NOT anonymous. Use DorXNG for anonymous search."
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

if [ -n "$INSTANCE" ]; then
    python3 "$SCRIPT_DIR/search.py" "$QUERY" --instance "$INSTANCE" --no-rotate
else
    python3 "$SCRIPT_DIR/search.py" "$QUERY"
fi
