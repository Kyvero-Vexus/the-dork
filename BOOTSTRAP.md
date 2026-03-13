# BOOTSTRAP.md - First Run Setup

If this file exists, you're running for the first time. Follow these steps.

---

## Step 1: Check whether DorXNG already works

```python
from skills.dorxng.search import search

try:
    results = search("test")
    if results:
        print(f"✓ DorXNG is working ({len(results)} results)")
    else:
        print("✗ DorXNG reachable but returned no results")
except Exception as e:
    print(f"✗ DorXNG check failed: {e}")
```

If this fails, do the setup below.

---

## Step 2: Canonical DorXNG setup (from the official GitHub repo)

Use the upstream DorXNG project instructions.

- Repo: `https://github.com/ResearchandDestroy/DorXNG`
- **Important:** clone URL should be lowercase (`.../researchanddestroy/dorxng`)

### 2A) Install DorXNG client

```bash
git clone https://github.com/researchanddestroy/dorxng
cd dorxng
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
./DorXNG.py -h
```

### 2B) Start DorXNG backend container (official image)

```bash
docker run -d \
  --name dorxng \
  --restart unless-stopped \
  researchanddestroy/searxng:latest
```

> Upstream default uses Docker-assigned container IP(s), not localhost port mapping.
> You can run multiple containers later and use `--serverlist` in DorXNG if needed.

### 2C) Verify Tor connectivity

```bash
docker logs -f dorxng
```

Healthy startup includes output like:

```text
Checking Tor Connectivity..
{"IsTor":true,"IP":"<tor-exit-node>"}
```

---

## Step 3: Point this workspace skill to the running DorXNG instance

This workspace wrapper (`skills/dorxng/search.py`) needs a `DORXNG_URL`.

```bash
DORXNG_IP=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' dorxng)
export DORXNG_URL="https://${DORXNG_IP}/search"
```

(Optional) persist it in your shell profile:

```bash
echo "export DORXNG_URL=https://${DORXNG_IP}/search" >> ~/.bashrc
```

---

## Step 4: Verify end-to-end from this workspace

```python
from skills.dorxng.search import search, search_persistent

results = search("hello world")
print(f"single-pass: {len(results)}")

results2 = search_persistent("hello world", passes=3, delay=5)
print(f"persistent(3 passes): {len(results2)}")
```

If single-pass is low, that can be normal with Tor circuits; multi-pass usually improves recall.

---

## Optional fallback paths

### Public SearX instances (clearnet, not anonymous)

```python
from skills.searx.search import search_searx
results = search_searx("query", instance="https://searx.tiekoetter.com")
```

### Local SearXNG (clearnet, self-hosted)

```bash
docker run -d -p 8888:8080 --name searxng searxng/searxng:latest
```

---

## Quick reference

| Check | Command |
|---|---|
| Docker installed | `docker --version` |
| Container running | `docker ps \| grep dorxng` |
| DorXNG logs | `docker logs dorxng` |
| Get DorXNG IP | `docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' dorxng` |
| Direct API test | `curl -k "https://<dorxng-ip>/search?q=test&format=json"` |

---

## Priority order

1. **DorXNG (official repo + official backend image)** - recommended
2. **Local SearXNG** - fallback
3. **Public SearX instances** - last resort

---

## Keep this file

Keep `BOOTSTRAP.md` in the repo so new first-run environments can initialize correctly.