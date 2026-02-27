from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import json

app = FastAPI(title="Echo Server")

@app.get("/anything")
@app.post("/anything")
@app.put("/anything")
@app.delete("/anything")
@app.patch("/anything")
async def echo_anything(request: Request):
    """Echo back request details similar to httpbin"""
    body = None
    try:
        raw_body = await request.body()
        if raw_body:
            body_str = raw_body.decode('utf-8')
            try:
                body = json.loads(body_str)
            except json.JSONDecodeError:
                body = body_str
    except Exception:
        pass
    
    return JSONResponse({
        "method": request.method,
        "url": str(request.url),
        "headers": dict(request.headers),
        "args": dict(request.query_params),
        "data": body,
        "origin": request.client.host if request.client else None,
    })

@app.get("/health")
async def health():
    return {"status": "ok"}
