# Issues Fixed

This file lists all the issues that have been identified and fixed in the CloudOps Ninja project.

## Format
- **Issue**: Brief description of the issue
- **Date Fixed**: When it was resolved
- **Fix**: What was done to resolve it
- **Files Changed**: Relevant files modified

## Fixed Issues

### Issue #1: Missing CI workflow reference
- **Issue**: README referenced .github/workflows/deploy.yml but the file was missing from the repository.
- **Date Fixed**: 2026-04-10
- **Fix**: Created the missing GitHub Actions workflow file with CI/CD pipeline for automated deployment.
- **Files Changed**: .github/workflows/deploy.yml

### Issue #2: Add database integration for persistent storage
- **Issue**: Currently using in-memory storage for deployments and servers. Data was lost on app restarts.
- **Date Fixed**: 2026-04-10
- **Fix**: Implemented SQLite database using Flask-SQLAlchemy. Created Deployment and Server models. Updated all routes to use database queries instead of in-memory lists/dicts. Added database initialization with default server data.
- **Files Changed**: backend/app.py, backend/requirements.txt

### Issue #3: Implement user authentication
- **Issue**: Dashboard was not secured, anyone could access it without login.
- **Date Fixed**: 2026-04-10
- **Fix**: Added Flask-Login for session management. Created User model with hashed passwords. Added login/logout routes with forms. Protected dashboard and deployment routes with @login_required. Added default admin user (admin/password). Updated dashboard to show current user and logout link.
- **Files Changed**: backend/app.py, backend/requirements.txt

### Issue #4: Integrate with Prometheus for real metrics
- **Issue**: App was using mock/hardcoded metrics instead of real Prometheus metrics.
- **Date Fixed**: 2026-04-10
- **Fix**: Implemented proper Prometheus instrumentation with Counter and Gauge metrics. Added /metrics endpoint for Prometheus scraping. Metrics are now updated in real-time when deployments occur and initialized from database on startup. Replaced mock data with actual metric objects.
- **Files Changed**: backend/app.py

