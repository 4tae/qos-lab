# Day 3 – EC2 Deployment and Cloud Environment Replication

## 📌 Objective

The objective of Day 3 was to replicate the local Docker-based service environment on AWS EC2 to ensure experimental reproducibility in a cloud infrastructure setting.

This step establishes a publicly accessible and controlled environment for upcoming network impairment and load testing experiments.

## 🏗 EC2 Instance Configuration

### Instance Details

- Instance Name: qos-lab-ec2
- AMI: Ubuntu Server 22.04 LTS (x86_64)
- Instance Type: t2.micro (AWS Free Tier eligible)
- Virtualization: HVM
- Storage: Default 8GB gp2

### Key Pair

- Key Type: RSA
- Format: .pem
- Authentication: SSH key-based authentication (no password login)

## 🔐 Security Group Configuration

### Inbound Rules

| Type        | Port | Source     | Purpose                |
|------------|------|------------|------------------------|
| SSH        | 22   | 0.0.0.0/0  | Remote administration  |
| Custom TCP | 8000 | 0.0.0.0/0  | API public access      |

Security considerations:

- SSH access is protected by key-based authentication.
- Password login is disabled by default on Ubuntu.
- No sensitive data or database connections are exposed.
- This configuration balances accessibility and reasonable security for a research environment.

## 🐳 Docker Installation on EC2

### System Update

```
sudo apt update
sudo apt upgrade -y
```

### Docker Installation

```
sudo apt install docker.io -y
sudo systemctl start docker
sudo systemctl enable docker
```

### User Permission Configuration
```
sudo usermod -aG docker ubuntu
```

After updating group permissions, the SSH session was restarted to apply changes.

## 📦 Project Deployment on EC2

### Repository Cloning

```
git clone https://github.com/<your-username>/qos-lab.git
cd qos-lab
```

### Docker Image Build

```
docker build -t qos-lab:latest .
```

### Container Execution

```
docker run -d -p 8000:8000 -e NODE_ID=node-ec2 qos-lab:latest
```

Container status verification:

```
docker ps
```

## 🌍 Public Endpoint Verification

The API was successfully accessed via:

```
http://<EC2_PUBLIC_IP>:8000/health
```

Response:

```
ok
```

This confirms successful deployment and public accessibility of the service.

## 🧠 Research Significance

- Cloud-based replication ensures environmental consistency across experiments.
- Enables realistic latency measurement over public internet routing.
- Prepares infrastructure for network impairment experiments (tc) and load testing (k6).
- Establishes baseline performance in a production-like environment.

## ✅ Day 3 Outcome

- Local Docker environment successfully replicated on AWS EC2
- Public endpoint verified
- Cloud-based experimental infrastructure established

Next step: Baseline latency measurement and network impairment experimentation.
