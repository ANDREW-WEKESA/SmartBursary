# Contributing to SmartBursary

Thank you for your interest in contributing to SmartBursary! This document provides guidelines for contributing to the project.

## Code of Conduct

Be respectful and inclusive. We welcome contributions from everyone.

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in Issues
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots if applicable
   - Environment details (OS, browser, etc.)

### Suggesting Features

1. Check if the feature has been suggested
2. Create a new issue with:
   - Clear description of the feature
   - Use cases and benefits
   - Possible implementation approach

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test your changes
5. Commit with clear messages
6. Push to your fork
7. Create a Pull Request

## Development Setup

### Backend
```bash
cd backend
python -m venv .venv
.\.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Mac/Linux
pip install -r requirements.txt
```

### Frontend
```bash
cd frontend
npm install
```

## Coding Standards

### Python (Backend)
- Follow PEP 8 style guide
- Use type hints where appropriate
- Write docstrings for functions and classes
- Keep functions focused and small

### JavaScript/React (Frontend)
- Use functional components
- Follow React best practices
- Use meaningful variable names
- Keep components small and reusable

## Commit Message Guidelines

Format: `type: description`

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

Examples:
- `feat: Add email notification for approved applications`
- `fix: Resolve CORS error on production`
- `docs: Update API documentation`

## Testing

### Backend
```bash
pytest
```

### Frontend
```bash
npm test
```

## Questions?

Feel free to open an issue or reach out to the maintainers.

Thank you for contributing! 🎉
