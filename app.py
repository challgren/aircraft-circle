#!/usr/bin/env python3
"""
TAR1090 Aircraft Circle Detector
A Python application to monitor aircraft and detect circular flight patterns.
"""

# HTML template for the map viewer
MAP_HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Aircraft Pattern Viewer</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <script>
        // Aircraft icon shapes from tar1090 - embedded directly to avoid loading issues
        const aircraftShapes = {
            'airliner': {
                svg: '<path d="m 16,1 -1.5,1 -1,2 -2,3 v 6 l -5,2 v 1.5 l 5,-0.5 v 5.5 l -1.5,1.5 v 1 l 2,-0.5 0.5,-0.5 h 1 l 0.5,0.5 2,0.5 v -1 l -1.5,-1.5 v -5.5 l 5,0.5 v -1.5 l -5,-2 v -6 l -2,-3 -1,-2 z"/>',
                width: 32,
                height: 32,
                viewBox: '0 0 32 32',
                scale: 1.0
            },
            'helicopter': {
                svg: '<path d="m 16,3 c -0.5,0 -1,0.5 -1,1 v 2 h -6 v 1 h 14 v -1 h -6 v -2 c 0,-0.5 -0.5,-1 -1,-1 z m -1,5 v 8 l -3,1 v 1.5 l 3,-0.5 v 4 h 2 v -4 l 3,0.5 v -1.5 l -3,-1 v -8 z m -7,16 v 1 h 16 v -1 z"/>',
                width: 32,
                height: 32,
                viewBox: '0 0 32 32',
                scale: 1.0,
                noRotate: true
            },
            'default': {
                svg: '<path d="M 12 2 L 12 8 L 20 14 L 20 16 L 12 13 L 12 18 L 15 20 L 15 21 L 12 20 L 9 21 L 9 20 L 12 18 L 12 13 L 4 16 L 4 14 L 12 8 L 12 2 Z"/>',
                width: 24,
                height: 24,
                viewBox: '0 0 24 24',
                scale: 1.0
            }
        };
        
        // Function to get appropriate icon for aircraft
        function getAircraftIcon(typeDesignator, category) {
            // For now, return default icon - can expand this later
            return aircraftShapes['default'];
        }
    </script>
    <style>
        body {
            margin: 0;
            padding: 0;
            font-family: Arial, sans-serif;
        }
        .header {
            background: white;
            padding: 10px 30px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            display: flex;
            justify-content: space-between;
            align-items: center;
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            z-index: 1001;
        }
        .header h1 {
            margin: 0;
            color: #333;
            font-size: 20px;
        }
        .nav-links {
            display: flex;
            gap: 20px;
        }
        .nav-links a {
            text-decoration: none;
            color: #007bff;
            padding: 8px 16px;
            border-radius: 4px;
            transition: background 0.3s;
        }
        .nav-links a:hover {
            background: #f0f0f0;
        }
        .nav-links a.active {
            background: #007bff;
            color: white;
        }
        #map {
            height: 100vh;
            width: 100%;
            margin-top: 50px;
        }
        .info-panel {
            position: absolute;
            top: 70px;
            right: 10px;
            background: white;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
            z-index: 1000;
            max-width: 300px;
        }
        .pattern-item {
            margin: 10px 0;
            padding: 10px;
            border-left: 4px solid #007bff;
            background: #f8f9fa;
            cursor: pointer;
        }
        .pattern-item:hover {
            background: #e9ecef;
        }
        .circle-pattern {
            border-left-color: #dc3545;
        }
        .grid-pattern {
            border-left-color: #28a745;
        }
        .stats {
            display: flex;
            justify-content: space-around;
            margin: 10px 0;
            padding: 10px;
            background: #f8f9fa;
            border-radius: 4px;
        }
        .stat-item {
            text-align: center;
        }
        .stat-value {
            font-size: 24px;
            font-weight: bold;
            color: #007bff;
        }
        .stat-label {
            font-size: 12px;
            color: #6c757d;
        }
        .legend {
            position: absolute;
            bottom: 20px;
            left: 20px;
            background: white;
            padding: 10px;
            border-radius: 4px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
            z-index: 1000;
        }
        .legend-item {
            margin: 5px 0;
            display: flex;
            align-items: center;
        }
        .legend-item input {
            margin-right: 8px;
        }
        .controls-panel {
            position: absolute;
            bottom: 20px;
            right: 20px;
            background: white;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
            z-index: 1000;
        }
        .control-item {
            margin: 8px 0;
            display: flex;
            align-items: center;
        }
        .control-item input[type="checkbox"] {
            margin-right: 8px;
        }
        .control-item label {
            cursor: pointer;
            user-select: none;
        }
        .aircraft-count {
            margin-top: 10px;
            padding-top: 10px;
            border-top: 1px solid #dee2e6;
            font-size: 12px;
            color: #6c757d;
        }
        .update-time {
            position: absolute;
            top: 60px;
            left: 50%;
            transform: translateX(-50%);
            background: white;
            padding: 5px 15px;
            border-radius: 20px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
            z-index: 1000;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>✈️ Aircraft Pattern Detector - Live View</h1>
        <div class="nav-links">
            <a href="/" class="active">Live View</a>
            <a href="/history">History</a>
        </div>
    </div>
    
    <div id="map"></div>
    
    <div class="update-time">
        <span id="updateTime">Waiting for data...</span>
    </div>
    
    <div class="info-panel">
        <h3>🛩️ Pattern Detection</h3>
        <div class="stats">
            <div class="stat-item">
                <div class="stat-value" id="totalAircraft">0</div>
                <div class="stat-label">Aircraft</div>
            </div>
            <div class="stat-item">
                <div class="stat-value" id="circleCount">0</div>
                <div class="stat-label">Circles</div>
            </div>
            <div class="stat-item">
                <div class="stat-value" id="gridCount">0</div>
                <div class="stat-label">Grids</div>
            </div>
        </div>
        
        <h4>Active Patterns</h4>
        <div id="patternList"></div>
    </div>
    
    <div class="legend">
        <div class="legend-item">🔴 Circle Pattern</div>
        <div class="legend-item">🟢 Grid Pattern</div>
        <div class="legend-item">✈️ All Aircraft</div>
    </div>
    
    <div class="controls-panel">
        <h4 style="margin-top: 0;">Display Options</h4>
        <div class="control-item">
            <input type="checkbox" id="showAllAircraft" checked>
            <label for="showAllAircraft">Show All Aircraft</label>
        </div>
        <div class="control-item">
            <input type="checkbox" id="showTracks" checked>
            <label for="showTracks">Show Track History</label>
        </div>
        <div class="control-item">
            <input type="checkbox" id="showPatterns" checked>
            <label for="showPatterns">Show Patterns</label>
        </div>
        <div class="control-item">
            <input type="checkbox" id="autoCenter" checked>
            <label for="autoCenter">Auto-Center on Patterns</label>
        </div>
        <div class="aircraft-count">
            <span id="visibleAircraft">0</span> aircraft visible
        </div>
    </div>

    <script>
        // Initialize map
        const map = L.map('map').setView([40.0, -95.0], 5);
        
        // Add OpenStreetMap tiles
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors'
        }).addTo(map);
        
        // Layer groups for patterns
        const circleLayer = L.layerGroup().addTo(map);
        const gridLayer = L.layerGroup().addTo(map);
        const pathLayer = L.layerGroup().addTo(map);
        const aircraftLayer = L.layerGroup().addTo(map);
        const trackLayer = L.layerGroup().addTo(map);
        
        // Store for aircraft markers and previous patterns
        const aircraftMarkers = {};
        const aircraftTracks = {};
        let previousCircles = new Set();
        let previousGrids = new Set();
        let hasInitialized = false;
        let visibleAircraftCount = 0;
        
        // Request notification permission on load
        if ("Notification" in window && Notification.permission === "default") {
            Notification.requestPermission();
        }
        
        // Show browser notification
        function showNotification(title, body, tag) {
            // Browser notification if permitted
            if ("Notification" in window && Notification.permission === "granted") {
                new Notification(title, {
                    body: body,
                    icon: 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><text y="50" font-size="50">✈️</text></svg>',
                    tag: tag,
                    requireInteraction: false
                });
            }
            
            // Also show in-page alert
            const alertDiv = document.createElement('div');
            alertDiv.style.cssText = `
                position: fixed;
                top: 70px;
                left: 50%;
                transform: translateX(-50%);
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 15px 25px;
                border-radius: 8px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.3);
                z-index: 2000;
                animation: slideDown 0.5s ease-out;
                font-weight: bold;
                cursor: pointer;
            `;
            alertDiv.innerHTML = `🚨 ${title}: ${body}`;
            alertDiv.onclick = () => alertDiv.remove();
            document.body.appendChild(alertDiv);
            
            // Auto-remove after 10 seconds
            setTimeout(() => alertDiv.remove(), 10000);
        }
        
        // Add CSS animation for alerts
        if (!document.getElementById('alertStyles')) {
            const style = document.createElement('style');
            style.id = 'alertStyles';
            style.textContent = `
                @keyframes slideDown {
                    from { transform: translate(-50%, -100%); opacity: 0; }
                    to { transform: translate(-50%, 0); opacity: 1; }
                }
            `;
            document.head.appendChild(style);
        }
        
        // Create aircraft icon using TAR1090 shapes
        function createAircraftIcon(typeDesignator, category, altitude, heading) {
            const rotation = heading || 0;
            
            // Get altitude-based color (similar to TAR1090)
            let color = '#00ff00';  // Default green
            if (altitude < 1000) {
                color = '#ff0000';  // Red for low altitude
            } else if (altitude < 5000) {
                color = '#ff8800';  // Orange
            } else if (altitude < 10000) {
                color = '#ffff00';  // Yellow
            } else if (altitude < 20000) {
                color = '#00ff00';  // Green
            } else if (altitude < 30000) {
                color = '#00ffff';  // Cyan
            } else {
                color = '#ff00ff';  // Magenta for high altitude
            }
            
            // Get the appropriate icon shape
            const icon = getAircraftIcon(typeDesignator, category);
            const scale = icon.scale || 1.0;
            const size = 32 * scale;
            
            // Don't rotate if icon has noRotate flag
            const rotateTransform = icon.noRotate ? '' : `transform: rotate(${rotation}deg);`;
            
            return L.divIcon({
                html: `
                    <div style="${rotateTransform} transform-origin: center;">
                        <svg width="${size}" height="${size}" viewBox="${icon.viewBox}" 
                             xmlns="http://www.w3.org/2000/svg" 
                             style="filter: drop-shadow(1px 1px 2px rgba(0,0,0,0.5));">
                            <g fill="${color}" stroke="white" stroke-width="0.5">
                                ${icon.svg}
                            </g>
                        </svg>
                    </div>
                `,
                iconSize: [size, size],
                iconAnchor: [size/2, size/2],
                className: ''
            });
        }
        
        // Calculate heading from last two points
        function calculateHeading(path) {
            if (path.length < 2) return 0;
            const p1 = path[path.length - 2];
            const p2 = path[path.length - 1];
            const dLon = (p2.lon - p1.lon) * Math.PI / 180;
            const lat1 = p1.lat * Math.PI / 180;
            const lat2 = p2.lat * Math.PI / 180;
            const y = Math.sin(dLon) * Math.cos(lat2);
            const x = Math.cos(lat1) * Math.sin(lat2) - Math.sin(lat1) * Math.cos(lat2) * Math.cos(dLon);
            const heading = Math.atan2(y, x) * 180 / Math.PI;
            return (heading + 360) % 360;
        }
        
        // Update patterns from API
        async function updatePatterns() {
            try {
                const response = await fetch('/api/patterns');
                const data = await response.json();
                
                // Debug logging
                console.log('Data received:', {
                    totalAircraft: data.aircraft_count,
                    circles: data.circles.length,
                    grids: data.grids.length,
                    allAircraft: data.all_aircraft ? data.all_aircraft.length : 0
                });
                
                // Update stats
                document.getElementById('totalAircraft').textContent = data.aircraft_count;
                document.getElementById('circleCount').textContent = data.circles.length;
                document.getElementById('gridCount').textContent = data.grids.length;
                document.getElementById('updateTime').textContent = 
                    'Updated: ' + new Date(data.timestamp).toLocaleTimeString();
                
                // Get control states
                const showAllAircraft = document.getElementById('showAllAircraft').checked;
                const showTracks = document.getElementById('showTracks').checked;
                const showPatterns = document.getElementById('showPatterns').checked;
                const autoCenter = document.getElementById('autoCenter').checked;
                
                // Clear existing layers
                circleLayer.clearLayers();
                gridLayer.clearLayers();
                pathLayer.clearLayers();
                aircraftLayer.clearLayers();
                trackLayer.clearLayers();
                visibleAircraftCount = 0;
                
                // Check for new patterns and send alerts
                const currentCircles = new Set(data.circles.map(c => c.hex_id));
                const currentGrids = new Set(data.grids.map(g => g.hex_id));
                
                if (hasInitialized) {
                    // Check for new circles
                    data.circles.forEach(circle => {
                        if (!previousCircles.has(circle.hex_id)) {
                            showNotification(
                                'New Circle Pattern Detected',
                                `${circle.callsign} - ${circle.turns.toFixed(1)} turns, ${circle.radius.toFixed(1)}km radius`,
                                `circle-${circle.hex_id}`
                            );
                        }
                    });
                    
                    // Check for new grids
                    data.grids.forEach(grid => {
                        if (!previousGrids.has(grid.hex_id)) {
                            showNotification(
                                'New Grid Pattern Detected',
                                `${grid.callsign} - ${grid.pattern_type}, ${grid.num_legs} legs`,
                                `grid-${grid.hex_id}`
                            );
                        }
                    });
                }
                
                previousCircles = currentCircles;
                previousGrids = currentGrids;
                hasInitialized = true;
                
                // Update pattern list
                const patternList = document.getElementById('patternList');
                patternList.innerHTML = '';
                
                // Process circles
                data.circles.forEach(circle => {
                    // Draw circle on map (only if patterns are enabled)
                    if (showPatterns) {
                        const circleMarker = L.circle([circle.center_lat, circle.center_lon], {
                            radius: circle.radius * 1000, // Convert km to meters
                            color: '#dc3545',
                            fillColor: '#dc3545',
                            fillOpacity: 0.2,
                            weight: 2
                        }).addTo(circleLayer);
                    }
                    
                    // Always show aircraft and paths if there's data
                    if (circle.path && circle.path.length > 1) {
                        // Draw flight path if patterns are enabled
                        if (showPatterns) {
                            const pathCoords = circle.path.map(p => [p.lat, p.lon]);
                            L.polyline(pathCoords, {
                                color: '#0066cc',
                                weight: 2,
                                opacity: 0.7
                            }).addTo(pathLayer);
                        }
                        
                        // Always add aircraft marker at last position
                        const lastPos = circle.path[circle.path.length - 1];
                        const heading = calculateHeading(circle.path);
                        const altitude = circle.current_alt || 0;
                        const typeDesignator = circle.type || null;
                        const category = circle.category || null;
                        const marker = L.marker([lastPos.lat, lastPos.lon], {
                            icon: createAircraftIcon(typeDesignator, category, altitude, heading)
                        }).addTo(aircraftLayer);
                        
                        marker.bindPopup(`
                            <strong>${circle.callsign}</strong><br>
                            Circling: ${circle.turns.toFixed(1)} turns<br>
                            Radius: ${circle.radius.toFixed(1)} km<br>
                            ${circle.current_alt ? `Altitude: ${circle.current_alt.toLocaleString()} ft<br>` : ''}
                            ${circle.current_speed ? `Speed: ${circle.current_speed} kts` : ''}
                        `);
                        
                        visibleAircraftCount++;
                    }
                    
                    // Add to pattern list
                    const patternDiv = document.createElement('div');
                    patternDiv.className = 'pattern-item circle-pattern';
                    patternDiv.innerHTML = `
                        <strong>🔴 ${circle.callsign}</strong><br>
                        <small>${circle.turns.toFixed(1)} turns, ${circle.radius.toFixed(1)} km radius</small>
                    `;
                    patternDiv.onclick = () => {
                        map.setView([circle.center_lat, circle.center_lon], 12);
                    };
                    patternList.appendChild(patternDiv);
                });
                
                // Process grids
                data.grids.forEach(grid => {
                    // Draw grid area (only if patterns are enabled)
                    if (showPatterns) {
                        const bounds = calculateGridBounds(grid);
                        L.rectangle(bounds, {
                            color: '#28a745',
                            fillColor: '#28a745',
                            fillOpacity: 0.1,
                            weight: 2
                        }).addTo(gridLayer);
                    }
                    
                    // Always show aircraft and paths if there's data
                    if (grid.path && grid.path.length > 1) {
                        // Draw flight path if patterns are enabled
                        if (showPatterns) {
                            const pathCoords = grid.path.map(p => [p.lat, p.lon]);
                            L.polyline(pathCoords, {
                                color: '#009900',
                                weight: 3,
                                opacity: 0.8,
                                dashArray: '5, 5'
                            }).addTo(pathLayer);
                        }
                        
                        // Always add aircraft marker at last position
                        const lastPos = grid.path[grid.path.length - 1];
                        const heading = calculateHeading(grid.path);
                        const altitude = grid.current_alt || 0;
                        const typeDesignator = grid.type || null;
                        const category = grid.category || null;
                        const marker = L.marker([lastPos.lat, lastPos.lon], {
                            icon: createAircraftIcon(typeDesignator, category, altitude, heading)
                        }).addTo(aircraftLayer);
                        
                        marker.bindPopup(`
                            <strong>${grid.callsign}</strong><br>
                            Pattern: ${grid.pattern_type}<br>
                            Legs: ${grid.num_legs}<br>
                            Coverage: ${grid.coverage_area.toFixed(1)} km²<br>
                            ${grid.current_alt ? `Altitude: ${grid.current_alt.toLocaleString()} ft<br>` : ''}
                            ${grid.current_speed ? `Speed: ${grid.current_speed} kts` : ''}
                        `);
                        
                        visibleAircraftCount++;
                    }
                    
                    // Add to pattern list
                    const patternDiv = document.createElement('div');
                    patternDiv.className = 'pattern-item grid-pattern';
                    patternDiv.innerHTML = `
                        <strong>🟢 ${grid.callsign}</strong><br>
                        <small>${grid.pattern_type}: ${grid.num_legs} legs, ${grid.coverage_area.toFixed(1)} km²</small>
                    `;
                    patternDiv.onclick = () => {
                        map.setView([grid.center_lat, grid.center_lon], 11);
                    };
                    patternList.appendChild(patternDiv);
                });
                
                // Add all aircraft if enabled
                if (showAllAircraft && data.all_aircraft) {
                    console.log(`Processing ${data.all_aircraft.length} additional aircraft`);
                    data.all_aircraft.forEach(aircraft => {
                        if (!aircraft.path || aircraft.path.length === 0) {
                            console.log(`Skipping aircraft ${aircraft.callsign} - no path data`);
                            return;
                        }
                        
                        const lastPos = aircraft.path[aircraft.path.length - 1];
                        if (!lastPos || !lastPos.lat || !lastPos.lon) {
                            console.log(`Skipping aircraft ${aircraft.callsign} - invalid position`);
                            return;
                        }
                        
                        const heading = calculateHeading(aircraft.path);
                        const altitude = aircraft.current_alt || 0;
                        
                        // Add aircraft marker
                        const marker = L.marker([lastPos.lat, lastPos.lon], {
                            icon: createAircraftIcon(aircraft.type, aircraft.category, altitude, heading)
                        }).addTo(aircraftLayer);
                        
                        marker.bindPopup(`
                            <strong>${aircraft.callsign}</strong><br>
                            Type: ${aircraft.type || 'Unknown'}<br>
                            ${aircraft.current_alt ? `Altitude: ${aircraft.current_alt.toLocaleString()} ft<br>` : ''}
                            ${aircraft.current_speed ? `Speed: ${aircraft.current_speed} kts` : ''}
                        `);
                        
                        visibleAircraftCount++;
                        
                        // Add track if enabled
                        if (showTracks && aircraft.path.length > 1) {
                            const trackCoords = aircraft.path.map(p => [p.lat, p.lon]);
                            const altitudeColor = altitude < 5000 ? '#ff6600' : 
                                                 altitude < 15000 ? '#ffaa00' : 
                                                 altitude < 25000 ? '#00aa00' : '#0066ff';
                            
                            L.polyline(trackCoords, {
                                color: altitudeColor,
                                weight: 1,
                                opacity: 0.4,
                                dashArray: '2, 4'
                            }).addTo(trackLayer);
                        }
                    });
                }
                
                // Update visible aircraft count
                document.getElementById('visibleAircraft').textContent = visibleAircraftCount;
                
                // Auto-center on new patterns if enabled
                if (autoCenter && hasInitialized) {
                    if (data.circles.length > 0) {
                        const firstCircle = data.circles[0];
                        if (!previousCircles.has(firstCircle.hex_id)) {
                            map.setView([firstCircle.center_lat, firstCircle.center_lon], 12);
                        }
                    } else if (data.grids.length > 0) {
                        const firstGrid = data.grids[0];
                        if (!previousGrids.has(firstGrid.hex_id)) {
                            map.setView([firstGrid.center_lat, firstGrid.center_lon], 11);
                        }
                    }
                }
                
            } catch (error) {
                console.error('Error fetching patterns:', error);
            }
        }
        
        // Calculate approximate grid bounds from path
        function calculateGridBounds(grid) {
            if (!grid.path || grid.path.length < 2) {
                return [[grid.center_lat - 0.01, grid.center_lon - 0.01],
                        [grid.center_lat + 0.01, grid.center_lon + 0.01]];
            }
            
            const lats = grid.path.map(p => p.lat);
            const lons = grid.path.map(p => p.lon);
            const minLat = Math.min(...lats);
            const maxLat = Math.max(...lats);
            const minLon = Math.min(...lons);
            const maxLon = Math.max(...lons);
            
            return [[minLat, minLon], [maxLat, maxLon]];
        }
        
        // Add event listeners for controls
        document.getElementById('showAllAircraft').addEventListener('change', updatePatterns);
        document.getElementById('showTracks').addEventListener('change', updatePatterns);
        document.getElementById('showPatterns').addEventListener('change', (e) => {
            if (e.target.checked) {
                map.addLayer(circleLayer);
                map.addLayer(gridLayer);
                map.addLayer(pathLayer);
            } else {
                map.removeLayer(circleLayer);
                map.removeLayer(gridLayer);
                map.removeLayer(pathLayer);
            }
        });
        
        // Update every 5 seconds
        updatePatterns();
        setInterval(updatePatterns, 5000);
    </script>
</body>
</html>
'''

# HTML template for the history viewer
HISTORY_HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Pattern Detection History</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <script>
        // Aircraft icon shapes from tar1090 - embedded directly to avoid loading issues
        const aircraftShapes = {
            'airliner': {
                svg: '<path d="m 16,1 -1.5,1 -1,2 -2,3 v 6 l -5,2 v 1.5 l 5,-0.5 v 5.5 l -1.5,1.5 v 1 l 2,-0.5 0.5,-0.5 h 1 l 0.5,0.5 2,0.5 v -1 l -1.5,-1.5 v -5.5 l 5,0.5 v -1.5 l -5,-2 v -6 l -2,-3 -1,-2 z"/>',
                width: 32,
                height: 32,
                viewBox: '0 0 32 32',
                scale: 1.0
            },
            'helicopter': {
                svg: '<path d="m 16,3 c -0.5,0 -1,0.5 -1,1 v 2 h -6 v 1 h 14 v -1 h -6 v -2 c 0,-0.5 -0.5,-1 -1,-1 z m -1,5 v 8 l -3,1 v 1.5 l 3,-0.5 v 4 h 2 v -4 l 3,0.5 v -1.5 l -3,-1 v -8 z m -7,16 v 1 h 16 v -1 z"/>',
                width: 32,
                height: 32,
                viewBox: '0 0 32 32',
                scale: 1.0,
                noRotate: true
            },
            'default': {
                svg: '<path d="M 12 2 L 12 8 L 20 14 L 20 16 L 12 13 L 12 18 L 15 20 L 15 21 L 12 20 L 9 21 L 9 20 L 12 18 L 12 13 L 4 16 L 4 14 L 12 8 L 12 2 Z"/>',
                width: 24,
                height: 24,
                viewBox: '0 0 24 24',
                scale: 1.0
            }
        };
        
        // Function to get appropriate icon for aircraft
        function getAircraftIcon(typeDesignator, category) {
            // For now, return default icon - can expand this later
            return aircraftShapes['default'];
        }
    </script>
    <style>
        body {
            margin: 0;
            padding: 0;
            font-family: Arial, sans-serif;
            background: #f5f5f5;
        }
        .header {
            background: white;
            padding: 15px 30px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .header h1 {
            margin: 0;
            color: #333;
            font-size: 24px;
        }
        .nav-links {
            display: flex;
            gap: 20px;
        }
        .nav-links a {
            text-decoration: none;
            color: #007bff;
            padding: 8px 16px;
            border-radius: 4px;
            transition: background 0.3s;
        }
        .nav-links a:hover {
            background: #f0f0f0;
        }
        .nav-links a.active {
            background: #007bff;
            color: white;
        }
        .container {
            display: flex;
            height: calc(100vh - 70px);
        }
        .sidebar {
            width: 400px;
            background: white;
            padding: 20px;
            overflow-y: auto;
            box-shadow: 2px 0 5px rgba(0,0,0,0.1);
        }
        #map {
            flex: 1;
        }
        .filters {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
        }
        .filter-group {
            margin-bottom: 15px;
        }
        .filter-group label {
            display: block;
            font-weight: bold;
            margin-bottom: 5px;
            color: #555;
        }
        .filter-group input, .filter-group select {
            width: 100%;
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin-bottom: 20px;
        }
        .stat-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
        }
        .stat-card.circles {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        }
        .stat-card.grids {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        }
        .stat-value {
            font-size: 32px;
            font-weight: bold;
            margin-bottom: 5px;
        }
        .stat-label {
            font-size: 14px;
            opacity: 0.9;
        }
        .history-list {
            max-height: 500px;
            overflow-y: auto;
        }
        .history-item {
            background: white;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 10px;
            cursor: pointer;
            transition: all 0.3s;
        }
        .history-item:hover {
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            transform: translateY(-2px);
        }
        .history-item.circle {
            border-left: 4px solid #dc3545;
        }
        .history-item.grid {
            border-left: 4px solid #28a745;
        }
        .history-item-header {
            display: flex;
            justify-content: space-between;
            margin-bottom: 8px;
        }
        .history-item-callsign {
            font-weight: bold;
            font-size: 16px;
        }
        .history-item-time {
            color: #666;
            font-size: 12px;
        }
        .history-item-details {
            color: #555;
            font-size: 14px;
            line-height: 1.5;
        }
        .history-item-details a {
            display: inline-block;
            margin-top: 8px;
            padding: 4px 8px;
            background: #f0f7ff;
            border: 1px solid #007bff;
            border-radius: 4px;
            color: #007bff;
            text-decoration: none;
            transition: all 0.3s;
        }
        .history-item-details a:hover {
            background: #007bff;
            color: white;
        }
        .date-range {
            display: flex;
            gap: 10px;
            align-items: center;
        }
        .date-range input {
            flex: 1;
        }
        .btn-group {
            display: flex;
            gap: 10px;
            margin-top: 15px;
        }
        .btn {
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
            transition: background 0.3s;
        }
        .btn-primary {
            background: #007bff;
            color: white;
        }
        .btn-primary:hover {
            background: #0056b3;
        }
        .btn-secondary {
            background: #6c757d;
            color: white;
        }
        .btn-secondary:hover {
            background: #545b62;
        }
        .timeline-view {
            margin-top: 20px;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 8px;
        }
        .timeline-header {
            font-weight: bold;
            margin-bottom: 10px;
            color: #333;
        }
        .heatmap-legend {
            position: absolute;
            bottom: 20px;
            right: 20px;
            background: white;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
            z-index: 1000;
        }
        .heatmap-legend h4 {
            margin: 0 0 10px 0;
            font-size: 14px;
        }
        .legend-item {
            display: flex;
            align-items: center;
            margin: 5px 0;
        }
        .legend-color {
            width: 20px;
            height: 20px;
            border-radius: 3px;
            margin-right: 8px;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>✈️ Pattern Detection History</h1>
        <div class="nav-links">
            <a href="/">Live View</a>
            <a href="/history" class="active">History</a>
        </div>
    </div>
    
    <div class="container">
        <div class="sidebar">
            <div class="filters">
                <h3 style="margin-top: 0;">Filters</h3>
                <div class="filter-group">
                    <label>Date Range</label>
                    <div class="date-range">
                        <input type="date" id="startDate">
                        <span>to</span>
                        <input type="date" id="endDate">
                    </div>
                </div>
                <div class="filter-group">
                    <label>Pattern Type</label>
                    <select id="patternType">
                        <option value="all">All Patterns</option>
                        <option value="circles">Circles Only</option>
                        <option value="grids">Grids Only</option>
                    </select>
                </div>
                <div class="filter-group">
                    <label>Callsign Search</label>
                    <input type="text" id="callsignSearch" placeholder="Enter callsign...">
                </div>
                <div class="filter-group">
                    <label>Minimum Duration (minutes)</label>
                    <input type="number" id="minDuration" min="0" value="0" step="1">
                </div>
                <div class="btn-group">
                    <button class="btn btn-primary" onclick="applyFilters()">Apply Filters</button>
                    <button class="btn btn-secondary" onclick="resetFilters()">Reset</button>
                </div>
            </div>
            
            <div class="stats-grid">
                <div class="stat-card circles">
                    <div class="stat-value" id="totalCircles">0</div>
                    <div class="stat-label">Total Circles</div>
                </div>
                <div class="stat-card grids">
                    <div class="stat-value" id="totalGrids">0</div>
                    <div class="stat-label">Total Grids</div>
                </div>
            </div>
            
            <div class="timeline-view">
                <div class="timeline-header">Pattern Timeline</div>
                <canvas id="timeline" width="350" height="100"></canvas>
            </div>
            
            <h3>Detection History</h3>
            <div class="history-list" id="historyList">
                <!-- History items will be populated here -->
            </div>
        </div>
        
        <div id="map"></div>
    </div>
    
    <div class="heatmap-legend">
        <h4>Pattern Density</h4>
        <div class="legend-item">
            <div class="legend-color" style="background: rgba(255, 0, 0, 0.8);"></div>
            <span>High Activity</span>
        </div>
        <div class="legend-item">
            <div class="legend-color" style="background: rgba(255, 255, 0, 0.6);"></div>
            <span>Medium Activity</span>
        </div>
        <div class="legend-item">
            <div class="legend-color" style="background: rgba(0, 255, 0, 0.4);"></div>
            <span>Low Activity</span>
        </div>
    </div>

    <script>
        // Initialize map
        const map = L.map('map').setView([40.0, -95.0], 5);
        
        // Add OpenStreetMap tiles
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors'
        }).addTo(map);
        
        // Layer groups
        const circleLayer = L.layerGroup().addTo(map);
        const gridLayer = L.layerGroup().addTo(map);
        const heatmapLayer = L.layerGroup().addTo(map);
        
        // Store all history data
        let allCircles = [];
        let allGrids = [];
        let filteredCircles = [];
        let filteredGrids = [];
        
        // Set default dates (last 7 days)
        const today = new Date();
        const lastWeek = new Date(today.getTime() - 7 * 24 * 60 * 60 * 1000);
        document.getElementById('endDate').value = today.toISOString().split('T')[0];
        document.getElementById('startDate').value = lastWeek.toISOString().split('T')[0];
        
        // Load history data
        async function loadHistory() {
            try {
                const response = await fetch('/api/history');
                const data = await response.json();
                
                allCircles = data.circles || [];
                allGrids = data.grids || [];
                
                // Update stats
                document.getElementById('totalCircles').textContent = allCircles.length;
                document.getElementById('totalGrids').textContent = allGrids.length;
                
                // Apply initial filters
                applyFilters();
                
                // Draw timeline
                drawTimeline();
                
            } catch (error) {
                console.error('Error loading history:', error);
            }
        }
        
        // Apply filters to data
        function applyFilters() {
            const startDate = new Date(document.getElementById('startDate').value);
            const endDate = new Date(document.getElementById('endDate').value + 'T23:59:59');
            const patternType = document.getElementById('patternType').value;
            const callsignSearch = document.getElementById('callsignSearch').value.toLowerCase();
            const minDuration = parseInt(document.getElementById('minDuration').value) || 0;
            
            // Filter circles
            filteredCircles = allCircles.filter(circle => {
                const detected = new Date(circle.detected_at);
                const duration = (new Date(circle.last_seen) - detected) / 60000; // minutes
                
                return detected >= startDate && 
                       detected <= endDate && 
                       (patternType === 'all' || patternType === 'circles') &&
                       (!callsignSearch || circle.callsign.toLowerCase().includes(callsignSearch)) &&
                       duration >= minDuration;
            });
            
            // Filter grids
            filteredGrids = allGrids.filter(grid => {
                const detected = new Date(grid.detected_at);
                const duration = (new Date(grid.last_seen) - detected) / 60000; // minutes
                
                return detected >= startDate && 
                       detected <= endDate && 
                       (patternType === 'all' || patternType === 'grids') &&
                       (!callsignSearch || grid.callsign.toLowerCase().includes(callsignSearch)) &&
                       duration >= minDuration;
            });
            
            // Update display
            displayHistory();
            updateMap();
        }
        
        // Display filtered history in sidebar
        function displayHistory() {
            const historyList = document.getElementById('historyList');
            historyList.innerHTML = '';
            
            // Combine and sort by time
            const allPatterns = [
                ...filteredCircles.map(c => ({...c, type: 'circle'})),
                ...filteredGrids.map(g => ({...g, type: 'grid'}))
            ].sort((a, b) => new Date(b.detected_at) - new Date(a.detected_at));
            
            allPatterns.forEach(pattern => {
                const item = document.createElement('div');
                item.className = `history-item ${pattern.type}`;
                
                const detectedTime = new Date(pattern.detected_at).toLocaleString();
                const duration = ((new Date(pattern.last_seen) - new Date(pattern.detected_at)) / 60000).toFixed(1);
                
                if (pattern.type === 'circle') {
                    item.innerHTML = `
                        <div class="history-item-header">
                            <span class="history-item-callsign">🔴 ${pattern.callsign}</span>
                            <span class="history-item-time">${detectedTime}</span>
                        </div>
                        <div class="history-item-details">
                            Radius: ${pattern.radius.toFixed(1)} km<br>
                            Turns: ${pattern.turns.toFixed(1)}<br>
                            Duration: ${duration} min<br>
                            Max Alt: ${pattern.max_altitude?.toLocaleString() || 'N/A'} ft<br>
                            ${pattern.tar1090_url ? `<a href="${pattern.tar1090_url}" target="_blank" style="color: #007bff; text-decoration: none;">🔗 View in TAR1090</a>` : ''}
                        </div>
                    `;
                    
                    item.onclick = () => {
                        map.setView([pattern.center_lat, pattern.center_lon], 12);
                        showPatternDetails(pattern);
                    };
                } else {
                    item.innerHTML = `
                        <div class="history-item-header">
                            <span class="history-item-callsign">🟢 ${pattern.callsign}</span>
                            <span class="history-item-time">${detectedTime}</span>
                        </div>
                        <div class="history-item-details">
                            Type: ${pattern.pattern_type}<br>
                            Legs: ${pattern.num_legs}<br>
                            Coverage: ${pattern.coverage_area?.toFixed(1) || 'N/A'} km²<br>
                            Duration: ${duration} min<br>
                            ${pattern.tar1090_url ? `<a href="${pattern.tar1090_url}" target="_blank" style="color: #007bff; text-decoration: none;">🔗 View in TAR1090</a>` : ''}
                        </div>
                    `;
                    
                    item.onclick = () => {
                        map.setView([pattern.center_lat, pattern.center_lon], 11);
                        showPatternDetails(pattern);
                    };
                }
                
                historyList.appendChild(item);
            });
        }
        
        // Update map with filtered patterns
        function updateMap() {
            // Clear existing layers
            circleLayer.clearLayers();
            gridLayer.clearLayers();
            heatmapLayer.clearLayers();
            
            // Create heatmap data
            const heatmapPoints = [];
            
            // Add circles to map
            filteredCircles.forEach(circle => {
                const marker = L.circle([circle.center_lat, circle.center_lon], {
                    radius: circle.radius * 1000,
                    color: '#dc3545',
                    fillColor: '#dc3545',
                    fillOpacity: 0.2,
                    weight: 1
                }).addTo(circleLayer);
                
                marker.bindPopup(`
                    <strong>${circle.callsign}</strong><br>
                    Detected: ${new Date(circle.detected_at).toLocaleString()}<br>
                    Radius: ${circle.radius.toFixed(1)} km<br>
                    Turns: ${circle.turns.toFixed(1)}<br>
                    ${circle.tar1090_url ? `<a href="${circle.tar1090_url}" target="_blank">🔗 View in TAR1090</a>` : ''}
                `);
                
                heatmapPoints.push([circle.center_lat, circle.center_lon]);
            });
            
            // Add grids to map
            filteredGrids.forEach(grid => {
                // Create a simple rectangle for grid pattern
                const bounds = [[grid.center_lat - 0.05, grid.center_lon - 0.05],
                               [grid.center_lat + 0.05, grid.center_lon + 0.05]];
                
                const marker = L.rectangle(bounds, {
                    color: '#28a745',
                    fillColor: '#28a745',
                    fillOpacity: 0.1,
                    weight: 1
                }).addTo(gridLayer);
                
                marker.bindPopup(`
                    <strong>${grid.callsign}</strong><br>
                    Detected: ${new Date(grid.detected_at).toLocaleString()}<br>
                    Type: ${grid.pattern_type}<br>
                    Legs: ${grid.num_legs}<br>
                    ${grid.tar1090_url ? `<a href="${grid.tar1090_url}" target="_blank">🔗 View in TAR1090</a>` : ''}
                `);
                
                heatmapPoints.push([grid.center_lat, grid.center_lon]);
            });
            
            // Add density visualization if we have points
            if (heatmapPoints.length > 0 && typeof L.heatLayer !== 'undefined') {
                L.heatLayer(heatmapPoints, {
                    radius: 25,
                    blur: 15,
                    maxZoom: 10
                }).addTo(heatmapLayer);
            }
        }
        
        // Show detailed pattern information
        function showPatternDetails(pattern) {
            // This could open a modal or expand details
            console.log('Pattern details:', pattern);
        }
        
        // Draw timeline visualization
        function drawTimeline() {
            const canvas = document.getElementById('timeline');
            const ctx = canvas.getContext('2d');
            
            // Clear canvas
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            
            // Get date range
            const startDate = new Date(document.getElementById('startDate').value);
            const endDate = new Date(document.getElementById('endDate').value + 'T23:59:59');
            const dayRange = (endDate - startDate) / (24 * 60 * 60 * 1000);
            
            if (dayRange <= 0) return;
            
            // Count patterns per day
            const dailyCounts = {};
            
            [...allCircles, ...allGrids].forEach(pattern => {
                const date = new Date(pattern.detected_at).toISOString().split('T')[0];
                dailyCounts[date] = (dailyCounts[date] || 0) + 1;
            });
            
            // Draw bars
            const barWidth = canvas.width / dayRange;
            const maxCount = Math.max(...Object.values(dailyCounts), 1);
            
            for (let i = 0; i < dayRange; i++) {
                const date = new Date(startDate.getTime() + i * 24 * 60 * 60 * 1000);
                const dateStr = date.toISOString().split('T')[0];
                const count = dailyCounts[dateStr] || 0;
                
                const barHeight = (count / maxCount) * (canvas.height - 20);
                const x = i * barWidth;
                const y = canvas.height - barHeight - 10;
                
                // Draw bar
                ctx.fillStyle = count > 0 ? '#007bff' : '#e0e0e0';
                ctx.fillRect(x, y, barWidth - 1, barHeight);
                
                // Draw count if > 0
                if (count > 0) {
                    ctx.fillStyle = '#333';
                    ctx.font = '10px Arial';
                    ctx.textAlign = 'center';
                    ctx.fillText(count, x + barWidth/2, y - 2);
                }
            }
            
            // Draw axis
            ctx.strokeStyle = '#ccc';
            ctx.beginPath();
            ctx.moveTo(0, canvas.height - 10);
            ctx.lineTo(canvas.width, canvas.height - 10);
            ctx.stroke();
        }
        
        // Reset filters
        function resetFilters() {
            const today = new Date();
            const lastWeek = new Date(today.getTime() - 7 * 24 * 60 * 60 * 1000);
            
            document.getElementById('endDate').value = today.toISOString().split('T')[0];
            document.getElementById('startDate').value = lastWeek.toISOString().split('T')[0];
            document.getElementById('patternType').value = 'all';
            document.getElementById('callsignSearch').value = '';
            document.getElementById('minDuration').value = '0';
            
            applyFilters();
        }
        
        // Load data on page load
        loadHistory();
    </script>
</body>
</html>
'''

import requests
import json
import time
import math
import threading
from datetime import datetime, timedelta
from collections import defaultdict
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Tuple, Set
import argparse
import sys
import csv
from pathlib import Path
import os
import shutil
from flask import Flask, render_template_string, jsonify
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix
import webbrowser


@dataclass
class Position:
    lat: float
    lon: float
    timestamp: float
    altitude: Optional[int] = None
    speed: Optional[int] = None


@dataclass
class Aircraft:
    hex_id: str
    callsign: str
    path: List[Position]
    last_update: float
    type: Optional[str] = None
    category: Optional[str] = None


@dataclass
class CircleDetection:
    is_circling: bool
    center_lat: float
    center_lon: float
    radius: float
    turns: float


@dataclass
class GridDetection:
    is_grid_pattern: bool
    pattern_type: str  # 'parallel_lines', 'racetrack', 'survey'
    grid_bearing: float  # Main bearing of the grid lines
    line_spacing: float  # Average spacing between parallel lines in km
    num_legs: int  # Number of parallel legs detected
    coverage_area: float  # Approximate area covered in sq km
    center_lat: float
    center_lon: float


@dataclass
class CircleLog:
    """Log entry for a detected circle event."""
    timestamp: datetime
    hex_id: str
    callsign: str
    center_lat: float
    center_lon: float
    radius: float
    turns: float
    altitude: Optional[int]
    speed: Optional[int]
    duration: int  # seconds
    tar1090_url: str


@dataclass
class GridLog:
    """Log entry for a detected grid pattern event."""
    timestamp: datetime
    hex_id: str
    callsign: str
    pattern_type: str
    center_lat: float
    center_lon: float
    grid_bearing: float
    line_spacing: float
    num_legs: int
    coverage_area: float
    altitude: Optional[int]
    speed: Optional[int]
    duration: int  # seconds
    tar1090_url: str


class GridDetector:
    def __init__(self, min_legs=3, min_leg_length=2.0, max_turn_angle=45, time_window=600):
        self.min_legs = min_legs  # Minimum parallel legs for detection
        self.min_leg_length = min_leg_length  # Minimum leg length in km
        self.max_turn_angle = max_turn_angle  # Max angle deviation for parallel legs
        self.time_window = time_window  # seconds
    
    @staticmethod
    def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate distance between two lat/lng points using Haversine formula."""
        R = 6371  # Earth's radius in km
        
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lon = math.radians(lon2 - lon1)
        
        a = (math.sin(delta_lat / 2) * math.sin(delta_lat / 2) +
             math.cos(lat1_rad) * math.cos(lat2_rad) *
             math.sin(delta_lon / 2) * math.sin(delta_lon / 2))
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        return R * c
    
    @staticmethod
    def calculate_bearing(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate bearing between two points."""
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lon = math.radians(lon2 - lon1)
        
        y = math.sin(delta_lon) * math.cos(lat2_rad)
        x = (math.cos(lat1_rad) * math.sin(lat2_rad) -
             math.sin(lat1_rad) * math.cos(lat2_rad) * math.cos(delta_lon))
        
        bearing = math.atan2(y, x)
        return (math.degrees(bearing) + 360) % 360
    
    def detect_turns(self, path: List[Position]) -> List[Tuple[int, float, float]]:
        """Detect significant turns in the flight path.
        Returns list of (index, bearing_before, bearing_after) for each turn."""
        if len(path) < 5:
            return []
        
        turns = []
        window = 3  # Points to average for bearing calculation
        
        for i in range(window, len(path) - window):
            # Calculate bearing before turn
            bearing_before = self.calculate_bearing(
                path[i-window].lat, path[i-window].lon,
                path[i].lat, path[i].lon
            )
            
            # Calculate bearing after turn
            bearing_after = self.calculate_bearing(
                path[i].lat, path[i].lon,
                path[i+window].lat, path[i+window].lon
            )
            
            # Calculate turn angle
            turn_angle = abs(bearing_after - bearing_before)
            if turn_angle > 180:
                turn_angle = 360 - turn_angle
            
            # Detect significant turns (> 60 degrees)
            if turn_angle > 60:
                turns.append((i, bearing_before, bearing_after))
        
        return turns
    
    def identify_legs(self, path: List[Position], turns: List[Tuple[int, float, float]]) -> List[Tuple[int, int, float, float]]:
        """Identify straight legs between turns.
        Returns list of (start_idx, end_idx, bearing, length_km) for each leg."""
        if not turns:
            return []
        
        legs = []
        
        # Add leg from start to first turn if long enough
        if turns[0][0] > 5:
            start_idx = 0
            end_idx = turns[0][0]
            bearing = self.calculate_bearing(
                path[start_idx].lat, path[start_idx].lon,
                path[end_idx].lat, path[end_idx].lon
            )
            length = self.calculate_distance(
                path[start_idx].lat, path[start_idx].lon,
                path[end_idx].lat, path[end_idx].lon
            )
            if length >= self.min_leg_length:
                legs.append((start_idx, end_idx, bearing, length))
        
        # Add legs between turns
        for i in range(len(turns) - 1):
            start_idx = turns[i][0]
            end_idx = turns[i + 1][0]
            
            if end_idx - start_idx > 3:  # Need at least a few points
                bearing = self.calculate_bearing(
                    path[start_idx].lat, path[start_idx].lon,
                    path[end_idx].lat, path[end_idx].lon
                )
                length = self.calculate_distance(
                    path[start_idx].lat, path[start_idx].lon,
                    path[end_idx].lat, path[end_idx].lon
                )
                if length >= self.min_leg_length:
                    legs.append((start_idx, end_idx, bearing, length))
        
        # Add leg from last turn to end if long enough
        if len(path) - turns[-1][0] > 5:
            start_idx = turns[-1][0]
            end_idx = len(path) - 1
            bearing = self.calculate_bearing(
                path[start_idx].lat, path[start_idx].lon,
                path[end_idx].lat, path[end_idx].lon
            )
            length = self.calculate_distance(
                path[start_idx].lat, path[start_idx].lon,
                path[end_idx].lat, path[end_idx].lon
            )
            if length >= self.min_leg_length:
                legs.append((start_idx, end_idx, bearing, length))
        
        return legs
    
    def find_parallel_legs(self, legs: List[Tuple[int, int, float, float]]) -> List[List[int]]:
        """Group legs that are roughly parallel to each other."""
        if len(legs) < 2:
            return []
        
        parallel_groups = []
        
        # Group legs by similar bearing
        for i, (_, _, bearing1, _) in enumerate(legs):
            found_group = False
            
            for group in parallel_groups:
                # Check if this leg is parallel to the group
                group_bearing = legs[group[0]][2]
                
                # Check both forward and reverse bearings
                diff1 = abs(bearing1 - group_bearing)
                diff2 = abs(bearing1 - (group_bearing + 180) % 360)
                
                if diff1 > 180:
                    diff1 = 360 - diff1
                if diff2 > 180:
                    diff2 = 360 - diff2
                
                if min(diff1, diff2) <= self.max_turn_angle:
                    group.append(i)
                    found_group = True
                    break
            
            if not found_group:
                parallel_groups.append([i])
        
        # Filter groups with minimum legs
        return [g for g in parallel_groups if len(g) >= self.min_legs]
    
    def calculate_coverage_area(self, path: List[Position], legs: List[Tuple[int, int, float, float]]) -> float:
        """Estimate the area covered by the grid pattern."""
        if len(legs) < 2:
            return 0
        
        # Find bounding box
        lats = [p.lat for p in path]
        lons = [p.lon for p in path]
        
        min_lat, max_lat = min(lats), max(lats)
        min_lon, max_lon = min(lons), max(lons)
        
        # Approximate area calculation
        lat_dist = self.calculate_distance(min_lat, min_lon, max_lat, min_lon)
        lon_dist = self.calculate_distance(min_lat, min_lon, min_lat, max_lon)
        
        return lat_dist * lon_dist
    
    def detect_grid_pattern(self, flight_path: List[Position]) -> GridDetection:
        """Detect if an aircraft is flying a grid pattern."""
        if len(flight_path) < 20:
            return GridDetection(False, '', 0, 0, 0, 0, 0, 0)
        
        # Find turns in the path
        turns = self.detect_turns(flight_path)
        
        if len(turns) < 2:
            return GridDetection(False, '', 0, 0, 0, 0, 0, 0)
        
        # Identify straight legs
        legs = self.identify_legs(flight_path, turns)
        
        if len(legs) < self.min_legs:
            return GridDetection(False, '', 0, 0, 0, 0, 0, 0)
        
        # Find parallel leg groups
        parallel_groups = self.find_parallel_legs(legs)
        
        if not parallel_groups:
            return GridDetection(False, '', 0, 0, 0, 0, 0, 0)
        
        # Use the largest group of parallel legs
        largest_group = max(parallel_groups, key=len)
        
        if len(largest_group) < self.min_legs:
            return GridDetection(False, '', 0, 0, 0, 0, 0, 0)
        
        # Calculate grid characteristics
        group_legs = [legs[i] for i in largest_group]
        main_bearing = sum(leg[2] for leg in group_legs) / len(group_legs)
        
        # Calculate average spacing between parallel lines
        spacings = []
        for i in range(len(group_legs) - 1):
            leg1 = group_legs[i]
            leg2 = group_legs[i + 1]
            
            # Use midpoints of legs
            mid1_idx = (leg1[0] + leg1[1]) // 2
            mid2_idx = (leg2[0] + leg2[1]) // 2
            
            spacing = self.calculate_distance(
                flight_path[mid1_idx].lat, flight_path[mid1_idx].lon,
                flight_path[mid2_idx].lat, flight_path[mid2_idx].lon
            )
            spacings.append(spacing)
        
        avg_spacing = sum(spacings) / len(spacings) if spacings else 0
        
        # Calculate center point
        center_lat = sum(p.lat for p in flight_path) / len(flight_path)
        center_lon = sum(p.lon for p in flight_path) / len(flight_path)
        
        # Calculate coverage area
        coverage_area = self.calculate_coverage_area(flight_path, legs)
        
        # Determine pattern type
        if len(largest_group) >= 4 and avg_spacing < 2.0:
            pattern_type = 'survey'
        elif len(turns) > len(legs) * 1.5:
            pattern_type = 'racetrack'
        else:
            pattern_type = 'parallel_lines'
        
        return GridDetection(
            is_grid_pattern=True,
            pattern_type=pattern_type,
            grid_bearing=main_bearing,
            line_spacing=avg_spacing,
            num_legs=len(largest_group),
            coverage_area=coverage_area,
            center_lat=center_lat,
            center_lon=center_lon
        )


class CircleDetector:
    def __init__(self, min_radius=0.5, max_radius=10.0, min_turns=1.5, time_window=300):
        self.min_radius = min_radius  # km
        self.max_radius = max_radius  # km
        self.min_turns = min_turns  # number of complete turns
        self.time_window = time_window  # seconds
    
    @staticmethod
    def smooth_path(path: List[Position], window_size: int = 3) -> List[Position]:
        """Apply simple moving average smoothing to reduce noise."""
        if len(path) < window_size:
            return path
        
        smoothed = []
        for i in range(len(path)):
            start_idx = max(0, i - window_size // 2)
            end_idx = min(len(path), i + window_size // 2 + 1)
            window = path[start_idx:end_idx]
            
            # Average positions in window
            avg_lat = sum(p.lat for p in window) / len(window)
            avg_lon = sum(p.lon for p in window) / len(window)
            
            # Keep original timestamp and altitude from center point
            smoothed_pos = Position(
                lat=avg_lat,
                lon=avg_lon,
                timestamp=path[i].timestamp,
                altitude=path[i].altitude,
                speed=path[i].speed
            )
            smoothed.append(smoothed_pos)
        
        return smoothed

    @staticmethod
    def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate distance between two lat/lng points using Haversine formula."""
        R = 6371  # Earth's radius in km

        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lon = math.radians(lon2 - lon1)

        a = (math.sin(delta_lat / 2) * math.sin(delta_lat / 2) +
             math.cos(lat1_rad) * math.cos(lat2_rad) *
             math.sin(delta_lon / 2) * math.sin(delta_lon / 2))
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        return R * c

    @staticmethod
    def calculate_bearing(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate bearing between two points."""
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lon = math.radians(lon2 - lon1)

        y = math.sin(delta_lon) * math.cos(lat2_rad)
        x = (math.cos(lat1_rad) * math.sin(lat2_rad) -
             math.sin(lat1_rad) * math.cos(lat2_rad) * math.cos(delta_lon))

        bearing = math.atan2(y, x)
        return (math.degrees(bearing) + 360) % 360

    def detect_circling(self, flight_path: List[Position]) -> CircleDetection:
        """Detect if an aircraft is performing circular flight patterns."""
        if len(flight_path) < 10:
            return CircleDetection(False, 0, 0, 0, 0)
        
        # Apply smoothing to reduce noise in circle detection
        # Only smooth for detection, keep original path for display
        smoothed_path = self.smooth_path(flight_path)

        # Calculate center point (average of all positions)
        # Use smoothed path for center calculation
        center_lat = sum(p.lat for p in smoothed_path) / len(smoothed_path)
        center_lon = sum(p.lon for p in smoothed_path) / len(smoothed_path)

        # Calculate distances from center using smoothed path
        distances = [
            self.calculate_distance(center_lat, center_lon, p.lat, p.lon)
            for p in smoothed_path
        ]
        avg_distance = sum(distances) / len(distances)
        
        # Calculate standard deviation to check consistency
        std_dev = (sum((d - avg_distance) ** 2 for d in distances) / len(distances)) ** 0.5
        
        # If path is too erratic (high std dev), it's probably not a real circle
        if std_dev > avg_distance * 0.5:  # More than 50% deviation
            return CircleDetection(False, center_lat, center_lon, avg_distance, 0)

        # Check if average distance is within our radius range
        if avg_distance < self.min_radius or avg_distance > self.max_radius:
            return CircleDetection(False, center_lat, center_lon, avg_distance, 0)

        # Calculate bearings from center for each point (use smoothed path)
        bearings = [
            self.calculate_bearing(center_lat, center_lon, p.lat, p.lon)
            for p in smoothed_path
        ]

        # Count direction changes to estimate turns
        total_turn = 0
        for i in range(1, len(bearings)):
            diff = bearings[i] - bearings[i - 1]
            if diff > 180:
                diff -= 360
            elif diff < -180:
                diff += 360
            total_turn += abs(diff)

        complete_turns = total_turn / 360
        is_circling = complete_turns >= self.min_turns

        return CircleDetection(is_circling, center_lat, center_lon, avg_distance, complete_turns)


class TAR1090Monitor:
    def __init__(self, server_url: str, update_interval: int = 5):
        self.server_url = server_url.rstrip('/')
        self.update_interval = update_interval
        self.aircraft: Dict[str, Aircraft] = {}
        self.detector = CircleDetector()
        self.grid_detector = GridDetector()
        self.running = False
        self.session = requests.Session()
        self.session.timeout = 10
        
        # Data quality settings
        self.max_speed_kmh = 1000  # Max realistic speed in km/h (about 540 knots)
        self.max_position_jump_km = 5.0  # Max distance jump between updates
        self.min_update_interval = 0.5  # Min seconds between position updates

        # Statistics
        self.total_requests = 0
        self.failed_requests = 0
        self.last_update = None
        
        # Logging
        self.circle_logs: List[CircleLog] = []
        self.grid_logs: List[GridLog] = []
        self.active_circles: Set[str] = set()  # Track aircraft currently circling
        self.active_grids: Set[str] = set()  # Track aircraft currently in grid patterns
        self.circle_start_times: Dict[str, float] = {}  # Track when circling started
        self.grid_start_times: Dict[str, float] = {}  # Track when grid pattern started
        self.log_file = Path("circle_detections.csv")
        self.grid_log_file = Path("grid_detections.csv")
        self.tar1090_base_url = "https://radar.hallgren.net/map"
        
        # Display settings
        self.terminal_size = shutil.get_terminal_size((80, 24))
        self.max_display_lines = self.terminal_size.lines - 5  # Leave room for header/footer
        self.compact_mode = False
        self.no_clear = False
        self.last_alert_time = 0
        self.recent_alerts = []  # Store recent alerts for display
        
        # Track filtered positions for statistics
        self.positions_filtered = 0
        self.positions_accepted = 0
        
        # Web server
        self.web_app = None
        self.web_thread = None

    def validate_position(self, aircraft: Aircraft, new_pos: Position) -> bool:
        """Validate if a new position is realistic based on physics and data quality."""
        if not aircraft.path:
            return True  # First position is always valid
        
        last_pos = aircraft.path[-1]
        time_diff = new_pos.timestamp - last_pos.timestamp
        
        # Skip if update is too frequent (likely duplicate or noise)
        if time_diff < self.min_update_interval:
            return False
        
        # Calculate distance
        distance = self.detector.calculate_distance(
            last_pos.lat, last_pos.lon,
            new_pos.lat, new_pos.lon
        )
        
        # Check for unrealistic jumps
        if distance > self.max_position_jump_km:
            # Could be teleportation/bad data
            return False
        
        # Check speed if we have time difference
        if time_diff > 0:
            speed_kmh = (distance / time_diff) * 3600  # km/h
            if speed_kmh > self.max_speed_kmh:
                return False
        
        # Additional validation: altitude changes
        if last_pos.altitude is not None and new_pos.altitude is not None:
            try:
                last_alt = float(last_pos.altitude) if isinstance(last_pos.altitude, (int, str)) else last_pos.altitude
                new_alt = float(new_pos.altitude) if isinstance(new_pos.altitude, (int, str)) else new_pos.altitude
                alt_change_rate = abs(new_alt - last_alt) / max(time_diff, 1)
                # Max climb/descent rate: 6000 fpm = 30.48 m/s = 100 ft/s
                if alt_change_rate > 100:  # ft/s
                    return False
            except (ValueError, TypeError):
                # If altitude can't be converted to float, skip this check
                pass
        
        return True
    
    def fetch_aircraft_data(self) -> bool:
        """Fetch aircraft data from TAR1090 server."""
        try:
            url = f"{self.server_url}/data/aircraft.json"
            response = self.session.get(url)
            response.raise_for_status()

            data = response.json()
            self.total_requests += 1
            self.last_update = datetime.now()

            current_time = time.time()

            # Process aircraft data
            if 'aircraft' in data:
                active_hex_ids = set()

                for ac_data in data['aircraft']:
                    if not ac_data.get('hex') or ac_data.get('lat') is None or ac_data.get('lon') is None:
                        continue

                    hex_id = ac_data['hex']
                    active_hex_ids.add(hex_id)

                    # Create or update aircraft
                    if hex_id not in self.aircraft:
                        self.aircraft[hex_id] = Aircraft(
                            hex_id=hex_id,
                            callsign=ac_data.get('flight', hex_id).strip(),
                            path=[],
                            last_update=current_time,
                            type=ac_data.get('t'),
                            category=ac_data.get('category')
                        )

                    aircraft = self.aircraft[hex_id]
                    aircraft.callsign = ac_data.get('flight', hex_id).strip()
                    aircraft.last_update = current_time
                    aircraft.type = ac_data.get('t')
                    aircraft.category = ac_data.get('category')

                    # Add new position if different from last
                    # Ensure altitude and speed are integers/floats, not strings
                    altitude = ac_data.get('alt_baro') or ac_data.get('alt_geom')
                    if altitude is not None:
                        try:
                            altitude = float(altitude)
                        except (ValueError, TypeError):
                            altitude = None
                    
                    speed = ac_data.get('gs')
                    if speed is not None:
                        try:
                            speed = float(speed)
                        except (ValueError, TypeError):
                            speed = None
                    
                    new_pos = Position(
                        lat=float(ac_data['lat']),
                        lon=float(ac_data['lon']),
                        timestamp=current_time,
                        altitude=altitude,
                        speed=speed
                    )

                    # Only add if position changed and is valid
                    if not aircraft.path or (aircraft.path[-1].lat != new_pos.lat or
                                             aircraft.path[-1].lon != new_pos.lon):
                        if self.validate_position(aircraft, new_pos):
                            aircraft.path.append(new_pos)
                            self.positions_accepted += 1
                        else:
                            self.positions_filtered += 1

                    # Remove old positions outside time window
                    cutoff_time = current_time - self.detector.time_window
                    aircraft.path = [p for p in aircraft.path if p.timestamp >= cutoff_time]

                # Remove aircraft not seen recently
                cutoff_time = current_time - self.detector.time_window
                self.aircraft = {
                    hex_id: aircraft for hex_id, aircraft in self.aircraft.items()
                    if aircraft.last_update >= cutoff_time
                }

            return True

        except requests.exceptions.RequestException as e:
            self.failed_requests += 1
            print(f"Error fetching data: {e}")
            return False
        except json.JSONDecodeError as e:
            self.failed_requests += 1
            print(f"Error parsing JSON: {e}")
            return False
        except Exception as e:
            self.failed_requests += 1
            print(f"Unexpected error: {e}")
            return False

    def get_circling_aircraft(self) -> List[Tuple[Aircraft, CircleDetection]]:
        """Get list of aircraft currently performing circles."""
        circling = []

        for aircraft in self.aircraft.values():
            if len(aircraft.path) >= 10:  # Need sufficient data points
                detection = self.detector.detect_circling(aircraft.path)
                if detection.is_circling:
                    circling.append((aircraft, detection))

        return circling
    
    def get_grid_aircraft(self) -> List[Tuple[Aircraft, GridDetection]]:
        """Get list of aircraft currently flying grid patterns."""
        grid_aircraft = []
        
        for aircraft in self.aircraft.values():
            if len(aircraft.path) >= 20:  # Need more data for grid detection
                detection = self.grid_detector.detect_grid_pattern(aircraft.path)
                if detection.is_grid_pattern:
                    grid_aircraft.append((aircraft, detection))
        
        return grid_aircraft
    
    def generate_tar1090_url(self, aircraft: Aircraft, detection) -> str:
        """Generate a direct link to the aircraft on TAR1090."""
        # Format: https://radar.hallgren.net/map/?icao=hex_id&lat=center_lat&lon=center_lon&zoom=13
        return (f"{self.tar1090_base_url}/?icao={aircraft.hex_id}"
                f"&lat={detection.center_lat:.4f}&lon={detection.center_lon:.4f}&zoom=13")
    
    def log_grid_detection(self, aircraft: Aircraft, detection: GridDetection):
        """Log a new grid pattern detection event."""
        current_time = time.time()
        
        # Check if this is a new grid detection
        if aircraft.hex_id not in self.active_grids:
            self.active_grids.add(aircraft.hex_id)
            self.grid_start_times[aircraft.hex_id] = current_time
            
            # Calculate duration if we have start time
            duration = 0
            if aircraft.path:
                duration = int(current_time - aircraft.path[0].timestamp)
            
            # Get current position data
            current_pos = aircraft.path[-1] if aircraft.path else None
            
            # Create log entry
            log_entry = GridLog(
                timestamp=datetime.now(),
                hex_id=aircraft.hex_id,
                callsign=aircraft.callsign,
                pattern_type=detection.pattern_type,
                center_lat=detection.center_lat,
                center_lon=detection.center_lon,
                grid_bearing=detection.grid_bearing,
                line_spacing=detection.line_spacing,
                num_legs=detection.num_legs,
                coverage_area=detection.coverage_area,
                altitude=current_pos.altitude if current_pos else None,
                speed=current_pos.speed if current_pos else None,
                duration=duration,
                tar1090_url=self.generate_tar1090_url(aircraft, detection)
            )
            
            self.grid_logs.append(log_entry)
            self.save_grid_log_to_file(log_entry)
            
            # Store alert for display
            alert_msg = f"📐 NEW GRID: {aircraft.callsign} - {detection.pattern_type}, {detection.num_legs} legs, {detection.coverage_area:.1f}km²"
            self.recent_alerts.append((datetime.now(), alert_msg, log_entry.tar1090_url))
            # Keep only last 5 alerts
            self.recent_alerts = self.recent_alerts[-5:]
            self.last_alert_time = current_time
    
    def log_circle_detection(self, aircraft: Aircraft, detection: CircleDetection):
        """Log a new circle detection event."""
        current_time = time.time()
        
        # Check if this is a new circle detection
        if aircraft.hex_id not in self.active_circles:
            self.active_circles.add(aircraft.hex_id)
            self.circle_start_times[aircraft.hex_id] = current_time
            
            # Calculate duration if we have start time
            duration = 0
            if aircraft.path:
                duration = int(current_time - aircraft.path[0].timestamp)
            
            # Get current position data
            current_pos = aircraft.path[-1] if aircraft.path else None
            
            # Create log entry
            log_entry = CircleLog(
                timestamp=datetime.now(),
                hex_id=aircraft.hex_id,
                callsign=aircraft.callsign,
                center_lat=detection.center_lat,
                center_lon=detection.center_lon,
                radius=detection.radius,
                turns=detection.turns,
                altitude=current_pos.altitude if current_pos else None,
                speed=current_pos.speed if current_pos else None,
                duration=duration,
                tar1090_url=self.generate_tar1090_url(aircraft, detection)
            )
            
            self.circle_logs.append(log_entry)
            self.save_log_to_file(log_entry)
            
            # Store alert for display
            alert_msg = f"🚨 NEW: {aircraft.callsign} - {detection.radius:.1f}km circle, {detection.turns:.1f} turns"
            self.recent_alerts.append((datetime.now(), alert_msg, log_entry.tar1090_url))
            # Keep only last 5 alerts
            self.recent_alerts = self.recent_alerts[-5:]
            self.last_alert_time = current_time
    
    def update_circle_tracking(self):
        """Update tracking of which aircraft are circling."""
        current_circling = set()
        
        for aircraft, detection in self.get_circling_aircraft():
            current_circling.add(aircraft.hex_id)
            self.log_circle_detection(aircraft, detection)
        
        # Remove aircraft that stopped circling
        stopped_circling = self.active_circles - current_circling
        for hex_id in stopped_circling:
            if hex_id in self.circle_start_times:
                duration = int(time.time() - self.circle_start_times[hex_id])
                aircraft = self.aircraft.get(hex_id)
                if aircraft:
                    print(f"✅ {aircraft.callsign} stopped circling after {duration}s")
                del self.circle_start_times[hex_id]
        
        self.active_circles = current_circling
    
    def update_grid_tracking(self):
        """Update tracking of which aircraft are flying grid patterns."""
        current_grids = set()
        
        for aircraft, detection in self.get_grid_aircraft():
            current_grids.add(aircraft.hex_id)
            self.log_grid_detection(aircraft, detection)
        
        # Remove aircraft that stopped grid patterns
        stopped_grids = self.active_grids - current_grids
        for hex_id in stopped_grids:
            if hex_id in self.grid_start_times:
                duration = int(time.time() - self.grid_start_times[hex_id])
                aircraft = self.aircraft.get(hex_id)
                if aircraft:
                    print(f"✅ {aircraft.callsign} stopped grid pattern after {duration}s")
                del self.grid_start_times[hex_id]
        
        self.active_grids = current_grids
    
    def save_log_to_file(self, log_entry: CircleLog):
        """Save a log entry to CSV file."""
        file_exists = self.log_file.exists()
        
        with open(self.log_file, 'a', newline='') as f:
            fieldnames = ['timestamp', 'hex_id', 'callsign', 'center_lat', 'center_lon', 
                         'radius_km', 'turns', 'altitude_ft', 'speed_kts', 'duration_s', 'tar1090_url']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            
            if not file_exists:
                writer.writeheader()
            
            writer.writerow({
                'timestamp': log_entry.timestamp.isoformat(),
                'hex_id': log_entry.hex_id,
                'callsign': log_entry.callsign,
                'center_lat': f"{log_entry.center_lat:.6f}",
                'center_lon': f"{log_entry.center_lon:.6f}",
                'radius_km': f"{log_entry.radius:.2f}",
                'turns': f"{log_entry.turns:.2f}",
                'altitude_ft': log_entry.altitude if log_entry.altitude else '',
                'speed_kts': log_entry.speed if log_entry.speed else '',
                'duration_s': log_entry.duration,
                'tar1090_url': log_entry.tar1090_url
            })
    
    def save_grid_log_to_file(self, log_entry: GridLog):
        """Save a grid log entry to CSV file."""
        file_exists = self.grid_log_file.exists()
        
        with open(self.grid_log_file, 'a', newline='') as f:
            fieldnames = ['timestamp', 'hex_id', 'callsign', 'pattern_type', 'center_lat', 'center_lon',
                         'grid_bearing', 'line_spacing_km', 'num_legs', 'coverage_area_km2', 
                         'altitude_ft', 'speed_kts', 'duration_s', 'tar1090_url']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            
            if not file_exists:
                writer.writeheader()
            
            writer.writerow({
                'timestamp': log_entry.timestamp.isoformat(),
                'hex_id': log_entry.hex_id,
                'callsign': log_entry.callsign,
                'pattern_type': log_entry.pattern_type,
                'center_lat': f"{log_entry.center_lat:.6f}",
                'center_lon': f"{log_entry.center_lon:.6f}",
                'grid_bearing': f"{log_entry.grid_bearing:.1f}",
                'line_spacing_km': f"{log_entry.line_spacing:.2f}",
                'num_legs': log_entry.num_legs,
                'coverage_area_km2': f"{log_entry.coverage_area:.2f}",
                'altitude_ft': log_entry.altitude if log_entry.altitude else '',
                'speed_kts': log_entry.speed if log_entry.speed else '',
                'duration_s': log_entry.duration,
                'tar1090_url': log_entry.tar1090_url
            })
    
    def print_log_summary(self):
        """Print a summary of all logged circle detections."""
        if not self.circle_logs:
            print("📋 No circle detections logged yet.")
            return
        
        print("\n📋 CIRCLE DETECTION LOG")
        print("=" * 80)
        print(f"Total detections: {len(self.circle_logs)}")
        print(f"Log file: {self.log_file.absolute()}")
        print("\nRecent detections (last 10):")
        print("-" * 80)
        
        for log in self.circle_logs[-10:]:
            print(f"\n{log.timestamp.strftime('%Y-%m-%d %H:%M:%S')} - {log.callsign} ({log.hex_id})")
            print(f"   ⭕ {log.radius:.1f}km radius, {log.turns:.1f} turns")
            if log.altitude:
                print(f"   ✈️  {log.altitude:,} ft")
            print(f"   🔗 {log.tar1090_url}")
        
        if len(self.circle_logs) > 10:
            print(f"\n... and {len(self.circle_logs) - 10} more detections in the log file")

    def clear_screen(self):
        """Clear the terminal screen."""
        if not self.no_clear:
            if os.name == 'nt':  # Windows
                os.system('cls')
            else:  # Unix/Linux/Mac
                print("\033[2J\033[H", end="", flush=True)
    
    def print_compact_status(self, circling_aircraft):
        """Print a compact single-line status."""
        current_time = time.time()
        status_parts = []
        
        if self.last_update:
            status_parts.append(f"📡 {len(self.aircraft)} aircraft")
        
        if circling_aircraft:
            status_parts.append(f"🔄 {len(circling_aircraft)} circling")
            # Show first circling aircraft
            aircraft, detection = circling_aircraft[0]
            status_parts.append(f"[{aircraft.callsign}: {detection.radius:.1f}km]")
        else:
            status_parts.append("🔍 Monitoring...")
        
        # Add timestamp
        timestamp = datetime.now().strftime('%H:%M:%S')
        status_line = f"[{timestamp}] " + " | ".join(status_parts)
        
        # Truncate if too long
        max_width = self.terminal_size.columns - 1
        if len(status_line) > max_width:
            status_line = status_line[:max_width-3] + "..."
        
        print(f"\r{status_line}", end="", flush=True)

    def print_status(self, show_all_aircraft=False, quiet_mode=False):
        """Print current monitoring status with user-friendly output."""
        circling_aircraft = self.get_circling_aircraft()
        grid_aircraft = self.get_grid_aircraft()
        current_time = time.time()
        
        # Calculate filter rate
        total_positions = self.positions_accepted + self.positions_filtered
        filter_rate = (self.positions_filtered / total_positions * 100) if total_positions > 0 else 0
        
        # In compact mode, just update the status line
        if self.compact_mode:
            self.print_compact_status(circling_aircraft)
            return

        # Categorize aircraft for better summary
        aircraft_with_data = [ac for ac in self.aircraft.values() if len(ac.path) >= 3]
        recent_aircraft = [ac for ac in self.aircraft.values() if current_time - ac.last_update < 60]

        # Build output buffer
        output_lines = []
        
        # Header
        output_lines.append("✈️  TAR1090 AIRCRAFT CIRCLE DETECTOR")
        output_lines.append("=" * min(60, self.terminal_size.columns))

        # Status summary
        try:
            time_since_update = (datetime.now() - self.last_update).total_seconds() if self.last_update else float('inf')
            status_color = "🟢" if time_since_update < 30 else "🔴"
        except Exception:
            status_color = "🔴"
        output_lines.append(f"{status_color} Status: {'ACTIVE' if self.last_update else 'DISCONNECTED'} | ⏰ {self.last_update.strftime('%H:%M:%S') if self.last_update else 'Never'}")
        output_lines.append(f"📡 Aircraft: {len(self.aircraft)} total | {len(recent_aircraft)} active | {len(aircraft_with_data)} tracked")
        if total_positions > 100:  # Only show after enough data
            output_lines.append(f"🔧 Data Quality: {filter_rate:.1f}% positions filtered (noise reduction)")
        
        # Recent alerts (if any)
        if self.recent_alerts and not quiet_mode:
            output_lines.append("")
            output_lines.append("📢 Recent Alerts:")
            for alert_time, msg, url in self.recent_alerts[-3:]:  # Show last 3
                output_lines.append(f"  {alert_time.strftime('%H:%M:%S')} {msg}")
                if len(output_lines) < self.max_display_lines - 10:  # Only show URL if space
                    output_lines.append(f"           🔗 {url}")
        
        # Circling aircraft
        if circling_aircraft:
            output_lines.append("")
            output_lines.append(f"🔄 CIRCLING NOW ({len(circling_aircraft)} aircraft):")
            output_lines.append("-" * min(60, self.terminal_size.columns))
            
            # Limit display to avoid overflow
            max_circle_display = min(3, (self.max_display_lines - len(output_lines) - 10) // 4)
            for i, (aircraft, detection) in enumerate(circling_aircraft[:max_circle_display], 1):
                current_pos = aircraft.path[-1] if aircraft.path else None
                alt_str = f" @ {current_pos.altitude:,}ft" if current_pos and current_pos.altitude else ""
                
                # Compact format
                output_lines.append(f"{i}. {aircraft.callsign} - {detection.radius:.1f}km radius, {detection.turns:.1f} turns{alt_str}")
                if not quiet_mode:
                    output_lines.append(f"   🔗 {self.generate_tar1090_url(aircraft, detection)}")
            
            if len(circling_aircraft) > max_circle_display:
                output_lines.append(f"   ... and {len(circling_aircraft) - max_circle_display} more circling")
        
        # Grid patterns
        if grid_aircraft:
            output_lines.append("")
            output_lines.append(f"📐 GRID PATTERNS ({len(grid_aircraft)} aircraft):")
            output_lines.append("-" * min(60, self.terminal_size.columns))
            
            # Limit display
            max_grid_display = min(3, (self.max_display_lines - len(output_lines) - 5) // 4)
            for i, (aircraft, detection) in enumerate(grid_aircraft[:max_grid_display], 1):
                current_pos = aircraft.path[-1] if aircraft.path else None
                alt_str = f" @ {current_pos.altitude:,}ft" if current_pos and current_pos.altitude else ""
                
                # Compact format
                output_lines.append(f"{i}. {aircraft.callsign} - {detection.pattern_type}: {detection.num_legs} legs, {detection.coverage_area:.1f}km²{alt_str}")
                if not quiet_mode:
                    output_lines.append(f"   🔗 {self.generate_tar1090_url(aircraft, detection)}")
            
            if len(grid_aircraft) > max_grid_display:
                output_lines.append(f"   ... and {len(grid_aircraft) - max_grid_display} more in grid patterns")
        
        if not circling_aircraft and not grid_aircraft:
            output_lines.append("")
            output_lines.append(f"🔍 No patterns detected | Monitoring {len(aircraft_with_data)} aircraft with tracks")
        
        # Footer
        output_lines.append("")
        output_lines.append("-" * min(60, self.terminal_size.columns))
        output_lines.append("[Ctrl+C: Exit] [--compact: Minimal] [--no-clear: Keep history]")
        
        # Clear screen and print
        self.clear_screen()
        
        # Print only what fits on screen
        for line in output_lines[:self.max_display_lines]:
            print(line)
        
        # If in quiet mode, only show alerts
        if quiet_mode:
            self.clear_screen()
            if circling_aircraft:
                print(f"🔄 [{datetime.now().strftime('%H:%M:%S')}] {len(circling_aircraft)} aircraft circling:")
                for aircraft, detection in circling_aircraft[:3]:
                    print(f"  • {aircraft.callsign}: {detection.radius:.1f}km @ {detection.turns:.1f} turns")
            else:
                print(f"🔍 [{datetime.now().strftime('%H:%M:%S')}] Monitoring {len(self.aircraft)} aircraft...")

    def get_pattern_data_json(self, include_all_aircraft=True, max_track_points=50):
        """Get current pattern data as JSON for the web viewer."""
        data = {
            'timestamp': datetime.now().isoformat(),
            'circles': [],
            'grids': [],
            'all_aircraft': [],
            'aircraft_count': len(self.aircraft),
            'server_url': self.server_url
        }
        
        # Add circling aircraft
        for aircraft, detection in self.get_circling_aircraft():
            circle_data = {
                'hex_id': aircraft.hex_id,
                'callsign': aircraft.callsign,
                'center_lat': detection.center_lat,
                'center_lon': detection.center_lon,
                'radius': detection.radius,
                'turns': detection.turns,
                'path': [
                    {'lat': p.lat, 'lon': p.lon, 'alt': p.altitude, 'time': p.timestamp}
                    for p in aircraft.path
                ],
                'current_alt': aircraft.path[-1].altitude if aircraft.path else None,
                'current_speed': aircraft.path[-1].speed if aircraft.path else None,
                'type': aircraft.type,
                'category': aircraft.category
            }
            data['circles'].append(circle_data)
        
        # Add grid aircraft
        for aircraft, detection in self.get_grid_aircraft():
            grid_data = {
                'hex_id': aircraft.hex_id,
                'callsign': aircraft.callsign,
                'pattern_type': detection.pattern_type,
                'center_lat': detection.center_lat,
                'center_lon': detection.center_lon,
                'grid_bearing': detection.grid_bearing,
                'line_spacing': detection.line_spacing,
                'num_legs': detection.num_legs,
                'coverage_area': detection.coverage_area,
                'path': [
                    {'lat': p.lat, 'lon': p.lon, 'alt': p.altitude, 'time': p.timestamp}
                    for p in aircraft.path
                ],
                'current_alt': aircraft.path[-1].altitude if aircraft.path else None,
                'current_speed': aircraft.path[-1].speed if aircraft.path else None,
                'type': aircraft.type,
                'category': aircraft.category
            }
            data['grids'].append(grid_data)
        
        # Add all aircraft if requested
        if include_all_aircraft:
            # Get hex IDs of aircraft already in patterns
            pattern_aircraft = set()
            for circle in data['circles']:
                pattern_aircraft.add(circle['hex_id'])
            for grid in data['grids']:
                pattern_aircraft.add(grid['hex_id'])
            
            # Add all other aircraft
            for hex_id, aircraft in self.aircraft.items():
                if hex_id not in pattern_aircraft and aircraft.path:
                    # Limit track points for performance
                    track_points = aircraft.path[-max_track_points:] if len(aircraft.path) > max_track_points else aircraft.path
                    
                    aircraft_data = {
                        'hex_id': aircraft.hex_id,
                        'callsign': aircraft.callsign,
                        'path': [
                            {'lat': p.lat, 'lon': p.lon, 'alt': p.altitude, 'time': p.timestamp}
                            for p in track_points
                        ],
                        'current_alt': aircraft.path[-1].altitude if aircraft.path else None,
                        'current_speed': aircraft.path[-1].speed if aircraft.path else None,
                        'type': aircraft.type,
                        'category': aircraft.category,
                        'in_pattern': False
                    }
                    data['all_aircraft'].append(aircraft_data)
        
        return data
    
    def start_web_server(self, port=8888):
        """Start a Flask web server to serve the map viewer."""
        # Determine static folder path - check for Docker environment first
        import os
        if os.path.exists('/app/static'):
            static_folder = '/app/static'
        elif os.path.exists('./rootfs/app/static'):
            static_folder = './rootfs/app/static'
        else:
            static_folder = None
            
        app = Flask(__name__, static_folder=static_folder)
        
        # Configure for reverse proxy - handles X-Forwarded-* headers
        # This allows the app to work correctly behind docker-reversewebproxy
        app.wsgi_app = ProxyFix(
            app.wsgi_app,
            x_for=1,      # Trust X-Forwarded-For header for client IP
            x_proto=1,    # Trust X-Forwarded-Proto for HTTP/HTTPS
            x_host=1,     # Trust X-Forwarded-Host for original host
            x_prefix=1    # Trust X-Forwarded-Prefix for URL prefix
        )
        
        CORS(app)
        self.web_app = app
        
        @app.route('/')
        def index():
            return render_template_string(MAP_HTML_TEMPLATE)
        
        @app.route('/static/<path:path>')
        def send_static(path):
            return app.send_static_file(path)
        
        @app.route('/api/patterns')
        def get_patterns():
            return jsonify(self.get_pattern_data_json())
        
        @app.route('/api/health')
        def health_check():
            """Health check endpoint for monitoring."""
            # Count active patterns
            circling_count = len(self.get_circling_aircraft())
            grid_count = len(self.get_grid_aircraft())
            
            health_status = {
                'status': 'healthy',
                'timestamp': time.time(),
                'checks': {
                    'web_server': True,
                    'tar1090_connection': self.last_update is not None,
                    'last_update': self.last_update.timestamp() if self.last_update else 0,
                    'aircraft_count': len(self.aircraft),
                    'active_circles': circling_count,
                    'active_grids': grid_count,
                    'total_requests': self.total_requests,
                    'failed_requests': self.failed_requests
                }
            }
            
            # Check if we haven't received updates in a while (5 minutes)
            if self.last_update and (time.time() - self.last_update.timestamp()) > 300:
                health_status['status'] = 'degraded'
                health_status['checks']['tar1090_connection'] = False
            
            # Check if too many requests are failing
            if self.total_requests > 10 and (self.failed_requests / self.total_requests) > 0.5:
                health_status['status'] = 'degraded'
                health_status['checks']['high_failure_rate'] = True
            
            return jsonify(health_status)
        
        @app.route('/history')
        def history():
            return render_template_string(HISTORY_HTML_TEMPLATE)
        
        @app.route('/api/history')
        def get_history():
            """Get historical pattern data from CSV files."""
            history_data = {
                'circles': [],
                'grids': []
            }
            
            print(f"Reading history from {self.log_file} and {self.grid_log_file}")
            
            # Read circle detections
            if self.log_file.exists():
                try:
                    with open(self.log_file, 'r') as f:
                        reader = csv.DictReader(f)
                        for row in reader:
                            try:
                                # Map CSV columns to expected fields
                                # The CSV uses different column names than what we expect
                                history_data['circles'].append({
                                    'hex_id': row.get('hex_id', ''),
                                    'callsign': row.get('callsign', ''),
                                    'detected_at': row.get('timestamp', row.get('detected_at', '')),
                                    'last_seen': row.get('timestamp', row.get('last_seen', '')),
                                    'center_lat': float(row.get('center_lat', 0)),
                                    'center_lon': float(row.get('center_lon', 0)),
                                    'radius': float(row.get('radius_km', row.get('radius', 0))),
                                    'turns': float(row.get('turns', 0)),
                                    'max_altitude': int(float(row.get('altitude_ft', 0))) if row.get('altitude_ft') else None,
                                    'min_altitude': None,  # Not in current CSV format
                                    'avg_speed': float(row.get('speed_kts', 0)) if row.get('speed_kts') else None,
                                    'tar1090_url': row.get('tar1090_url', '')
                                })
                            except Exception as e:
                                print(f"Error parsing circle row: {e}, row: {row}")
                except Exception as e:
                    print(f"Error reading circle history file: {e}")
            
            # Read grid detections
            if self.grid_log_file.exists():
                try:
                    with open(self.grid_log_file, 'r') as f:
                        reader = csv.DictReader(f)
                        for row in reader:
                            try:
                                # Map CSV columns to expected fields
                                history_data['grids'].append({
                                    'hex_id': row.get('hex_id', ''),
                                    'callsign': row.get('callsign', ''),
                                    'detected_at': row.get('timestamp', row.get('detected_at', '')),
                                    'last_seen': row.get('timestamp', row.get('last_seen', '')),
                                    'pattern_type': row.get('pattern_type', ''),
                                    'center_lat': float(row.get('center_lat', 0)),
                                    'center_lon': float(row.get('center_lon', 0)),
                                    'num_legs': int(row.get('num_legs', 0)),
                                    'coverage_area': float(row.get('coverage_area_km2', row.get('coverage_area', 0))) if row.get('coverage_area_km2') or row.get('coverage_area') else None,
                                    'max_altitude': int(float(row.get('altitude_ft', 0))) if row.get('altitude_ft') else None,
                                    'min_altitude': None,  # Not in current CSV format
                                    'tar1090_url': row.get('tar1090_url', '')
                                })
                            except Exception as e:
                                print(f"Error parsing grid row: {e}, row: {row}")
                except Exception as e:
                    print(f"Error reading grid history file: {e}")
            
            return jsonify(history_data)
        
        @app.route('/api/aircraft')
        def get_aircraft():
            # Return all aircraft with paths for debugging
            aircraft_data = []
            for aircraft in self.aircraft.values():
                if len(aircraft.path) > 2:
                    aircraft_data.append({
                        'hex_id': aircraft.hex_id,
                        'callsign': aircraft.callsign,
                        'path': [
                            {'lat': p.lat, 'lon': p.lon, 'alt': p.altitude}
                            for p in aircraft.path[-50:]  # Last 50 points
                        ]
                    })
            return jsonify(aircraft_data)
        
        # Run Flask in a separate thread
        def run_flask():
            app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)
        
        self.web_thread = threading.Thread(target=run_flask, daemon=True)
        self.web_thread.start()
        
        # Open browser after a short delay
        time.sleep(1)
        webbrowser.open(f'http://localhost:{port}')
        print(f"\n🌐 Web viewer started at http://localhost:{port}")
    
    def run_monitoring(self, show_all_aircraft=False, quiet_mode=False, compact_mode=False, no_clear=False):
        """Run continuous monitoring loop."""
        self.running = True
        self.compact_mode = compact_mode
        self.no_clear = no_clear
        
        # Initial startup message
        if not compact_mode:
            print(f"🛰️  Connecting to {self.server_url}")
            print(f"⏱️  Update interval: {self.update_interval} seconds")
            print(f"🎯 Circle Detection: {self.detector.min_radius}-{self.detector.max_radius}km radius, {self.detector.min_turns}+ turns")
            print(f"📐 Grid Detection: {self.grid_detector.min_legs}+ legs, {self.grid_detector.min_leg_length}+km length")
            print(f"📝 Logging circles to: {self.log_file.absolute()}")
            print(f"📝 Logging grids to: {self.grid_log_file.absolute()}")
            print("🔄 Starting monitoring...\n")

        try:
            while self.running:
                success = self.fetch_aircraft_data()
                if success:
                    # Update circle and grid tracking and logging
                    self.update_circle_tracking()
                    self.update_grid_tracking()
                    
                    # Print status based on mode
                    if not self.compact_mode or self.recent_alerts:
                        self.print_status(show_all_aircraft=show_all_aircraft, quiet_mode=quiet_mode)
                else:
                    if not quiet_mode and not compact_mode:
                        print(f"\r❌ Connection failed. Retrying in {self.update_interval}s...", end="", flush=True)

                time.sleep(self.update_interval)

        except KeyboardInterrupt:
            print("\n\n👋 Stopping monitor... Thanks for using Aircraft Circle Detector!")
            self.print_log_summary()
            self.running = False
        except Exception as e:
            print(f"\n💥 Unexpected error: {e}")
            self.running = False


def main():
    parser = argparse.ArgumentParser(description='Monitor TAR1090 for aircraft performing circles')
    parser.add_argument('--server', '-s',
                        default='http://fr24.hallgren.net:8080',
                        help='TAR1090 server URL (default: http://fr24.hallgren.net:8080)')
    parser.add_argument('--interval', '-i', type=int, default=5,
                        help='Update interval in seconds (default: 5)')
    parser.add_argument('--min-radius', type=float, default=0.5,
                        help='Minimum circle radius in km (default: 0.5)')
    parser.add_argument('--max-radius', type=float, default=10.0,
                        help='Maximum circle radius in km (default: 10.0)')
    parser.add_argument('--min-turns', type=float, default=1.5,
                        help='Minimum number of turns to detect (default: 1.5)')
    parser.add_argument('--time-window', type=int, default=300,
                        help='Time window for analysis in seconds (default: 300)')
    parser.add_argument('--show-all', action='store_true',
                        help='Show all tracked aircraft (warning: may be overwhelming with many aircraft)')
    parser.add_argument('--quiet', '-q', action='store_true',
                        help='Quiet mode - only show circling aircraft alerts')
    parser.add_argument('--min-track-points', type=int, default=10,
                        help='Minimum track points needed for circle detection (default: 10)')
    parser.add_argument('--test', action='store_true',
                        help='Test connection and show sample data')
    parser.add_argument('--show-log', action='store_true',
                        help='Show logged circle detections and exit')
    parser.add_argument('--clear-log', action='store_true',
                        help='Clear the circle detection log file')
    parser.add_argument('--compact', action='store_true',
                        help='Compact mode - minimal display output')
    parser.add_argument('--no-clear', action='store_true',
                        help='Do not clear screen between updates')
    parser.add_argument('--max-speed', type=float, default=1000,
                        help='Maximum realistic aircraft speed in km/h (default: 1000)')
    parser.add_argument('--max-jump', type=float, default=5.0,
                        help='Maximum position jump between updates in km (default: 5.0)')
    parser.add_argument('--smoothing', type=int, default=3,
                        help='Smoothing window size for circle detection (default: 3, 0=disabled)')
    parser.add_argument('--min-grid-legs', type=int, default=3,
                        help='Minimum parallel legs for grid detection (default: 3)')
    parser.add_argument('--min-leg-length', type=float, default=2.0,
                        help='Minimum leg length in km for grid detection (default: 2.0)')
    parser.add_argument('--grid-time-window', type=int, default=600,
                        help='Time window for grid analysis in seconds (default: 600)')
    parser.add_argument('--web', action='store_true',
                        help='Start web map viewer')
    parser.add_argument('--web-port', type=int, default=8888,
                        help='Port for web viewer (default: 8888)')

    args = parser.parse_args()
    
    # Handle log-related commands first
    if args.show_log:
        log_file = Path("circle_detections.csv")
        if not log_file.exists():
            print("📋 No log file found. Start monitoring to create one.")
            sys.exit(0)
        
        print("\n📋 CIRCLE DETECTION LOG")
        print("=" * 80)
        print(f"Log file: {log_file.absolute()}")
        print("\nDetections:")
        print("-" * 80)
        
        with open(log_file, 'r') as f:
            reader = csv.DictReader(f)
            detections = list(reader)
            
            if not detections:
                print("No detections logged yet.")
            else:
                print(f"Total detections: {len(detections)}\n")
                
                for i, row in enumerate(detections, 1):
                    timestamp = datetime.fromisoformat(row['timestamp'])
                    print(f"\n{i}. {timestamp.strftime('%Y-%m-%d %H:%M:%S')} - {row['callsign']} ({row['hex_id']})")
                    print(f"   ⭕ {row['radius_km']}km radius, {row['turns']} turns")
                    if row['altitude_ft']:
                        print(f"   ✈️  {int(float(row['altitude_ft'])):,} ft")
                    print(f"   📍 Center: {row['center_lat']}, {row['center_lon']}")
                    print(f"   🔗 {row['tar1090_url']}")
        
        sys.exit(0)
    
    if args.clear_log:
        log_file = Path("circle_detections.csv")
        if log_file.exists():
            log_file.unlink()
            print("✅ Log file cleared.")
        else:
            print("📋 No log file to clear.")
        sys.exit(0)

    # Create monitor with custom settings
    monitor = TAR1090Monitor(args.server, args.interval)
    monitor.detector = CircleDetector(
        min_radius=args.min_radius,
        max_radius=args.max_radius,
        min_turns=args.min_turns,
        time_window=args.time_window
    )
    monitor.grid_detector = GridDetector(
        min_legs=args.min_grid_legs,
        min_leg_length=args.min_leg_length,
        time_window=args.grid_time_window
    )
    
    # Apply data quality settings
    monitor.max_speed_kmh = args.max_speed
    monitor.max_position_jump_km = args.max_jump
    
    # Configure smoothing
    if args.smoothing == 0:
        # Disable smoothing
        monitor.detector.smooth_path = lambda path: path

    # Override minimum track points for detection
    original_detect = monitor.detector.detect_circling

    def enhanced_detect(flight_path):
        if len(flight_path) < args.min_track_points:
            from dataclasses import dataclass
            @dataclass
            class CircleDetection:
                is_circling: bool
                center_lat: float
                center_lon: float
                radius: float
                turns: float

            return CircleDetection(False, 0, 0, 0, 0)
        return original_detect(flight_path)

    monitor.detector.detect_circling = enhanced_detect

    if args.test:
        print(f"🧪 Testing connection to {args.server}...")
        success = monitor.fetch_aircraft_data()
        if success:
            print(f"✅ Connection successful!")
            print(f"📊 Found {len(monitor.aircraft)} aircraft with position data")

            # Show useful statistics
            aircraft_with_tracks = [ac for ac in monitor.aircraft.values() if len(ac.path) >= 3]
            print(f"📈 {len(aircraft_with_tracks)} aircraft have track data")

            if monitor.aircraft:
                print(f"\n📡 Sample aircraft (showing first 5):")
                for i, (hex_id, aircraft) in enumerate(monitor.aircraft.items()):
                    if i >= 5:
                        break
                    pos = aircraft.path[-1] if aircraft.path else None
                    if pos:
                        alt_str = f", {pos.altitude} ft" if pos.altitude else ""
                        print(f"   {aircraft.callsign} ({hex_id}): {pos.lat:.4f}, {pos.lon:.4f}{alt_str}")

            if len(monitor.aircraft) > 50:
                print(f"\n💡 You have {len(monitor.aircraft)} aircraft - consider using --quiet mode")
                print("   to focus only on circling aircraft alerts!")
        else:
            print("❌ Connection failed!")
            sys.exit(1)
    else:
        if getattr(args, 'quiet', False):
            # Quiet mode - minimal output, focus on alerts
            print("🔇 Quiet mode: Will only show circling aircraft alerts")
            print("   Press Ctrl+C to stop\n")
        
        # Start web server if requested
        if args.web:
            monitor.start_web_server(port=args.web_port)

        monitor.run_monitoring(show_all_aircraft=getattr(args, 'show_all', False),
                               quiet_mode=getattr(args, 'quiet', False),
                               compact_mode=getattr(args, 'compact', False),
                               no_clear=getattr(args, 'no_clear', False))


if __name__ == "__main__":
    main()