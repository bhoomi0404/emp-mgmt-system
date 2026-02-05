# Employee Management System

A full-stack employee management application with FastAPI backend, MySQL database, and frontend served via Nginx.

## Architecture

- **Backend**: FastAPI (Python) - REST API
- **Frontend**: HTML/JavaScript - Single Page Application
- **Database**: MySQL 8.0
- **Web Server**: Nginx - Reverse proxy and static file serving
- **Containerization**: Docker & Docker Compose

## Prerequisites

- Docker (version 20.10+)
- Docker Compose (version 2.0+)
- Git (optional)

## Quick Start

### 1. Clone/Navigate to the project
```bash
cd c:\employee-mgmt
```

### 2. Build and Start All Services
```bash
docker-compose -f deploy/docker-compose.yml up -d
```

This command will:
- Build the backend Docker image
- Create and start all containers (MySQL, Backend API, Nginx)
- Initialize the database schema
- Expose services on their respective ports

### 3. Access the Application

Once all services are running:
- **Web Application**: http://localhost
- **API Documentation**: http://localhost/docs
- **API**: http://localhost/api/employees

## Services

### MySQL Database
- **Container Name**: employee_db
- **Port**: 3306 (internal) / 3306 (host)
- **Database**: employee_db
- **User**: emp_user
- **Password**: emp_pass

### Backend API
- **Container Name**: employee_api
- **Port**: 8000 (internal) / 8000 (host)
- **Framework**: FastAPI
- **Status**: http://localhost:8000/healthz

### Nginx Reverse Proxy
- **Container Name**: employee_nginx
- **Port**: 80 (HTTP), 443 (HTTPS - if configured)
- **Routes**:
  - `/` → Backend (frontend)
  - `/api/*` → Backend API
  - `/static/*` → Static files
  - `/docs` → Swagger UI

## Management Commands

### View Running Containers
```bash
docker-compose -f deploy/docker-compose.yml ps
```

### View Logs
```bash
# All services
docker-compose -f deploy/docker-compose.yml logs -f

# Specific service
docker-compose -f deploy/docker-compose.yml logs -f backend
docker-compose -f deploy/docker-compose.yml logs -f mysql
docker-compose -f deploy/docker-compose.yml logs -f nginx
```

### Stop All Services
```bash
docker-compose -f deploy/docker-compose.yml down
```

### Stop and Remove Volumes (Clean slate)
```bash
docker-compose -f deploy/docker-compose.yml down -v
```

### Restart Services
```bash
docker-compose -f deploy/docker-compose.yml restart
```

### Execute Commands in Container
```bash
# Backend
docker exec -it employee_api bash

# MySQL
docker exec -it employee_db mysql -u emp_user -pemp_pass employee_db
```

## Environment Configuration

### Backend Configuration
Environment variables are set in `docker-compose.yml`:

- `DB_HOST`: MySQL host (default: mysql)
- `DB_PORT`: MySQL port (default: 3306)
- `DB_USER`: MySQL user (default: emp_user)
- `DB_PASSWORD`: MySQL password (default: emp_pass)
- `DB_NAME`: Database name (default: employee_db)
- `CORS_ORIGINS`: Allowed origins for CORS

To override, edit `deploy/docker-compose.yml` or create a `.env` file.

## Development

### Local Development (Without Docker)
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r backend/requirements.txt

# Set environment variables
# Create .env file in backend/ directory with database configuration

# Run the backend
cd backend
uvicorn app.main:app --reload
```

## API Endpoints

### Employees
- `GET /api/employees` - List all employees
- `GET /api/employees/{id}` - Get employee by ID
- `POST /api/employees` - Create new employee
- `PUT /api/employees/{id}` - Update employee
- `DELETE /api/employees/{id}` - Delete employee

### Web Routes
- `GET /` - Home page
- `GET /employees` - Employee list page

## Database Schema

The database is automatically initialized on first run using the schema defined in `backend/app/db/migrations/schema.sql`.

## Troubleshooting

### Port Already in Use
If you get an error about ports being in use, you can modify the port mappings in `docker-compose.yml`:
```yaml
ports:
  - "8080:8000"  # Maps container port 8000 to host port 8080
```

### Database Connection Issues
1. Ensure MySQL is healthy: `docker-compose -f deploy/docker-compose.yml ps`
2. Check logs: `docker-compose -f deploy/docker-compose.yml logs mysql`
3. Wait for MySQL to be ready (may take 10-15 seconds)

### Permission Denied
On Linux/macOS, you may need to use `sudo`:
```bash
sudo docker-compose -f deploy/docker-compose.yml up -d
```

## Production Deployment

For production use:

1. **Update Environment Variables**: Replace hardcoded passwords in `docker-compose.yml`
2. **Enable HTTPS**: Configure SSL certificates in Nginx
3. **Set Resource Limits**: Add CPU/memory limits in docker-compose.yml
4. **Database Backups**: Configure automated backups for MySQL volume
5. **Logging**: Configure centralized logging
6. **Health Checks**: Verify all health checks are properly configured

Example resource limits:
```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M
```

## License

[Your License Here]
