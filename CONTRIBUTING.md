# Contributing to Reddit Persona Agent

Thank you for your interest in contributing to the Reddit Persona Agent! This document provides guidelines for contributing to the project.

## 🚀 Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/reddit-persona-agent.git`
3. Create a new branch: `git checkout -b feature/your-feature-name`
4. Install dependencies: `pip install -r requirements.txt`
5. Set up your `.env` file with API keys

## 🛠️ Development Setup

### Prerequisites
- Python 3.10+
- Reddit API credentials
- OpenRouter API key

### Installation
```bash
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API keys
```

### Running Tests
```bash
python test_features.py
pytest tests/
```

## 📝 Contribution Guidelines

### Code Style
- Follow PEP 8 Python style guidelines
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and modular

### Commit Messages
- Use clear, descriptive commit messages
- Start with a verb (Add, Fix, Update, Remove)
- Keep the first line under 50 characters
- Add detailed description if needed

Example:
```
Add sentiment analysis visualization

- Implement emotion heatmap using Plotly
- Add sentiment timeline chart
- Update Streamlit dashboard with new charts
```

### Pull Request Process

1. **Update Documentation**: Ensure README.md reflects any changes
2. **Add Tests**: Include tests for new features
3. **Update Requirements**: Add any new dependencies to requirements.txt
4. **Test Thoroughly**: Run all tests and manual testing
5. **Create PR**: Provide clear description of changes

### Areas for Contribution

#### 🎯 High Priority
- **Performance Optimization**: Improve analysis speed
- **Error Handling**: Better error messages and recovery
- **Data Validation**: Input sanitization and validation
- **Documentation**: Code comments and user guides

#### 🔧 Medium Priority
- **New Analysis Features**: Additional personality metrics
- **Visualization Improvements**: New chart types
- **Export Options**: Additional file formats
- **API Enhancements**: Rate limiting and caching

#### 💡 Ideas Welcome
- **Machine Learning Models**: Custom trained models
- **Real-time Analysis**: Live data processing
- **Mobile Interface**: Responsive design improvements
- **Integration**: APIs for external tools

## 🐛 Bug Reports

When reporting bugs, please include:

1. **Environment**: Python version, OS, dependencies
2. **Steps to Reproduce**: Clear step-by-step instructions
3. **Expected Behavior**: What should happen
4. **Actual Behavior**: What actually happens
5. **Screenshots**: If applicable
6. **Error Messages**: Full error logs

## 💡 Feature Requests

For new features, please provide:

1. **Use Case**: Why is this feature needed?
2. **Description**: Detailed explanation of the feature
3. **Examples**: How would it work?
4. **Implementation Ideas**: Technical approach (if any)

## 📚 Resources

- [Reddit API Documentation](https://www.reddit.com/dev/api/)
- [OpenRouter API Docs](https://openrouter.ai/docs)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [LangChain Documentation](https://python.langchain.com/)

## 🤝 Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow
- Maintain a positive environment

## 📞 Getting Help

- **Issues**: Use GitHub Issues for bugs and features
- **Discussions**: Use GitHub Discussions for questions
- **Documentation**: Check README.md and code comments

## 🏆 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes for significant contributions
- Special thanks for major features

Thank you for contributing to Reddit Persona Agent! 🎉