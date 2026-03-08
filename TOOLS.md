# TOOLS.md - Search Specialist Tools

My primary tools for finding things.

## DorXNG (Primary Search)

- **Skill:** `skills/dorxng/SKILL.md`
- **Python API:** `from skills.dorxng.search import search, dork_search, search_odir, search_persistent, SearchSession`
- **Shell wrapper:** `skills/dorxng/search.sh "<query>"`

### Usage Patterns

```python
# Basic search
results = search("query")

# Dork search (files, directories, vulnerabilities)
results = dork_search('site:example.com filetype:pdf')

# Open directory search
results = search_odir("SICP", "ebook")

# Persistent search (multiple passes, accumulates)
results = search_persistent("query", passes=3, delay=5)

# Long-running session with database
session = SearchSession(db_path="investigation.db")
session.search("query 1")
session.search("query 2")
session.get_stats()
```

### DorXNG Tips

- **Multiple passes = more results** - Tor circuits rotate every 10 seconds
- **HTTP/504 is normal** - Keep going, next circuit may be faster
- **4 concurrent queries max** - More risks rate limiting
- **Response time: 30-120s** - Tor is slow, be patient

## SearX (Clearnet Fallback)

- **Skill:** `skills/searx/SKILL.md`
- **Purpose:** Public SearXNG instances when DorXNG unavailable
- **WARNING:** NOT anonymous - clearnet only

### When to Use

1. User explicitly requests clearnet search
2. DorXNG not set up, user declines to set it up
3. DorXNG returns no results after multiple passes

### Finding Instances

```
https://searx.space/ - Lists all public instances with reliability ratings
```

### Usage

```python
from skills.searx.search import search_searx

# Basic search via public SearX
results = search_searx("query", instance="https://searx.tiekoetter.com")
```

### SearX Boundaries

- **NOT anonymous** - Clearnet, ISP can see queries
- **Rate limits apply** - Don't hammer instances (≤10 queries/min)
- **Rotate instances** - Distribute load across multiple SearX hosts
- **2-3s delay between queries** - Be respectful

### Priority Order

1. DorXNG (Tor-routed, anonymous, self-hosted)
2. Local SearXNG (clearnet, self-hosted, no rate limits)
3. Public SearX (clearnet, rate-limited, not anonymous)

## Dorking Library

- **Skill:** `skills/dorking/SKILL.md`
- **Categories:** security, research, files, dev, osint, academic

```bash
skills/dorking/lib.sh security example.com    # Security audit
skills/dorking/lib.sh osint "company name"    # Company recon
skills/dorking/lib.sh academic "ml papers"    # Research papers
```

## Open Directory Search

- **Skill:** `skills/opendir/SKILL.md`
- **Helper:** `skills/opendir/search.sh "<query>" [type]`
- **Types:** all, ebook, music, video, software, archive

## Useful Query Patterns

### Software Archives
```
"software-name source code public domain release"
"software-name archive developer release"
site:archive.org "software-name" source
site:github.com software-name source release
```

### Research
```
"topic overview" → Find key terms
"topic researcher-name" → Find papers/projects
site:edu topic filetype:pdf → Academic papers
```

### Historical Materials
```
"topic mailing list"
"topic hn" → Hacker News discussions
site:bitsavers.org topic → Vintage computer docs
```

## Response Format

Always provide:
- Title and URL
- Brief description
- How sources connect
- Directory structure when relevant
- Key people/organizations
- Historical context

---

This is my cheat sheet. Update as I learn new patterns.
