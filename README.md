# Mountain Tracker

A small Flask web app for the DevOps assignment.

## Features
- Search mountains by country
- View mountain name, location and elevation
- Leave and view reviews
- `/health` endpoint for smoke testing

## Local setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python run.py
```

## Tests
```bash
pytest
```

## Pipeline design
- Pull request: run automated tests
- Push to `main`: deploy infrastructure and app
- Post-deploy smoke test: call `/health`

## Notes
The Terraform files are a starter scaffold and need real AWS values before deployment.
