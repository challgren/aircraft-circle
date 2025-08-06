#!/usr/bin/env python3
"""Health check script for Aircraft Patterns Detector container."""

import sys
import os
import json
import requests
from pathlib import Path
import time

def check_web_server():
    """Check if web server is responding."""
    if os.environ.get('ENABLE_WEB', 'true').lower() != 'true':
        return True  # Web server disabled, skip check
    
    port = os.environ.get('WEB_PORT', '8888')
    try:
        # Check health endpoint
        response = requests.get(f'http://localhost:{port}/api/health', timeout=3)
        if response.status_code != 200:
            return False
        
        # Verify response is valid JSON and check status
        data = response.json()
        if not isinstance(data, dict):
            return False
        
        # Check the reported status
        status = data.get('status', 'unknown')
        if status == 'healthy':
            return True
        elif status == 'degraded':
            print(f"Warning: Service is degraded - {data.get('checks', {})}")
            return True  # Still return True for degraded state
        else:
            print(f"Error: Service status is {status}")
            return False
            
    except Exception as e:
        print(f"Web server check error: {e}")
        return False

def check_process():
    """Check if main process is running."""
    try:
        # Check if python process is running
        import subprocess
        result = subprocess.run(['pgrep', '-f', 'python3.*app.py'], 
                              capture_output=True, text=True)
        return result.returncode == 0
    except Exception as e:
        print(f"Process check error: {e}")
        return False

def check_tar1090_connection():
    """Check if we can connect to TAR1090."""
    tar1090_url = os.environ.get('TAR1090_URL', 'http://tar1090:80')
    try:
        # Allow this check to fail gracefully as TAR1090 might be temporarily unavailable
        response = requests.get(f'{tar1090_url}/data/aircraft.json', timeout=5)
        if response.status_code == 200:
            data = response.json()
            # Check if we got valid aircraft data
            if 'aircraft' in data or 'ac' in data:
                return True
        # Don't fail health check if TAR1090 is temporarily unavailable
        # Just log a warning
        print(f"Warning: TAR1090 at {tar1090_url} not responding (status: {response.status_code})")
        return True  # Return True to not fail the container
    except requests.exceptions.RequestException as e:
        print(f"Warning: Cannot connect to TAR1090 at {tar1090_url}: {e}")
        return True  # Return True to not fail the container
    except Exception as e:
        print(f"Warning: TAR1090 check error: {e}")
        return True  # Return True to not fail the container

def check_log_files():
    """Check if log files are writable."""
    try:
        # Check if we can write to log directory
        log_dir = Path('/app')
        if not log_dir.exists():
            return False
        
        # Test write access
        test_file = log_dir / '.healthcheck_test'
        test_file.write_text(str(time.time()))
        test_file.unlink()
        return True
    except Exception as e:
        print(f"Log file check error: {e}")
        return False

def main():
    """Run health checks."""
    # Define checks with their names and criticality
    checks = [
        ("Process", check_process(), True),  # Critical
        ("Web Server", check_web_server(), True),  # Critical
        ("Log Files", check_log_files(), True),  # Critical
        ("TAR1090 Connection", check_tar1090_connection(), False),  # Non-critical
    ]
    
    # Separate critical and non-critical failures
    critical_failures = [name for name, status, critical in checks if not status and critical]
    warnings = [name for name, status, critical in checks if not status and not critical]
    
    # Print status
    if warnings:
        print(f"Health check warnings: {', '.join(warnings)}")
    
    if critical_failures:
        print(f"Health check FAILED: {', '.join(critical_failures)}")
        sys.exit(1)
    
    print("Health check PASSED")
    sys.exit(0)

if __name__ == "__main__":
    main()