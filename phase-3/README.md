# Phase 3: Multi-Service App with Database (LAB 03)

Complete multi-service application with frontend, backend API, and PostgreSQL database running together in Docker Compose.

## Architecture

```
┌─────────────────────────────────────────────────┐
│                                                 │
│  Frontend (HTML/Bootstrap)                      │
│  Port: 5000                                     │
│                                                 │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│                                                 │
│  FastAPI Backend                                │
│  Port: 5000                                     │
│  Health Check: /health                          │
│                                                 │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│                                                 │
│  PostgreSQL Database                            │
│  Port: 5432                                     │
│  Volume: postgres_data                          │
│                                                 │
└─────────────────────────────────────────────────┘

Additional Service:
┌─────────────────────────────────────────────────┐
│                                                 │
│  pgAdmin (Database Management)                  │
│  Port: 5050                                     │
│                                                 │
└─────────────────────────────────────────────────┘
```

## Project Structure

```
phase-3/
├── app/
│   ├── main.py                 # FastAPI backend with SQLAlchemy ORM
│   ├── Dockerfile              # Docker image for backend
│   ├── requirements.txt         # Python dependencies
│   └── templates/
│       └── index.html          # Frontend UI
├── kubernetes/                 # Kubernetes manifests
│   ├── deployment.yaml
│   └── service.yaml
├── init.sql                    # PostgreSQL initialization script
├── docker-compose.yaml         # Docker Compose orchestration
├── .env                        # Environment variables (production)
├── .env.dev                    # Environment variables (development)
├── .env.example                # Example environment file
└── README.md                   # Documentation
```

## Services

### 1. PostgreSQL Database (`db`)
- **Image**: postgres:16-alpine
- **Port**: 5432
- **Database**: registration_db
- **User**: postgres
- **Password**: postgres_password_123
- **Volume**: postgres_data (persistent storage)
- **Health Check**: Enabled (10s interval)

### 2. FastAPI Backend (`backend`)
- **Image**: Custom built from ./app/Dockerfile
- **Port**: 5000
- **Language**: Python 3.11
- **Framework**: FastAPI with SQLAlchemy ORM
- **Volume**: ./app (code mount for hot reload)
- **Depends On**: db service with health check
- **Health Check**: Enabled (/health endpoint)

### 3. pgAdmin (`pgadmin`)
- **Image**: dpage/pgadmin4:latest
- **Port**: 5050
- **Email**: admin@example.com
- **Password**: admin_password_123
- **Volume**: pgadmin_data (persistent storage)

## Quick Start

### Prerequisites
- Docker & Docker Compose installed
- Git
- Text editor

### Start the Application

```bash
# Navigate to phase-3 directory
cd phase-3

# Build and start all services
docker-compose up --build

# Or start in detached mode (background)
docker-compose up -d --build
```

**Access the services:**
- **Frontend/API**: http://localhost:5000
- **API Documentation**: http://localhost:5000/docs
- **pgAdmin**: http://localhost:5050

### Verify Services Running

```bash
# Check status of all containers
docker-compose ps

# View logs from all services
docker-compose logs

# View logs from specific service
docker-compose logs backend
docker-compose logs db
docker-compose logs pgadmin
```

## Common Commands

### Stop Services

```bash
# Stop all services (keeps data)
docker-compose stop

# Stop specific service
docker-compose stop backend
```

### Start Services

```bash
# Start all services
docker-compose start

# Start specific service
docker-compose start backend
```

### Restart Services

```bash
# Restart all services
docker-compose restart

# Restart specific service
docker-compose restart backend

# Force rebuild and restart
docker-compose up -d --build
```

### Remove All Containers and Volumes

```bash
# Stop and remove all containers
docker-compose down

# Remove containers and volumes (WARNING: deletes data!)
docker-compose down -v

# Remove containers, volumes, and images
docker-compose down -v --rmi all
```

### View Container Logs

```bash
# View all logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f backend
docker-compose logs -f db

# View last 100 lines
docker-compose logs --tail=100 backend

# View logs with timestamps
docker-compose logs -f --timestamps backend
```

### Execute Commands in Container

```bash
# Access PostgreSQL CLI
docker exec -it registration-db-container psql -U postgres -d registration_db

# Access backend shell
docker exec -it registration-app-container /bin/sh

# Run Python command in backend
docker exec registration-app-container python -c "import sqlalchemy; print(sqlalchemy.__version__)"
```

### Database Management

#### Via psql CLI

```bash
# Connect to PostgreSQL
docker exec -it registration-db-container psql -U postgres -d registration_db

# Useful SQL commands:
\dt                    # List all tables
SELECT * FROM users;   # View all users
SELECT count(*) FROM users;  # Count users
\d users               # Show users table schema
DROP TABLE users;      # Delete table
```

#### Via pgAdmin Web Interface

1. Open http://localhost:5050 in browser
2. Login with:
   - Email: admin@example.com
   - Password: admin_password_123
3. Add new server connection:
   - Host: db
   - Port: 5432
   - Username: postgres
   - Password: postgres_password_123

## API Endpoints

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

### Get All Users
```bash
curl http://localhost:5000/api/data
```

### Health Check
```bash
curl http://localhost:5000/health
```

### Get Statistics
```bash
curl http://localhost:5000/api/stats
```

### API Documentation
- Swagger UI: http://localhost:5000/docs
- ReDoc: http://localhost:5000/redoc

## Environment Variables

Edit `.env` file to change database credentials:

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres_password_123
POSTGRES_DB=registration_db
DATABASE_URL=postgresql://postgres:postgres_password_123@db:5432/registration_db
```

To change PostgreSQL port, modify `docker-compose.yaml`:
```yaml
db:
  ports:
    - "5433:5432"  # Change 5432 to your desired port
```

## Challenges & Solutions

### Challenge 1: Add Volume for Database Persistence

**Solution**: The `docker-compose.yaml` includes volumes:
```yaml
volumes:
  postgres_data:
    driver: local
```

This ensures data persists even if containers are stopped/removed.

### Challenge 2: Restart Only 1 Service

```bash
# Restart only the backend
docker-compose restart backend

# Restart only the database
docker-compose restart db
```

### Challenge 3: Kill Backend then Recover

```bash
# Kill the backend container
docker kill registration-app-container

# Or stop it gracefully
docker-compose stop backend

# Restart it
docker-compose start backend

# Or restart it
docker-compose restart backend
```

### Challenge 4: Check Logs

```bash
# All services logs
docker-compose logs -f

# Follow backend logs
docker-compose logs -f backend

# Follow database logs
docker-compose logs -f db

# View last 50 lines
docker-compose logs --tail=50 backend
```

### Challenge 5: Change Database Name

Edit `.env`:
```env
POSTGRES_DB=new_database_name
```

Edit `docker-compose.yaml`:
```yaml
environment:
  POSTGRES_DB: new_database_name
DATABASE_URL: postgresql://postgres:password@db:5432/new_database_name
```

Edit `init.sql` if needed to match the new database name.

## Troubleshooting

### Containers not starting

```bash
# Check logs
docker-compose logs

# Rebuild images
docker-compose down -v
docker-compose up --build
```

### Database connection error

```bash
# Check if db service is healthy
docker-compose ps

# View database logs
docker-compose logs db

# Verify network connectivity
docker exec registration-app-container ping db
```

### Port already in use

```bash
# Find process using port
netstat -ano | findstr :5000  # Windows
lsof -i :5000                 # macOS/Linux

# Change port in docker-compose.yaml
services:
  backend:
    ports:
      - "5001:5000"  # Map to different port
```

### Data persistence issue

```bash
# List volumes
docker volume ls

# Inspect volume
docker volume inspect phase-3_postgres_data

# Remove volume (WARNING: deletes data!)
docker volume rm phase-3_postgres_data
```

## Performance Monitoring

```bash
# View container resource usage
docker stats

# View specific container stats
docker stats registration-db-container

# View detailed container info
docker inspect registration-db-container
```

## Production Considerations

1. **Secrets Management**
   - Use Docker Secrets for production
   - Never commit `.env` to version control
   - Use `.env.example` as template

2. **Database Backup**
   ```bash
   docker exec registration-db-container pg_dump -U postgres registration_db > backup.sql
   ```

3. **Database Restore**
   ```bash
   docker exec -i registration-db-container psql -U postgres < backup.sql
   ```

4. **Resource Limits**
   - Add resource limits in docker-compose.yaml
   - Monitor container memory usage

5. **Network Security**
   - Use environment-specific passwords
   - Restrict network access
   - Use VPN for database access

## Summary of Files

| File | Purpose |
|------|---------|
| `docker-compose.yaml` | Defines all services and their configurations |
| `init.sql` | PostgreSQL database initialization and schema |
| `.env` | Production environment variables |
| `.env.dev` | Development environment variables |
| `.env.example` | Template for environment variables |
| `app/main.py` | FastAPI backend with SQLAlchemy ORM |
| `app/Dockerfile` | Docker image definition for backend |
| `app/requirements.txt` | Python package dependencies |
| `app/templates/index.html` | Frontend HTML/CSS/JS |

## Next Steps

- Implement authentication & authorization
- Add more API endpoints
- Setup continuous integration/deployment
- Deploy to Kubernetes (Phase 4)
- Add monitoring and logging
- Implement database backups

