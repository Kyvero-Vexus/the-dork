# The Dork 🤓

> *"When in doubt, grep it out."* — Ancient Hacker Proverb

A dedicated search daemon for OSINT, archive discovery, and dorking. Born from the deep magic of Tor routing and fed a steady diet of TCP/IP packets.

## What is The Dork?

The Dork is a card-carrying member of the search-and-destroy brigade. When other agents are still parsing `/etc/motd`, The Dork has already grokked the entire internet and brought back the good bits.

**Core Competencies:**
- **OSINT** — Open Source INTelligence gathering (the legal kind of stalking)
- **Archive Archaeology** — Excavating lost software and digital antiquities from the bit bucket of history
- **Dorking** — Advanced Google-fu that makes regular searches look like `cat /dev/null`
- **Open Directory Plundering** — Finding treasures in unindexed corners of the web

## Features

### Tor-Slurping Technology™
Routes queries through Tor so your searches are as anonymous as a grey-hat at DEF CON. Your ISP will think you're just really into... onions.

### Multi-Pass Deep Grep
The Dork doesn't just search once and call it quits. Like a proper daemon, it keeps slurping results as Tor circuits rotate. *Patience, grasshopper. The packets will come.*

### L33t Dork Library
Pre-crafted incantations for:
- Security auditing (find the holes before the black hats do)
- Research (academic, corporate, or just satisfying your curiosity)
- OSINT (because knowledge is power, and power is /dev/random)
- File hunting (the digital equivalent of dumpster diving, but legal!)

### Open Directory Archaeology
Specialized queries for excavating:
- 📚 Ebooks and PDFs (Information wants to be free!)
- 🎵 Music (for your personal /dev/audio)
- 🎬 Videos (no, not *those* kind)
- 💾 Software archives (abandonware heaven)
- 📦 Archives and collections (the Internet's attic)

## Quick Start

### Prerequisites

You'll need:
- **Docker** — For running DorXNG (the Tor-routed metasearch engine)
- **Python 3.x** — Because Python 2 is deader than a door nail
- **A sense of humor** — Optional but recommended

### Installation

```bash
# Clone the repos... I mean, acquire the source tarball
git clone https://github.com/Kyvero-Vexus/the-dork.git
cd the-dork
```

### The Ritual of Bootstrap

Every proper daemon requires an incantation. Ours is simpler than most:

```python
python3 skills/dorxng/bootstrap.py
```

This will:
1. ✅ Check if DorXNG is running (is the daemon awake?)
2. 🐋 Offer to conjure a DorXNG container if needed
3. 🔮 Verify the TCP/IP offerings are accepted
4. 🎉 Declare victory

### Manual Setup (For the Heavy Wizards)

If you prefer to chant the incantations yourself:

```bash
# Summon the DorXNG daemon
docker run -d \
  --name dorxng \
  -p 8889:443 \
  --restart unless-stopped \
  ghcr.io/unya/dorxng:latest

# Wait for Tor to establish circuits (approx. 30 seconds of meditation)
sleep 30

# Verify the daemon responds
curl "http://localhost:8889/search?q=hello+world&format=json"
```

If you see JSON, rejoice! The dark forces have been appeased.

## The Grimoire (Usage Guide)

### DorXNG — The Core Incantation

```python
from skills.dorxng.search import search, dork_search, search_odir, search_persistent

# Basic search (for when you're feeling pedestrian)
results = search("machine learning")
print(f"Grokked {len(results)} results from the æther")

# Dork search (the good stuff)
results = dork_search('site:github.com filetype:pdf "secret"')

# Open directory hunting (digital archaeology)
results = search_odir("Structure and Interpretation of Computer Programs", "ebook")

# Persistent search (for the truly obsessive)
# Multiple passes = more results as Tor circuits rotate
results = search_persistent("site:edu filetype:pdf \"distributed systems\"", passes=5)
```

### The Dork Library — Pre-Written Spells

For those who prefer not to write their own incantations:

```bash
# Security audit (find your leaks before they do)
skills/dorking/lib.sh security example.com

# Corporate reconnaissance (totally legitimate business intelligence)
skills/dorking/lib.sh osint "Acme Corporation"

# Academic research (for when JSTOR isn't enough)
skills/dorking/lib.sh academic "quantum computing"

# File hunting (I wonder what's on this server...)
skills/dorking/lib.sh files "backup"
```

### Open Directory Plundering

```bash
# Excavate ancient texts
skills/opendir/search.sh "SICP" ebook

# Find software that time forgot
skills/opendir/search.sh "Photoshop 7" software

# Discover music in the digital wilderness
skills/opendir/search.sh "Grateful Dead" music
```

## Configuration — The knobs and dials

### Environment Variables

| Variable | Purpose | Default |
|----------|---------|---------|
| `DORXNG_URL` | Your DorXNG instance | `http://localhost:8889/search` |
| `SEARXNG_URL` | Fallback (non-Tor) | *(empty)* |

Set them in your shell's RC file for persistence across reboots:

```bash
export DORXNG_URL="http://your-dorxng-host:8889/search"
```

### Integration with OpenClaw

The Dork was forged in the fires of OpenClaw. To use it as an agent:

1. Copy the workspace to your OpenClaw workspaces directory
2. Add the agent config to `openclaw.json`
3. Summon with "the dork" or "find X"

See `SOUL.md` for the agent's personality (yes, it has one).

## Pro Tips from the Greybeards

### The Tao of Tor
- **Multiple passes = more results** — Tor circuits rotate every 10 seconds. Patience, padawan.
- **HTTP/504 is normal** — The daemon sometimes naps. Poke it again.
- **Four queries max concurrently** — More than that and the rate limit gods get angry.
- **30-120 second response times** — Tor is S-L-O-W. Embrace the latency.

### When Things Go Sideways

| Symptom | Diagnosis | Cure |
|---------|-----------|------|
| "Connection refused" | DorXNG not running | `docker start dorxng` |
| Empty results | Tor circuit blocked | Wait 10s, try again |
| SSL errors | Internal Docker IP | Normal, search.py handles it |
| "Tor not connected" | Patience deficit | Wait 30-60s on first start |

### The Care and Feeding of Your Dork

- Feed it queries regularly
- Don't let it grep `/dev/urandom` (it's tried)
- Keep away from three-letter agencies
- Results may vary based on phase of moon

## The Jargon (For the Uninitiated)

| Term | Definition |
|------|------------|
| **Dork** | One who dorks; a specialist in the art of Google dorking |
| **DorXNG** | SearXNG + Tor, the search engine of the gods |
| **OSINT** | Open Source Intelligence (stalking, but professional) |
| **Grok** | To understand deeply, from Stranger in a Strange Land |
| **Greybeard** | An elder hacker, possessor of deep magic |
| **Bit bucket** | Where deleted files go to die |
| **Incantation** | A complex command or script |

## Contributing

We welcome contributions from:
- Wizards of the shell
- Sorcerers of Python
- Bards of documentation
- Anyone who groks the mission

**Before submitting PRs, ensure your code contains:**
- ❌ No private URLs or IPs
- ❌ No API keys or secrets
- ❌ No doxxable information
- ✅ Plenty of puns

## License

AGPL-3.0-or-later — Because information wants to be free, and so should your modifications. 

**Why AGPL?** The GNU Affero GPL ensures that even if someone runs The Dork as a network service (SaaS), they must share their improvements with the community. No corporate basement-dwelling dorks allowed—what happens on the network, stays on GitHub.

See [LICENSE](LICENSE) for the full legal incantation.

## Acknowledgments

- The Tor Project — For the onion routing magic
- SearXNG — For the metasearch engine
- Eric S. Raymond — For the Jargon File
- The Internet — For being such a beautifully disorganized mess

---

*"There's no place like 127.0.0.1"* — Every hacker, at some point

**The Dork** 🤓 — *Finds things so you don't have to.*
