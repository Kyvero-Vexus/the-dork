#!/bin/bash
#
# SearX Search - Search via public SearX instances
#
# Usage: search.sh "<query>" [instance_url]
#
# WARNING: SearX is NOT anonymous. Queries go over clearnet.
# For anonymous search, use DorXNG instead.
#

set -e

QUERY="$1"
INSTANCE="${2:-https://search.bus-hit.me}"

if [ -z "$QUERY" ]; then
    echo "Usage: search.sh \"<query>\" [instance_url]"
    echo ""
    echo "Instances (see searx.space for full list):"
    echo "  https://search.bus-hit.me"
    echo "  https://searx.be"
    echo "  https://search.sapti.me"
    echo ""
    echo "WARNING: SearX is NOT anonymous. Use DorXNG for anonymous search."
    exit 1
fi

# URL encode the query
ENCODED=$(python3 -c "import urllib.parse; print(urllib.parse.quote('''$QUERY''', safe=''))")

# Execute search (respect rate limits - add delay)
echo "Searching via $INSTANCE..."
sleep 1

curl -s --max-time 30 "${INSTANCE}/search?q=${ENCODED}&format=json"
