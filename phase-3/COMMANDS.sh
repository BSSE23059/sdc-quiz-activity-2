#!/bin/bash
# Quick reference for Phase 3 Docker Compose commands

# ============================================
# 1. START AND STOP SERVICES
# ============================================

# Start all services
docker-compose up -d --build

# Start without build
docker-compose up -d

# Start in foreground (see logs)
docker-compose up --build

# Stop all services (keeps data)
docker-compose stop

# Start all services
docker-compose start

# Stop and remove containers
docker-compose down

# Remove containers, volumes, and images (WARNING: deletes all data!)
docker-compose down -v --rmi all

# ============================================
# 2. VIEW STATUS AND LOGS
# ============================================

# See all containers status
docker-compose ps

# View all logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f backend
docker-compose logs -f db
docker-compose logs -f pgadmin

# View last 100 lines of logs
docker-compose logs --tail=100 backend

# ============================================
# 3. RESTART SERVICES
# ============================================

# Restart all services
docker-compose restart

# Restart specific service
docker-compose restart backend
docker-compose restart db

# Rebuild and restart
docker-compose up -d --build

# ============================================
# 4. KILL AND RECOVER
# ============================================

# Kill backend container (hard stop)
docker kill registration-app-container

# Graceful stop
docker-compose stop backend

# Recover/restart backend
docker-compose start backend
docker-compose restart backend

# ============================================
# 5. DATABASE MANAGEMENT
# ============================================

# Access PostgreSQL CLI
docker exec -it registration-db-container psql -U postgres -d registration_db

# List tables
docker exec -it registration-db-container psql -U postgres -d registration_db -c "\dt"

# View all users
docker exec -it registration-db-container psql -U postgres -d registration_db -c "SELECT * FROM users;"

# Count users
docker exec -it registration-db-container psql -U postgres -d registration_db -c "SELECT count(*) FROM users;"

# Backup database
docker exec registration-db-container pg_dump -U postgres registration_db > backup.sql

# ============================================
# 6. CHANGE CONFIGURATION
# ============================================

# Change database name:
# 1. Edit .env file: POSTGRES_DB=new_name
# 2. Edit docker-compose.yaml: POSTGRES_DB: new_name
# 3. Edit DATABASE_URL: ...@db:5432/new_name
# 4. Restart: docker-compose down -v && docker-compose up -d --build

# Change database port in docker-compose.yaml:
# db:
#   ports:
#     - "5433:5432"  # Change 5432 to desired port

# ============================================
# 7. ACCESS SERVICES
# ============================================

# Frontend: http://localhost:5000
# API Docs: http://localhost:5000/docs
# pgAdmin: http://localhost:5050
# pgAdmin login: admin@example.com / admin_password_123

# ============================================
# 8. API TESTING
# ============================================

# Register user
curl -X POST http://localhost:5000/api/register \
  -H "Content-Type: application/json" \
  -d '{"first_name":"John","last_name":"Doe","username":"john@example.com","password":"secure123"}'

# Get all users
curl http://localhost:5000/api/data

# Health check
curl http://localhost:5000/health

# Get stats
curl http://localhost:5000/api/stats

# ============================================
# 9. DOCKER STATS AND MONITORING
# ============================================

# View container resource usage
docker stats

# View specific container resource usage
docker stats registration-db-container registration-app-container

# ============================================
# 10. TROUBLESHOOTING
# ============================================

# Check container details
docker-compose ps
docker inspect registration-db-container

# Test network connectivity
docker exec registration-app-container ping db

# Execute shell in container
docker exec -it registration-app-container /bin/sh

# View volume information
docker volume ls
docker volume inspect phase-3_postgres_data

# ============================================
# 11. CLEANUP
# ============================================

# Remove all stopped containers
docker container prune

# Remove all unused volumes
docker volume prune

# Remove all unused images
docker image prune

# Complete cleanup
docker system prune -a --volumes
