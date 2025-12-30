# CrawJUD - Copilot Instructions

## Project Overview

CrawJUD is a Brazilian judicial automation backend system that provides web scraping, document processing, and task management capabilities for various Brazilian court systems (PJE, ESAJ, Projudi, elaw, etc.). The project uses Flask for REST API, Celery for async task processing, and Selenium for web automation.

**Repository Size**: ~120MB | **Python Files**: 215 files | **Lines of Code**: ~30,000+ lines
**Python Version**: 3.14 (specified in `.python-version` as 3.14t - GIL-free mode)

## Tech Stack

- **Backend Framework**: Flask 3.1.2 with SocketIO for real-time communication
- **Task Queue**: Celery 5.5.3 with Redis broker
- **Database**: PostgreSQL via SQLAlchemy 2.0.43 + pg8000
- **Web Automation**: Selenium 4.36.0 with selenium-wire
- **Configuration**: Dynaconf for multi-environment settings
- **Security**: JWT authentication, Passlib (Argon2/bcrypt), PyKeePass for credential management
- **Storage**: MinIO for object storage
- **Package Manager**: uv (modern Python package manager)

## Critical: Always Follow Language-Specific Instructions

**BEFORE making ANY code changes**, verify the file language and consult `.github/instructions/`:

- Python files: `.github/instructions/doc-python.instructions.md`
- JavaScript/TypeScript: `.github/instructions/doc-javascript.instructions.md`
- Markdown docs: `.github/instructions/doc-markdown.instructions.md`

## Environment Setup & Installation

### 1. Install uv Package Manager (Required)

```bash
pip install uv
```

### 2. Install Dependencies

```bash
# Production dependencies (takes ~2-3 minutes)
uv sync --no-dev

# With development dependencies
uv sync
```

**IMPORTANT**: This creates a `.venv` virtual environment. Always activate it before running commands:

```bash
source .venv/bin/activate
```

> Disclaimer: If windows, run:
>
> ```powershell
>
> & ".\.venv\Scripts\activate"
>
> ```

### 3. Install Linting Tools

```bash
uv pip install ruff  # Required for code quality checks
```

## Configuration Requirements

**Before running the application**, you MUST create secret configuration files:

1. **`.secrets.flask.yaml`** - Main Flask secrets (see `backend/config/secret-flask.template.md`)

   - Database URI (PostgreSQL)
   - SECRET_KEY, JWT tokens
   - Redis/Celery broker URL
   - CORS origins
   - Email config (Flask-Mail)
   - MinIO credentials
   - Root user credentials

2. **`.secrets.celery.yaml`** - Celery worker secrets (see `backend/config/secret-celery.template.md`)

3. **`.env`** - Environment variables (gitignored)
   - FLASK_PORT (default: 5000)
   - REDIS_PASSWORD

The app will fail on import if these files don't exist. For testing code changes without full setup, mock or skip config loading.

## Linting & Code Quality

### Run Linting (Always Before Committing)

```bash
# Check for issues (fast: ~0.03s)
ruff check backend

# Auto-fix safe issues
ruff check backend --fix

# Check formatting (fast: ~0.02s)
ruff format --check backend

# Apply formatting
ruff format backend
```

### Common Linting Warnings to Ignore

- **D203/D211 incompatibility**: Expected (docstring style conflict)
- **D212/D213 incompatibility**: Expected (multi-line summary conflict)
- **COM812 with formatter**: Expected (trailing comma conflict)

### Expected Errors (84 total as of baseline)

- 41x E501 (line too long) - mostly docstrings
- 13x BLE001 (blind except) - intentional in bot error handling
- 8x ANN002/ANN003 (missing type annotations for \*args/\*\*kwargs)
- 4x F821 (undefined name) - in incomplete code blocks
- Various FURB101/103 (Path.open suggestions) - can be fixed

**DO NOT introduce new linting errors**. Run `ruff check backend` after changes.

## Project Structure

```
backend/
├── __init__.py, __main__.py    # Entry point with Typer CLI
├── _hook.py                     # Custom import hooks for JSON/legacy modules
├── api/                         # Flask REST API
│   ├── __init__.py             # Flask app factory (create_app)
│   ├── routes/                 # API endpoints (bot, admin, auth, status)
│   ├── decorators/             # CORS, auth, logging decorators
│   ├── _forms/                 # Request validation forms
│   ├── base/                   # SQLAlchemy base classes
│   └── resources/              # Shared API resources
├── task_manager/               # Celery tasks
│   ├── bots/                   # Court automation bots
│   │   ├── admin/              # Administrative tasks
│   │   ├── buscadores/         # Case search bots
│   │   ├── calculadoras/       # Court fee calculators
│   │   ├── capa/               # Case cover page extractors
│   │   ├── emissao/            # Document issuance
│   │   ├── habilitacao/        # Lawyer registration
│   │   ├── intimacoes/         # Notifications/summons
│   │   ├── movimentacao/       # Case movement tracking
│   │   ├── protocolo/          # Filing/submission bots
│   │   └── provisionamento/    # Provisioning tasks
│   ├── tasks/                  # Celery task definitions
│   └── extensions/             # Celery-specific extensions
├── models/                      # SQLAlchemy models (User, JWT, Bot)
├── resources/                   # Reusable components
│   ├── driver/                 # Selenium WebDriver wrappers
│   ├── auth/                   # Authentication helpers
│   ├── keystore/               # Certificate/keystore management
│   ├── formatadores.py         # Data formatters
│   └── assinador.py            # Digital signature tools
├── controllers/                 # Court-specific controllers (PJE, ESAJ, Projudi)
├── extensions/                  # Flask extensions (MinIO, DB)
├── config/                      # Settings and configuration
│   ├── settings.yaml           # Base configuration
│   └── _interfaces.py          # Config type definitions
├── interfaces/                  # Data interfaces/schemas
├── types_app/                   # Type definitions
└── utilities/                   # Helper functions

data/                            # IP2Location database
docs/                            # Auto-generated documentation
chrome-extensions/               # Browser extensions (keepass, websigner)
```

## Running the Application

### CLI Commands (via Typer)

```bash
# Run API server only
python -m backend api

# Run Celery worker only
python -m backend celery
```

**Note**: Both commands run indefinitely. API runs on `localhost:5000` (or FLASK_PORT from .env).

### Docker Compose Services

```bash
# Start Redis (required for Celery)
docker-compose up -d redis
```

Redis runs on port 6380 (host) → 6379 (container) with password from `.env`.

## Testing

**No automated test suite exists**. Testing strategy:

1. Manually validate code changes by running the affected bot/endpoint
2. Check for import errors: `python -c "import backend"`
3. Lint with ruff before committing
4. Test API endpoints with curl/Postman if modifying routes
5. For bot changes, run the specific bot task through Celery

## Common Development Patterns

### Adding New Bot

1. Create module in `backend/task_manager/bots/<category>/<court_system>/`
2. Inherit from appropriate controller (`backend/controllers/<court>.py`)
3. Use `backend/resources/driver/` for Selenium operations
4. Define task in `backend/task_manager/tasks/`
5. Register with Celery

### Adding API Endpoint

1. Create route in `backend/api/routes/<category>/`
2. Use decorators from `backend/api/decorators/` (CORS, JWT)
3. Use forms from `backend/api/_forms/` for validation
4. Register in `backend/api/routes/__init__.py`

### Working with Selenium

- Use `WebElement` wrapper from `backend/resources/driver/web_element.py`
- Element locators in `backend/resources/elements/<court>.py`
- Driver management in `backend/resources/driver/`

## Key Configuration Files

- **pyproject.toml**: Dependencies, project metadata (requires Python >=3.14)
- **uv.lock**: Locked dependency versions (like requirements.lock)
- **ruff.toml**: Linter configuration (line-length: 89, select: ALL with ignores)
- **.pre-commit-config.yaml**: Git hooks (ruff check + format)
- **pyrightconfig.json**: Type checker config (currently disabled)
- **.coveragerc**: Coverage config (omits bot/utils/routes)
- **.editorconfig**: Editor settings (4-space indent for Python)

## Important Notes

1. **Python 3.14t (GIL-free)**: May see GIL warnings when importing non-GIL-safe modules like `_brotli`. This is expected.

2. **No Tests**: Don't create test files unless explicitly requested. Focus on manual validation.

3. **Secret Files**: Never commit `.secrets.*.yaml` or `.env` files (gitignored).

4. **Selenium Bots**: Require Chrome/ChromeDriver setup. Use `webdriver-manager` for auto-installation.

5. **Database Migrations**: No migration system detected. Schema changes require manual SQL or recreation.

6. **CORS**: Configured per-endpoint with `@CrossDomain` decorator. Origins in `.secrets.flask.yaml`.

7. **Logging**: Uses Python logging + Rich console. Bot tasks emit to SocketIO for real-time UI updates.

8. **File Uploads**: Max 5GB (`MAX_CONTENT_LENGTH: 5368709120` in settings.yaml)

## Troubleshooting

**Import errors on `backend` module**: Ensure `.venv` is activated and `uv sync` completed.

**"ModuleNotFoundError: No module named 'celery'"**: Run `uv sync` (not just `pip install`).

**App won't start**: Check for `.secrets.flask.yaml` and `.secrets.celery.yaml`. See templates in `backend/config/`.

**Ruff warnings about D203/D212**: Ignore (configuration conflict, not an error).

**Git force push disabled**: Never use `git reset` or `git rebase`. Use additive commits only.

## Validation Checklist Before PR

1. ✅ Run `ruff check backend --fix` - resolve new errors
2. ✅ Run `ruff format backend` - ensure consistent formatting
3. ✅ Test imports: `python -c "import backend"`
4. ✅ Check docstrings follow `.github/instructions/doc-python.instructions.md`
5. ✅ No secrets in code or committed files
6. ✅ No new blind except without justification
7. ✅ Type annotations on new functions (avoid `Any`, use `AnyType = any` alias)

---

**Trust these instructions.** Only search codebase if info is incomplete or incorrect.
