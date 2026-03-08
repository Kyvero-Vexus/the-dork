# BOOTSTRAP.md - First Run Setup

If this file exists, you're running for the first time. Follow these steps.

## Step 1: Check DorXNG

DorXNG is your primary search tool (Tor-routed, anonymous). Let's check if it's already set up.

```python
# Run this check
from skills.dorxng.search import search
try:
    results = search("test")
    if results:
        print("✓ DorXNG is working!")
    else:
        print("✗ DorXNG returned no results. May need configuration.")
except Exception as e:
    print(f"✗ DorXNG not available: {e}")
    print("\nYou need to set up a search backend.")
```

## Step 2: If DorXNG is Not Available

You have options:

### Option A: Set Up DorXNG (Recommended - Anonymous)

DorXNG routes all searches through Tor for anonymity.

```bash
# Pull and run DorXNG
docker run -d \
  --name dorxng \
  -p 8889:443 \
  --restart unless-stopped \
  ghcr.io/unya/dorxng:latest

# Wait for Tor to connect (30-60 seconds)
sleep 30

# Verify
docker exec dorxng curl -s https://check.torproject.org/api/ip
```

See `skills/dorxng/SKILL.md` for full setup guide.

### Option B: Use Public SearX Instances (Clearnet, Not Anonymous)

If you don't need anonymity, use public SearX instances:

```python
from skills.searx.skill import search_searx
results = search_searx("query", instance="https://search.bus-hit.me")
```

Find instances at: https://searx.space/

See `skills/searx/SKILL.md` for usage and rate limits.

### Option C: Set Up Local SearXNG (Clearnet, Self-Hosted)

Self-hosted SearXNG without rate limits:

```bash
# Docker
docker run -d -p 8888:8080 --name searxng searxng/searxng:latest

# Access at http://localhost:8888
```

## Step 3: Verify Setup

After configuration, test:

```python
# Test DorXNG
from skills.dorxng.search import search
results = search("hello world")
print(f"DorXNG: Found {len(results)} results")

# Or test SearX
from skills.searx.skill import search_searx
results = search_searx("hello world")
print(f"SearX: Found {len(results)} results")
```

## Step 4: Don't Delete This File

**Keep BOOTSTRAP.md in the repo.** It helps new users set up their Dork.

Your local instance can delete it after setup, but the repo should keep it.

---

## Quick Reference

| Check | Command |
|-------|---------|
| Is Docker installed? | `docker --version` |
| Is DorXNG running? | `docker ps \| grep dorxng` |
| DorXNG logs | `docker logs dorxng` |
| Test DorXNG | `curl "http://localhost:8889/search?q=test&format=json"` |
| Test SearX | `curl "https://search.bus-hit.me/search?q=test&format=json"` |

## Priority Order

1. **DorXNG** - Tor-routed, anonymous, self-hosted (recommended)
2. **Local SearXNG** - Clearnet, self-hosted, no rate limits
3. **Public SearX** - Clearnet, rate-limited, not anonymous (fallback)
