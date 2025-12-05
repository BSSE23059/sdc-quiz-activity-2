# Phase 2: App to Containers & Kubernetes (FastAPI Backend)

User registration application with:
- **Frontend**: Interactive HTML interface with Bootstrap 5
- **Backend**: FastAPI REST API with CORS support
- **Containerization**: Docker with optimized multi-stage build
- **Orchestration**: Kubernetes Deployment and Service manifests

## Project Structure

```
phase-2/
├── app/
│   ├── main.py                # FastAPI backend application
│   ├── Dockerfile             # Docker image definition
│   ├── requirements.txt        # Python dependencies
│   └── templates/
│       └── index.html         # Frontend HTML with Bootstrap
├── kubernetes/
│   ├── deployment.yaml        # Kubernetes Deployment manifest
│   └── service.yaml           # Kubernetes Service manifests
└── docker-compose.yaml        # Docker Compose for local testing
```

## Features

### Frontend (HTML/Bootstrap)
- Modern, responsive registration form
- Real-time form validation
- Submit button with loading indicator
- Display submitted user data below form
- List all previous submissions
- Bootstrap 5 styling with gradient background
- XSS protection with HTML escaping

### Backend (FastAPI)
- Fast, modern Python web framework
- Automatic interactive API documentation (Swagger UI)
- CORS enabled for cross-origin requests
- Request/response validation with Pydantic
- Health check endpoint for Kubernetes
- In-memory data storage
- Comprehensive error handling

### API Endpoints
- `GET /` - Serve main registration page
- `POST /api/register` - Submit user registration
- `GET /api/data` - Retrieve all submissions
- `GET /health` - Health check for Kubernetes probes
- `GET /api/stats` - Get registration statistics
- `GET /docs` - Swagger UI API documentation
- `GET /redoc` - ReDoc API documentation

## Prerequisites

- Docker & Docker Compose (for containerization)
- Kubernetes cluster (Minikube, Docker Desktop K8s, or cloud)
- kubectl CLI tool
- Python 3.11+ (for local development)

## Local Development

### Option 1: Run with Docker Compose

```bash
cd phase-2
docker-compose up --build
```

Access the app at: `http://localhost:5000`

### Option 2: Run FastAPI directly

```bash
cd phase-2/app
pip install -r requirements.txt
python -m uvicorn main:app --host 0.0.0.0 --port 5000 --reload
```

Access the app at: `http://localhost:5000`
View API docs at: `http://localhost:5000/docs`

## Docker Deployment

### Build Docker Image

```bash
cd phase-2/app
docker build -t registration-app:latest .
```

### Run as Docker Container

```bash
docker run -d \
  --name registration-app-container \
  -p 5000:5000 \
  registration-app:latest
```

## Kubernetes Deployment

### Step 1: Load Docker Image (for local Kubernetes)

```bash
# For Minikube
minikube image load registration-app:latest

# For Docker Desktop
# Image is automatically available
```

### Step 2: Apply Kubernetes Manifests

```bash
cd phase-2/kubernetes
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
```

### Step 3: Verify Deployment

```bash
# Check deployments
kubectl get deployments
kubectl describe deployment registration-app-deployment

# Check pods
kubectl get pods
kubectl describe pod <pod-name>

# Check services
kubectl get svc
```

### Step 4: View Logs

```bash
kubectl logs -f <pod-name>
```

## Accessing the Application

### Option 1: NodePort (Port 30007)

```bash
# Get node IP
kubectl get nodes -o wide

# Access: http://<NODE_IP>:30007
```

### Option 2: Port Forwarding

```bash
# Forward service port
kubectl port-forward svc/registration-app-service 8080:80

# Access: http://localhost:8080
```

### Option 3: LoadBalancer Service

```bash
kubectl get svc registration-app-lb
# Access via external IP (if available)
```

## API Testing

### Register User

```bash
curl -X POST http://localhost:5000/api/register \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "username": "john@example.com",
    "password": "secure123"
  }'
```

### Get All Submissions

```bash
curl http://localhost:5000/api/data
```

### Health Check

```bash
curl http://localhost:5000/health
```

### Get Stats

```bash
curl http://localhost:5000/api/stats
```

## Troubleshooting

### Pod not running

```bash
kubectl describe pod <pod-name>
kubectl get events --sort-by='.lastTimestamp'
kubectl logs <pod-name>
```

### Port forwarding issues

```bash
kubectl get svc registration-app-service
kubectl get endpoints registration-app-service
kubectl exec -it <pod-name> -- curl localhost:5000/health
```

## Cleanup

### Remove Kubernetes Resources

```bash
kubectl delete -f kubernetes/
```

### Remove Docker Container

```bash
docker stop registration-app-container
docker rm registration-app-container
docker rmi registration-app:latest
```
