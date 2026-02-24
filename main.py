import os
import time
import json
import random
import hashlib
from typing import Optional

from fastapi import FastAPI, Response, Query, Request
from fastapi.responses import PlainTextResponse

APP_NAME = "qos-lab-api"
NODE_ID = os.getenv("NODE_ID", "node-local")
READ_BYTES_DEFAULT = int(os.getenv("READ_BYTES_DEFAULT", "65536"))  # 64KB

app = FastAPI(title=APP_NAME)

def now_ms() -> int:
    return int(time.time() * 1000)

def log_event(event: dict) -> None:
    # JSONL (한 줄 = 한 이벤트) 형태로 stdout에 출력 → Docker/EC2에서 수집 용이
    print(json.dumps(event, ensure_ascii=False), flush=True)

@app.middleware("http")
async def log_latency(request: Request, call_next):
    start = time.perf_counter()
    status_code = 500
    try:
        response = await call_next(request)
        status_code = response.status_code
        return response
    finally:
        elapsed_ms = (time.perf_counter() - start) * 1000.0
        log_event({
            "ts_ms": now_ms(),
            "node_id": NODE_ID,
            "method": request.method,
            "path": request.url.path,
            "query": str(request.url.query),
            "status": status_code,
            "latency_ms": round(elapsed_ms, 3),
        })

@app.get("/health", response_class=PlainTextResponse)
def health():
    return "ok"

@app.get("/read")
def read(n: int = Query(default=READ_BYTES_DEFAULT, ge=1, le=5_000_000)):
    """
    가벼운 I/O 흉내: 메모리에서 n bytes 생성 후 해시 계산.
    (실제 디스크 읽기 대신, 환경 차이를 줄이고 CPU+메모리 비용만 일정하게 주려는 목적)
    """
    data = os.urandom(n)
    digest = hashlib.sha256(data).hexdigest()
    return {"node_id": NODE_ID, "bytes": n, "sha256": digest}

@app.get("/work")
def work(
    ms: int = Query(default=10, ge=0, le=5000),
    jitter: int = Query(default=0, ge=0, le=2000),
    fail_prob: float = Query(default=0.0, ge=0.0, le=1.0),
):
    """
    연구 실험용 엔드포인트:
    - ms: 처리 지연(바쁜 대기)로 서버-side latency를 인위적으로 만들기
    - jitter: 0~jitter 범위 랜덤 추가 지연
    - fail_prob: 확률적으로 500 오류 발생 (부분 장애/오류율 실험용)
    """
    if fail_prob > 0 and random.random() < fail_prob:
        return Response(content="injected failure", status_code=500)

    extra = random.randint(0, jitter) if jitter > 0 else 0
    target = ms + extra

    # 바쁜 대기(busy-wait): CPU를 실제로 소모 → 노드 불균형/부하 상황에서 tail 관찰에 유리
    end = time.perf_counter() + (target / 1000.0)
    x = 0
    while time.perf_counter() < end:
        x += 1

    return {"node_id": NODE_ID, "target_ms": target, "spin": x}