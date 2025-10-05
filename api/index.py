from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import json

app = FastAPI()

# Enable CORS for POST from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["*"],
)

@app.post("/api/latency")
async def latency_metrics(request: Request):
    body = await request.json()
    regions = body.get("regions", [])
    threshold = body.get("threshold_ms", 180)

    # Load telemetry data
    with open("q-vercel-latency.json") as f:
        telemetry = json.load(f)

    result = {}
    for region in regions:
        records = telemetry.get(region, [])
        latencies = [r["latency_ms"] for r in records]
        uptimes = [r["uptime"] for r in records]
        breaches = sum(1 for r in records if r["latency_ms"] > threshold)

        result[region] = {
            "avg_latency": round(np.mean(latencies), 2),
            "p95_latency": round(np.percentile(latencies, 95), 2),
            "avg_uptime": round(np.mean(uptimes), 2),
            "breaches": breaches
        }

    return result
