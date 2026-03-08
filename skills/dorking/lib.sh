#!/bin/bash
#
# Google Dork Library
# Pre-built dork queries for common use cases
#
# Usage: lib.sh <category> [target]
# Categories: security, research, files, dev, osint, academic
#

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CATEGORY="$1"
TARGET="$2"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

encode_query() {
    python3 -c "import urllib.parse; print(urllib.parse.quote('''$1''', safe=''))"
}

print_query() {
    local name="$1"
    local query="$2"
    local encoded=$(encode_query "$query")
    
    echo -e "${GREEN}[$name]${NC}"
    echo "Query: $query"
    echo "Google: https://www.google.com/search?q=$encoded"
    echo "DDG: https://duckduckgo.com/?q=$encoded"
    echo ""
}

if [ -z "$CATEGORY" ]; then
    echo "Usage: lib.sh <category> [target]"
    echo ""
    echo "Categories:"
    echo "  security  - Security audit and recon queries"
    echo "  research  - General research queries"
    echo "  files     - Find specific file types"
    echo "  dev       - Web development queries"
    echo "  osint     - OSINT and company recon"
    echo "  academic  - Academic and research papers"
    echo ""
    echo "Target is optional - some queries are general, others use target as domain/topic"
    exit 1
fi

case "$CATEGORY" in
    security)
        if [ -z "$TARGET" ]; then
            echo -e "${RED}Error: security category requires a target domain${NC}"
            echo "Usage: lib.sh security example.com"
            exit 1
        fi
        
        echo -e "${YELLOW}Security Recon Queries for: $TARGET${NC}"
        echo ""
        
        print_query "Exposed Configs" "site:$TARGET filetype:env OR filetype:conf OR filetype:ini \"password\" OR \"secret\""
        print_query "Log Files" "site:$TARGET filetype:log \"error\" OR \"password\" OR \"exception\""
        print_query "Backup Files" "site:$TARGET filetype:bak OR filetype:backup OR filetype:old"
        print_query "Database Files" "site:$TARGET filetype:sql OR filetype:db OR filetype:sqlite"
        print_query "Admin Pages" "site:$TARGET inurl:admin OR inurl:login OR inurl:signin"
        print_query "Directory Listing" "site:$TARGET intitle:\"index of\" \"parent directory\""
        print_query "WordPress" "site:$TARGET inurl:wp-admin OR inurl:wp-login.php"
        print_query "PHP Info" "site:$TARGET inurl:phpinfo.php OR intitle:\"phpinfo()\""
        print_query "Exposed Git" "site:$TARGET inurl:.git intitle:\"index of\""
        print_query "API Keys" "site:$TARGET \"api_key\" OR \"apikey\" OR \"api-key\" filetype:json OR filetype:yaml"
        ;;
        
    research)
        if [ -z "$TARGET" ]; then
            echo -e "${RED}Error: research category requires a topic${NC}"
            echo "Usage: lib.sh research \"topic\""
            exit 1
        fi
        
        echo -e "${YELLOW}Research Queries for: $TARGET${NC}"
        echo ""
        
        print_query "PDF Documents" "\"$TARGET\" filetype:pdf"
        print_query "Presentations" "\"$TARGET\" filetype:pptx OR filetype:ppt"
        print_query "Spreadsheets" "\"$TARGET\" filetype:xlsx OR filetype:xls"
        print_query "Documents" "\"$TARGET\" filetype:docx OR filetype:doc"
        print_query "News Articles" "\"$TARGET\" site:news.google.com"
        print_query "Forum Discussions" "\"$TARGET\" site:reddit.com OR site:stackoverflow.com"
        print_query "Videos" "\"$TARGET\" site:youtube.com OR site:vimeo.com"
        ;;
        
    files)
        if [ -z "$TARGET" ]; then
            echo -e "${RED}Error: files category requires a file type or topic${NC}"
            echo "Usage: lib.sh files \"topic\" or lib.sh files pdf"
            exit 1
        fi
        
        echo -e "${YELLOW}File Search Queries for: $TARGET${NC}"
        echo ""
        
        # Check if TARGET is a known file type
        case "$TARGET" in
            pdf|ppt|pptx|doc|docx|xls|xlsx|epub|mobi|svg|zip|rar|mp3|mp4)
                print_query "$TARGET Files" "filetype:$TARGET"
                print_query "$TARGET Files (Edu)" "filetype:$TARGET site:edu"
                print_query "$TARGET Files (Gov)" "filetype:$TARGET site:gov"
                ;;
            *)
                # Treat as topic
                print_query "PDFs" "\"$TARGET\" filetype:pdf"
                print_query "Presentations" "\"$TARGET\" filetype:pptx OR filetype:ppt"
                print_query "Documents" "\"$TARGET\" filetype:docx OR filetype:doc"
                print_query "Spreadsheets" "\"$TARGET\" filetype:xlsx OR filetype:xls"
                print_query "eBooks" "\"$TARGET\" filetype:epub OR filetype:mobi"
                ;;
        esac
        ;;
        
    dev)
        if [ -z "$TARGET" ]; then
            echo -e "${RED}Error: dev category requires a target domain${NC}"
            echo "Usage: lib.sh dev example.com"
            exit 1
        fi
        
        echo -e "${YELLOW}Development Queries for: $TARGET${NC}"
        echo ""
        
        print_query "Subdomains" "site:*.$TARGET"
        print_query "Staging/Dev" "site:$TARGET inurl:staging OR inurl:dev OR inurl:test OR inurl:beta"
        print_query "API Endpoints" "site:$TARGET inurl:api OR inurl:v1 OR inurl:v2 OR inurl:rest"
        print_query "Source Code" "site:$TARGET filetype:php OR filetype:aspx OR filetype:js OR filetype:rb"
        print_query "Config Files" "site:$TARGET filetype:xml OR filetype:json OR filetype:yaml -package.json"
        print_query "Error Pages" "site:$TARGET intitle:\"error\" OR intitle:\"exception\""
        print_query "Git Repos" "site:github.com \"$TARGET\""
        ;;
        
    osint)
        if [ -z "$TARGET" ]; then
            echo -e "${RED}Error: osint category requires a target (company/person)${NC}"
            echo "Usage: lib.sh osint \"company name\""
            exit 1
        fi
        
        echo -e "${YELLOW}OSINT Queries for: $TARGET${NC}"
        echo ""
        
        print_query "LinkedIn Company" "site:linkedin.com/company/ \"$TARGET\""
        print_query "LinkedIn People" "site:linkedin.com/in/ \"$TARGET\""
        print_query "Crunchbase" "site:crunchbase.com \"$TARGET\""
        print_query "Job Postings" "site:lever.co OR site:greenhouse.io \"$TARGET\""
        print_query "Glassdoor" "site:glassdoor.com \"$TARGET\""
        print_query "Twitter/X" "site:twitter.com \"$TARGET\" OR site:x.com \"$TARGET\""
        print_query "Reddit Mentions" "site:reddit.com \"$TARGET\""
        print_query "News Articles" "\"$TARGET\" site:news.google.com"
        print_query "SEC Filings" "site:sec.gov \"$TARGET\""
        print_query "Court Records" "\"$TARGET\" site:pacer.gov OR site:courtlistener.com"
        ;;
        
    academic)
        if [ -z "$TARGET" ]; then
            echo -e "${RED}Error: academic category requires a topic${NC}"
            echo "Usage: lib.sh academic \"research topic\""
            exit 1
        fi
        
        echo -e "${YELLOW}Academic Queries for: $TARGET${NC}"
        echo ""
        
        print_query "University PDFs" "\"$TARGET\" site:edu filetype:pdf"
        print_query "University PPTs" "\"$TARGET\" site:edu filetype:pptx OR filetype:ppt"
        print_query "Theses" "\"$TARGET\" site:edu filetype:pdf \"thesis\" OR \"dissertation\""
        print_query "arXiv Papers" "site:arxiv.org \"$TARGET\""
        print_query "Semantic Scholar" "site:semanticscholar.org \"$TARGET\""
        print_query "Google Scholar" "site:scholar.google.com \"$TARGET\""
        print_query "ResearchGate" "site:researchgate.net \"$TARGET\""
        print_query "Gov Research" "\"$TARGET\" site:gov filetype:pdf"
        print_query "European Universities" "\"$TARGET\" site:.ac.uk OR site:.edu filetype:pdf"
        ;;
        
    *)
        echo -e "${RED}Unknown category: $CATEGORY${NC}"
        echo "Valid categories: security, research, files, dev, osint, academic"
        exit 1
        ;;
esac

echo -e "${YELLOW}Tip: Use browser tool to open and extract results${NC}"
