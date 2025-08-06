FROM ghcr.io/sdr-enthusiasts/docker-baseimage:base

ENV PUID=1000 \
    PGID=1000 \
    TAR1090_URL="http://tar1090:80" \
    WEB_PORT=8888 \
    ENABLE_WEB=true \
    MIN_RADIUS=0.5 \
    MAX_RADIUS=10 \
    MIN_TURNS=1.5 \
    MIN_GRID_LEGS=3 \
    MIN_LEG_LENGTH=2.0 \
    COMPACT_MODE=false \
    QUIET_MODE=false \
    UPDATE_INTERVAL=5 \
    SHOW_ALL_AIRCRAFT=true \
    SHOW_TRACKS=true \
    MAX_TRACK_POINTS=50

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Install Python dependencies
RUN set -x && \
    KEPT_PACKAGES=() && \
    TEMP_PACKAGES=() && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-venv \
        "${KEPT_PACKAGES[@]}" \
        "${TEMP_PACKAGES[@]}" && \
    # Clean up
    apt-get remove -y "${TEMP_PACKAGES[@]}" && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

# Copy application files
COPY requirements.txt /app/
COPY app.py /app/

WORKDIR /app

# Install Python requirements
RUN python3 -m pip install --no-cache-dir --break-system-packages -r requirements.txt

# Copy rootfs overlay (includes static files)
COPY rootfs/ /

# Ensure scripts are executable
RUN chmod +x /etc/s6-overlay/s6-rc.d/aircraft-circle/run && \
    chmod +x /scripts/healthcheck.py

# Expose web port
EXPOSE 8888

# Health check
# Start period: 60s to allow service to fully start
# Interval: 30s for regular checks
# Timeout: 10s to allow for TAR1090 connection check
# Retries: 3 failures before marking unhealthy
HEALTHCHECK --start-period=60s --interval=30s --timeout=10s --retries=3 \
    CMD python3 /scripts/healthcheck.py || exit 1