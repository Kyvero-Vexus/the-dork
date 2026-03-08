# DorXNG Search Skill

Privacy-focused metasearch via self-hosted DorXNG (SearXNG over Tor). Routes queries through Tor for anonymity.

## Configuration

Set the `DORXNG_URL` environment variable to your DorXNG instance:
```bash
export DORXNG_URL="http://your-dorxng-host:8889/search"
```

Optional fallback (clearnet SearXNG):
```bash
export SEARXNG_URL="http://your-searxng-host:8888/search"
```

---

# DorXNG Setup Guide

## What is DorXNG?

DorXNG is SearXNG configured to route all searches through Tor for anonymity. It provides:
- **Privacy** - All searches go through Tor exit nodes
- **Metasearch** - Queries 7+ search engines simultaneously
- **API access** - JSON output for programmatic use
- **Result accumulation** - Results improve over time as Tor circuits rotate

## Quick Start (Docker)

### Option 1: Use the Official DorXNG Image

```bash
# Pull and run DorXNG
docker run -d \
  --name dorxng \
  -p 8889:443 \
  --restart unless-stopped \
  ghcr.io/unya/dorxng:latest

# Wait for Tor to connect (check logs)
docker logs -f dorxng

# You should see: {"IsTor":true,"IP":"<tor-exit-ip>"}
```

### Option 2: Build from SearXNG + Tor

```bash
# Create docker-compose.yml
cat > docker-compose.yml << 'EOF'
version: '3'
services:
  dorxng:
    image: searxng/searxng:latest
    container_name: dorxng
    ports:
      - "8889:8080"
    environment:
      - SEARXNG_BASE_URL=http://localhost:8889/
    volumes:
      - ./searxng:/etc/searxng:rw
    restart: unless-stopped
EOF

# Run through Tor proxy (requires tor service)
# Or use a Tor-proxying network configuration
```

### Option 3: Use System Tor + SearXNG

If you have Tor running locally:

```bash
# Install Tor
sudo apt install tor  # Debian/Ubuntu
# or
brew install tor      # macOS

# Start Tor
sudo systemctl start tor  # Linux
# or
brew services start tor   # macOS

# Run SearXNG with Tor proxy
docker run -d \
  --name searxng \
  -p 8888:8080 \
  -e HTTP_PROXY=socks5://host.docker.internal:9050 \
  -e HTTPS_PROXY=socks5://host.docker.internal:9050 \
  searxng/searxng:latest
```

## Verification

After starting DorXNG, verify it's working:

```bash
# Check Tor connectivity
docker exec dorxng curl -s https://check.torproject.org/api/ip

# Should return: {"IsTor":true,"IP":"..."}

# Test search
curl "http://localhost:8889/search?q=test&format=json" | head -100
```

## Bootstrap Check

When first using this skill, run the bootstrap check:

```python
from skills.dorxng.search import search

# Quick test
results = search("test")
if results:
    print(f"✓ DorXNG working! Found {len(results)} results")
else:
    print("✗ DorXNG not responding. Check setup.")
```

## Common Issues

### "Connection refused"
- DorXNG container not running: `docker start dorxng`
- Wrong port: Check `docker ps` for actual port mapping

### "Empty results"
- Tor circuit blocked: Wait 10 seconds for circuit rotation
- Rate limited: Reduce query frequency
- Try multiple passes with `search_persistent()`

### "SSL certificate error"
- Normal for internal Docker IPs
- The search.py script handles this automatically

### "Tor not connected"
- Check logs: `docker logs dorxng`
- Look for `{"IsTor":true,...}`
- May take 30-60 seconds on first start

## Resource Requirements

- **RAM:** ~1.25GB per DorXNG container
- **CPU:** Low when idle, spikes during searches
- **Disk:** ~500MB for image
- **Network:** Tor bandwidth is limited (~2-5 Mbps typical)

## Alternative: Public SearXNG Instances

If you can't run DorXNG, you can use public SearXNG instances (less private):

```bash
# Set to a public instance
export DORXNG_URL="https://searx.be/search"
export DORXNG_URL="https://search.bus-hit.me/search"
```

**Warning:** Public instances may log queries and have rate limits.

---

## Usage

### Basic Search
```bash
skills/dorxng/search.sh "<query>"
```

### Python API
```python
from skills.dorxng.search import search, dork_search, search_odir, search_persistent

# Basic search
results = search("machine learning")
print(f"Found {len(results)} results")

# Dork search
results = dork_search('site:github.com "api_key"')

# Open directory search
results = search_odir("SICP", "ebook")

# Persistent search (multiple passes, accumulates results)
results = search_persistent("site:example.com filetype:pdf", passes=3, delay=5)
```

### Agent Workflow

When you need to search the web:

1. **Execute via DorXNG** - Anonymous, Tor-routed
2. **Parse JSON results** - Already in structured format
3. **If no results, retry with more passes** - Tor circuits rotate

## Tools

| Tool | Description |
|------|-------------|
| `search.sh` | Shell wrapper for quick searches |
| `search.py` | Python module with full API |

## Search Types

### Regular Search
```
query: "machine learning tutorials"
```

### Dork Search
```
query: "site:example.com filetype:pdf"
query: "intitle:\"index of\" \"parent directory\""
```

### Engine-Specific
```
query: "!google machine learning"     # Force Google
query: "!duckduckgo privacy"          # Force DDG
query: "!brave search"                # Force Brave
```

## Result Format

```json
{
  "query": "test",
  "number_of_results": 100,
  "results": [
    {
      "title": "Result Title",
      "url": "https://example.com",
      "content": "Snippet of content...",
      "engine": "google",
      "parsed_url": ["https", "example.com", "/path", "", ""]
    }
  ]
}
```

## Agents

When asked to search for something:

1. **Identify search type:**
   - General info → Regular search
   - Files/media → Use dork patterns
   - Security research → Use dork library

2. **Execute via DorXNG:**
   ```python
   from skills.dorxng import search
   results = search("your query here")
   ```

3. **Process results:**
   - Filter by relevance
   - Extract URLs and titles
   - Present top 5-10 to user

4. **Fallback if needed:**
   ```python
   from skills.dorxng import search_with_fallback
   results = search_with_fallback("query")  # Tries DorXNG then SearXNG
   ```

## Integration with Other Skills

This skill is used by:
- **dorking** - Execute Google dork queries
- **opendir** - Find open directory files

Both skills default to DorXNG API instead of browser automation.

---

# DorXNG Tips (CRITICAL)

## Result Accumulation

**IMPORTANT:** DorXNG accumulates results over time. A single query pass may only return a few results, but repeated passes will find more.

```python
# Use persistent search for better results
from skills.dorxng.search import search_persistent

# Makes 3 passes with 5-second delays between them
results = search_persistent("site:example.com filetype:pdf", passes=3, delay=5)
```

### Why Multiple Passes?

- Tor exit nodes may be rate-limited by search engines
- Different Tor circuits = different results
- Upstream engines may return different results on retry
- **More passes = more results** 🍻

## Upstream Search Providers

Each query is sent to **7 upstream engines**:
- Google
- DuckDuckGo
- Qwant
- Bing
- Brave
- Startpage
- Yahoo

This generates a lot of requests - have patience!

## Common Issues

### Minimal Results

Sometimes you'll hit a Tor exit node that's already blocked by search providers, giving you minimal results.

**Solution:** Just keep firing off queries. Try again with a new pass.

### HTTP/504 Gateway Timeout

This is expected sometimes - means the Tor circuit is too slow.

**Solution:** Just keep going! The next circuit may be faster.

### HTTP/500 Errors

If you see HTTP/500 responses from the SearXNG container:

**Solution:** Kill and restart the Docker container:
```bash
docker restart dorxng
# Wait for {"IsTor":true,"IP":"..."} in logs
```

### Empty Results

Tor circuit may be blocked.

**Solution:**
1. Wait a few seconds (circuit rotates every 10s)
2. Retry the query
3. Use `search_persistent()` with multiple passes

## Container Management

### Resource Usage

Each DorXNG container uses approximately **1.25GB RAM**.

### Starting Containers

When starting multiple containers, **wait a few seconds between each** to let Tor establish connections.

### Healthy Startup

A valid startup shows:
```
Checking Tor Connectivity..
{"IsTor":true,"IP":"<tor-exit-node-ip>"}
```

If you see anything else, kill and restart.

### Circuit Rotation

Tor circuits refresh every **10 seconds** automatically (via `MaxCircuitDirtiness`).

## Rate Limiting & Timeouts

### Default Timeouts

- DorXNG: 120 seconds (Tor is slow)
- SearXNG: 30 seconds (clearnet)

### Delay Between Requests

For repeated queries, add a delay to avoid overwhelming Tor:
```python
import time
for query in queries:
    results = search(query)
    time.sleep(4)  # 4-second delay
```

### Concurrent Queries

If running multiple concurrent queries, **4 concurrent** seems to be the sweet spot. More increases the chance of HTTP/429 responses.

## Database Persistence (DorXNG Client)

The full DorXNG client stores results in SQLite (`dorxng.db`). Our API wrapper doesn't use the database by default, but you can enable persistence:

```python
from skills.dorxng.search import SearchSession

# Create a session that accumulates results
session = SearchSession(db_path="my_search.db")
session.search("query 1")
session.search("query 2")
# Results are stored and de-duplicated in the database

# Query the database later
all_results = session.query_database(".*sql$")
```

### Database Limits

For large-scale harvesting:
- Suggested max database size: **50k entries**
- Use `--limitdatabase 50` with DorXNG client
- Split into multiple databases if needed

## Troubleshooting

### Container Unhealthy

```bash
docker logs dorxng  # Check for Tor connectivity
docker restart dorxng  # Restart if needed
```

### Slow Responses

This is normal for Tor. Expected response times:
- 30-120 seconds per query
- Longer if Tor circuit is slow

### Memory Issues

If the DorXNG client process crashes with "Killed":
- Machine ran out of memory
- Database file is still intact
- Use smaller databases or limit recursion

---

## Quick Reference

| Scenario | Solution |
|----------|----------|
| Few results | Run multiple passes with delay |
| HTTP/504 timeout | Normal, keep going |
| HTTP/500 errors | Restart container |
| Slow responses | Normal for Tor (30-120s) |
| Rate limited | Wait 10s for circuit rotation |
| Memory crash | Use smaller databases |

---

# Effective Search Workflows

## Iterative Query Refinement

Don't stop at the first query. Refine based on what you find:

```
Pass 1: "DECtalk public domain release"        → Found HN thread mentioning Edward Bruckert
Pass 2: "Edward Bruckert DECtalk archive"      → Found GitHub repo with archive URL
Pass 3: "datajake.braillescreen.net tts"       → Found the full directory structure
```

Each query builds on discoveries from the previous one.

## Follow the Breadcrumbs

When search results show promising URLs, **fetch them for context**:

```python
# Search gives you a lead
results = search("topic source code release")

# Fetch promising pages to get the full story
web_fetch("https://news.ycombinator.com/item?id=XXXXX")  # HN thread with details
web_fetch("https://github.com/user/repo")                 # README with archive links
```

Search results are snippets. The actual information is often in the pages they link to.

## Explore Directory Structures

When you find an open directory or archive:

```
1. Fetch the parent directory to see what else exists
2. Fetch the root to understand the full scope
3. Map the structure before downloading

Example:
  Found: /TTS/DECtalk/source%20code/
  Explore: /TTS/ → / (root) → discover 15+ categories
```

## Effective Query Patterns

### For Software Archives

```python
# Find source releases
"software-name source code public domain release"
"software-name archive developer release"

# Find specific files
"site:archive.org software-name source"
"site:github.com software-name source release"

# Find communities discussing it
"software-name developer mailing list"
"software-name source code hn"  # Hacker News threads
```

### For Research Topics

```python
# Start broad, then narrow
"topic overview"           → Find key terms
"topic researcher-name"    → Find papers/projects
"site:edu topic filetype:pdf" → Find academic papers
```

## Multi-Source Verification

Cross-reference findings across multiple sources:

```
1. Search finds HN thread → mentions developer
2. Search developer name → finds GitHub repo
3. Fetch GitHub README → finds archive URL
4. Fetch archive directory → confirms contents
```

Each source validates the others.

## Recommended Pass Strategy

| Query Type | Passes | Delay | Reason |
|------------|--------|-------|--------|
| Quick lookup | 1 | 0 | Single result sufficient |
| Research | 2 | 5s | More context |
| OSINT/Archives | 3 | 5s | Comprehensive coverage |
| File hunting | 3-5 | 5s | Maximize discovery |

## Output Richness

Provide value beyond just URLs:

```
✓ Title and URL
✓ Brief description of what was found
✓ How sources connect (HN → GitHub → Archive)
✓ Directory structure when relevant
✓ Key people/organizations involved
✓ Historical context if discovered
```

This turns raw search results into actionable intelligence.
