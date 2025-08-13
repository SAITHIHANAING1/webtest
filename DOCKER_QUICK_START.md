# SafeStep Docker Quick Start

🚀 **Get SafeStep running in under 5 minutes!**

## Prerequisites
- Docker & Docker Compose installed
- 2GB RAM, 10GB disk space

## Instant Deployment

### 1. Clone & Setup
```bash
git clone https://github.com/SAITHIHANAING1/webtest.git
cd webtest
cp .env.docker .env
```

### 2. Configure (required)
Edit `.env` file:
```env
SECRET_KEY=your-secure-secret-key-here-make-it-long-and-random
DATABASE_URL=postgresql://postgres:postgres@db:5432/postgres
```

### 3. Launch
```bash
docker-compose up -d
```

### 4. Access
- **URL**: http://localhost:5000
- **Admin**: `admin` / `admin123`
- **Demo**: `demo` / `demo123`

## Status Check
```bash
# Check if running
docker-compose ps

# View logs
docker-compose logs -f
```

## Stop
```bash
docker-compose down
```

## Production Ready?
For production deployment with Supabase, see [DOCKER_DEPLOYMENT_GUIDE.md](./DOCKER_DEPLOYMENT_GUIDE.md)

---
**Need help?** Check the full deployment guide or container logs for troubleshooting.