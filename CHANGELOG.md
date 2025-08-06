# Changelog

All notable changes to Aircraft Patterns will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-01-06

### Added

- Initial release of Aircraft Patterns detection system
- Real-time circle pattern detection for training and holding patterns
- Grid pattern detection for survey and search operations
- Web interface with live map visualization
- TAR1090-style aircraft icons with altitude-based coloring
- Aircraft track history display
- Historical pattern viewer with filtering capabilities
- CSV logging of all detected patterns
- Direct TAR1090 integration with replay links
- Docker support with multi-architecture builds
- Configurable detection parameters
- Interactive display controls
- Pattern timeline visualization
- Comprehensive documentation

### Features

- Circle Detection
  - Configurable radius range (0.5-10km default)
  - Minimum turn detection (1.5 turns default)
  - Center point calculation
  - Real-time alerts

- Grid Detection
  - Parallel leg identification
  - Survey pattern recognition
  - Coverage area calculation
  - Pattern type classification

- Web Interface
  - Live aircraft tracking
  - Pattern overlay visualization
  - History page with filters
  - TAR1090 replay links
  - Interactive controls

### Technical

- Python 3.8+ support
- Flask web framework
- Leaflet.js mapping
- Docker containerization
- Multi-architecture support (amd64, arm64, arm/v7)
- GitHub Actions CI/CD
- CSV data persistence

### Documentation

- Comprehensive README
- Docker deployment guide
- Configuration reference
- Contributing guidelines
- MIT License

---

## Future Releases

### [Planned Features]

- Additional pattern types (figure-8, racetrack)
- Email/webhook notifications
- Pattern statistics dashboard
- Machine learning pattern prediction
- Multi-language support
- Mobile responsive design
- API endpoints for integration
- Prometheus metrics export
