#!/usr/bin/env python3
"""Health check script for Aircraft Circle Detector container."""

import sys
import os
import requests
from pathlib import Path

def check_web_server():
    """Check if web server is responding."""
    if os.environ.get('ENABLE_WEB', 'true').lower() == 'true':
        port = os.environ.get('WEB_PORT', '8888')
        try:
            response = requests.get(f'http://localhost:{port}/data.json', timeout=3)
            return response.status_code == 200
        except:
            return False
    return True

def check_process():
    """Check if main process is running."""
    try:
        # Check if python process is running
        import subprocess
        result = subprocess.run(['pgrep', '-f', 'python3.*app.py'], 
                              capture_output=True, text=True)
        return result.returncode == 0
    except:
        return False

def main():
    """Run health checks."""
    checks = [
        ("Process", check_process()),
        ("Web Server", check_web_server()),
    ]
    
    failed = [name for name, status in checks if not status]
    
    if failed:
        print(f"Health check failed: {', '.join(failed)}")
        sys.exit(1)
    
    print("Health check passed")
    sys.exit(0)

if __name__ == "__main__":
    main()