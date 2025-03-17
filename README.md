# 🤖 AI Coder - Intelligent Code Assistant

AI Coder is an advanced AI-powered coding assistant that leverages Google's Gemini model (with support for multiple AI providers) to help developers write, analyze, and improve code. Built with FastAPI and designed for seamless integration with modern development workflows.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.0+-00a393.svg)](https://fastapi.tiangolo.com)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## 🌟 Features

### 🎯 Core Capabilities
- **AI-Powered Code Generation**: Utilizing Google's Gemini model
- **Multi-Model Support**: Gemini, OpenAI, Claude, and HuggingFace models
- **Code Analysis**: Deep code understanding and improvement suggestions
- **Intelligent Refactoring**: Smart code restructuring and optimization
- **Test Generation**: Automated test case creation
- **Documentation**: Automatic documentation generation
- **Security Analysis**: Code security scanning and suggestions

### 🛠 Development Tools
- **Version Control Integration**: GitHub, GitLab, Bitbucket support
- **Code Quality**: Automated linting, formatting, and style checking
- **Performance Analysis**: Code performance optimization suggestions
- **Type Checking**: Automated type inference and validation
- **Dependency Management**: Smart dependency tracking and updates

### 🚀 Deployment & Infrastructure
- **Docker Support**: Full containerization with Docker Compose
- **Internal Databases**: Self-contained PostgreSQL and Redis
- **Coolify Ready**: Optimized for Coolify deployment
- **Health Monitoring**: Built-in health checks and monitoring
- **Auto Scaling**: Automatic resource management

## 📋 Requirements

### Minimum Requirements
- Python 3.11+
- Docker and Docker Compose
- 4GB RAM
- 2 CPU cores

### Recommended
- 8GB+ RAM
- 4+ CPU cores
- SSD Storage
- NVIDIA GPU (optional, for local AI models)

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/ai-coder.git
cd ai-coder
```

### 2. Set Up Environment
```bash
# Copy environment file
cp .env.example .env

# Update required variables in .env
GEMINI_API_KEY=your_key_here
SECRET_KEY=your_secret_here
JWT_SECRET_KEY=your_jwt_secret_here
```

### 3. Run with Docker Compose
```bash
docker compose up -d
```

### 4. Access the API
- API Documentation: http://localhost:8000/docs
- ReDoc Documentation: http://localhost:8000/redoc
- Health Check: http://localhost:8000/health

## 📖 Documentation

### API Endpoints

#### Code Generation
```python
POST /api/v1/generate
{
    "prompt": "Create a FastAPI user authentication system",
    "language": "python",
    "framework": "fastapi"
}
```

#### Code Analysis
```python
POST /api/v1/analyze
{
    "code": "your code here",
    "analysis_type": "security"  # or "performance", "style"
}
```

#### Test Generation
```python
POST /api/v1/generate-tests
{
    "code": "your code here",
    "test_framework": "pytest"
}
```

### Configuration

#### Environment Variables
See [Environment Variables Documentation](docs/environment-variables.md) for a complete list.

#### Model Configuration
```python
# Available AI Models
- Gemini (Default)
- OpenAI GPT-4
- Anthropic Claude
- HuggingFace Models
```

## 🛠 Development

### Local Development Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run development server
uvicorn main:app --reload
```

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/
```

### Code Quality
```bash
# Format code
black .

# Sort imports
isort .

# Lint code
pylint app/

# Type checking
mypy app/
```

## 🚀 Deployment

### Coolify Deployment
1. Fork this repository
2. In Coolify:
   - Create new service
   - Select your forked repository
   - Choose "Docker Compose" deployment
   - Set required environment variables
   - Deploy

### Manual Deployment
```bash
# Clone repository
git clone https://github.com/yourusername/ai-coder.git

# Configure environment
cp .env.example .env
nano .env  # Edit variables

# Deploy with Docker Compose
docker compose up -d
```

## 📊 Monitoring

### Health Checks
- `/health`: Basic health check
- `/health/live`: Liveness probe
- `/health/ready`: Readiness probe

### Metrics
- Prometheus metrics: `/metrics`
- Grafana dashboard included

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Process
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Google's Gemini team for the amazing AI model
- FastAPI team for the excellent framework
- OpenHands project for inspiration
- All contributors and supporters

## 📞 Support

- GitHub Issues: For bugs and feature requests
- Discussions: For questions and community support
- Email: support@example.com

## 🔄 Updates & Versioning

We use [SemVer](http://semver.org/) for versioning. For available versions, see the [tags on this repository](https://github.com/yourusername/ai-coder/tags).

## 🗺 Roadmap

- [ ] Support for more AI models
- [ ] Enhanced code generation capabilities
- [ ] Improved test coverage
- [ ] Additional language support
- [ ] Advanced security features

## 📈 Project Status

- **Current Version**: 1.0.0
- **Status**: Active Development
- **Last Updated**: [Current Date]

## 🔗 Links

- [Documentation](docs/README.md)
- [API Reference](docs/api-reference.md)
- [Contributing](CONTRIBUTING.md)
- [Change Log](CHANGELOG.md)
