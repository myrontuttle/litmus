# Litmus

A FastAPI + MongoDB + HTMX web application built with the vibetuner framework. This project serves as a scaffolded template for modern web applications with real-time features and robust backend architecture.

## ✨ Features

- **Modern Stack**: FastAPI backend with MongoDB (Beanie ODM) and HTMX frontend
- **Real-time Updates**: Server-Sent Events (SSE) for live data updates
- **Authentication**: Built-in user management with OAuth support
- **Responsive UI**: Tailwind CSS with DaisyUI components
- **Background Jobs**: Redis-powered task queue for async processing
- **Internationalization**: Multi-language support with Babel
- **Testing**: Comprehensive test suite with pytest fixtures
- **Development Tools**: Hot reload, auto-formatting, and linting

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- MongoDB (local or cloud)
- Redis (optional, for background jobs)
- Node.js (for asset compilation)

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/litmus.git
   cd litmus
   ```

2. **Install dependencies**

   ```bash
   just install-deps
   ```

3. **Set up environment**

   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Start development server**

   ```bash
   just local-all
   ```

5. **Open your browser**

   ```text
   http://localhost:8000
   ```

## 📖 Usage

### Development Commands

```bash
# Start development server (frontend + assets)
just local-all

# Start with background worker
just local-all-with-worker

# Run tests
uv run pytest -v

# Format and lint code
just format && just lint

# Update dependencies
just update-repo-deps
```

### Project Structure

```text
src/litmus/              # Your application code
├── models/             # Beanie document models
├── frontend/
│   ├── routes/         # HTTP endpoints
│   └── templates/      # Jinja2 templates
├── services/           # Business logic
└── tasks/              # Background jobs

templates/              # Custom templates
assets/                 # Static assets (CSS/JS)
docs/dev/              # Development documentation
```

## 🛠️ Development

This project follows agile and lean software engineering practices with comprehensive documentation for both human developers and coding agents.

### 📚 Development Documentation

| Document | Purpose | Read Time |
|----------|---------|-----------|
| **[GETTING_STARTED.md](docs/dev/GETTING_STARTED.md)** | Entry point for all development docs | 10-15 min |
| **[DEVELOPMENT_WORKFLOW.md](docs/dev/DEVELOPMENT_WORKFLOW.md)** | Main development workflow guide | 40 min |
| **[QUICK_REFERENCE.md](docs/dev/QUICK_REFERENCE.md)** | Daily command reference | 5 min |
| **[TEMPLATES.md](docs/dev/TEMPLATES.md)** | GitHub issue & PR templates | 20 min |
| **[TDD_AND_CODEGEN.md](docs/dev/TDD_AND_CODEGEN.md)** | TDD patterns & code generation | 30 min |
| **[WORKFLOW_VISUAL_GUIDE.md](docs/dev/WORKFLOW_VISUAL_GUIDE.md)** | Visual flowcharts & decision trees | 5 min |
| **[README_DEVELOPMENT.md](docs/dev/README_DEVELOPMENT.md)** | Complete documentation index | 15 min |

### 🤖 Agent Collaboration

This project is designed for seamless human-agent collaboration:

- **Clear handoff protocols** for work transitions
- **Structured issue templates** for consistent requirements
- **Test-driven development** with comprehensive patterns
- **Code generation** using framework factories
- **Weekly sync cycles** for dependency updates

### 🧪 Testing

```bash
# Run all tests
uv run pytest -v

# Run specific test file
uv run pytest tests/test_user_auth.py -v

# Run with coverage
uv run pytest --cov=src/litmus --cov-report=html

# Type checking
just type-check
```

### 📝 Code Quality

- **Formatting**: `ruff format .` (always run after changes)
- **Linting**: `just lint` (Python, Jinja, TOML, YAML)
- **Type checking**: `just type-check` (MyPy)
- **Framework diagnostics**: `uv run vibetuner doctor`

## 🔧 Configuration

### Environment Variables

Create a `.env` file with:

```bash
# Database
DATABASE_URL=mongodb://localhost:27017/litmus

# Redis (optional)
REDIS_URL=redis://localhost:6379

# Security
SECRET_KEY=your-secret-key-here

# Development
DEBUG=true
LOCALDEV_URL=https://{port}.localdev.localhost:12000
```

### App Configuration

Customize `src/litmus/tune.py` to register your components:

```python
from vibetuner import VibetunerApp
from litmus.models import User, Post
from litmus.frontend.routes import api_router

app = VibetunerApp(
    models=[User, Post],
    routes=[api_router],
    # Add more configuration as needed
)
```

## 🚀 Deployment

### Docker Development

```bash
# Build and run
just dev

# With background worker
just worker-dev
```

### Production Build

```bash
# Test production build
just test-build-prod

# Build for deployment
just build-prod

# Deploy
just deploy-latest HOST=your-server.com
```

## 🤝 Contributing

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Follow the development workflow**: See [DEVELOPMENT_WORKFLOW.md](docs/dev/DEVELOPMENT_WORKFLOW.md)
4. **Write tests first**: Reference [TDD_AND_CODEGEN.md](docs/dev/TDD_AND_CODEGEN.md)
5. **Create a PR**: Use templates from [TEMPLATES.md](docs/dev/TEMPLATES.md)
6. **Code review**: Follow the checklist in [TEMPLATES.md](docs/dev/TEMPLATES.md)

### Development Guidelines

- **Test-Driven Development**: Write failing tests before implementation
- **Atomic commits**: One logical change per commit
- **Conventional commits**: `feat(scope): description` format
- **Code generation**: Use framework factories for CRUD operations
- **Documentation**: Update docs for architectural changes

## 📋 Roadmap

- [ ] User authentication and profiles
- [ ] Real-time notifications
- [ ] Admin dashboard
- [ ] API documentation
- [ ] Mobile-responsive design
- [ ] Multi-tenant support
- [ ] Advanced search and filtering
- [ ] Export/import functionality

## 🐛 Issues & Support

- **Framework issues**: Report to [vibetuner](https://github.com/alltuner/vibetuner/issues)
- **Project issues**: Use GitHub Issues with templates from [TEMPLATES.md](docs/dev/TEMPLATES.md)
- **Documentation**: See [AGENTS.md](AGENTS.md) for framework guide

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Framework**: Built on [vibetuner](https://vibetuner.alltuner.com/) - FastAPI + MongoDB + HTMX scaffold
- **UI**: [Tailwind CSS](https://tailwindcss.com/) + [DaisyUI](https://daisyui.com/)
- **Icons**: [Heroicons](https://heroicons.com/)
- **Testing**: [pytest](https://pytest.org/) with custom fixtures
- **Development**: Comprehensive tooling with `uv`, `ruff`, `djlint`, and more

---

**Built with ❤️ using vibetuner framework**

*For detailed development guidance, start with [GETTING_STARTED.md](docs/dev/GETTING_STARTED.md)*
