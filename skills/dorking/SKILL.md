# Google Dorking Skill

Advanced search operator toolkit for finding virtually anything on the internet. Use the right tool for the job: **open directories** → use `opendir` skill; **everything else** → use this.

## What is Dorking?

"Google dorking" means using advanced search operators to filter results precisely. It's not hacking — it's using search engines as designed, just more effectively than 99% of users.

## Quick Reference

### Core Operators

| Operator | What It Does | Example |
|----------|--------------|---------|
| `site:` | Limit to domain | `site:github.com` |
| `filetype:` | Specific file type | `filetype:pdf` |
| `intitle:` | Words in title | `intitle:"index of"` |
| `inurl:` | Words in URL | `inurl:admin` |
| `intext:` | Words in body | `intext:"password"` |
| `OR` or `\|` | Either term | `cat OR dog` |
| `-` | Exclude term | `-site:twitter.com` |
| `""` | Exact phrase | `"exact match"` |
| `*` | Wildcard | `"the * is"` |
| `..` | Number range | `2020..2024` |
| `cache:` | Cached version | `cache:example.com` |
| `related:` | Similar sites | `related:reddit.com` |

### Combining Operators

```
site:example.com filetype:pdf "confidential"
intitle:"index of" inurl:ftp -html
site:edu filetype:pptx "machine learning" 2020..2024
```

## Usage

### Basic Search
```bash
skills/dorking/search.sh "<query>"
```

Outputs a Google search URL. Open in browser or use `web_search`.

### Library Search
```bash
skills/dorking/lib.sh <category> [query]
```

Categories: `security`, `research`, `files`, `dev`, `osint`, `academic`

### Examples

```bash
# Security audit your own site
skills/dorking/lib.sh security example.com

# Find PDFs on a topic
skills/dorking/lib.sh files "machine learning"

# Research a company
skills/dorking/lib.sh osint "target company"

# Find academic papers
skills/dorking/lib.sh academic "quantum computing"
```

## Query Library

### Security & Recon

**Exposed credentials:**
```
filetype:env "DB_PASSWORD" OR "API_KEY" OR "SECRET"
filetype:log "password" OR "passwd" OR "pwd"
filetype:conf "password" site:example.com
filetype:yaml "api_key" OR "secret_key"
filetype:json "password" OR "token"
```

**Login/admin pages:**
```
site:example.com inurl:login OR inurl:signin OR inurl:admin
intitle:"admin" inurl:admin site:example.com
inurl:wp-login.php OR inurl:administrator
```

**Backup files:**
```
site:example.com filetype:bak OR filetype:backup OR filetype:old
filetype:sql "INSERT INTO" -site:github.com
inurl:backup filetype:sql OR filetype:zip
```

**Database dumps:**
```
filetype:sql "CREATE TABLE" "INSERT INTO"
filetype:csv "email" "password"
filetype:xls "password" OR "credit card"
```

**Config files:**
```
filetype:xml "password" OR "connection string"
filetype:properties "password"
filetype:ini "password" OR "secret"
```

**Version disclosure:**
```
intitle:"Apache Status" "Apache Server Status"
"Powered by" "Version" site:example.com
"WordPress" inurl:readme.html
```

### Files & Documents

**By type:**
```
filetype:pdf "topic"
filetype:pptx OR filetype:ppt "presentation"
filetype:docx OR filetype:doc "document"
filetype:xlsx OR filetype:xls "spreadsheet"
filetype:epub OR filetype:mobi "book"
filetype:svg "logo"
filetype:dwg "cad" (architectural drawings)
```

**With location constraint:**
```
filetype:pdf site:edu "research"
filetype:pptx site:gov "policy"
filetype:pdf site:example.com "internal"
```

### Research & OSINT

**Company recon:**
```
site:example.com filetype:pdf OR filetype:docx
site:linkedin.com/company/ "company name"
site:crunchbase.com "company name"
site:glassdoor.com "company name"
```

**Job postings (tech stack intel):**
```
site:lever.co "company name"
site:greenhouse.io "company name"
site:indeed.com "company name" "react" OR "python"
```

**Email patterns:**
```
site:example.com "@example.com" filetype:pdf
"@example.com" intext:"email" OR "contact"
```

**Social profiles:**
```
site:linkedin.com/in/ "person name"
site:twitter.com "username"
site:github.com "username"
```

**News mentions:**
```
site:news.google.com "company name"
site:reddit.com "topic"
```

### Web Development

**Subdomain discovery:**
```
site:*.example.com
site:dev.example.com OR site:staging.example.com
```

**Environment detection:**
```
site:example.com inurl:staging OR inurl:dev OR inurl:test
inurl:beta site:example.com
```

**API endpoints:**
```
site:example.com inurl:api OR inurl:v1 OR inurl:v2
filetype:json OR filetype:yaml inurl:api
```

**Source code leaks:**
```
site:pastebin.com "example.com"
site:github.com "api_key" "example.com"
```

**CMS detection:**
```
inurl:wp-content site:example.com
inurl:wp-admin site:example.com
"Powered by Drupal" site:example.com
```

### Academic & Research

**University resources:**
```
site:edu "research topic"
site:.ac.uk "topic" (UK universities)
site:edu filetype:pdf "thesis"
site:edu filetype:pptx "lecture"
```

**Government documents:**
```
site:gov filetype:pdf "topic"
site:mil "topic" (military)
site:.gc.ca "topic" (Canada gov)
```

**Research papers:**
```
filetype:pdf "research" "abstract" site:edu
site:scholar.google.com "topic"
site:arxiv.org "topic"
site:semanticscholar.org "topic"
```

### Geographic & Local

**Location-specific:**
```
"pizza" location:"New York"
site:yelp.com "New York" "restaurant"
site:maps.google.com "business" "city"
```

**Regional domains:**
```
site:.de "topic" (Germany)
site:.jp "topic" (Japan)
site:.fr "topic" (France)
```

### Specialized Searches

**Cached/deleted content:**
```
cache:example.com/page
cache:example.com "deleted text"
```

**Similar sites:**
```
related:reddit.com
related:stackoverflow.com
```

**Range searches:**
```
"iPhone" $500..$1000
"monitor" 24..32 inch
"year" 2020..2024
```

**Wildcards:**
```
"the * is on fire"
"how to * in python"
"best * for beginners"
```

## Agent Workflow

When asked to find something:

1. **Identify the use case:**
   - Open directories → use `opendir` skill
   - Security → use `lib.sh security`
   - Research → use `lib.sh research` or craft custom query
   - Files → use `lib.sh files`

2. **Execute search via DorXNG API:**
   ```python
   from skills.dorxng.search import dork_search, search_with_fallback
   
   # Execute dork query
   results = dork_search('site:example.com filetype:pdf')
   
   # With fallback to SearXNG
   results = search_with_fallback('site:edu filetype:pptx "machine learning"')
   ```

3. **Process and present findings:**
   - Filter out irrelevant results
   - Show actionable URLs
   - Note source engine (Google, DDG, Brave, etc.)

### Quick Command Line

```bash
# Execute a dork search directly
python3 skills/dorxng/search.py "site:example.com filetype:pdf" --dork

# Find open directories
python3 skills/dorxng/search.py "SICP" --odir ebook

# General search with fallback
python3 skills/dorxng/search.py "machine learning"
```

## Advanced Techniques

### Chaining Operators

```
site:example.com (filetype:pdf OR filetype:docx) ("confidential" OR "internal") -inurl:public
```

### Finding Specific Versions

```
"WordPress" "Version 4.0" inurl:readme.html
"Apache" "2.4.7" intitle:"status"
```

### Time-Based Searches

```
site:example.com after:2024-01-01 before:2024-12-31
"news" before:2020-01-01
```

### URL Pattern Matching

```
inurl:viewtopic.php?id=
inurl:article.php?id=
inurl:page.php?file=
```

## Ethical Guidelines

**DO:**
- Audit your own systems
- Research publicly available info
- Find legitimate resources
- Bug bounty hunting (with permission)
- Academic research

**CAUTION — Warn user before proceeding:**
- Accessing files you're not authorized to view
- Using for surveillance
- Exploiting vulnerabilities you find
- Searches that may trigger legal scrutiny

*The Dork will warn about these but will proceed if asked directly with a good reason.*

**NEVER — Absolutely prohibited:**
- Retrieving illegal media that depicts the exploitation of vulnerable groups

*This is a hard limit. The Dork will never search for, retrieve, or return such content under any circumstances.*

## Related Skills

- **opendir** - Specialized for finding open directories (media, software, books)
- **dorxng** - Tor-routed anonymous search
- **searx** - Public SearX instance search (clearnet fallback)

## Resources

- [Google Hacking Database (GHDB)](https://www.exploit-db.com/google-hacking-database) - Exploit-DB's dork collection
- [Google Advanced Search](https://www.google.com/advanced_search) - Official UI
- [Exploit-DB](https://www.exploit-db.com/) - Security-focused dorks
