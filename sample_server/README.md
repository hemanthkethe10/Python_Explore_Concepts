# Echo Server with TLS

Simple FastAPI server that echoes request details, with Caddy for TLS termination.

## Setup

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Place your TLS certificates:
   - `echo.pem` and `echo-key.pem` in `/etc/caddy/certs/` (or update Caddyfile path)

3. Add to `/etc/hosts`:
```
127.0.0.1 echo.lab.local
```

## Running

Start FastAPI server:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

Start Caddy (in another terminal):
```bash
caddy run --config Caddyfile
```

## Testing

```bash
curl https://echo.lab.local/anything
curl -X POST https://echo.lab.local/anything -d '{"test": "data"}'
```

The `/anything` endpoint echoes back:
- HTTP method
- URL
- Headers
- Query parameters
- Request body
- Client IP
