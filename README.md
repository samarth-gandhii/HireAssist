# HireAssist

Intelligent Candidate Screening & Management — a lightweight Django-based resume manager to upload, analyze, rank, and manage candidate resumes and hired employees.

## Features
- Upload and store PDF/Word resumes
- Derive candidate name from uploaded filename
- View uploaded resumes and quick stats
- Manage hired employees with skills and score fields
- Simple Bootstrap-based UI

## Tech stack
- Python 3.8+ (recommended)
- Django
- SQLite (default DB used in repo)
- Bootstrap for front-end styling

## Repository structure (important files)
- `manage.py` — Django management entry point
- `hireassit/` — project settings and URL configuration
- `resume_manager/` — main application (models, views, templates)
- `templates/resume_manager/` — UI templates (homepage, upload, list, login, signup)
- `db.sqlite3` — default SQLite database (created after migrations)

## Prerequisites
- Python 3.8 or newer
- pip
- (Optional but recommended) virtual environment (`venv`)

## Quick setup (Windows PowerShell)
Run these commands from the project root (for your workspace this is `d:\web prog\hireassit`).

```powershell
# (optional) Create and activate a virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Upgrade pip and install requirements
python -m pip install --upgrade pip
# If you don't have a requirements file, install Django
pip install django

# Apply database migrations
python manage.py migrate

# Create a superuser (follow prompts)
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

Open http://127.0.0.1:8000/ in your browser and log in with the superuser credentials.

## Local development notes
- Uploaded resumes are stored using Django's default file storage. Check `hireassit/settings.py` for `MEDIA_ROOT`/`MEDIA_URL` if you change storage.
- The `Resume.candidate_name()` method currently extracts the candidate name using string splitting on `/` and `.`; this can strip parts of names when filenames include dots. Consider using `os.path.basename` and `os.path.splitext` for a safer implementation.

## Common tasks
- Run tests:

```powershell
python manage.py test
```

- Collect static files (for production):

```powershell
python manage.py collectstatic
```

## Deploying (notes)
This project is configured for local development. For production deployments consider:
- Using a production database (Postgres, MySQL)
- Proper static and media hosting (S3, CDN)
- Serving with Gunicorn/Uvicorn behind Nginx
- Setting `DEBUG = False` and configuring secret keys in `hireassit/settings.py`

## Suggested improvements
- Improve `candidate_name()` to handle multiple dots and edge cases (use `os.path` helpers)
- Add resume text extraction and NLP skill parsing
- Add pagination and search for the resume lists
- Add more unit tests (parsing, ranking logic)

## Contributing
1. Fork the repository
2. Create a feature branch
3. Add changes and tests
4. Open a pull request with a description of changes

## License
Add a `LICENSE` file to declare the project's license if you plan to publish it.

---
If you'd like, I can also:
- Add a `requirements.txt` with pinned deps
- Patch `resume_manager/models.py` to use `os.path` for safer filename parsing
- Add a short script to create a demo superuser

Tell me which of those you'd like next.
