#!/bin/bash
#
# DorXNG Search - Execute searches via Tor-routed SearXNG
#
# Usage: dorxng-search.sh "<query>" [format]
# Format: json (default), html
#
# Requires: DORXNG_URL environment variable or dorxng Docker container
#

set -e

QUERY="$1"
FORMAT="${2:-json}"

# Get DorXNG URL from environment or detect from Docker
if [ -z "$DORXNG_URL" ]; then
    DORXNG_IP=$(docker inspect dorxng --format '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' 2>/dev/null || echo "")
    if [ -n "$DORXNG_IP" ]; then
        DORXNG_URL="https://${DORXNG_IP}/search"
    else
        echo "Error: Set DORXNG_URL environment variable or run dorxng container"
        exit 1
    fi
fi

if [ -z "$QUERY" ]; then
    echo "Usage: dorxng-search.sh \"<query>\" [format]"
    echo "Format: json (default), html"
    exit 1
fi

# URL encode the query
ENCODED=$(python3 -c "import urllib.parse; print(urllib.parse.quote('''$QUERY''', safe=''))")

# Execute search (skip SSL verification for internal Docker IPs)
curl -sk --max-time 120 "${DORXNG_URL}?q=${ENCODED}&format=${FORMAT}"
