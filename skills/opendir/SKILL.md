# Open Directory Search Skill

Search open directories on the internet to find files hosted publicly — useful for finding lost media, old software, ebooks, music, and more.

## What Are Open Directories?

Open directories are web server folders that display their contents publicly (no authentication). They typically show "Index of /path" in the title when no default page exists. People accidentally or intentionally leave directories open, hosting everything from retro software to obscure media.

## Usage

### Basic Search
```
skills/opendir/search.sh "<query>" [type]
```

**Types:**
- `all` - General open directory search (default)
- `ebook` - Books, PDFs, comics, documents
- `music` - MP3, FLAC, audio files
- `video` - Movies, TV, video files
- `software` - Programs, ISOs, archives
- `archive` - ZIP, RAR, 7z collections

### Examples

```bash
# Find old software
skills/opendir/search.sh "photoshop 7" software

# Find a specific book
skills/opendir/search.sh "structure and interpretation of computer programs" ebook

# Find music
skills/opendir/search.sh "aphex twin" music

# Find video files
skills/opendir/search.sh "star trek ds9" video

# General search
skills/opendir/search.sh "retrowave collection"
```

## How It Works

The script generates Google dork URLs optimized for finding open directories. You can:
1. Run the script to get a Google search URL
2. Open in browser OR
3. Use `web_search` with the generated query

## Google Dork Patterns

The skill uses these proven dork patterns:

### General
```
intitle:"index of" "query" "parent directory" -html -htm -php -asp -jsp
```

### Ebooks
```
query +(.MOBI|.CBZ|.CBR|.EPUB|.PDF|.RTF) intitle:"index of" -inurl:(jsp|pl|php|html|aspx|htm|cf|shtml)
```

### Music
```
query intitle:"music" (mp3|aac|flac|wav) "Parent Directory" -htm -html -asp -php -listen77 -idmusic -airmp3
```

### Video
```
query (avi|mp4|mkv|mpg|wmv|mov) "Parent Directory" -"Trailer" -torrent -serial -asp -html -htm -jsp
```

### Software
```
query (exe|iso|zip|rar|tar|gz|dmg|apk) intitle:"index of" -inurl:(html|htm|php|asp|jsp)
```

### Archives
```
query (zip|rar|7z|tar|gz|bz2) intitle:"index of" "parent directory" -html -htm -php
```

## Agent Integration

When the user asks to find something on open directories:

### Method 1: DorXNG API (Recommended)

Execute searches directly via DorXNG's Tor-routed SearXNG:

```python
from skills.dorxng.search import search_odir

# Find ebooks
results = search_odir("SICP", "ebook")

# Find music
results = search_odir("aphex twin", "music")

# Find software
results = search_odir("photoshop 7", "software")
```

### Method 2: Command Line

```bash
# Execute open directory search directly
python3 skills/dorxng/search.py "SICP" --odir ebook

# Returns filtered results from DorXNG (Tor-routed, anonymous)
```

### Method 3: Browser Fallback

If DorXNG is slow or unavailable:

1. **Generate URL** - Run `skills/opendir/search.sh "<query>" <type>` to get Google URL
2. **Open in browser** - Use `browser open` with the URL
3. **Snapshot** - Use `browser snapshot` to get search results
4. **Extract links** - Find URLs that look like open directories

### What to Look For

Open directory URLs typically:
- Have "Index of" in the title
- Show file listings with sizes/dates
- Contain paths like `/files/`, `/pub/`, `/uploads/`, `/media/`
- Don't have .html/.php/.asp extensions
- Show "Parent Directory" link

### Example Workflow

```
User: "Find SICP ebook on open directories"

1. results = search_odir("SICP", "ebook")
2. Present results[:5] to user with notes
```

## Specialized Search Engines

For additional resources:

- **FilePursuit** - https://filepursuit.com (file search engine)
- **ODCrawler** - https://odcrawler.xyz (open directory crawler)
- **The-Eye** - https://the-eye.eu (curated public directory)
- **Anna's Archive** - https://annas-archive.org (books/academic)

## Ethical Notes

- Open directories are publicly accessible by design
- Respect bandwidth — don't hammer servers
- Some files may be copyrighted — use judgment
- This is for finding **lost/obscure content**, not piracy

## Tips

1. **Be specific** - "photoshop 7.0 windows" works better than "photoshop"
2. **Try variations** - If "SICP" fails, try "Structure and Interpretation of Computer Programs"
3. **Year helps** - Add years for old software: "windows 95" or "1998"
4. **File extensions** - Sometimes searching for specific extensions helps: `filetype:iso`
5. **Parent Directory** - This phrase often appears in listings and helps filter

## File Types Reference

| Category | Extensions |
|----------|------------|
| Ebooks | .pdf .epub .mobi .cbz .cbr .chm .lit .rtf |
| Music | .mp3 .flac .aac .wav .ogg .m4a |
| Video | .mp4 .mkv .avi .mov .wmv .mpg .mpeg |
| Software | .exe .iso .dmg .apk .deb .rpm .msi |
| Archives | .zip .rar .7z .tar .gz .bz2 |
