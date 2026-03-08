#!/usr/bin/env python3
"""
SearX Search Module

Search via public SearX instances (clearnet, not anonymous).
Use as fallback when DorXNG is unavailable.
"""

import urllib.request
import urllib.parse
import json
import time
from typing import List, Dict, Any, Optional

# Default instances (check searx.space for current reliable ones)
DEFAULT_INSTANCES = [
    "https://search.bus-hit.me",
    "https://searx.be",
    "https://search.sapti.me",
]

# Track last query time per instance for rate limiting
_last_query_time: Dict[str, float] = {}
_MIN_DELAY = 2.0  # Minimum seconds between queries to same instance


def search_searx(
    query: str,
    instance: Optional[str] = None,
    timeout: int = 30,
    rotate: bool = False
) -> List[Dict[str, Any]]:
    """
    Search via SearX instance.
    
    Args:
        query: Search query
        instance: SearX instance URL (default: first from DEFAULT_INSTANCES)
        timeout: Request timeout in seconds
        rotate: If True, try other instances on failure
    
    Returns:
        List of result dictionaries with title, url, content, engine
    
    Note:
        SearX is NOT anonymous. Queries go over clearnet.
        Rate limits apply - don't hammer instances.
    """
    if instance is None:
        instance = DEFAULT_INSTANCES[0]
    
    # Rate limiting - enforce minimum delay
    now = time.time()
    last = _last_query_time.get(instance, 0)
    if now - last < _MIN_DELAY:
        time.sleep(_MIN_DELAY - (now - last))
    
    encoded = urllib.parse.quote(query, safe='')
    url = f"{instance}/search?q={encoded}&format=json"
    
    req = urllib.request.Request(url, headers={
        'User-Agent': 'The-Dork/1.0 (https://github.com/Kyvero-Vexus/the-dork)'
    })
    
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            _last_query_time[instance] = time.time()
            data = json.loads(response.read().decode('utf-8'))
            return data.get('results', [])
    except Exception as e:
        if rotate:
            # Try other instances
            for alt_instance in DEFAULT_INSTANCES:
                if alt_instance != instance:
                    try:
                        return search_searx(query, alt_instance, timeout, rotate=False)
                    except:
                        continue
        print(f"SearX error ({instance}): {e}")
        return []


def check_instance(instance_url: str, timeout: int = 10) -> bool:
    """
    Check if a SearX instance is responding.
    
    Args:
        instance_url: SearX instance base URL
        timeout: Request timeout
    
    Returns:
        True if instance is responding
    """
    try:
        req = urllib.request.Request(
            f"{instance_url}/search?q=test&format=json",
            headers={'User-Agent': 'The-Dork/1.0'}
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status == 200
    except:
        return False


def find_instances() -> List[str]:
    """
    Return list of known SearX instances.
    
    For full list with ratings, see: https://searx.space/
    """
    return DEFAULT_INSTANCES.copy()


# CLI interface
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python search.py <query> [--instance URL] [--rotate]")
        print("")
        print("Options:")
        print("  --instance URL  Use specific SearX instance")
        print("  --rotate        Try other instances on failure")
        print("")
        print("Instances (see searx.space for full list):")
        for inst in DEFAULT_INSTANCES:
            print(f"  {inst}")
        sys.exit(1)
    
    query = sys.argv[1]
    instance = None
    rotate = False
    
    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == "--instance" and i + 1 < len(sys.argv):
            instance = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "--rotate":
            rotate = True
            i += 1
        else:
            i += 1
    
    print(f"Searching via SearX: {query}")
    print(f"Instance: {instance or 'default'}")
    print()
    
    results = search_searx(query, instance=instance, rotate=rotate)
    
    print(f"Found {len(results)} results:\n")
    for r in results[:10]:
        print(f"  {r.get('title', 'No title')[:70]}")
        print(f"    {r.get('url', '')}")
        if r.get('content'):
            print(f"    {r.get('content')[:100]}...")
        print()
