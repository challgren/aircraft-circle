# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Aircraft Patterns is a Python-based pattern detection system for monitoring aircraft via TAR1090 feeds. It identifies circular holding patterns, training flights, and grid survey patterns in real-time, with a Flask web interface for visualization.

## Key Architecture

### Core Components

1. **app.py** - Monolithic Python application (~2900 lines) containing:
   - `TAR1090Monitor` - Main monitoring class that polls TAR1090 for aircraft data
   - `CircleDetector` - Analyzes flight paths for circular patterns
   - `GridDetector` - Identifies grid/survey flight patterns
   - Flask web server with embedded HTML templates (MAP_HTML_TEMPLATE, HISTORY_HTML_TEMPLATE)
   - Pattern logging to CSV files

2. **Docker Structure**:
   - Based on `ghcr.io/sdr-enthusiasts/docker-baseimage:base`
   - Uses s6-overlay v3 for process management
   - Service configuration in `rootfs/etc/s6-overlay/s6-rc.d/aircraft-patterns/`
   - Health check script in `rootfs/scripts/healthcheck.py`

3. **Web Interface**:
   - Self-contained HTML/JavaScript in Python string templates
   - Dynamic base URL detection for reverse proxy support
   - TAR1090-style aircraft icons embedded in templates
   - Real-time updates via polling `/api/patterns` endpoint

## Essential Commands

### Building and Testing

```bash
# Build Docker image locally
docker build -t aircraft-patterns:dev .

# Multi-architecture build
docker buildx build --platform linux/amd64,linux/arm64,linux/arm/v7 -t aircraft-patterns:dev .

# Run locally with Docker
docker run -it --rm -p 8888:8888 -e TAR1090_URL=http://fr24.hallgren.net:8080 aircraft-patterns:dev

# Run Python directly (for development)
python3 app.py --server http://fr24.hallgren.net:8080 --web --web-port 8888
```

### Testing Behind Reverse Proxy

```bash
# Use the test compose file
docker-compose -f docker-compose.proxy-test.yml up

# Access at http://localhost:8080/circles/
```

### CI/CD and Linting

The project uses GitHub Actions for automated checks:

- **hadolint** - Dockerfile linting
- **shellcheck** - Shell script validation  
- **markdownlint** - Markdown formatting
- **deploy** - Multi-arch build and push to GHCR on main branch changes

To run linters locally:

```bash
hadolint Dockerfile
shellcheck rootfs/**/*.sh
markdownlint *.md
```

## Important Implementation Details

### S6-Overlay Service

The s6 service configuration is critical for Docker container operation:

- Run script must use `#!/command/with-contenv bash` (not `/usr/bin/with-contenv`)
- Service runs as root (no `abc` user in base image)
- Located at `/etc/s6-overlay/s6-rc.d/aircraft-patterns/run`

### Reverse Proxy Support

The application supports mounting at subpaths (e.g., `/circles/`):

- JavaScript dynamically detects base URL from `window.location.pathname`
- All navigation uses relative links (`./`, `history` not `/`, `/history`)
- API calls use computed `baseUrl + '/api/...'`
- ProxyFix middleware handles X-Forwarded headers

### Pattern Detection Parameters

Key thresholds that affect detection sensitivity:

- Circle: MIN_RADIUS=0.5km, MAX_RADIUS=10km, MIN_TURNS=1.5
- Grid: MIN_GRID_LEGS=3, MIN_LEG_LENGTH=2.0km
- Data quality: max_speed_kmh=1000, max_position_jump_km=5.0

### API Endpoints

- `/` - Main map view
- `/history` - Historical patterns viewer
- `/api/patterns` - Current aircraft and active patterns (JSON)
- `/api/history` - Historical patterns from CSV files (JSON)
- `/api/health` - Health check with detailed status

### CSV Data Files

Pattern detections are logged to:

- `/app/circle_detections.csv` - Circular patterns
- `/app/grid_detections.csv` - Grid patterns

Each entry includes timestamp, aircraft info, pattern parameters, and TAR1090 replay URL.

## Common Issues and Solutions

1. **Docker s6 service fails**: Check shebang in run script is `#!/command/with-contenv bash`

2. **No aircraft showing**: Verify TAR1090_URL is accessible and returns data at `/data/aircraft.json`

3. **Reverse proxy issues**: Ensure proxy sets proper headers and uses `proxy_redirect / /subpath/`

4. **Markdown linting failures**: Files must end with newline, code blocks need surrounding blank lines

## Testing TAR1090 Connection

The application expects TAR1090 API format:

```bash
curl http://your-tar1090/data/aircraft.json
```

Should return JSON with `aircraft` or `ac` array containing objects with lat, lon, hex, flight fields.
