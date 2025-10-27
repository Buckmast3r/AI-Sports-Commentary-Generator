# Contributing to AI Sports Commentary Generator

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/AI-Sports-Commentary-Generator.git`
3. Create a branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Test your changes
6. Commit: `git commit -m "Description of changes"`
7. Push: `git push origin feature/your-feature-name`
8. Create a Pull Request

## Development Setup

```bash
# Install in development mode
pip install -r requirements.txt

# Install dev dependencies (optional)
pip install pytest black flake8 mypy

# Run tests
python -m pytest tests/

# Format code
black src/ main.py

# Lint
flake8 src/ main.py
```

## Code Style

- Follow PEP 8 guidelines
- Use type hints where appropriate
- Write docstrings for all functions and classes
- Keep functions focused and small
- Add comments for complex logic

### Example:
```python
def process_headline(headline: str, summary: str = "") -> Optional[str]:
    """
    Process a sports headline into a script
    
    Args:
        headline: The sports headline text
        summary: Optional summary for context
        
    Returns:
        Generated script or None if processing fails
    """
    # Implementation
    pass
```

## Testing

- Add tests for new features
- Ensure existing tests pass
- Aim for >80% code coverage
- Write both unit and integration tests

Example test:
```python
def test_rss_feed_handler():
    handler = RSSFeedHandler(["https://example.com/rss"])
    headlines = handler.fetch_headlines(limit=1)
    assert isinstance(headlines, list)
```

## Project Structure

```
src/
├── rss/          # RSS feed handling
├── llm/          # LLM script generation
├── tts/          # Text-to-speech
├── avatar/       # Avatar animation
├── video/        # Video composition
└── youtube/      # YouTube upload
```

When adding new features:
- Create appropriate module in `src/`
- Add `__init__.py` with exports
- Update main.py if needed
- Update README.md
- Add example usage to EXAMPLES.md

## Adding New Features

### Adding a New RSS Source

1. Update `config.example.json`:
```json
"rss_feeds": [
  "https://new-source.com/rss"
]
```

2. Test the feed:
```python
from src.rss import RSSFeedHandler
handler = RSSFeedHandler(["https://new-source.com/rss"])
print(handler.fetch_headlines(1))
```

### Adding a New LLM Provider

1. Create new file: `src/llm/new_provider.py`
2. Implement the interface:
```python
class NewLLMProvider:
    def generate_script(self, headline: str, summary: str = "") -> str:
        # Implementation
        pass
```
3. Update `src/llm/__init__.py`
4. Add configuration support
5. Update documentation

### Adding Video Effects

1. Add new method to `VideoComposer` class
2. Update FFmpeg filters
3. Test with sample video
4. Document usage

## Pull Request Guidelines

### PR Title Format
- `feat: Add new feature`
- `fix: Fix bug description`
- `docs: Update documentation`
- `refactor: Code refactoring`
- `test: Add or update tests`
- `chore: Maintenance tasks`

### PR Description Should Include
- What changes were made
- Why the changes were necessary
- How to test the changes
- Screenshots/videos if applicable
- Related issue numbers

### Before Submitting
- [ ] Code follows project style
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] All tests pass
- [ ] No new warnings
- [ ] Commit messages are clear

## Bug Reports

When filing a bug report, include:

1. **Description**: Clear description of the issue
2. **Steps to Reproduce**: Detailed steps
3. **Expected Behavior**: What should happen
4. **Actual Behavior**: What actually happens
5. **Environment**:
   - OS version
   - Python version
   - Package versions
   - Ollama version
6. **Logs**: Relevant log output
7. **Screenshots**: If applicable

### Bug Report Template

```markdown
**Description**
A clear description of the bug.

**Steps to Reproduce**
1. Run command '...'
2. See error '...'

**Expected Behavior**
What you expected to happen.

**Actual Behavior**
What actually happened.

**Environment**
- OS: Ubuntu 22.04
- Python: 3.10.0
- Ollama: 0.1.17

**Logs**
```
Paste relevant logs here
```

**Additional Context**
Any other relevant information.
```

## Feature Requests

When requesting a feature:

1. **Use Case**: Describe the use case
2. **Proposed Solution**: How you envision it working
3. **Alternatives**: Other solutions you've considered
4. **Additional Context**: Screenshots, mockups, examples

## Code Review Process

1. Maintainer reviews PR
2. Feedback provided
3. Author makes requested changes
4. Approval and merge

We aim to review PRs within 7 days.

## Areas for Contribution

### High Priority
- [ ] Instagram Reels integration
- [ ] TikTok API integration
- [ ] Better error handling
- [ ] Retry logic for failed operations
- [ ] Unit tests for all modules
- [ ] Docker support

### Medium Priority
- [ ] Web UI for easier usage
- [ ] Multiple avatar support
- [ ] Background music
- [ ] Video transitions
- [ ] Analytics dashboard

### Low Priority
- [ ] Multiple language support
- [ ] Custom fonts for captions
- [ ] Video filters and effects
- [ ] Batch processing improvements

## Documentation

Good documentation is crucial. When updating code:

1. Update relevant docstrings
2. Update README.md if needed
3. Add examples to EXAMPLES.md
4. Update configuration examples
5. Add inline comments for complex logic

## Community

- Be respectful and inclusive
- Help others in discussions
- Share your use cases
- Provide constructive feedback

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Questions?

Open an issue with the `question` label or reach out to the maintainers.

---

Thank you for contributing to AI Sports Commentary Generator! 🎉
