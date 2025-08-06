# Contributing to Aircraft Circle

Thank you for your interest in contributing to Aircraft Circle! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

By participating in this project, you agree to abide by our code of conduct:

- Be respectful and inclusive
- Welcome newcomers and help them get started
- Focus on constructive criticism
- Accept feedback gracefully

## How to Contribute

### Reporting Issues

1. Check if the issue already exists in [GitHub Issues](https://github.com/challgren/aircraft-circle/issues)
2. If not, create a new issue with:
   - Clear, descriptive title
   - Steps to reproduce the problem
   - Expected vs actual behavior
   - System information (OS, Python version, Docker version if applicable)
   - Relevant logs or error messages

### Suggesting Features

1. Check existing issues for similar suggestions
2. Create a new issue with the `enhancement` label
3. Describe the feature and its use case
4. Explain why it would be valuable to the project

### Submitting Code

#### Setup Development Environment

```bash
# Fork and clone the repository
git clone https://github.com/YOUR-USERNAME/aircraft-circle.git
cd aircraft-circle

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install black flake8 pytest
```

#### Development Workflow

1. Create a feature branch:

   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes following our coding standards

3. Test your changes:

   ```bash
   # Run the application
   python app.py --test
   
   # Format code
   black app.py
   
   # Check code style
   flake8 app.py
   ```

4. Commit your changes:

   ```bash
   git add .
   git commit -m "Add: brief description of changes"
   ```

5. Push to your fork:

   ```bash
   git push origin feature/your-feature-name
   ```

6. Create a Pull Request

## Coding Standards

### Python Style

- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and under 50 lines when possible
- Use type hints where appropriate

### Code Organization

```python
# Good example
def calculate_circle_radius(positions: List[Position]) -> float:
    """
    Calculate the radius of a circular flight pattern.
    
    Args:
        positions: List of aircraft positions
        
    Returns:
        Radius in kilometers
    """
    # Implementation here
    pass
```

### Commit Messages

Use clear, descriptive commit messages:

- `Add: new feature description`
- `Fix: bug description`
- `Update: component description`
- `Refactor: what was refactored`
- `Docs: what documentation was updated`

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_detection.py
```

### Writing Tests

Create test files in the `tests/` directory:

```python
def test_circle_detection():
    """Test circle pattern detection."""
    detector = CircleDetector()
    positions = generate_circle_path()
    result = detector.detect(positions)
    assert result.is_circle == True
    assert 0.5 <= result.radius <= 10
```

## Docker Development

### Building Local Image

```bash
# Build for testing
docker build -t aircraft-circle:dev .

# Run local build
docker run -it --rm \
  -p 8888:8888 \
  -e TAR1090_URL=http://your-tar1090:80 \
  aircraft-circle:dev
```

### Multi-Architecture Build

```bash
# Setup buildx
docker buildx create --use

# Build for multiple platforms
docker buildx build \
  --platform linux/amd64,linux/arm64,linux/arm/v7 \
  -t aircraft-circle:dev \
  .
```

## Documentation

### Updating Documentation

- Keep README.md up to date with new features
- Add docstrings to all new functions
- Update configuration tables when adding new options
- Include examples for new features

### Documentation Style

- Use clear, concise language
- Include code examples
- Add screenshots for UI changes
- Update the changelog

## Pull Request Process

1. **Before Submitting**
   - Ensure all tests pass
   - Update documentation
   - Add entry to CHANGELOG.md
   - Verify Docker build works

2. **PR Description Should Include**
   - Summary of changes
   - Related issue numbers
   - Testing performed
   - Screenshots (if UI changes)

3. **Review Process**
   - PRs require at least one review
   - Address all feedback
   - Ensure CI checks pass
   - Squash commits if requested

## Release Process

1. Update version in relevant files
2. Update CHANGELOG.md
3. Create release PR
4. After merge, tag release
5. Docker images auto-build on tag

## Getting Help

- Join [SDR-Enthusiasts Discord](https://discord.gg/sTf9uYF)
- Ask questions in GitHub Issues
- Check existing documentation

## Recognition

Contributors will be recognized in:

- README.md acknowledgments
- Release notes
- Project documentation

Thank you for contributing to Aircraft Circle!
