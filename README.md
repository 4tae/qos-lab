# QoS Lab

Experimental platform to analyze tail latency under network impairment
in containerized distributed systems.

## Features (current stage)

- FastAPI-based HTTP API
- Latency logging middleware
- Failure injection support
- Dockerized environment
- Node identification via environment variable

## Next Steps

- Deploy to EC2
- Apply network impairment (tc)
- Run load tests (k6)
- Analyze P95/P99 behavior
