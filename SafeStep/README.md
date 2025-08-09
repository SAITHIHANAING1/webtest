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

## 🚀 Quick Start

### 1. Environment Setup
```bash
# Clone the repository
git clone <repository-url>
cd SafeStep

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Configuration
Create a `.env` file in the SafeStep directory:
```env
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key
FLASK_SECRET_KEY=your_secret_key
```

### 3. Database Setup
1. Create a Supabase project
2. Execute the SQL schema in Supabase SQL Editor
3. Populate with sample data using the provided SQL scripts

### 4. Run the Application
```bash
python app.py
```

Access the application at: `http://localhost:5000`

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
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Using Docker (if configured)
docker build -t safestep .
docker run -p 5000:5000 safestep
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
