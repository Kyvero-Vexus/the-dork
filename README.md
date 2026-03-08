# The Dork 🤓

A dedicated search specialist agent for OSINT, archive discovery, and dorking.

## What is The Dork?

The Dork is an AI agent designed to find things. It specializes in:
- **OSINT** - Open source intelligence gathering
- **Archive Discovery** - Finding software archives, source code, historical materials
- **Dorking** - Advanced Google dork queries for files, directories, and vulnerabilities
- **Open Directory Hunting** - Locating files on public open directories

## Features

- **DorXNG Integration** - Tor-routed anonymous metasearch through 7+ engines
- **Multi-pass Search** - Results accumulate over time as Tor circuits rotate
- **Dork Query Library** - Pre-built queries for security, research, OSINT, and more
- **Open Directory Search** - Find ebooks, music, video, software, archives

## Quick Start

### Prerequisites

- Docker (for DorXNG)
- Python 3.x

### Setup

1. Clone this repo:
```bash
git clone https://github.com/Kyvero-Vexus/the-dork.git
cd the-dork
```

2. Run the bootstrap:
```python
python3 skills/dorxng/bootstrap.py
```

This will:
- Check if DorXNG is running
- Offer to set it up automatically if not
- Verify everything works

3. Test a search:
```bash
python3 skills/dorxng/search.py "hello world"
```

### Manual DorXNG Setup

If you prefer to set up DorXNG manually:

```bash
docker run -d \
  --name dorxng \
  -p 8889:443 \
  --restart unless-stopped \
  ghcr.io/unya/dorxng:latest
```

Wait 30 seconds for Tor to connect, then test:
```bash
curl "http://localhost:8889/search?q=test&format=json"
```

## Skills

### DorXNG (`skills/dorxng/`)

Tor-routed anonymous metasearch.

```python
from skills.dorxng.search import search, dork_search, search_odir, search_persistent

# Basic search
results = search("machine learning")

# Dork search
results = dork_search('site:github.com filetype:pdf')

# Open directory search
results = search_odir("SICP", "ebook")

# Persistent search (multiple passes)
results = search_persistent("query", passes=3, delay=5)
```

### Dorking (`skills/dorking/`)

Pre-built Google dork queries.

```bash
# Security audit
skills/dorking/lib.sh security example.com

# OSINT
skills/dorking/lib.sh osint "company name"

# Academic research
skills/dorking/lib.sh academic "machine learning"
```

### Open Directory (`skills/opendir/`)

Find files on public open directories.

```bash
# Find ebooks
skills/opendir/search.sh "SICP" ebook

# Find software
skills/opendir/search.sh "photoshop" software

# Find music
skills/opendir/search.sh "pink floyd" music
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DORXNG_URL` | DorXNG instance URL | `http://localhost:8889/search` |
| `SEARXNG_URL` | Optional fallback URL | (none) |

### Using with OpenClaw

The Dork is designed to work as an OpenClaw agent. See the workspace files:
- `SOUL.md` - Agent personality and workflow
- `IDENTITY.md` - Agent identity
- `TOOLS.md` - Tool reference
- `USER.md` - User guidance

## Tips

- **Multiple passes = more results** - Tor circuits rotate every 10 seconds
- **HTTP/504 is normal** - Keep going, next circuit may be faster
- **4 concurrent queries max** - More risks rate limiting
- **Response time: 30-120s** - Tor is slow, be patient

## License

MIT

## Contributing

Contributions welcome! Please ensure any additions don't include:
- Private URLs or IPs
- API keys or secrets
- Personal information
