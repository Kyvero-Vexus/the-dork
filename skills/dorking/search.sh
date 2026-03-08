#!/bin/bash
#
# Google Dork Query Generator
# Generates Google search URLs from dork queries
#
# Usage: search.sh "<dork query>"
#

set -e

QUERY="$1"

if [ -z "$QUERY" ]; then
    echo "Usage: search.sh \"<dork query>\""
    echo ""
    echo "Examples:"
    echo "  search.sh \"site:example.com filetype:pdf\""
    echo "  search.sh \"intitle:\\\"index of\\\" \\\"parent directory\\\"\""
    echo "  search.sh \"site:edu filetype:pptx \\\"machine learning\\\"\""
    exit 1
fi

# URL encode the query
encode_query() {
    local string="$1"
    python3 -c "import urllib.parse; print(urllib.parse.quote('$string', safe=''))"
}

ENCODED=$(encode_query "$QUERY")

# Output
echo "=== Google Search ==="
echo "https://www.google.com/search?q=$ENCODED"
echo ""
echo "=== DuckDuckGo Search ==="
echo "https://duckduckgo.com/?q=$ENCODED"
