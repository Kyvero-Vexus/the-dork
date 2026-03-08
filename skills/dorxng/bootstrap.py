#!/usr/bin/env python3
"""
DorXNG Bootstrap Check

Verifies DorXNG is working and guides setup if not.
Run this on first use.
"""

import subprocess
import sys
import os

def check_docker():
    """Check if Docker is available."""
    try:
        result = subprocess.run(
            ["docker", "--version"],
            capture_output=True, text=True, timeout=5
        )
        return result.returncode == 0
    except Exception:
        return False

def check_dorxng_container():
    """Check if DorXNG container is running."""
    try:
        result = subprocess.run(
            ["docker", "ps", "--filter", "name=dorxng", "--format", "{{.Names}}"],
            capture_output=True, text=True, timeout=5
        )
        return "dorxng" in result.stdout
    except Exception:
        return False

def check_dorxng_search():
    """Try to execute a search."""
    try:
        # Set a default URL if not configured
        if not os.environ.get("DORXNG_URL"):
            os.environ["DORXNG_URL"] = "http://localhost:8889/search"
        
        from search import search
        results = search("test", timeout=30)
        return len(results) > 0
    except Exception as e:
        print(f"  Error: {e}")
        return False

def setup_dorxng():
    """Set up DorXNG container."""
    print("\n📦 Setting up DorXNG...")
    
    # Pull and run
    cmd = [
        "docker", "run", "-d",
        "--name", "dorxng",
        "-p", "8889:443",
        "--restart", "unless-stopped",
        "ghcr.io/unya/dorxng:latest"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if result.returncode == 0:
            print("✓ DorXNG container started")
            print("⏳ Waiting 30 seconds for Tor to connect...")
            import time
            time.sleep(30)
            return True
        else:
            print(f"✗ Failed to start container: {result.stderr}")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def main():
    print("=" * 50)
    print("DorXNG Bootstrap Check")
    print("=" * 50)
    
    # Check Docker
    print("\n1. Checking Docker...")
    if check_docker():
        print("  ✓ Docker is available")
    else:
        print("  ✗ Docker not found")
        print("  → Install Docker: https://docs.docker.com/get-docker/")
        print("  → Or set DORXNG_URL to a public SearXNG instance")
        return False
    
    # Check container
    print("\n2. Checking DorXNG container...")
    if check_dorxng_container():
        print("  ✓ DorXNG container is running")
    else:
        print("  ✗ DorXNG container not found")
        
        # Offer to set up
        response = input("\n  Set up DorXNG automatically? [y/N] ")
        if response.lower() == 'y':
            if not setup_dorxng():
                return False
        else:
            print("  → Run manually:")
            print("    docker run -d --name dorxng -p 8889:443 ghcr.io/unya/dorxng:latest")
            print("  → Or set DORXNG_URL to a public instance")
            return False
    
    # Check search
    print("\n3. Testing search...")
    if check_dorxng_search():
        print("  ✓ Search is working!")
        print("\n" + "=" * 50)
        print("✓ DorXNG is ready!")
        print("=" * 50)
        print("\nYou can delete BOOTSTRAP.md now.")
        return True
    else:
        print("  ✗ Search returned no results")
        print("  → Check logs: docker logs dorxng")
        print("  → May need to wait for Tor to connect")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
