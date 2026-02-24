# QoS Lab
### Experimental Platform for Tail Latency Analysis under Network Impairment

---

## 📌 Overview

QoS Lab is an experimental platform designed to analyze how network QoS degradation (delay, loss, jitter) affects tail latency (P95/P99) in containerized distributed systems.

This project focuses on measuring and analyzing latency behavior under controlled network conditions using a reproducible Docker-based environment.

The goal is to move beyond average latency and investigate tail amplification phenomena in heterogeneous distributed environments.

---

## 🎯 Research Objective

- Analyze the impact of network delay, loss, and jitter on service latency
- Evaluate tail latency behavior (P95, P99) under varying QoS conditions
- Investigate performance degradation in round-robin load-balanced environments
- Provide a reproducible experimental infrastructure

---

## 🏗 Architecture (Current Stage)

Client  
↓  
FastAPI Service (Docker Container)  
↓  
Latency Logging Middleware  
↓  
JSON Structured Logs  

### Planned Experimental Architecture

Client  
↓  
k6 Load Generator  
↓  
tc Network Impairment  
↓  
Nginx Load Balancer (Round Robin)  
↓  
Multiple Docker Nodes  
↓  
Latency & Statistical Analysis  

---

## ⚙️ Features (Implemented)

- FastAPI-based HTTP API  
- Latency measurement middleware  
- Structured JSON logging  
- Failure injection support  
- CPU workload simulation  
- Dockerized environment  
- Node identification via environment variables  

---

## 🔬 Endpoints

### `/health`
Basic health check endpoint.

### `/read`
Simulates controlled CPU and memory workload.

### `/work`
Experimental endpoint supporting:
- Configurable processing delay  
- Jitter injection  
- Failure probability injection  

Example (local execution):

```
http://localhost:8000/work?ms=50&jitter=20&fail_prob=0.01
```

---

## 🐳 Docker Usage

### Build Image


```
docker build -t qos-lab:latest .
```

### Run Container

```
docker run -p 8000:8000 -e NODE_ID=node1 qos-lab:latest
```

Then access:

```
http://localhost:8000/health
```

---

## 📊 Research Focus (Upcoming Work)

- EC2 deployment for reproducible cloud experiments  
- Network impairment using `tc netem`  
- Load testing with `k6`  
- Statistical analysis (Mean, Median, P95, P99)  
- Tail amplification ratio analysis  
- Heterogeneous node experiments  
- Partial failure experiments  

---

## 📈 Key Concepts

- Tail Latency  
- QoS Degradation  
- Network Impairment  
- Distributed Systems  
- Round Robin Load Balancing  
- Experimental Reproducibility  

---

## 🧪 Project Status

Current Progress (Day 1–2):
- Local API implementation  
- Docker containerization  
- GitHub repository setup  

Deployment and network experimentation in progress.

---

## 📌 Author

Undergraduate research project  
Focused on distributed systems and QoS experimentation