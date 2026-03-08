#!/bin/bash
#
# Open Directory Search Query Generator
# Generates Google dork queries for finding files on open directories
#
# Usage: search.sh "<query>" [type]
# Types: all, ebook, music, video, software, archive
#

set -e

QUERY="$1"
TYPE="${2:-all}"

if [ -z "$QUERY" ]; then
    echo "Usage: search.sh \"<query>\" [type]"
    echo "Types: all, ebook, music, video, software, archive"
    exit 1
fi

# URL encode the query
encode_query() {
    local string="$1"
    python3 -c "import urllib.parse; print(urllib.parse.quote('$string', safe=''))"
}

ENCODED=$(encode_query "$QUERY")

generate_query() {
    local q="$1"
    local type="$2"
    
    case "$type" in
        ebook)
            # Ebooks, PDFs, comics
            echo "+(.MOBI|.CBZ|.CBR|.CBC|.CHM|.EPUB|.FB2|.LIT|.LRF|.ODT|.PDF|.PRC|.PDB|.PML|.RB|.RTF|.TCR) \"$q\" intitle:\"index of\" -inurl:(jsp|pl|php|html|aspx|htm|cf|shtml) -inurl:(listen77|mp3raid|mp3toss|mp3drug|index_of|wallywashis)"
            ;;
        music)
            # Music files
            echo "\"$q\" intitle:\"music\" (mp3|aac|flac|wav|ogg|m4a) \"Parent Directory\" -htm -html -asp -php -listen77 -idmusic -airmp3 -shexy -vmp3"
            ;;
        video)
            # Video files
            echo "\"$q\" (avi|mp4|mkv|mpg|wmv|mov|divx|m4v) \"Parent Directory\" -\"Trailer\" -torrent -serial -cdkey -web-shelf -asp -html -zoozle -jsp -htm -listen77 -idmovies -shexy"
            ;;
        software)
            # Software, ISOs, programs
            echo "\"$q\" (exe|iso|dmg|apk|deb|rpm|msi|bin) intitle:\"index of\" \"Parent Directory\" -inurl:(html|htm|php|asp|jsp) -torrent -magnet"
            ;;
        archive)
            # Archives, collections
            echo "\"$q\" (zip|rar|7z|tar|gz|bz2|tgz) intitle:\"index of\" \"Parent Directory\" -html -htm -php -asp -jsp"
            ;;
        all|*)
            # General open directory search
            echo "\"$q\" intitle:\"index of\" \"Parent Directory\" -html -htm -php -asp -jsp -blog -forum -store -shop"
            ;;
    esac
}

# Generate the dork query
DORK=$(generate_query "$QUERY" "$TYPE")

# Output both plain query and Google URL
echo "=== Search Query ==="
echo "$DORK"
echo ""
echo "=== Google URL ==="
echo "https://www.google.com/search?q=$(encode_query "$DORK")"
