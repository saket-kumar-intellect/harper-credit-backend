# Harper Credit Backend

A Django + DRF project with a health check endpoint.

## Setup

1. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run migrations:
   ```bash
   python manage.py migrate
   ```

4. Start the development server:
   ```bash
   python manage.py runserver
   ```

## Health Check

Visit `http://localhost:8000/health/` to check the API health status.

The endpoint returns:
```json
{
  "ok": true,
  "version": "1.0.0",
  "commit": "unknown"
}
```

## Environment Variables

- `VERSION`: Set the application version (default: "1.0.0")
- `COMMIT`: Set the git commit hash (default: "unknown")
