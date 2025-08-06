// Aircraft icon shapes from tar1090 (https://github.com/wiedehopf/tar1090)
// Licensed under GNU GPLv3

const aircraftShapes = {
    'airliner': {
        svg: '<path d="m 16,1 -1.5,1 -1,2 -2,3 v 6 l -5,2 v 1.5 l 5,-0.5 v 5.5 l -1.5,1.5 v 1 l 2,-0.5 0.5,-0.5 h 1 l 0.5,0.5 2,0.5 v -1 l -1.5,-1.5 v -5.5 l 5,0.5 v -1.5 l -5,-2 v -6 l -2,-3 -1,-2 z"/>',
        width: 32,
        height: 32,
        viewBox: '0 0 32 32',
        scale: 1.0
    },
    'jet_nonmil': {
        svg: '<path d="m 16,2 -0.7,0.5 -1.3,1.5 -2,3 v 7 l -4,1.5 v 2 l 4,-0.5 v 4.5 l -1.5,1.5 v 1.5 l 2,-0.5 0.5,-0.5 h 2 l 0.5,0.5 2,0.5 v -1.5 l -1.5,-1.5 v -4.5 l 4,0.5 v -2 l -4,-1.5 v -7 l -2,-3 -1.3,-1.5 z"/>',
        width: 32,
        height: 32,
        viewBox: '0 0 32 32',
        scale: 0.9
    },
    'helicopter': {
        svg: '<path d="m 16,3 c -0.5,0 -1,0.5 -1,1 v 2 h -6 v 1 h 14 v -1 h -6 v -2 c 0,-0.5 -0.5,-1 -1,-1 z m -1,5 v 8 l -3,1 v 1.5 l 3,-0.5 v 4 h 2 v -4 l 3,0.5 v -1.5 l -3,-1 v -8 z m -7,16 v 1 h 16 v -1 z"/>',
        width: 32,
        height: 32,
        viewBox: '0 0 32 32',
        scale: 1.0,
        noRotate: true
    },
    'light_single': {
        svg: '<path d="m 16,4 -0.5,1 -1.5,2 v 8 l -6,2 v 1 l 6,-1 v 5 l -2,1 v 1 l 2.5,-0.5 h 3 l 2.5,0.5 v -1 l -2,-1 v -5 l 6,1 v -1 l -6,-2 v -8 l -1.5,-2 z"/>',
        width: 32,
        height: 32,
        viewBox: '0 0 32 32',
        scale: 0.8
    },
    'light_twin': {
        svg: '<path d="m 16,3 -1,1 -1,2 v 7 l -2,0.5 v 2 l -3,1 v 1 l 5,-1 v 5 l -2,1 v 1 l 2.5,-0.5 h 3 l 2.5,0.5 v -1 l -2,-1 v -5 l 5,1 v -1 l -3,-1 v -2 l -2,-0.5 v -7 l -1,-2 z"/>',
        width: 32,
        height: 32,
        viewBox: '0 0 32 32',
        scale: 0.85
    },
    'heavy_4e': {
        svg: '<path d="m 16,2 -1,1 -2,2 -1,2 v 5 l -2,0.5 v 2 l -2,0.5 v 1 l -2,1 v 1 l 6,-1 v 5 l -2,1 v 1 l 3,-0.5 h 2 l 3,0.5 v -1 l -2,-1 v -5 l 6,1 v -1 l -2,-1 v -1 l -2,-0.5 v -2 l -2,-0.5 v -5 l -1,-2 -2,-2 z"/>',
        width: 32,
        height: 32,
        viewBox: '0 0 32 32',
        scale: 1.1
    },
    'glider': {
        svg: '<path d="m 16,5 -0.5,0.5 -0.5,1.5 v 5 l -8,2 v 1 l 8,-1 v 6 l -2,1 v 1 l 2.5,-0.5 h 1 l 2.5,0.5 v -1 l -2,-1 v -6 l 8,1 v -1 l -8,-2 v -5 l -0.5,-1.5 z"/>',
        width: 32,
        height: 32,
        viewBox: '0 0 32 32',
        scale: 0.9
    },
    'ground_vehicle': {
        svg: '<rect x="12" y="10" width="8" height="12" rx="1" ry="1"/>',
        width: 32,
        height: 32,
        viewBox: '0 0 32 32',
        scale: 0.7,
        noRotate: true
    },
    'tower': {
        svg: '<path d="m 16,8 -4,4 v 2 h 2 v 8 h 4 v -8 h 2 v -2 z m -2,2 h 4 v 2 h -4 z"/>',
        width: 32,
        height: 32,
        viewBox: '0 0 32 32',
        scale: 0.8,
        noRotate: true
    },
    'default': {
        svg: '<circle cx="16" cy="16" r="4"/>',
        width: 32,
        height: 32,
        viewBox: '0 0 32 32',
        scale: 0.6,
        noRotate: true
    }
};

// Type to shape mapping
const typeToShape = {
    // Airliners
    'A320': 'airliner',
    'A321': 'airliner',
    'A319': 'airliner',
    'A318': 'airliner',
    'A330': 'airliner',
    'A340': 'heavy_4e',
    'A350': 'airliner',
    'A380': 'heavy_4e',
    'B737': 'airliner',
    'B738': 'airliner',
    'B739': 'airliner',
    'B747': 'heavy_4e',
    'B757': 'airliner',
    'B767': 'airliner',
    'B777': 'airliner',
    'B787': 'airliner',
    
    // Regional jets
    'CRJ2': 'jet_nonmil',
    'CRJ7': 'jet_nonmil',
    'CRJ9': 'jet_nonmil',
    'E145': 'jet_nonmil',
    'E170': 'jet_nonmil',
    'E175': 'jet_nonmil',
    'E190': 'jet_nonmil',
    
    // Light aircraft
    'C172': 'light_single',
    'C152': 'light_single',
    'C182': 'light_single',
    'PA28': 'light_single',
    'PA34': 'light_twin',
    'BE36': 'light_single',
    'BE58': 'light_twin',
    'DA40': 'light_single',
    'DA42': 'light_twin',
    'SR22': 'light_single',
    
    // Helicopters
    'R44': 'helicopter',
    'R66': 'helicopter',
    'AS50': 'helicopter',
    'EC35': 'helicopter',
    'EC45': 'helicopter',
    'B407': 'helicopter',
    'S76': 'helicopter',
    
    // Gliders
    'GLID': 'glider',
    'ASK21': 'glider',
    'DG1000': 'glider'
};

// Category to shape mapping (fallback)
const categoryToShape = {
    'A1': 'light_single',  // Light single engine
    'A2': 'light_twin',    // Light twin engine
    'A3': 'airliner',      // Large aircraft
    'A4': 'heavy_4e',      // Heavy aircraft
    'A5': 'airliner',      // Super heavy
    'B1': 'glider',        // Glider/sailplane
    'B2': 'balloon',       // Lighter than air
    'B3': 'balloon',       // Airship
    'B4': 'helicopter',    // Rotorcraft
    'C1': 'ground_vehicle', // Ground vehicle
    'C2': 'ground_vehicle', // Ground vehicle
    'C3': 'tower'          // Tower/obstacle
};

// Function to get appropriate icon for aircraft
function getAircraftIcon(typeDesignator, category) {
    // First try type designator
    if (typeDesignator && typeToShape[typeDesignator]) {
        return aircraftShapes[typeToShape[typeDesignator]];
    }
    
    // Then try category
    if (category && categoryToShape[category]) {
        return aircraftShapes[categoryToShape[category]] || aircraftShapes['default'];
    }
    
    // Default
    return aircraftShapes['default'];
}

// Function to create SVG element for aircraft
function createAircraftSVG(typeDesignator, category, color = '#000000', rotation = 0) {
    const icon = getAircraftIcon(typeDesignator, category);
    const rotateTransform = icon.noRotate ? '' : ` transform="rotate(${rotation} 16 16)"`;
    
    return `
        <svg width="${icon.width}" height="${icon.height}" viewBox="${icon.viewBox}" xmlns="http://www.w3.org/2000/svg">
            <g${rotateTransform}>
                <g fill="${color}" stroke="none">
                    ${icon.svg}
                </g>
            </g>
        </svg>
    `;
}

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        aircraftShapes,
        typeToShape,
        categoryToShape,
        getAircraftIcon,
        createAircraftSVG
    };
}