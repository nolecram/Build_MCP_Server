# Contributing to Playwright MCP Server

We welcome contributions! This guide will help you get started.

## Getting Started

### Prerequisites

- Python 3.8+
- Git
- Playwright (installed via pip)

### Development Setup

```bash
# Clone the repository
git clone https://github.com/nolecram/Build_MCP_Server.git
cd Build_MCP_Server

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .
pip install -r requirements-dev.txt

# Install Playwright browsers
playwright install chromium
```

## Making Changes

### Code Style

We follow PEP 8 with these tools:

- **Black** for code formatting
- **isort** for import sorting
- **flake8** for linting
- **mypy** for type checking

### Before Committing

```bash
# Format code
black src/ tests/

# Sort imports
isort src/ tests/

# Run linting
flake8 src/ tests/

# Type checking
mypy src/
```

### Writing Tests

- Add tests for new features in `tests/`
- Use `pytest` and `pytest-asyncio`
- Follow the existing test structure
- Aim for >80% code coverage

```bash
# Run tests
pytest

# With coverage
pytest --cov=playwright_mcp_server tests/

# Specific test
pytest tests/test_tools.py::TestPlaywrightTools::test_navigate
```

### Documentation

- Update docstrings using Google style
- Include type hints for all functions
- Update README.md if adding features
- Add examples to EXAMPLES.md

## Pull Request Process

1. **Fork and Branch**: Create a branch for your feature
   ```bash
   git checkout -b feature/my-awesome-feature
   ```

2. **Make Changes**: Implement your feature with tests

3. **Run Tests**: Ensure all tests pass
   ```bash
   pytest
   flake8 src/ tests/
   mypy src/
   black --check src/ tests/
   ```

4. **Commit**: Use clear commit messages
   ```bash
   git commit -m "Add feature: detailed description"
   ```

5. **Push**: Push to your fork
   ```bash
   git push origin feature/my-awesome-feature
   ```

6. **Create PR**: Open a Pull Request with a clear description

## Commit Message Guidelines

- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit first line to 50 characters
- Reference issues and pull requests liberally after the first line

Examples:
```
Add screenshot capability
Fix timeout handling in click method
Update documentation for new tools
```

## Feature Request Process

1. Check if the feature exists in issues
2. Create an issue with the `enhancement` label
3. Include:
   - Clear description of the feature
   - Use cases and examples
   - Proposed implementation (optional)

## Bug Report Process

1. Check if the bug is already reported
2. Create an issue with the `bug` label
3. Include:
   - Python version and OS
   - Error message and traceback
   - Minimal code to reproduce
   - Expected vs. actual behavior

## Code Review

All submissions require code review. We use GitHub reviews to:
- Ensure code quality and style
- Check test coverage
- Verify documentation
- Discuss design decisions

## Release Process

- Maintainers handle version bumping and releases
- Follow semantic versioning
- Update CHANGELOG with all changes

## Questions or Need Help?

- Check existing issues and documentation
- Ask in pull request comments
- Open an issue with the `question` label

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to Playwright MCP Server! 🎉