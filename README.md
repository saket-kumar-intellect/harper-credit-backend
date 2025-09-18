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

## Observability

### Request ID propagation

- Header: `X-Request-ID`
- Behavior: If a client sends `X-Request-ID`, the same value is attached to `request.request_id` and echoed back in the response header. If absent, a UUID is generated server-side and echoed.

### JSON access logs

Each request emits exactly one JSON log line at INFO level with fields:

- `timestamp` (ISO-8601 UTC)
- `level`
- `logger` ("access")
- `method`, `path`, `status_code`, `duration_ms`
- `request_id`
- `client_ip`, `user_agent` (best-effort)

Logs are written to stdout by default.

### JSON error responses

In non-DEBUG mode, error responses are compact JSON with schema:

```
{
  "request_id": "...",
  "status": 404,
  "error": "NotFound",
  "message": "The requested resource was not found",
  "details": {"field": ["validation errors..."]}
}
```

Status codes covered consistently: 400, 404, 500.

## Local testing

Header auto-generation:

```
curl -i http://127.0.0.1:8000/health/
```

Header echo:

```
curl -i http://127.0.0.1:8000/health/ -H "X-Request-ID: demo-req-123"
```

JSON error (404):

```
curl -i http://127.0.0.1:8000/does-not-exist
```

JSON error (400):

```
curl -i -X POST http://127.0.0.1:8000/api/applications -H "Content-Type: application/json" -d '{}'
```

You should also see one JSON access log line per request in the server terminal.

## Validation & Normalization

- Names: `first_name` and `last_name` are trimmed (leading/trailing whitespace removed).
- `middle_name` may be null or omitted. If provided as a string, it is trimmed; if it becomes empty after trimming, it is stored as null.
- Email must be unique. Duplicate emails return a `400` with a JSON validation error on `applicant.email`.
- Other field validations remain as-is.
