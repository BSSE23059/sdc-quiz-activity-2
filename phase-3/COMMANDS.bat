@REM Quick reference for Phase 3 Docker Compose commands (Windows)

@REM ============================================
@REM 1. START AND STOP SERVICES
@REM ============================================

@REM Start all services with build
docker-compose up -d --build

@REM Start all services without rebuild
docker-compose up -d

@REM Start in foreground (see logs)
docker-compose up --build

@REM Stop all services (keeps data)
docker-compose stop

@REM Start all services
docker-compose start

@REM Stop and remove containers
docker-compose down

@REM Remove containers, volumes, and images
docker-compose down -v --rmi all

@REM ============================================
@REM 2. VIEW STATUS AND LOGS
@REM ============================================

@REM Check all containers status
docker-compose ps

@REM View all logs
docker-compose logs -f

@REM View specific service logs
docker-compose logs -f backend
docker-compose logs -f db
docker-compose logs -f pgadmin

@REM View last 100 lines
docker-compose logs --tail=100 backend

@REM ============================================
@REM 3. RESTART SERVICES
@REM ============================================

@REM Restart all services
docker-compose restart

@REM Restart specific service
docker-compose restart backend
docker-compose restart db

@REM ============================================
@REM 4. KILL AND RECOVER
@REM ============================================

@REM Kill backend container (hard stop)
docker kill registration-app-container

@REM Graceful stop
docker-compose stop backend

@REM Recover backend
docker-compose start backend

@REM ============================================
@REM 5. DATABASE MANAGEMENT
@REM ============================================

@REM Access PostgreSQL CLI
docker exec -it registration-db-container psql -U postgres -d registration_db

@REM List tables
docker exec -it registration-db-container psql -U postgres -d registration_db -c "\dt"

@REM View all users
docker exec -it registration-db-container psql -U postgres -d registration_db -c "SELECT * FROM users;"

@REM Count users
docker exec -it registration-db-container psql -U postgres -d registration_db -c "SELECT count(*) FROM users;"

@REM ============================================
@REM 6. ACCESS SERVICES
@REM ============================================

@REM Frontend: http://localhost:5000
@REM API Docs: http://localhost:5000/docs
@REM pgAdmin: http://localhost:5050

@REM ============================================
@REM 7. API TESTING (PowerShell)
@REM ============================================

@REM Register user
curl -X POST http://localhost:5000/api/register ^
  -H "Content-Type: application/json" ^
  -d "{\"first_name\":\"John\",\"last_name\":\"Doe\",\"username\":\"john@example.com\",\"password\":\"secure123\"}"

@REM Get all users
curl http://localhost:5000/api/data

@REM Health check
curl http://localhost:5000/health

@REM Get stats
curl http://localhost:5000/api/stats

@REM ============================================
@REM 8. MONITORING
@REM ============================================

@REM View container resource usage
docker stats

@REM ============================================
@REM 9. CLEANUP
@REM ============================================

@REM Remove all stopped containers
docker container prune

@REM Remove all unused volumes
docker volume prune

@REM System cleanup
docker system prune -a --volumes
