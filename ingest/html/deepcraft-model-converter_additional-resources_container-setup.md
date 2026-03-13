---
source_url: "https://developer.imagimob.com/deepcraft-model-converter/additional-resources/container-setup"
fetched_at: "2026-03-10T15:52:08Z"
title: "Container Setup"
content_format: "markdown"
tags: ["deepcraft", "checked-url", "web-mirror", "deepcraft-model-converter", "additional-resources", "container-setup"]
---

# Container Setup

## Setup and Run the PyTorch to TFLite Converter API with Docker or Podman

This section explains how to set up and run the PyTorch to TFLite Converter API using the public container image `public.ecr.aws/j3h0k9w0/imagimob/pytorch-converter:latest`

### Key Steps at a Glance

This section covers the following sub-sections:

- - **[Prerequisites](https://developer.imagimob.com/deepcraft-model-converter/additional-resources/container-setup#prerequisites)**
- - **[Running the API Container](https://developer.imagimob.com/deepcraft-model-converter/additional-resources/container-setup#running-the-api-container)**
- - **[Network Configuration](https://developer.imagimob.com/deepcraft-model-converter/additional-resources/container-setup#network-configuration)**
- - **[Container Management](https://developer.imagimob.com/deepcraft-model-converter/additional-resources/container-setup#container-management)**
- - **[Troubleshooting](https://developer.imagimob.com/deepcraft-model-converter/additional-resources/container-setup#troubleshooting)**

### Prerequisites

#### Install Docker or Podman

|  | **Docker** | **Podman** |
| --- | --- | --- |
| **Installation Guide** | <https://docs.docker.com/get-docker/> | <https://podman.io/getting-started/installation> |
| **Windows** | Docker Desktop or Docker Engine on WSL2 | Docker Engine via package manager |
| **macOS** | Docker Desktop or via Homebrew | via Homebrew (`brew install podman`) |
| **Linux** | Docker Engine via package manager | via package manager (`apt install podman` or `dnf install podman`) |

### Running the API Container

If you are running Podman on Windows or macOS, ensure the Podman Linux machine is initialized and started. For guidance on creating and starting the machine, see the official Podman documentation.

#### Quick Start Commands

Below are the commands to run the API Containers:

##### Using Docker

```
# Run on localhost only (single machine access)
docker run -d \
  --name pytorch-converter \
  -p 127.0.0.1:8000:8000 \
  public.ecr.aws/j3h0k9w0/imagimob/pytorch-converter:latest

# Run on all interfaces (local network access)
docker run -d \
  --name pytorch-converter \
  -p 8000:8000 \
  public.ecr.aws/j3h0k9w0/imagimob/pytorch-converter:latest
```

##### Using Podman

```
# Run on localhost only (single machine access)
podman run -d \
  --name pytorch-converter \
  -p 127.0.0.1:8000:8000 \
  public.ecr.aws/j3h0k9w0/imagimob/pytorch-converter:latest

# Run on all interfaces (local network access)
podman run -d \
  --name pytorch-converter \
  -p 8000:8000 \
  public.ecr.aws/j3h0k9w0/imagimob/pytorch-converter:latest
```

#### Advanced Configuration

Below are the commands to set the advanced configuration for the containers:

##### Docker with Resource Limits

```
# Create a temporary directory for file processing
mkdir -p ./tmp

# Run with resource limits, health checks, and auto-restart
docker run -d \
  --name pytorch-converter \
  --memory="4g" \
  --cpus="2.0" \
  -p 8000:8000 \
  -v $(pwd)/tmp:/app/tmp \
  --restart unless-stopped \
  --health-cmd="curl -f http://localhost:8000/health || exit 1" \
  --health-interval=30s \
  --health-timeout=10s \
  --health-retries=3 \
  --health-start-period=40s \
  public.ecr.aws/j3h0k9w0/imagimob/pytorch-converter:latest
```

##### Podman with Resource Limits

```
# Create a temporary directory for file processing
mkdir -p ./tmp

# Run with resource limits and auto-restart (rootless)
podman run -d \
  --name pytorch-converter \
  --memory="4g" \
  --cpus="2.0" \
  -p 8000:8000 \
  -v $(pwd)/tmp:/app/tmp:Z \
  --restart unless-stopped \
  --health-cmd="curl -f http://localhost:8000/health || exit 1" \
  --health-interval=30s \
  --health-timeout=10s \
  --health-retries=3 \
  --health-start-period=40s \
  public.ecr.aws/j3h0k9w0/imagimob/pytorch-converter:latest
```

### Network Configuration

You can select either of the following network configuration: **Single Machine Access** or **Local Network Access**.

#### Single Machine Access (Localhost Only)

Only the machine running the container can access the API.

**Configuration**

```
# Bind to localhost only
-p 127.0.0.1:8000:8000
```

**Access URLs:**

- - <http://localhost:8000>
- - <http://127.0.0.1:8000>

#### Local Network Access

Other devices on your local network can access the API.

**Configuration:**

```
# Bind to all interfaces
-p 8000:8000
```

**Access URLs:**

- - <http://localhost:8000> (from the host machine)
- - http://[MACHINE\_IP]:8000 (from other devices on the network - replace [MACHINE\_IP] with your actual IP address)

Ensure that the assigned ports (8000) are accessible on your network if you want to host the container on a different machine than the one that will use it. You may need to configure your firewall or network settings to allow local incoming connections on the specified port (do not attempt without proper network/infrastructure knowledge and permissions, exposing ports to the internet can create vulnerabilities).

### Container Management

#### Basic Commands

Following are the basic commands for the Docker and Podman:

1. - **Start/Stop Container**

```
# Docker
docker start pytorch-converter
docker stop pytorch-converter
docker restart pytorch-converter

# Podman
podman start pytorch-converter
podman stop pytorch-converter
podman restart pytorch-converter
```

1. - **Check Container Status**

```
# Docker
docker ps                    # Running containers
docker ps -a                 # All containers
docker logs pytorch-converter # View logs

# Podman
podman ps                    # Running containers
podman ps -a                 # All containers
podman logs pytorch-converter # View logs
```

1. - **Remove Container**

```
# Docker
docker stop pytorch-converter
docker rm pytorch-converter

# Podman
podman stop pytorch-converter
podman rm pytorch-converter
```

1. - **Update Container Image**

```
# Docker
docker pull public.ecr.aws/j3h0k9w0/imagimob/pytorch-converter:latest
docker stop pytorch-converter
docker rm pytorch-converter
# Then run the container again with the new image

# Podman
podman pull public.ecr.aws/j3h0k9w0/imagimob/pytorch-converter:latest
podman stop pytorch-converter
podman rm pytorch-converter
# Then run the container again with the new image
```

### Troubleshooting

#### Common Issues

Listed below are some common issues:

1. - **Container is not starting**

```
# Check container logs
docker logs pytorch-converter
# or
podman logs pytorch-converter

# Common causes:
# - Port already in use
# - Insufficient memory
# - Permission issues
```

1. - **Port already in Use**

```
# Find what's using port 8000
# Windows
netstat -ano | findstr :8000

# Linux/macOS
lsof -i :8000
netstat -tulpn | grep :8000

# Solution: Use a different port
docker run -p 8080:8000 public.ecr.aws/j3h0k9w0/imagimob/pytorch-converter:latest
```

1. - **Cannot Pull Image**

```
# Test connectivity
docker pull hello-world

# If ECR pull fails, try:
# 1. Check internet connection
# 2. Check if behind corporate firewall
# 3. Verify image URL
```

1. - **Network Connectivity Issues**

```
# Test network connectivity from container
docker exec pytorch-converter curl -I http://google.com

# Check container network settings
docker inspect pytorch-converter | grep -A 20 "NetworkSettings"
```

1. - **Volume Mount Issues**

```
# Check volume permissions (Linux)
ls -la ./tmp

# If using SELinux (RHEL/CentOS/Fedora), use :Z flag
podman run -v $(pwd)/tmp:/app/tmp:Z ...

# Create directory if it doesn't exist
mkdir -p ./tmp
```

#### Performance Optimization

Listed below are some performance optimization issues:

1. - **Resource Allocation**

```
# Monitor container resource usage
docker stats pytorch-converter

# Adjust memory and CPU limits based on your workload:
# - For small models: --memory="2g" --cpus="1.0"
# - For large models: --memory="8g" --cpus="4.0"
```

1. - **Storage Optimization**

```
# Clean up old images and containers periodically
docker system prune -a

# For Podman
podman system prune -a
```

#### Getting Help

##### Log Analysis

```
# View detailed logs
docker logs --details --timestamps pytorch-converter

# Follow logs in real-time
docker logs -f pytorch-converter
```

### Security Considerations

#### Network Security

- - **Localhost Only:** Use `-p 127.0.0.1:8000:8000` for maximum security
- - **Local Network:** Only use `-p 8000:8000` on trusted networks
- - **Internet Access:** Never expose directly to the internet without proper authentication and HTTPS

#### Container Security

- - Both Docker and Podman configurations use non-root users
- - Podman provides additional security with rootless operation

#### Firewall Rules

- - Open necessary ports only
- - Consider using VPN for remote access instead of exposing ports
