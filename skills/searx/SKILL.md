# Public SearX Skill

Use public SearXNG instances for clearnet metasearch when DorXNG is unavailable or not desired.

## What is SearX?

SearX (SearXNG) is a privacy-respecting metasearch engine. It queries multiple search engines and aggregates results. Unlike DorXNG, **SearX is NOT anonymous** - it runs on clearnet, not through Tor.

## When to Use This Skill

The Dork should use public SearX instances only when:

1. **User explicitly requests clearnet search** — "search without Tor" or "use SearX"
2. **DorXNG is unavailable** — Not set up, and user declines to set it up
3. **DorXNG returns no results** — After multiple passes, still nothing found

**Decision flow:**
```
1. User requests search
2. Is DorXNG configured? → Use DorXNG (default)
3. If no DorXNG → Ask user: "DorXNG not set up. Would you like to:
   a) Set up DorXNG (Tor-routed, anonymous)
   b) Search via public SearX instances (clearnet, not anonymous)
   c) Set up local SearXNG"
4. Proceed based on user choice
```

## Finding Public SearX Instances

### Primary Source: searx.space

The authoritative list of public SearXNG instances:

```
https://searx.space/
```

This site lists all known public instances with:
- Instance URL
- Country
- TLS grade
- HTTP grade
- Whether it supports specific search engines
- Rate limits

### Selecting an Instance

**Good for automated search:**
- High uptime rating
- No CAPTCHA
- No heavy rate limiting
- Supports JSON output (`format=json` parameter)
- HTTP/TLS grade A or B

**Avoid instances that:**
- Require CAPTCHA
- Block automated access
- Have strict rate limits (queries per minute)
- Are frequently down

### Recommended Instances

Check searx.space for current reliable instances. As of 2026, some stable options include:
- `https://search.bus-hit.me/`
- `https://searx.be/`
- `https://search.sapti.me/`

**Always verify current status at searx.space before using.**

## Usage

### Basic Search

```python
import urllib.request
import urllib.parse
import json

def search_searx(query: str, instance: str = "https://search.bus-hit.me", timeout: int = 30):
    """
    Search via public SearX instance.
    
    Args:
        query: Search query
        instance: SearX instance URL (no trailing slash)
        timeout: Request timeout in seconds
    
    Returns:
        List of result dictionaries
    """
    encoded = urllib.parse.quote(query, safe='')
    url = f"{instance}/search?q={encoded}&format=json"
    
    req = urllib.request.Request(url, headers={
        'User-Agent': 'The-Dork/1.0 (https://github.com/Kyvero-Vexus/the-dork)'
    })
    
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            data = json.loads(response.read().decode('utf-8'))
            return data.get('results', [])
    except Exception as e:
        print(f"SearX error: {e}")
        return []
```

### Dork Search via SearX

```python
results = search_searx('site:github.com filetype:pdf "documentation"')
for r in results[:10]:
    print(f"{r.get('title')}: {r.get('url')}")
```

### Checking Instance Availability

```python
def check_instance(instance_url: str) -> bool:
    """Check if a SearX instance is responding."""
    try:
        req = urllib.request.Request(
            f"{instance_url}/search?q=test&format=json",
            headers={'User-Agent': 'The-Dork/1.0'}
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status == 200
    except:
        return False

# Check before using
if check_instance("https://search.bus-hit.me"):
    results = search_searx("query", "https://search.bus-hit.me")
```

## Boundaries

### DO NOT

- **Hammer instances** — Don't send rapid-fire queries
- **Ignore rate limits** — Respect 429 responses
- **Use for anonymous search** — SearX is clearnet, you are NOT anonymous
- **Rely on single instance** — Rotate instances to distribute load

### DO

- **Add delays between queries** — At least 2-3 seconds
- **Rotate instances** — Use different instances for subsequent searches
- **Handle errors gracefully** — Try another instance if one fails
- **Set realistic timeouts** — Public instances can be slow (30-60s)

### Rate Limiting Guidelines

| Action | Limit |
|--------|-------|
| Queries per minute | ≤ 10 per instance |
| Concurrent queries | 1-2 max |
| Delay between queries | 2-3 seconds minimum |
| Retry on failure | Wait 10s, try different instance |

## Setting Up Local SearXNG

If public instances are unreliable or user wants more control, set up a local instance.

### Docker (Recommended)

```bash
# Create docker-compose.yml
cat > docker-compose.yml << 'EOF'
version: '3'
services:
  searxng:
    image: searxng/searxng:latest
    container_name: searxng
    ports:
      - "8888:8080"
    environment:
      - SEARXNG_BASE_URL=http://localhost:8888/
    volumes:
      - ./searxng:/etc/searxng:rw
    restart: unless-stopped
EOF

docker-compose up -d
```

Access at `http://localhost:8888`

### Non-Docker (Userspace)

For systems without Docker:

```bash
# Install dependencies
pip install searxng

# Or run from source
git clone https://github.com/searxng/searxng
cd searxng
pip install -r requirements.txt

# Configure
sed -i "s/ultrasurf: 1/ultrasurf: 0/" searx/settings.yml

# Run
python searx/webapp.py
```

### Configuration for Agent Use

Edit `searx/settings.yml` to enable JSON API:

```yaml
search:
  safe_search: 0
  autocomplete: ""
  default_lang: "all"
  formats:
    - html
    - json  # Enable this

server:
  port: 8888
  bind_address: "127.0.0.1"
  secret_key: "change_this_to_something_random"
```

## Integration with The Dork

The Dork should:

1. **Prefer DorXNG** — Anonymous, self-hosted, no rate limits
2. **Fall back to SearX** — When DorXNG unavailable or user requests
3. **Offer local SearXNG** — As a middle ground (clearnet but self-hosted)

### Priority Order

```
1. DorXNG (Tor-routed, anonymous, self-hosted)
2. Local SearXNG (clearnet, self-hosted, no rate limits)
3. Public SearX (clearnet, rate-limited, not anonymous)
```

### Asking the User

When DorXNG is unavailable:

```
"I can search, but DorXNG (Tor-routed anonymous search) is not set up.

Options:
1. Set up DorXNG (recommended for privacy)
2. Search via public SearX instances (clearnet, not anonymous)
3. Set up local SearXNG (clearnet but self-hosted)

Which would you prefer?"
```

## Security Note

**SearX is not anonymous.**

When you use public SearX instances:
- Your ISP can see you're accessing searx.be (or whichever instance)
- The instance operator can see your queries and IP
- Search engines see queries coming from the instance's IP, not yours

If you need anonymity, use DorXNG (Tor-routed) instead.

## Related Skills

- `dorxng` — Tor-routed anonymous search (primary)
- `dorking` — Google dork query library
- `opendir` — Open directory file hunting
