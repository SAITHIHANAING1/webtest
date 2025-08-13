# SafeStep Docker Deployment Guide

This guide provides comprehensive instructions for deploying the SafeStep application using Docker and Docker Compose.

## 📋 Prerequisites

- Docker Engine 20.10 or later
- Docker Compose 2.0 or later
- 2GB RAM minimum (4GB recommended)
- 10GB disk space

## 🚀 Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/SAITHIHANAING1/webtest.git
cd webtest
```

### 2. Environment Configuration
Copy the environment template and configure:
```bash
cp .env.docker .env
```

Edit `.env` with your configuration:
```env
# Required
SECRET_KEY=your-very-secure-secret-key-here

# Database (choose one option)
# Option A: Use built-in PostgreSQL
DATABASE_URL=postgresql://postgres:postgres@db:5432/postgres

# Option B: Use external Supabase
# DATABASE_URL=postgresql://postgres:your_password@db.your_project.supabase.co:5432/postgres
# SUPABASE_URL=https://your-project-ref.supabase.co
# SUPABASE_KEY=your_anon_key_here

# Optional Features
GEMINI_API_KEY=your_gemini_api_key_for_chatbot
```

### 3. Deploy
```bash
# Development with local database
docker-compose up -d

# Production with external Supabase
docker-compose -f docker-compose.prod.yml up -d
```

### 4. Access Application
- **Web Interface**: http://localhost:5000
- **Admin Login**: `admin` / `admin123`
- **Demo Login**: `demo` / `demo123`

## 🏗️ Deployment Options

### Option 1: Development Setup (Local PostgreSQL)

Use the standard `docker-compose.yml` for development:

```bash
docker-compose up -d
```

This creates:
- SafeStep web application container
- PostgreSQL database container
- Persistent data volumes

### Option 2: Production Setup (External Supabase)

Use `docker-compose.prod.yml` for production with Supabase:

```bash
# Set environment variables
export DATABASE_URL="postgresql://postgres:password@db.project.supabase.co:5432/postgres"
export SUPABASE_URL="https://project.supabase.co"
export SUPABASE_KEY="your_anon_key"
export SECRET_KEY="your-production-secret"

# Deploy
docker-compose -f docker-compose.prod.yml up -d
```

### Option 3: Production with Nginx SSL

For production with reverse proxy and SSL:

1. **Prepare SSL certificates** (place in `./ssl/` directory):
   ```bash
   mkdir ssl
   # Copy your SSL certificates
   cp your-cert.pem ssl/
   cp your-key.pem ssl/
   ```

2. **Update nginx.conf** for SSL:
   ```nginx
   server {
       listen 443 ssl;
       server_name your-domain.com;
       
       ssl_certificate /etc/ssl/certs/your-cert.pem;
       ssl_certificate_key /etc/ssl/certs/your-key.pem;
       
       # ... rest of configuration
   }
   ```

3. **Deploy**:
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

## 🔧 Configuration Options

### Environment Variables

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `SECRET_KEY` | Yes | Flask secret key | `your-secret-key-here` |
| `DATABASE_URL` | Yes | Database connection string | `postgresql://user:pass@host:5432/db` |
| `SUPABASE_URL` | No | Supabase project URL | `https://project.supabase.co` |
| `SUPABASE_KEY` | No | Supabase anon key | `eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...` |
| `SUPABASE_SERVICE_KEY` | No | Supabase service role key | `eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...` |
| `GEMINI_API_KEY` | No | Google Gemini API for chatbot | `AIzaSyD...` |
| `SESSION_COOKIE_SECURE` | No | Enable secure cookies (HTTPS) | `true` |

### Docker Compose Volumes

- `db_data`: PostgreSQL database files
- `instance_data`: Application instance data
- `./SafeStep/prediction`: ML model files (bind mount)

## 🔍 Health Checks

The application includes built-in health checks:

```bash
# Check container health
docker ps
docker-compose ps

# View health check logs
docker logs safestep-web
```

Health check endpoint: `http://localhost:5000/`

## 📊 Monitoring and Logs

### View Application Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f web
docker-compose logs -f db
```

### Database Access
```bash
# Connect to PostgreSQL container
docker-compose exec db psql -U postgres -d postgres

# Backup database
docker-compose exec db pg_dump -U postgres postgres > backup.sql

# Restore database
docker-compose exec -T db psql -U postgres postgres < backup.sql
```

## 🚨 Troubleshooting

### Common Issues

#### 1. Database Connection Errors
```
ERROR: PostgreSQL connection failed
```

**Solutions:**
- Check `DATABASE_URL` format
- Verify database server is running
- Check network connectivity
- Verify credentials

#### 2. Permission Errors
```
ERROR: Permission denied for volume mounts
```

**Solutions:**
```bash
# Linux/Mac: Fix permissions
sudo chown -R $USER:$USER ./SafeStep/prediction
chmod -R 755 ./SafeStep/prediction

# Windows: Run Docker Desktop as Administrator
```

#### 3. Port Already in Use
```
ERROR: Port 5000 is already allocated
```

**Solutions:**
```bash
# Check what's using the port
netstat -tulpn | grep :5000
# or
lsof -i :5000

# Change port in docker-compose.yml
ports:
  - "5001:5000"  # Use port 5001 instead
```

#### 4. Out of Memory
```
ERROR: Container killed (OOMKilled)
```

**Solutions:**
- Increase Docker memory limit
- Use fewer Gunicorn workers:
  ```bash
  docker-compose exec web gunicorn --workers 2 --bind 0.0.0.0:5000 app:app
  ```

#### 5. SSL Certificate Issues
```
ERROR: SSL certificate verify failed
```

**Solutions:**
- Use valid SSL certificates
- For development, disable SSL verification (not recommended for production)

### Debug Mode

Enable debug mode for troubleshooting:

```yaml
# In docker-compose.yml
services:
  web:
    environment:
      FLASK_ENV: development
      FLASK_DEBUG: "1"
```

## 🔒 Security Considerations

### Production Checklist

- [ ] Use strong `SECRET_KEY`
- [ ] Enable `SESSION_COOKIE_SECURE=true` for HTTPS
- [ ] Use environment-specific credentials
- [ ] Enable firewall rules
- [ ] Use SSL/TLS certificates
- [ ] Regular security updates
- [ ] Backup encryption
- [ ] Log monitoring

### Database Security

- Use strong database passwords
- Enable SSL for database connections
- Restrict database access to application only
- Regular backups with encryption

## 🔄 Updates and Maintenance

### Update Application
```bash
# Pull latest changes
git pull

# Rebuild containers
docker-compose build --no-cache
docker-compose up -d
```

### Database Migrations
```bash
# Run migrations in container
docker-compose exec web python migrate_db.py
```

### Backup Strategy
```bash
#!/bin/bash
# Backup script example
DATE=$(date +%Y%m%d_%H%M%S)

# Backup database
docker-compose exec db pg_dump -U postgres postgres > backup_${DATE}.sql

# Backup application data
docker run --rm -v $(pwd)/SafeStep/prediction:/source -v $(pwd)/backups:/backup alpine tar czf /backup/prediction_${DATE}.tar.gz -C /source .
```

## 📈 Scaling

### Horizontal Scaling
```yaml
# docker-compose.yml
services:
  web:
    deploy:
      replicas: 3
  
  nginx:
    # Load balancer configuration
    image: nginx:alpine
    # Configure upstream servers
```

### Resource Limits
```yaml
services:
  web:
    deploy:
      resources:
        limits:
          memory: 1G
          cpus: '0.5'
        reservations:
          memory: 512M
```

## 🆘 Support

### Debug Information Collection
```bash
# System information
docker version
docker-compose version

# Container status
docker ps -a
docker-compose logs --tail=100

# System resources
docker stats
df -h
```

### Log Files Location
- Application logs: Docker container stdout/stderr
- Database logs: PostgreSQL container logs
- Nginx logs: `/var/log/nginx/` in nginx container

For additional support, provide:
1. Docker version and OS
2. Complete error messages
3. Environment configuration (without secrets)
4. Container logs