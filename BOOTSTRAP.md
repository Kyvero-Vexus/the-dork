# BOOTSTRAP.md - First Run Setup

If this file exists, you're running for the first time. Follow these steps.

## Step 1: Check DorXNG

DorXNG is your primary search tool. Let's check if it's already set up.

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
    print("\nYou need to set up DorXNG. See skills/dorxng/SKILL.md for setup guide.")
```

## Step 2: If DorXNG is Not Available

You have options:

### Option A: Let Me Set It Up (Docker Required)

I can set up DorXNG for you if you have Docker installed:

```
Ask the user: "I can set up DorXNG using Docker. Should I proceed?"
```

If yes:
```bash
# Pull and run DorXNG
docker run -d \
  --name dorxng \
  -p 8889:443 \
  --restart unless-stopped \
  ghcr.io/unya/dorxng:latest

# Wait for Tor to connect
sleep 30

# Verify
docker exec dorxng curl -s https://check.torproject.org/api/ip
```

### Option B: Manual Setup

Guide the user to `skills/dorxng/SKILL.md` which contains detailed setup instructions.

### Option C: Use Public Instance

Set a public SearXNG instance (less private but works immediately):

```bash
export DORXNG_URL="https://searx.be/search"
```

## Step 3: Verify Setup

After configuration, test:

```python
from skills.dorxng.search import search
results = search("hello world")
print(f"Found {len(results)} results")
for r in results[:3]:
    print(f"  - {r.get('title', 'No title')[:50]}")
```

## Step 4: Delete This File

Once DorXNG is working, delete this file:

```bash
rm BOOTSTRAP.md
```

You won't need it again.

---

## Quick Reference

| Check | Command |
|-------|---------|
| Is Docker installed? | `docker --version` |
| Is DorXNG running? | `docker ps \| grep dorxng` |
| DorXNG logs | `docker logs dorxng` |
| Test search | `curl "http://localhost:8889/search?q=test&format=json"` |
