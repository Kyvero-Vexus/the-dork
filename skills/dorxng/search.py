#!/usr/bin/env python3
"""
SearXNG / DorXNG Search Module

Provides search functionality via self-hosted SearXNG instances.
DorXNG routes queries through Tor for anonymity.

CRITICAL: DorXNG accumulates results over time. Multiple passes yield more results.
Use search_persistent() for thorough searches.
"""

import json
import subprocess
import time
import sqlite3
import hashlib
import urllib.parse
from typing import Optional, List, Dict, Any

# Instance URLs (configure for your environment)
# Set DORXNG_URL via environment variable or modify here
import os
DORXNG_URL = os.environ.get("DORXNG_URL", "http://localhost:8889/search")
# Optional fallback instance
SEARXNG_URL = os.environ.get("SEARXNG_URL", "")

def get_dorxng_url() -> str:
    """Get DorXNG URL from environment or default."""
    return DORXNG_URL

def _execute_search(url: str, query: str, timeout: int = 120, verify_ssl: bool = False) -> Dict[str, Any]:
    """Execute a search query against a SearXNG instance."""
    import urllib.request
    import ssl
    
    encoded_query = urllib.parse.quote(query, safe='')
    search_url = f"{url}?q={encoded_query}&format=json"
    
    # Create SSL context (skip verification for internal Docker IPs)
    ctx = ssl.create_default_context()
    if not verify_ssl:
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
    
    try:
        req = urllib.request.Request(search_url, headers={'User-Agent': 'DorXNG-Client/1.0'})
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as response:
            return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        return {"error": str(e), "results": []}

def search(query: str, instance: str = "dorxng", timeout: int = 120) -> List[Dict[str, Any]]:
    """
    Execute a search query.
    
    Args:
        query: Search query string
        instance: "dorxng" (Tor-routed) or "searxng" (clearnet)
        timeout: Request timeout in seconds
    
    Returns:
        List of result dictionaries with title, url, content, engine
    """
    if instance == "dorxng":
        url = get_dorxng_url()
        verify_ssl = False
    else:
        url = SEARXNG_URL
        verify_ssl = True
    
    result = _execute_search(url, query, timeout, verify_ssl)
    return result.get("results", [])

def search_with_fallback(query: str, timeout: int = 120) -> List[Dict[str, Any]]:
    """
    Search with DorXNG first, fall back to SearXNG if configured and DorXNG fails.
    """
    # Try DorXNG first
    results = search(query, instance="dorxng", timeout=timeout)
    if results:
        return results
    
    # Fall back to SearXNG if configured
    if SEARXNG_URL:
        return search(query, instance="searxng", timeout=timeout)
    
    return []

def search_persistent(query: str, passes: int = 3, delay: int = 5, 
                       instance: str = "dorxng", timeout: int = 120,
                       dedup: bool = True) -> List[Dict[str, Any]]:
    """
    Execute multiple search passes with delays.
    
    IMPORTANT: DorXNG accumulates results over time. Multiple passes
    will find more results as Tor circuits rotate and upstream
    engines return different results.
    
    Args:
        query: Search query string
        passes: Number of search passes to make (default 3)
        delay: Seconds to wait between passes (default 5)
        instance: "dorxng" or "searxng"
        timeout: Request timeout per pass
        dedup: Remove duplicate URLs (default True)
    
    Returns:
        Accumulated list of unique results
    """
    all_results = []
    seen_urls = set()
    
    for i in range(passes):
        if i > 0 and delay > 0:
            time.sleep(delay)
        
        results = search(query, instance=instance, timeout=timeout)
        
        for r in results:
            url = r.get("url", "")
            if dedup and url in seen_urls:
                continue
            if url:
                seen_urls.add(url)
            all_results.append(r)
    
    return all_results

def dork_search(dork: str, passes: int = 1, delay: int = 5, 
                 timeout: int = 120) -> List[Dict[str, Any]]:
    """
    Execute a Google dork query.
    
    Args:
        dork: Google dork query (e.g., 'site:example.com filetype:pdf')
        passes: Number of passes (default 1, increase for more results)
        delay: Seconds between passes
        timeout: Request timeout in seconds
    
    Returns:
        List of result dictionaries
    """
    if passes > 1:
        return search_persistent(dork, passes=passes, delay=delay, timeout=timeout)
    return search_with_fallback(dork, timeout)

def search_odir(query: str, content_type: str = "all", passes: int = 2,
                delay: int = 5, timeout: int = 120) -> List[Dict[str, Any]]:
    """
    Search for open directories containing files.
    
    Args:
        query: Search query (e.g., "SICP" or "retro software")
        content_type: Type of content - all, ebook, music, video, software, archive
        passes: Number of passes (default 2 for open directories)
        delay: Seconds between passes
        timeout: Request timeout in seconds
    
    Returns:
        List of result dictionaries (URLs that look like open directories)
    """
    # Build dork query based on content type
    dork_patterns = {
        "ebook": f'+(.MOBI|.CBZ|.CBR|.CBC|.CHM|.EPUB|.FB2|.LIT|.LRF|.ODT|.PDF|.PRC|.PDB|.PML|.RB|.RTF|.TCR) "{query}" intitle:"index of" -inurl:(jsp|pl|php|html|aspx|htm|cf|shtml) -inurl:(listen77|mp3raid|mp3toss|mp3drug|index_of|wallywashis)',
        
        "music": f'"{query}" intitle:"music" (mp3|aac|flac|wav|ogg|m4a) "Parent Directory" -htm -html -asp -php -listen77 -idmusic -airmp3 -shexy -vmp3',
        
        "video": f'"{query}" (avi|mp4|mkv|mpg|wmv|mov|divx|m4v) "Parent Directory" -"Trailer" -torrent -serial -cdkey -web-shelf -asp -html -zoozle -jsp -htm -listen77 -idmovies -shexy',
        
        "software": f'"{query}" (exe|iso|dmg|apk|deb|rpm|msi|bin) intitle:"index of" "Parent Directory" -inurl:(html|htm|php|asp|jsp) -torrent -magnet',
        
        "archive": f'"{query}" (zip|rar|7z|tar|gz|bz2|tgz) intitle:"index of" "Parent Directory" -html -htm -php -asp -jsp',
        
        "all": f'"{query}" intitle:"index of" "Parent Directory" -html -htm -php -asp -jsp -blog -forum -store -shop'
    }
    
    dork = dork_patterns.get(content_type, dork_patterns["all"])
    
    # Use persistent search for open directories
    results = search_persistent(dork, passes=passes, delay=delay, timeout=timeout)
    
    # Filter for likely open directory URLs
    odir_indicators = ["index of", "parent directory", "/pub/", "/files/", "/uploads/", 
                       "/media/", "/software/", "/ftp/", "/archive/", "/public/",
                       "/share/", "/dl/", "/downloads/"]
    
    filtered = []
    for r in results:
        url = r.get("url", "").lower()
        title = r.get("title", "").lower()
        
        # Check if it looks like an open directory
        is_odir = any(ind in url or ind in title for ind in odir_indicators)
        
        # Also check for directory-style URLs (ending in /, no file extension)
        if not is_odir:
            path = urllib.parse.urlparse(url).path
            has_extension = any(path.endswith(ext) for ext in ['.html', '.htm', '.php', '.asp', '.jsp'])
            is_odir = url.endswith("/") and not has_extension
        
        if is_odir:
            filtered.append(r)
    
    # If filtering removed everything, return original results
    return filtered if filtered else results


class SearchSession:
    """
    Persistent search session with SQLite storage.
    
    Accumulates results across multiple searches and de-duplicates.
    Useful for long-running OSINT investigations.
    """
    
    def __init__(self, db_path: str = ":memory:"):
        """
        Initialize search session.
        
        Args:
            db_path: Path to SQLite database (default in-memory)
        """
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """Initialize database schema."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS results (
                id INTEGER PRIMARY KEY,
                url_hash TEXT UNIQUE,
                query TEXT,
                title TEXT,
                url TEXT,
                content TEXT,
                engine TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()
    
    def _hash_url(self, url: str) -> str:
        """Create hash of URL for deduplication."""
        return hashlib.sha256(url.encode()).hexdigest()[:16]
    
    def search(self, query: str, instance: str = "dorxng", 
               timeout: int = 120) -> List[Dict[str, Any]]:
        """
        Execute search and store results.
        
        Returns only NEW results not already in database.
        """
        results = search(query, instance=instance, timeout=timeout)
        new_results = []
        
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        for r in results:
            url = r.get("url", "")
            url_hash = self._hash_url(url)
            
            try:
                c.execute('''
                    INSERT INTO results (url_hash, query, title, url, content, engine)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (url_hash, query, r.get("title", ""), url, 
                      r.get("content", ""), r.get("engine", "")))
                new_results.append(r)
            except sqlite3.IntegrityError:
                # URL already exists, skip
                pass
        
        conn.commit()
        conn.close()
        
        return new_results
    
    def search_persistent(self, query: str, passes: int = 3, 
                          delay: int = 5) -> List[Dict[str, Any]]:
        """Execute persistent search and store results."""
        all_new = []
        for i in range(passes):
            if i > 0 and delay > 0:
                time.sleep(delay)
            new_results = self.search(query)
            all_new.extend(new_results)
        return all_new
    
    def query_database(self, pattern: str) -> List[Dict[str, Any]]:
        """
        Query stored results by regex pattern.
        
        Args:
            pattern: Regex pattern to match against URL or title
        
        Returns:
            List of matching results
        """
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute('''
            SELECT query, title, url, content, engine, timestamp 
            FROM results 
            WHERE url REGEXP ? OR title REGEXP ?
            ORDER BY timestamp DESC
        ''', (pattern, pattern))
        
        results = []
        for row in c.fetchall():
            results.append({
                "query": row[0],
                "title": row[1],
                "url": row[2],
                "content": row[3],
                "engine": row[4],
                "timestamp": row[5]
            })
        
        conn.close()
        return results
    
    def get_all_results(self) -> List[Dict[str, Any]]:
        """Get all stored results."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('SELECT COUNT(*) FROM results')
        count = c.fetchone()[0]
        conn.close()
        return {"total": count}
    
    def get_stats(self) -> Dict[str, Any]:
        """Get session statistics."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute('SELECT COUNT(*) FROM results')
        total = c.fetchone()[0]
        
        c.execute('SELECT COUNT(DISTINCT query) FROM results')
        queries = c.fetchone()[0]
        
        c.execute('SELECT COUNT(DISTINCT engine) FROM results')
        engines = c.fetchone()[0]
        
        conn.close()
        return {"total_results": total, "unique_queries": queries, "engines": engines}


# CLI interface
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: search.py <query> [--odir TYPE] [--dork] [--passes N] [--delay S]")
        print("Types: all, ebook, music, video, software, archive")
        print("")
        print("Examples:")
        print("  search.py 'machine learning'")
        print("  search.py 'SICP' --odir ebook --passes 3")
        print("  search.py 'site:example.com filetype:pdf' --dork --passes 2")
        print("")
        print("Tip: Multiple passes find more results (Tor circuits rotate every 10s)")
        sys.exit(1)
    
    query = sys.argv[1]
    odir_type = None
    is_dork = False
    passes = 1
    delay = 5
    
    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == "--odir" and i + 1 < len(sys.argv):
            odir_type = sys.argv[i + 1]
            passes = max(passes, 2)  # Default 2 passes for open directories
            i += 2
        elif sys.argv[i] == "--dork":
            is_dork = True
            i += 1
        elif sys.argv[i] == "--passes" and i + 1 < len(sys.argv):
            passes = int(sys.argv[i + 1])
            i += 2
        elif sys.argv[i] == "--delay" and i + 1 < len(sys.argv):
            delay = int(sys.argv[i + 1])
            i += 2
        else:
            i += 1
    
    if odir_type:
        results = search_odir(query, odir_type, passes=passes, delay=delay)
    elif is_dork:
        if passes > 1:
            results = search_persistent(query, passes=passes, delay=delay)
        else:
            results = dork_search(query)
    elif passes > 1:
        results = search_persistent(query, passes=passes, delay=delay)
    else:
        results = search_with_fallback(query)
    
    print(f"Found {len(results)} results:\n")
    for r in results[:15]:
        print(f"  {r.get('title', 'No title')[:70]}")
        print(f"    {r.get('url', '')}")
        if r.get('content'):
            print(f"    {r.get('content')[:100]}...")
        print()
