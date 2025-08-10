<div align="center">
  <h1>🧠 SafeStep</h1>
  <p><strong>Advanced Epilepsy Management & Analytics Platform</strong></p>
  
  <p>
    <a href="#features">Features</a> •
    <a href="#quick-start">Quick Start</a> •
    <a href="#installation">Installation</a> •
    <a href="#documentation">Documentation</a> •
    <a href="#contributing">Contributing</a>
  </p>

  <p>
    <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python Version">
    <img src="https://img.shields.io/badge/Flask-2.3.3-green.svg" alt="Flask Version">
    <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License">
    <img src="https://img.shields.io/badge/Platform-Web-lightgrey.svg" alt="Platform">
  </p>
</div>

## 📋 Table of Contents

- [About](#about)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [API Documentation](#api-documentation)
- [Contributing](#contributing)
- [License](#license)
- [Support](#support)

## 🎯 About

SafeStep is a comprehensive web application designed to revolutionize epilepsy care through intelligent monitoring, AI-powered predictions, and advanced analytics. The platform empowers caregivers and healthcare professionals with real-time insights, safety zone management, and evidence-based training modules.

### Key Highlights
- 🤖 **AI-Powered Predictions** - Machine learning models for seizure risk assessment
- 📊 **Real-time Analytics** - Interactive dashboards with comprehensive KPIs
- 🗺️ **GPS Safety Zones** - Location-based monitoring and alerts
- 📚 **Training Modules** - Evidence-based educational content
- 🔄 **Cloud Integration** - Supabase backend with offline fallback
- 👥 **Multi-user Support** - Role-based access for caregivers and administrators

## ✨ Features

### 🩺 For Caregivers
| Feature | Description |
|---------|-------------|
| **Smart Dashboard** | Overview of recent seizure sessions, safety zones, and training progress |
| **Real-time Monitoring** | Live seizure tracking with instant notifications |
| **Seizure History** | Detailed analytics and pattern recognition |
| **Safety Zones** | GPS-based zone creation and breach alerts |
| **Training Hub** | Interactive modules with progress tracking |
| **AI Predictions** | Personalized risk assessments and recommendations |
| **Support System** | Direct communication with healthcare teams |

### 👨‍💼 For Administrators
| Feature | Description |
|---------|-------------|
| **Analytics Dashboard** | System-wide metrics and performance insights |
| **User Management** | Complete CRUD operations with role-based access |
| **Ticket Management** | Support request handling and resolution |
| **Content Management** | Training module creation and updates |
| **System Monitoring** | Real-time health checks and performance metrics |
| **Report Generation** | Comprehensive PDF reports with custom filters |

## 🛠️ Technology Stack

### Backend
- **Framework**: Flask 2.3.3 (Python)
- **Database**: SQLAlchemy with PostgreSQL (Supabase) / SQLite fallback
- **Authentication**: Flask-Login + Supabase Auth
- **ML/AI**: scikit-learn, numpy, pandas
- **Cloud**: Supabase for real-time database and authentication

### Frontend
- **UI Framework**: Bootstrap 5.3.0
- **Visualizations**: Chart.js for interactive analytics
- **Icons**: Font Awesome
- **JavaScript**: ES6+ with modern browser APIs

### DevOps & Production
- **Server**: Gunicorn for production deployment
- **Environment**: python-dotenv for configuration
- **Security**: bcrypt for password hashing, Row Level Security

## 🚀 Quick Start

Get SafeStep running in under 5 minutes:

```bash
# Clone the repository
git clone https://github.com/SAITHIHANAING1/webtest.git
cd webtest/SafeStep

# Set up virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the application
python app.py
```

🌐 **Access the app**: Open [http://127.0.0.1:5000](http://127.0.0.1:5000)  
🔑 **Default login**: username `admin`, password `admin123`

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git

### Step-by-Step Setup

#### 1. Clone and Navigate
```bash
git clone https://github.com/SAITHIHANAING1/webtest.git
cd webtest/SafeStep
```

#### 2. Environment Setup
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Configuration
Create a `.env` file in the SafeStep directory:
```env
# Required for Supabase integration
SUPABASE_URL=your-supabase-project-url
SUPABASE_KEY=your-supabase-anon-key

# Flask configuration
FLASK_SECRET_KEY=your-secret-key-here

# Optional: Custom database URL
DATABASE_URL=your-database-url
```

#### 5. Database Initialization
```bash
# Initialize the database with sample data
python app.py
```

### 🐳 Docker Setup (Optional)
```bash
# Build the container
docker build -t safestep .

# Run the application
docker run -p 5000:5000 safestep
```

## 🎮 Usage

### Starting the Application
```bash
# Development mode
python app.py

# Production mode with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### User Access Levels

#### 🩺 Caregiver Dashboard
- **URL**: `http://127.0.0.1:5000/caregiver/dashboard`
- **Access**: Monitor patients, view analytics, manage safety zones
- **Features**: Real-time monitoring, seizure history, training modules

#### 👨‍💼 Admin Panel  
- **URL**: `http://127.0.0.1:5000/admin/dashboard`
- **Access**: Full system management and analytics
- **Features**: User management, system monitoring, advanced analytics

#### 🤖 AI Predictions
- **URL**: `http://127.0.0.1:5000/analytics`
- **Access**: Machine learning risk assessments
- **Features**: Individual patient predictions, batch processing, risk factor analysis

### Key Workflows

1. **Patient Monitoring**
   - Set up safety zones → Monitor real-time → Review analytics → Generate reports

2. **Risk Assessment**
   - Run AI predictions → Review risk factors → Implement recommendations → Track outcomes

3. **Training Management**
   - Create modules → Assign to users → Track progress → Update content

## 📁 Project Structure

```
webtest/
├── README.md                    # Main documentation (this file)
├── SafeStep/                    # Core application directory
│   ├── app.py                   # Flask application entry point
│   ├── requirements.txt         # Python dependencies
│   ├── .env.example            # Environment configuration template
│   ├── models.py               # Database models and schema
│   ├── prediction_model.py     # AI/ML prediction engine
│   ├── supabase_integration.py # Cloud database integration
│   ├── static/                 # Static assets (CSS, JS, images)
│   │   ├── css/style.css       # Custom styles
│   │   └── js/main.js          # Frontend JavaScript
│   ├── templates/              # HTML templates
│   │   ├── base.html           # Base template
│   │   ├── auth/               # Authentication pages
│   │   ├── caregiver/          # Caregiver dashboard templates
│   │   └── admin/              # Admin panel templates
│   ├── prediction/             # ML model storage
│   │   └── epilepsy_model.pkl  # Trained model files
│   └── instance/
│       └── safestep.db        # SQLite database (fallback)
└── .vscode/                    # VS Code configuration
```

### Key Components

| Component | Description | Location |
|-----------|-------------|----------|
| **Main App** | Flask application with routing | `SafeStep/app.py` |
| **ML Engine** | AI prediction models | `SafeStep/prediction_model.py` |
| **Database** | ORM models and schema | `SafeStep/models.py` |
| **Cloud Integration** | Supabase authentication/database | `SafeStep/supabase_integration.py` |
| **Frontend** | Bootstrap UI with Chart.js | `SafeStep/templates/` |
| **Analytics** | Admin dashboard templates | `SafeStep/templates/admin/Arbaz/` |

## 📚 API Documentation

### Core Endpoints

#### Authentication
```http
POST /login              # User authentication
POST /signup             # User registration  
GET  /logout             # User logout
```

#### Caregiver Routes
```http
GET  /caregiver/dashboard        # Main dashboard
GET  /caregiver/monitoring       # Real-time monitoring
GET  /caregiver/history         # Seizure history
GET  /caregiver/zones           # Safety zone management
GET  /caregiver/training        # Training modules
GET  /caregiver/predictions     # AI risk assessments
```

#### Admin Routes
```http
GET  /admin/dashboard                    # Admin overview
GET  /admin/users                       # User management
POST /admin/users/delete/<id>           # Delete user
POST /admin/users/toggle-status/<id>    # Toggle user status
GET  /admin/analytics                   # Analytics dashboard
```

#### Analytics API
```http
GET  /api/analytics/metrics             # KPIs with filters
GET  /api/analytics/seizure-trends      # Risk trend data
GET  /api/analytics/location-distribution # Location analytics
POST /api/analytics/run-prediction      # Trigger AI analysis
GET  /api/analytics/predict-patient/<id> # Individual prediction
POST /api/analytics/export-pdf          # Export reports
```

### Response Formats

All API endpoints return JSON responses:
```json
{
  "status": "success|error",
  "data": { ... },
  "message": "Human readable message",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

## 🤝 Contributing

We welcome contributions from the community! Here's how you can help improve SafeStep:

### 🚀 Getting Started

1. **Fork the repository**
   ```bash
   git clone https://github.com/yourusername/webtest.git
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-new-feature
   ```

3. **Make your changes**
   - Follow the existing code style
   - Add tests for new features
   - Update documentation as needed

4. **Test your changes**
   ```bash
   # Run the application
   python SafeStep/app.py
   
   # Test key functionality
   # - User authentication
   # - Dashboard loading
   # - Analytics generation
   ```

5. **Commit and push**
   ```bash
   git add .
   git commit -m "feat: add amazing new feature"
   git push origin feature/amazing-new-feature
   ```

6. **Submit a Pull Request**
   - Provide a clear description of changes
   - Reference any related issues
   - Include screenshots for UI changes

### 📋 Development Guidelines

#### Code Style
- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add comments for complex logic
- Maintain consistent indentation (4 spaces)

#### Testing
- Test new features thoroughly
- Verify existing functionality still works
- Test with both Supabase and SQLite databases
- Check responsiveness on different screen sizes

#### Documentation
- Update README.md for significant changes
- Add docstrings to new functions
- Update API documentation for new endpoints
- Include usage examples where helpful

### 🐛 Bug Reports

Found a bug? Please create an issue with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Screenshots (if applicable)
- System information (OS, Python version, browser)

### 💡 Feature Requests

Have an idea for improvement? We'd love to hear it!
- Check if the feature already exists
- Describe the use case clearly
- Explain how it would benefit users
- Consider implementation complexity

### 🏗️ Areas for Contribution

- **AI/ML Models**: Improve prediction accuracy
- **UI/UX**: Enhance user experience and design
- **Performance**: Optimize database queries and page load times
- **Security**: Strengthen authentication and data protection
- **Documentation**: Improve guides and API documentation
- **Testing**: Add automated tests and quality assurance
- **Accessibility**: Ensure compliance with WCAG guidelines

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

### MIT License Summary
- ✅ Commercial use allowed
- ✅ Modification allowed
- ✅ Distribution allowed
- ✅ Private use allowed
- ❌ No warranty provided
- ❌ No liability assumed

## 🆘 Support

Need help? We're here to assist you!

### 📞 Getting Help

| Type | Contact | Response Time |
|------|---------|---------------|
| **Bug Reports** | [Create an Issue](https://github.com/SAITHIHANAING1/webtest/issues) | 24-48 hours |
| **Feature Requests** | [GitHub Discussions](https://github.com/SAITHIHANAING1/webtest/discussions) | 2-3 days |
| **General Questions** | Email: support@safestep.com | 1-2 business days |
| **Documentation** | [Wiki](https://github.com/SAITHIHANAING1/webtest/wiki) | Self-service |

### 🔧 Troubleshooting

#### Common Issues

**Installation Problems**
```bash
# If pip install fails
pip install --upgrade pip
pip install -r requirements.txt --no-cache-dir

# If virtual environment issues
python -m venv --clear venv
```

**Database Connection Issues**
```bash
# Check environment variables
cat .env

# Test Supabase connection
python -c "from supabase_integration import test_connection; test_connection()"
```

**Authentication Problems**
- Verify Supabase credentials in `.env`
- Check user roles and permissions
- Clear browser cache and cookies

### 📊 System Status
- **Application Status**: ✅ Operational
- **Database**: ✅ Connected
- **AI Models**: ✅ Active
- **Support**: ✅ Available

---

<div align="center">
  <h3>🧠 SafeStep</h3>
  <p><em>Empowering epilepsy care through intelligent analytics and AI-driven insights</em></p>
  
  <p>
    <a href="https://github.com/SAITHIHANAING1/webtest">🏠 Home</a> •
    <a href="https://github.com/SAITHIHANAING1/webtest/issues">🐛 Issues</a> •
    <a href="https://github.com/SAITHIHANAING1/webtest/discussions">💬 Discussions</a> •
    <a href="https://github.com/SAITHIHANAING1/webtest/wiki">📚 Wiki</a>
  </p>

  <p>
    <strong>Made with ❤️ by the SafeStep Development Team</strong><br>
    <small>© 2024 SafeStep. All rights reserved.</small>
  </p>
</div>