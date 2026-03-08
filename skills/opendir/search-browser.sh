#!/bin/bash
#
# Open Directory Browser Search
# Uses browser automation to search Google and extract open directory URLs
#
# Usage: search-browser.sh "<query>" [type]
#
# Requires: browser tool available in OpenClaw
#

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
QUERY="$1"
TYPE="${2:-all}"

if [ -z "$QUERY" ]; then
    echo "Usage: search-browser.sh \"<query>\" [type]"
    echo "Types: all, ebook, music, video, software, archive"
    exit 1
fi

# Get the Google URL from search.sh
GOOGLE_URL=$("$SCRIPT_DIR/search.sh" "$QUERY" "$TYPE" | grep "Google URL" -A1 | tail -1)

echo "Open this URL in browser:"
echo "$GOOGLE_URL"
echo ""
echo "In OpenClaw, use:"
echo "  browser open \"$GOOGLE_URL\""
echo "  browser snapshot"
echo "  Then extract directory links from the snapshot"
