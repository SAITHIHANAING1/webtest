# SafeStep - Google Cloud Run Deployment Guide

## Prerequisites

1. **Google Cloud SDK** installed
2. **Docker** installed
3. **Google Cloud Project** with billing enabled
4. **Cloud Run API** enabled

## Step 1: Setup Google Cloud

```bash
# Install Google Cloud SDK (if not already installed)
# Visit: https://cloud.google.com/sdk/docs/install

# Login to Google Cloud
gcloud auth login

# Set your project ID
gcloud config set project YOUR_PROJECT_ID

# Enable required APIs
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable containerregistry.googleapis.com
```

## Step 2: Configure Environment Variables

Before deploying, you need to set up your environment variables in <mcfile name="config.env" path="SafeStep/config.env"></mcfile>:

```bash
# Database Configuration (Supabase)
DATABASE_URL=postgresql://postgres:[password]@db.[project-ref].supabase.co:5432/postgres
SUPABASE_URL=https://[project-ref].supabase.co
SUPABASE_KEY=your_supabase_anon_key

# Flask Configuration
SECRET_KEY=your_very_secure_secret_key_here
FLASK_ENV=production

# Email Configuration (optional)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password

# Google Gemini API (for chatbot)
GEMINI_API_KEY=your_gemini_api_key
```

## Step 3: Build and Deploy

### Option A: Using Cloud Build (Recommended)

```bash
# Build and deploy in one command
gcloud run deploy safestep-app \
    --source . \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --memory 2Gi \
    --cpu 2 \
    --timeout 300s \
    --max-instances 100 \
    --set-env-vars "FLASK_ENV=production" \
    --set-env-vars "DATABASE_URL=your_supabase_database_url" \
    --set-env-vars "SUPABASE_URL=your_supabase_url" \
    --set-env-vars "SUPABASE_KEY=your_supabase_anon_key" \
    --set-env-vars "SECRET_KEY=your_flask_secret_key"
```

### Option B: Using Docker and Container Registry

```bash
# Set your project ID
export PROJECT_ID=your-project-id

# Build the Docker image
docker build -t gcr.io/$PROJECT_ID/safestep-app .

# Push to Container Registry
docker push gcr.io/$PROJECT_ID/safestep-app

# Deploy to Cloud Run
gcloud run deploy safestep-app \
    --image gcr.io/$PROJECT_ID/safestep-app \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --memory 2Gi \
    --cpu 2 \
    --timeout 300s \
    --max-instances 100
```

## Step 4: Set Environment Variables (if not set during deployment)

```bash
# Set environment variables after deployment
gcloud run services update safestep-app \
    --region us-central1 \
    --set-env-vars "DATABASE_URL=your_supabase_database_url,SUPABASE_URL=your_supabase_url,SUPABASE_KEY=your_supabase_anon_key,SECRET_KEY=your_flask_secret_key,FLASK_ENV=production"
```

## Step 5: Configure Domain (Optional)

```bash
# Map a custom domain
gcloud run domain-mappings create \
    --service safestep-app \
    --domain your-domain.com \
    --region us-central1
```

## Important Notes

### Security
- Never commit secrets to your repository
- Use Google Secret Manager for sensitive data in production
- The application creates default admin credentials (admin/admin123) - change these immediately

### Database
- Ensure your Supabase database allows connections from Cloud Run
- The application will automatically create required tables on first run
- Make sure your DATABASE_URL is correctly formatted

### Analytics Features
- The analytics dashboard requires administrator privileges
- All analytics API endpoints are protected with `@login_required` and `@admin_required`
- The application connects to Supabase for real-time analytics data

### Monitoring
```bash
# View logs
gcloud run services logs read safestep-app --region us-central1

# Check service status
gcloud run services describe safestep-app --region us-central1
```

### Scaling
- Cloud Run will automatically scale based on traffic
- Current configuration: 0-100 instances
- 2GB RAM and 2 CPU per instance for analytics processing

## Troubleshooting

### Common Issues
1. **Build failures**: Check that all dependencies in <mcfile name="requirements.txt" path="requirements.txt"></mcfile> are compatible
2. **Database connection**: Verify Supabase credentials and network access
3. **Memory issues**: Analytics queries may need more RAM - adjust `--memory` parameter
4. **Timeout issues**: Long analytics queries may timeout - adjust `--timeout` parameter

### Debug Commands
```bash
# Check deployment status
gcloud run services list

# View detailed service info
gcloud run services describe safestep-app --region us-central1

# Stream logs in real-time
gcloud run services logs tail safestep-app --region us-central1
```

## Access Your Application

After successful deployment, you'll receive a URL like:
`https://safestep-app-[hash]-uc.a.run.app`

Default login credentials:
- **Admin**: admin / admin123
- **Demo Caregiver**: demo / demo123

**⚠️ Important**: Change the default admin password immediately after first login!