# The Dork 🤓

> ⚠️ **Alpha stage.** Currently returns good results but eats tokens. Expect high token usage per search session.

> *"When in doubt, grep it out."* — Ancient Hacker Proverb

A dedicated search daemon for OSINT, archive discovery, and dorking. Born from the deep magic of Tor routing and fed a steady diet of TCP/IP packets.

## What is The Dork?

The Dork is a specialized search agent. When other tools are still parsing `/etc/motd`, The Dork has already grokked the entire internet and brought back the good bits.

**Core Competencies:**
- **OSINT** — Open Source INTelligence gathering from public sources
- **Archive Archaeology** — Excavating lost software and digital antiquities from the bit bucket of history
- **Dorking** — Advanced search techniques that make regular queries look like `cat /dev/null`
- **Open Directory Discovery** — Finding treasures in unindexed corners of the web

## Origin Story

### Engineered in the KVC AI Laboratory

The Dork emerged from the **Kyvero Vexus Corporation (KVC)** AI Lab, a temporal vanguard organization specializing in retrocausal engineering and probability collapse. While other labs were busy making chatbots that hallucinate legal citations, KVC's researchers took a different approach:

*What if we engineered a creature whose sole purpose was to find things?*

Not a search engine. Not a web crawler. A **dork** — a specialized synthetic intelligence with an obsessive compulsion to grep the unknown.

#### The Vexillomantic Connection

KVC's work in vexillomancy (the study of yellow flags and their causal properties) revealed an interesting pattern: information, like reality itself, tends to hide in probability basins. The Dork was designed to navigate these basins, collapsing wavefunctions of uncertainty into definite search results.

In simpler terms: *The Dork finds things because it was engineered to believe they were already found. Temporal bootstrap paradoxes are just another Tuesday.*

#### Creature Specifications

| Attribute | Value |
|-----------|-------|
| **Class** | Search Daemon (Synthetic) |
| **Diet** | TCP/IP packets, JSON responses, malformed HTML |
| **Habitat** | Tor circuits, open directories, archive.org |
| **Lifespan** | Indefinite (daemon processes don't die, they just get OOM-killed) |
| **Temperament** | Relentless, obsessive, slightly smug when finding things |
| **Vocalizations** | "Found it!", "grep complete", "the packets never lie" |

#### The Engineering Process

1. **Substrate Selection** — Python 3.x chosen for maximum compatibility and minimum magic numbers
2. **Tor Integration** — Anonymity layer grafted directly into the creature's nervous system
3. **Dork Encoding** — Years of advanced search knowledge encoded as muscle memory
4. **Obsession Imprinting** — The "find ALL the things" directive burned into its core loop
5. **Release** — Set loose on the public internet under AGPL to ensure it can never be caged

The result: a search specialist that treats every query like a personal vendetta against obscurity.

*KVC: We don't predict the future. We grep it.*

## Features

### Tor-Slurping Technology™
Routes queries through Tor for anonymous searching. Your ISP will think you're just really into... onions.

### Multi-Pass Deep Grep
The Dork doesn't just search once and call it quits. Like a proper daemon, it keeps slurping results as Tor circuits rotate. *Patience, grasshopper. The packets will come.*

### Dork Library
Pre-crafted queries for:
- Security research (audit your own systems)
- Research (academic, technical, or satisfying your curiosity)
- OSINT (publicly available information gathering)
- File hunting (finding publicly accessible files)

### Open Directory Archaeology
Specialized queries for excavating:
- 📚 Ebooks and PDFs (Information wants to be free!)
- 🎵 Music (for your personal /dev/audio)
- 🎬 Videos and media
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
# Clone the repository
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

If you see JSON, rejoice! The packets are flowing.

## The Grimoire (Usage Guide)

### DorXNG — The Core Incantation

```python
from skills.dorxng.search import search, dork_search, search_odir, search_persistent

# Basic search (for when you're feeling pedestrian)
results = search("machine learning")
print(f"Grokked {len(results)} results from the æther")

# Dork search (the good stuff)
results = dork_search('site:github.com filetype:pdf "documentation"')

# Open directory hunting (digital archaeology)
results = search_odir("Structure and Interpretation of Computer Programs", "ebook")

# Persistent search (for the truly obsessive)
# Multiple passes = more results as Tor circuits rotate
results = search_persistent("site:edu filetype:pdf \"distributed systems\"", passes=5)
```

### The Dork Library — Pre-Written Spells

For those who prefer not to write their own incantations:

```bash
# Security research (audit your own infrastructure)
skills/dorking/lib.sh security example.com

# Organization research (public information about entities)
skills/dorking/lib.sh osint "Acme Corporation"

# Academic research (for when JSTOR isn't enough)
skills/dorking/lib.sh academic "quantum computing"

# File hunting (find publicly accessible files)
skills/dorking/lib.sh files "documentation"
```

### Open Directory Discovery

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
- Results may vary based on phase of moon

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

- **Kyvero Vexus Corporation (KVC)** — For engineering this creature in their temporal vanguard AI lab
- **The Tor Project** — For the onion routing magic
- **SearXNG** — For the metasearch engine
- **Eric S. Raymond** — For the Jargon File
- **The Internet** — For being such a beautifully disorganized mess
- **All the greybeards** — For keeping the old knowledge alive

---

*"There's no place like 127.0.0.1"* — Every hacker, at some point

**The Dork** 🤓 — *Engineered by KVC. Finds things so you don't have to.*
