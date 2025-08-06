#!/usr/bin/env python3
"""Generate test data for history page debugging."""

import csv
from datetime import datetime, timedelta
from pathlib import Path
import random

# Create data directory
data_dir = Path("/tmp/aircraft-test-data")
data_dir.mkdir(parents=True, exist_ok=True)

# Generate sample circle detections
circles_file = data_dir / "circle_detections.csv"
with open(circles_file, 'w', newline='') as f:
    fieldnames = ['timestamp', 'hex_id', 'callsign', 'center_lat', 'center_lon', 
                  'radius_km', 'turns', 'altitude_ft', 'speed_kts', 'tar1090_url']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    
    # Generate 10 sample circle detections
    for i in range(10):
        timestamp = datetime.now() - timedelta(hours=random.randint(1, 72))
        writer.writerow({
            'timestamp': timestamp.isoformat(),
            'hex_id': f"ABC{i:03d}",
            'callsign': f"TEST{i:03d}",
            'center_lat': 40.0 + random.uniform(-5, 5),
            'center_lon': -74.0 + random.uniform(-5, 5),
            'radius_km': random.uniform(0.5, 10),
            'turns': random.uniform(1.5, 5),
            'altitude_ft': random.randint(2000, 40000),
            'speed_kts': random.randint(100, 500),
            'tar1090_url': f"https://radar.hallgren.net/map/?icao=ABC{i:03d}&time={int(timestamp.timestamp())}"
        })

# Generate sample grid detections
grids_file = data_dir / "grid_detections.csv"
with open(grids_file, 'w', newline='') as f:
    fieldnames = ['timestamp', 'hex_id', 'callsign', 'pattern_type', 'center_lat', 
                  'center_lon', 'num_legs', 'coverage_area_km2', 'altitude_ft', 'tar1090_url']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    
    # Generate 5 sample grid detections
    for i in range(5):
        timestamp = datetime.now() - timedelta(hours=random.randint(1, 48))
        writer.writerow({
            'timestamp': timestamp.isoformat(),
            'hex_id': f"GRD{i:03d}",
            'callsign': f"GRID{i:03d}",
            'pattern_type': random.choice(['Survey Grid', 'Search Pattern', 'Mapping Grid']),
            'center_lat': 40.0 + random.uniform(-5, 5),
            'center_lon': -74.0 + random.uniform(-5, 5),
            'num_legs': random.randint(3, 10),
            'coverage_area_km2': random.uniform(10, 200),
            'altitude_ft': random.randint(5000, 35000),
            'tar1090_url': f"https://radar.hallgren.net/map/?icao=GRD{i:03d}&time={int(timestamp.timestamp())}"
        })

print(f"✅ Test data generated in {data_dir}")
print(f"  - {circles_file}: 10 circle detections")
print(f"  - {grids_file}: 5 grid detections")
print("\nTo test with Docker:")
print(f"docker run -d --name aircraft-history-test -p 8893:8888 \\")
print(f"  -v {data_dir}:/app/data \\")
print(f"  -e TAR1090_URL=http://fr24.hallgren.net:8080 \\")
print(f"  aircraft-circle:latest")
print("\nThen visit: http://localhost:8893/history")