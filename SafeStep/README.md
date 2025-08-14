# SafeStep - Epilepsy Management & Analytics Platform

A comprehensive web application for epilepsy management, featuring real-time analytics, AI-powered risk prediction, and interactive dashboards.

## 🚀 Features

### Core Analytics Dashboard
- **Real-time KPIs**: Total incidents, seizure events, response times, high-risk cases
- **Interactive Charts**: Seizure risk trends, location distribution with dynamic filtering
- **Advanced Filters**: Date range, patient type, location, incident type
- **Export Functionality**: PDF reports with filtered data

### AI-Powered Prediction Engine
- **Machine Learning Model**: Random Forest + Gradient Boosting for risk assessment
- **Individual Patient Predictions**: Real-time risk scoring with confidence levels
- **Risk Factor Analysis**: Identifies key risk factors for each patient
- **Personalized Recommendations**: AI-generated care recommendations
- **Batch Processing**: Updates risk scores for all patients automatically

### Database Integration
- **Supabase First**: Cloud database with real-time sync
- **SQLite Fallback**: Local database for offline functionality
- **Error Handling**: Graceful degradation with user feedback

## 🛠️ Technology Stack

### Backend
- **Flask**: Python web framework
- **SQLAlchemy**: Database ORM
- **Supabase**: Cloud database and authentication
- **scikit-learn**: Machine learning library
- **numpy/pandas**: Data processing

### Frontend
- **Bootstrap 5**: Responsive UI framework
- **Chart.js**: Interactive data visualizations
- **Font Awesome**: Icons and UI elements
- **JavaScript ES6+**: Modern frontend functionality

### Machine Learning
- **Random Forest Classifier**: Risk level classification (Low/Medium/High/Critical)
- **Gradient Boosting Regressor**: Risk score prediction (0-100)
- **Feature Engineering**: Patient demographics, medical history, incident patterns
- **Model Persistence**: Trained models saved locally

## 📊 Analytics Features

### Key Performance Indicators
- Total incidents with trend analysis
- Seizure event tracking
- Average response time monitoring
- High-risk case identification

### Interactive Visualizations
- **Risk Trend Chart**: Time-series analysis of seizure patterns
- **Location Distribution**: Doughnut chart showing incident locations
- **Real-time Updates**: Charts refresh based on filter changes

### Advanced Filtering
- Date range selection (7, 30, 90 days)
- Patient type filtering
- Location-based filtering
- Incident type categorization

## 🤖 AI Prediction Features

### Risk Assessment
- **Risk Level Classification**: Low, Medium, High, Critical
- **Risk Score Calculation**: 0-100 scale with confidence intervals
- **Risk Factor Identification**: Key factors contributing to risk
- **Recommendation Engine**: Personalized care suggestions

### Model Features
- Patient demographics (age, gender)
- Epilepsy type (focal, generalized, combined)
- Seizure frequency patterns
- Medication regimen complexity
- Recent incident history
- Response time analysis
- Hospital admission patterns

### Prediction Capabilities
- **Individual Patient Analysis**: Real-time risk assessment
- **Batch Processing**: Update all patient risk scores
- **Confidence Scoring**: Model confidence for each prediction
- **Historical Pattern Analysis**: Learning from past incidents

## 🗄️ Database Schema

### Patients Table (`pwids`)
```sql
- patient_id (VARCHAR, unique)
- name, age, gender
- epilepsy_type, seizure_frequency
- medication_regimen (JSON)
- risk_status, risk_score
- recent_seizure_count
- average_response_time
- electrode_implant, monitoring_type
- hfo_burden
- timestamps
```

### Incidents Table (`incidents`)
```sql
- patient_id (foreign key)
- incident_date, incident_type
- severity, duration_seconds
- seizure_type, consciousness_state
- location, environment
- response_time_minutes
- outcome, intervention_type
- EEG data (sampling_rate, electrode_count)
- timestamps
```

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.8 or higher
- Git
- Internet connection (for Supabase integration)

### Step 1: Clone and Setup
```bash
# Clone the repository
git clone <repository-url>
cd SafeStep

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Environment Configuration
Create a `.env` file in the SafeStep directory with the following content:
```env
# Supabase Configuration (Required for full functionality)
SUPABASE_URL=https://hduukqxhrebuifafooxv.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhkdXVrcXhocmVidWlmYWZvb3h2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQwNjA4NjAsImV4cCI6MjA2OTYzNjg2MH0.IBG_hPMoeM0_TAfhhZseiug0wI_o7_rTsIeGMWvy8o8

# Flask Configuration
SECRET_KEY=your-secret-key-here
FLASK_ENV=development

# Optional: Email Configuration
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# Security
SESSION_COOKIE_SECURE=false

# AI Configuration
GEMINI_API_KEY=your_gemini_api_key_here
```

### Step 3: Database Setup
The application uses Supabase as the primary database with SQLite fallback:

```bash
# Run database migration (IMPORTANT!)
python migrate_db.py
```

This script will:
- Add missing database columns
- Fix demo user password hashes
- Create missing demo users if needed
- Set up proper database schema

### Step 4: Run the Application
```bash
# Start the Flask server
python app.py
```

The application will be available at: `http://localhost:5000`

### Step 5: Login and Access Features
Use these demo credentials:
- **Admin**: username=`admin`, password=`admin123`
- **Caregiver**: username=`demo`, password=`demo123`
- **Caregiver**: username=`caregiver`, password=`caregiver123`

### Available Pages
After logging in, you can access:
- **Dashboard**: `http://localhost:5000/dashboard`
- **Analytics**: `http://localhost:5000/analytics`
- **Enhanced Features**:
  - Medications: `http://localhost:5000/enhanced/medications`
  - Care Plans: `http://localhost:5000/enhanced/care-plans`
  - Emergency Contacts: `http://localhost:5000/enhanced/emergency-contacts`
  - Providers: `http://localhost:5000/enhanced/providers`

## 🛠️ Troubleshooting

### Common Issues and Solutions

#### 1. "Failed to load medications/care-plans/emergency-contacts" Error
**Cause**: Missing database tables or permission issues
**Solution**: The application now handles this gracefully by returning empty data. If you want full functionality:
```bash
# Run the migration script to create missing tables
python run_migration.py
```

#### 2. SQLite Database Error: `no such column: seizure_session.patient_id`
**Solution**: Run the database migration script
```bash
python migrate_db.py
```

#### 3. Login Failed: Invalid password for demo users
**Solution**: The migration script will fix this automatically:
```bash
python migrate_db.py
```

#### 4. "Permission denied for table users" in Supabase
**Cause**: Medications table doesn't exist or has permission restrictions
**Solution**: The app gracefully handles this and shows empty data. For full functionality, create the tables in Supabase using the migration SQL.

#### 5. Database File Not Found
**Solution**: Start the app once to create the database, then run migration:
```bash
# Start app (it will create the database then exit with error)
python app.py
# Stop with Ctrl+C, then run migration
python migrate_db.py
# Start app again
python app.py
```

#### 6. Missing Dependencies
**Solution**: Install requirements
```bash
pip install -r requirements.txt
```

#### 7. Supabase Connection Issues
**Solution**: The app falls back to SQLite. Check your `.env` file:
```env
SUPABASE_URL=https://hduukqxhrebuifafooxv.supabase.co
SUPABASE_KEY=your_actual_anon_key
```

#### 8. "TypeError: Cannot read properties of undefined" in Frontend
**Cause**: API response format mismatch
**Solution**: This has been fixed in the latest version. Restart the server:
```bash
# Stop the server (Ctrl+C) and restart
python app.py
```

#### 9. Enhanced Features Not Loading
**Solution**: Ensure you're accessing the correct URLs:
- Medications: `http://localhost:5000/enhanced/medications`
- Care Plans: `http://localhost:5000/enhanced/care-plans`
- Emergency Contacts: `http://localhost:5000/enhanced/emergency-contacts`
- Providers: `http://localhost:5000/enhanced/providers`

### Development Workflow
1. Clone repository
2. Create virtual environment and install dependencies
3. Create `.env` file with proper configuration
4. Run `python migrate_db.py` after cloning
5. Start development with `python app.py`
6. Access application at `http://localhost:5000`

### Verification Steps
After setup, verify everything works:
1. Login with demo credentials
2. Check dashboard loads without errors
3. Test enhanced features (medications, care plans, etc.)
4. Verify API endpoints return proper JSON responses

### Getting Help
If you encounter issues:
1. Check the terminal/console for error messages
2. Verify your `.env` file configuration
3. Ensure all dependencies are installed
4. Try running the migration script again
5. Check that you're using the correct URLs for enhanced features

## 📈 Analytics Dashboard

### Access
- URL: `/analytics` or `/admin/analytics`
- Login: `admin` / `admin123`

### Features
1. **Metrics Overview**: Real-time KPIs with trend indicators
2. **Interactive Charts**: Click and filter data dynamically
3. **Advanced Filters**: Multi-dimensional data filtering
4. **Export Reports**: PDF generation with current filters
5. **AI Predictions**: Machine learning risk assessment

### Chart Types
- **Risk Trend Chart**: Line chart showing seizure risk over time
- **Location Distribution**: Doughnut chart of incident locations
- **Prediction Results**: Table with ML-generated risk scores

## 🤖 AI Prediction Engine

### Training the Model
The ML model is automatically trained when:
1. Running the prediction engine for the first time
2. New patient data is added to the system
3. Manual retraining is triggered

### Model Features
- **Patient Demographics**: Age, gender, epilepsy type
- **Medical History**: Seizure frequency, medication count
- **Recent Activity**: Recent seizures, response times
- **Incident Patterns**: Severity, location, outcomes

### Prediction Output
- **Risk Level**: Classification (Low/Medium/High/Critical)
- **Risk Score**: Numerical score (0-100)
- **Confidence**: Model confidence percentage
- **Risk Factors**: Identified contributing factors
- **Recommendations**: Personalized care suggestions

## 🔧 API Endpoints

### Analytics
- `GET /api/analytics/metrics` - Get KPIs with filters
- `GET /api/analytics/seizure-trends` - Risk trend data
- `GET /api/analytics/location-distribution` - Location data
- `GET /api/analytics/prediction-results` - ML predictions
- `POST /api/analytics/run-prediction` - Trigger AI analysis
- `GET /api/analytics/predict-patient/<id>` - Individual prediction
- `POST /api/analytics/export-pdf` - Export reports

### Authentication
- `POST /login` - User authentication
- `POST /logout` - User logout
- `GET /admin/*` - Admin-only routes

## 📁 Project Structure

```
SafeStep/
├── app.py                 # Main Flask application
├── models.py             # Database models
├── prediction_model.py   # ML prediction engine
├── supabase_integration.py # Supabase integration
├── requirements.txt      # Python dependencies
├── templates/           # HTML templates
│   ├── admin/
│   │   └── Arbaz/
│   │       └── analytics.html
│   └── base.html
├── static/             # Static assets
│   ├── css/
│   └── js/
└── prediction/         # ML model storage
    └── epilepsy_model.pkl
```

## 🔒 Security Features

- **Authentication**: User login/logout system
- **Authorization**: Role-based access control (admin/caregiver)
- **Data Protection**: Supabase Row Level Security
- **Input Validation**: Server-side data validation
- **Error Handling**: Graceful error management

## 📊 Data Sources

The system uses realistic epilepsy data based on:
- EEG datasets from Nature Scientific Data 2025
- Long-term multi-site LFP activity datasets
- Mesoscale insights in Epileptic Networks
- SzCORE seizure detection challenge datasets

## 🚀 Deployment

### Local Development
```bash
python app.py
```

### Production Deployment
```bash
# Using Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app

# Run the application
python app.py
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation

---

**SafeStep** - Empowering epilepsy care through intelligent analytics and AI-driven insights.
