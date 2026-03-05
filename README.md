# 🛡️ Ez-Lab: Zero Trust Hybrid Cloud Infrastructure

![Status](https://img.shields.io/badge/Status-Production-green?style=flat-square)
![Docker](https://img.shields.io/badge/Infrastructure-Docker_Compose-blue?style=flat-square&logo=docker)
![Security](https://img.shields.io/badge/Security-Zero%20Trust-red?style=flat-square&logo=cloudflare)
![Hardware](https://img.shields.io/badge/Hardware-RPi_5-C51A4A?style=flat-square&logo=raspberrypi)

## 🚀 Project Overview

**Ez-Lab** is a cloud-native home laboratory designed to simulate a production environment on a **Raspberry Pi 5**. The goal was to build a resilient, secure, and automated infrastructure for media streaming, observability, and self-hosting, strictly following **DevSecOps** and **SRE** principles.

This project solves the challenge of accessing local services behind an ISP CGNAT without exposing public ports, utilizing a **Cloudflare Zero Trust** tunnel and automated Python scripting for telemetry.

## 🏗️ Architecture

The system follows a microservices architecture orchestrated by Docker Compose with **Network Segmentation**.

```mermaid
graph TD
    %% Custom Colors (SRE Dark Theme)
    classDef internet fill:#16161e,stroke:#7aa2f7,stroke-width:2px,color:#c0caf5
    classDef cf fill:#f6821f,stroke:#fff,stroke-width:2px,color:#fff,font-weight:bold
    classDef daemon fill:#1a1b26,stroke:#7aa2f7,stroke-width:2px,color:#c0caf5
    classDef app fill:#292e42,stroke:#9ece6a,stroke-width:2px,color:#c0caf5
    classDef media fill:#292e42,stroke:#bb9af7,stroke-width:2px,color:#c0caf5
    classDef hw fill:#16161e,stroke:#f7768e,stroke-width:2px,color:#c0caf5
    classDef alert fill:#16161e,stroke:#e0af68,stroke-width:2px,color:#c0caf5

    User((🌐 Internet)):::internet -->|HTTPS / SSL| Cloudflare{☁️ Cloudflare Edge}:::cf
    Cloudflare -->|Encrypted Tunnel| Cloudflared[🛡️ Cloudflared Daemon]:::daemon
    
    subgraph "Ez-Lab (RPi 5 Cluster)"
        Cloudflared -->|web-net| Frontend["🖥️ Portfolio (Hugo/Nginx)"]:::app
        Cloudflared -->|web-net| Backend["⚙️ API Telemetry (Go)"]:::app
        Cloudflared -->|media-net| Portainer["🐳 Portainer"]:::app
        
        Frontend -.->|Internal API Call| Backend
        
        subgraph "Media Segment (Isolated)"
            ArrStack["🎬 *Arr Suite"]:::media
            Jellyfin["🍿 Jellyfin"]:::media
        end
        
        Auditor["🐍 Python Auditor"]:::hw -->|Telemetry| OS[("🌡️ Kernel / Sensors")]:::hw
        Auditor -->|Alerts| Telegram["📱 Telegram API"]:::alert
    end
    
    ArrStack -->|IO| HDD[("💾 External Storage")]:::hw
```

## 🛠️ Tech Stack

* **Hardware:** Raspberry Pi 5 (4GB RAM) + NVMe/SSD Storage.
* **OS:** Debian Bookworm (Headless / Hardened).
* **Orchestration:** Docker Compose (Infrastructure as Code).
* **Networking:** Cloudflare Tunnels (Zero Trust) + Tailscale VPN.
* **Services:**
    * **Web/API:** Nginx, Hugo, Golang (REST API).
    * **Media:** *Arr Suite, Jellyfin, Samba.
    * **Observability (The SRE Stack):** Prometheus, Grafana, Loki, Promtail, Uptime Kuma.

## 💡 Key Challenges & Solutions (SRE Journal)

### 1. The CGNAT Barrier (Bypass Architecture)
**Challenge:** My ISP uses CGNAT, making traditional Port Forwarding impossible.
**Solution:** Implemented **Cloudflare Tunnels**. A lightweight daemon (`cloudflared`) creates an outbound-only encrypted connection to the Edge, allowing secure access via HTTPS without exposing public IPs.

### 2. Network Segmentation
**Challenge:** Preventing a vulnerability in the Media stack from affecting the Public Portfolio.
**Solution:** Implemented Docker Networks (`web-net` for public services, `media-net` for internal operations).

### 3. The "Black Box" Problem (Enterprise Observability)
**Challenge:** Lack of visibility into real-time metrics, logs, and external uptime.
**Solution:** Retired basic Python telemetry scripts and deployed an industry-standard observability stack.
* **Metrics:** Prometheus scrapes hardware data via Node Exporter.
* **Logs:** Loki & Promtail aggregate container logs centrally, eliminating SSH manual debugging.
* **Visualization & Alerting:** Grafana visualizes the cluster and triggers Webhooks (Telegram) on critical thresholds (CPU > 75°C, Disk > 85%).
* **Blackbox Monitoring:** Uptime Kuma constantly pings the public endpoints to verify 99.9% availability and SSL certificate health.

## 📦 How to Run

1. **Prerequisite:** You must build the Portfolio images locally first (since they live in a separate repo).
   ```bash
   # Clone the Application Repo
   git clone [https://github.com/ezequieldlv/portfolio-sre](https://github.com/ezequieldlv/portfolio-sre)
   cd portfolio-sre
   
   # Build the Images (Manual Step)
   docker build -t ez-backend:v1 ./backend
   docker build -t ez-portfolio:v4 ./frontend
   ```

2. **Deploy Infrastructure:**
   Clone this repo and deploy:
   ```bash
   cd ez-lab/docker
   docker compose up -d
   ```

## 📂 Repository Structure

* `/docker`: Main `docker-compose.yml` and `.env` file.
* `/docker/scripts`:
    * `auditor.py`: Python telemetry script.
    * `requirements.txt`: Python dependencies.

---
*Built with ❤️ and ☕ by Ez. Hosted on a Raspberry Pi 5.*