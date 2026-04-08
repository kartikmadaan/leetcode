# Week 9: Containers & Kubernetes

> From beginner to proficient with container orchestration

---

## 📖 High-Level Overview

Containers and Kubernetes have become the standard for deploying and scaling applications. This week covers:
- Container fundamentals (Docker)
- Kubernetes architecture and concepts
- Deployments, services, and scaling
- Configuration and secrets management

### Prerequisites:
- Basic Linux command line knowledge
- Understanding of networking concepts
- Familiarity with YAML

---

## 🐳 Part 1: Docker Fundamentals

### What is a Container?

```
Virtual Machine vs Container:

VM:                              Container:
┌─────────────────────────┐     ┌─────────────────────────┐
│      Application        │     │      Application        │
├─────────────────────────┤     ├─────────────────────────┤
│    Guest OS (Linux)     │     │   Container Runtime     │
├─────────────────────────┤     │     (Docker Engine)     │
│      Hypervisor         │     ├─────────────────────────┤
├─────────────────────────┤     │        Host OS          │
│        Host OS          │     ├─────────────────────────┤
├─────────────────────────┤     │       Hardware          │
│       Hardware          │     └─────────────────────────┘
└─────────────────────────┘

Containers share the host OS kernel.
- Faster startup (seconds vs minutes)
- Less resource overhead
- More portable
```

### Docker Key Concepts

```
IMAGE:     Read-only template for creating containers
           Built from Dockerfile, stored in registries

CONTAINER: Running instance of an image
           Isolated process with its own filesystem

DOCKERFILE: Instructions to build an image
            Layers for efficiency

REGISTRY:  Storage for images (Docker Hub, ECR, GCR)
```

### Dockerfile Example

```dockerfile
# Base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first (better layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Run command
CMD ["python", "app.py"]
```

### Essential Docker Commands

```bash
# Build image
docker build -t myapp:v1 .

# Run container
docker run -d -p 8000:8000 --name myapp myapp:v1

# Run with environment variables
docker run -d -e DATABASE_URL=postgres://... myapp:v1

# Run with volume mount
docker run -v /host/data:/container/data myapp:v1

# List containers
docker ps        # running
docker ps -a     # all

# View logs
docker logs myapp
docker logs -f myapp  # follow

# Execute command in container
docker exec -it myapp bash

# Stop and remove
docker stop myapp
docker rm myapp

# Clean up
docker system prune     # remove unused data
docker image prune -a   # remove unused images
```

### Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgres://user:pass@db:5432/mydb
    depends_on:
      - db
      - redis
    volumes:
      - ./app:/app  # Development: mount source code

  db:
    image: postgres:15
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: mydb
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  postgres_data:
```

```bash
# Docker Compose commands
docker-compose up -d           # Start all services
docker-compose down            # Stop and remove
docker-compose logs -f web     # Follow logs for web service
docker-compose exec web bash   # Shell into web container
docker-compose build           # Rebuild images
```

---

## ☸️ Part 2: Kubernetes Fundamentals

### What is Kubernetes (K8s)?

```
Kubernetes is a container orchestration platform that:
- Automates deployment, scaling, and management
- Provides self-healing (restarts failed containers)
- Enables rolling updates and rollbacks
- Manages configuration and secrets
- Provides service discovery and load balancing
```

### Kubernetes Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      CONTROL PLANE (Master)                     │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐  │
│  │ API Server  │  │ Scheduler   │  │ Controller Manager      │  │
│  │             │  │             │  │ (Node, Replication, etc)│  │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘  │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                          etcd                               ││
│  │              (Distributed key-value store)                  ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
                               │
                               │ API calls
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                      WORKER NODE 1                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐  │
│  │   kubelet   │  │ kube-proxy  │  │   Container Runtime     │  │
│  │             │  │             │  │   (containerd/CRI-O)    │  │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ POD         │ POD         │ POD         │ POD             │  │
│  │ ┌─────────┐ │ ┌─────────┐ │ ┌─────────┐ │ ┌─────────┐     │  │
│  │ │Container│ │ │Container│ │ │Container│ │ │Container│     │  │
│  │ └─────────┘ │ └─────────┘ │ └─────────┘ │ └─────────┘     │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### Core Kubernetes Objects

#### Pod
The smallest deployable unit. Contains one or more containers.

```yaml
# pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: myapp-pod
  labels:
    app: myapp
spec:
  containers:
  - name: myapp
    image: myapp:v1
    ports:
    - containerPort: 8000
    resources:
      requests:
        memory: "64Mi"
        cpu: "250m"
      limits:
        memory: "128Mi"
        cpu: "500m"
    env:
    - name: DATABASE_URL
      valueFrom:
        secretKeyRef:
          name: db-secret
          key: url
```

#### Deployment
Manages ReplicaSets and provides declarative updates.

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-deployment
  labels:
    app: myapp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: myapp
        image: myapp:v1
        ports:
        - containerPort: 8000
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 10
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 15
          periodSeconds: 20
```

#### Service
Exposes pods to the network.

```yaml
# service.yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
spec:
  selector:
    app: myapp
  type: ClusterIP  # Internal only
  ports:
  - port: 80       # Service port
    targetPort: 8000  # Container port
---
# LoadBalancer type (external access)
apiVersion: v1
kind: Service
metadata:
  name: myapp-lb
spec:
  selector:
    app: myapp
  type: LoadBalancer
  ports:
  - port: 80
    targetPort: 8000
```

**Service Types:**
```
ClusterIP:    Internal IP, only accessible within cluster
NodePort:     Exposes on each Node's IP at a static port
LoadBalancer: Provisions external load balancer (cloud)
ExternalName: Maps to external DNS name
```

#### ConfigMap and Secret

```yaml
# configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  APP_ENV: production
  LOG_LEVEL: info
  config.json: |
    {
      "feature_flags": {
        "new_ui": true
      }
    }
---
# secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: db-secret
type: Opaque
data:
  # Base64 encoded values
  username: YWRtaW4=      # admin
  password: cGFzc3dvcmQ=  # password
```

Using ConfigMaps and Secrets:
```yaml
spec:
  containers:
  - name: myapp
    image: myapp:v1
    envFrom:
    - configMapRef:
        name: app-config
    env:
    - name: DB_PASSWORD
      valueFrom:
        secretKeyRef:
          name: db-secret
          key: password
    volumeMounts:
    - name: config-volume
      mountPath: /etc/config
  volumes:
  - name: config-volume
    configMap:
      name: app-config
```

#### Ingress
HTTP(S) routing from outside the cluster.

```yaml
# ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: myapp-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  ingressClassName: nginx
  rules:
  - host: myapp.example.com
    http:
      paths:
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: api-service
            port:
              number: 80
      - path: /
        pathType: Prefix
        backend:
          service:
            name: web-service
            port:
              number: 80
  tls:
  - hosts:
    - myapp.example.com
    secretName: tls-secret
```

### Essential kubectl Commands

```bash
# Cluster info
kubectl cluster-info
kubectl get nodes

# Apply/create resources
kubectl apply -f deployment.yaml
kubectl create -f pod.yaml

# Get resources
kubectl get pods
kubectl get pods -o wide              # More info
kubectl get deployments
kubectl get services
kubectl get all                       # Everything
kubectl get all -n my-namespace       # In namespace

# Describe (detailed info)
kubectl describe pod myapp-pod
kubectl describe deployment myapp-deployment

# Logs
kubectl logs myapp-pod
kubectl logs -f myapp-pod             # Follow
kubectl logs myapp-pod -c container   # Specific container

# Execute command in pod
kubectl exec -it myapp-pod -- bash
kubectl exec myapp-pod -- ls /app

# Port forwarding (debugging)
kubectl port-forward pod/myapp-pod 8000:8000
kubectl port-forward service/myapp-service 8000:80

# Scaling
kubectl scale deployment myapp-deployment --replicas=5

# Rolling update
kubectl set image deployment/myapp-deployment myapp=myapp:v2
kubectl rollout status deployment/myapp-deployment
kubectl rollout history deployment/myapp-deployment
kubectl rollout undo deployment/myapp-deployment

# Delete resources
kubectl delete pod myapp-pod
kubectl delete -f deployment.yaml
```

### Horizontal Pod Autoscaler (HPA)

```yaml
# hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: myapp-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: myapp-deployment
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

### Namespaces

```yaml
# namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: production
---
apiVersion: v1
kind: Namespace
metadata:
  name: staging
```

```bash
# Use namespace
kubectl get pods -n production
kubectl config set-context --current --namespace=production
```

---

## 📊 Kubernetes Concepts Cheat Sheet

```
┌─────────────────────────────────────────────────────────────────┐
│                    Kubernetes Object Hierarchy                   │
└─────────────────────────────────────────────────────────────────┘

    Deployment
        │
        │ manages
        ▼
    ReplicaSet
        │
        │ manages
        ▼
    Pods (multiple)
        │
        │ contains
        ▼
    Containers

┌─────────────────────────────────────────────────────────────────┐
│                    Traffic Flow                                  │
└─────────────────────────────────────────────────────────────────┘

Internet → Ingress → Service → Pod → Container
                         │
                    LoadBalancer
                         │
                    (Cloud LB)
```

---

## 📝 Practice Exercises

### Docker

| # | Exercise | Focus |
|---|----------|-------|
| 1 | Create Dockerfile for a Python Flask app | Basic Dockerfile |
| 2 | Multi-stage build for a Go application | Optimization |
| 3 | Docker Compose for app + DB + cache | Multi-container |
| 4 | Debug a container that keeps crashing | Troubleshooting |

### Kubernetes

| # | Exercise | Focus |
|---|----------|-------|
| 5 | Deploy a simple web app with 3 replicas | Deployment, Service |
| 6 | Configure HPA based on CPU | Autoscaling |
| 7 | Set up rolling update with zero downtime | Deployments |
| 8 | Configure Ingress with TLS | Ingress |
| 9 | Debug a pod in CrashLoopBackOff | Troubleshooting |
| 10 | Set up ConfigMaps and Secrets | Configuration |

### Hints

<details>
<summary>Multi-stage Dockerfile for Go</summary>

```dockerfile
# Build stage
FROM golang:1.21 AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o main .

# Final stage
FROM alpine:3.18
RUN apk --no-cache add ca-certificates
WORKDIR /root/
COPY --from=builder /app/main .
EXPOSE 8080
CMD ["./main"]
```
</details>

<details>
<summary>Debugging CrashLoopBackOff</summary>

```bash
# Check pod status
kubectl describe pod myapp-pod

# Common issues:
# 1. Image not found → Check image name and registry access
# 2. OOMKilled → Increase memory limits
# 3. CrashLoopBackOff → Check logs

# Get logs (even from crashed container)
kubectl logs myapp-pod --previous

# Run shell in container to debug
kubectl run debug --image=busybox --restart=Never -- sleep 3600
kubectl exec -it debug -- sh

# Check events
kubectl get events --sort-by=.lastTimestamp
```
</details>

---

## 📚 Resources

- **Docker Official Documentation**: https://docs.docker.com/
- **Kubernetes Official Documentation**: https://kubernetes.io/docs/
- **Play with Kubernetes**: https://labs.play-with-k8s.com/
- **Katacoda Kubernetes Courses**: Interactive learning

---

## ✅ Week 9 Checklist

- [ ] Write Dockerfiles for different applications
- [ ] Understand Docker networking and volumes
- [ ] Use Docker Compose for multi-container apps
- [ ] Understand Kubernetes architecture
- [ ] Create Deployments and Services
- [ ] Configure ConfigMaps and Secrets
- [ ] Set up autoscaling with HPA
- [ ] Debug common Kubernetes issues

