# SafeStep - Seizure Monitoring and Caregiver Support Platform

SafeStep is a comprehensive web application designed to help caregivers monitor and support individuals with seizure conditions. The platform provides real-time monitoring, training modules, safety zone management, and administrative tools.

## Features

### For Caregivers
- **Dashboard**: Overview of recent seizure sessions, safety zones, and training progress
- **Seizure Monitoring**: Real-time monitoring and session tracking
- **Seizure History**: Detailed history of seizure sessions with analytics
- **Safety Zones**: GPS-based safety zone creation and management
- **Training Modules**: Interactive training content with progress tracking
- **Prediction Dashboard**: AI-powered seizure prediction insights
- **Support Tickets**: Direct communication with support team

### For Administrators
- **Admin Dashboard**: System-wide analytics and metrics
- **User Management**: Complete CRUD operations for user accounts
- **Ticket Management**: Support ticket handling and resolution
- **Training Management**: Content creation and module management
- **System Monitoring**: Real-time system health and performance
- **Analytics**: Comprehensive reporting and data visualization

## Technology Stack

- **Backend**: Flask (Python)
- **Database**: SQLAlchemy with PostgreSQL (Supabase) / SQLite fallback
- **Authentication**: Flask-Login with Supabase Auth integration
- **Frontend**: Bootstrap 5.3.0, JavaScript, HTML5
- **Cloud Services**: Supabase for authentication and database

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/SAITHIHANAING1/webtest.git
   cd webtest/SafeStep
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # or
   source venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Setup**:
   Create a `.env` file in the SafeStep directory:
   ```env
   SECRET_KEY=your-secret-key-here
   SUPABASE_URL=your-supabase-url
   SUPABASE_KEY=your-supabase-anon-key
   DATABASE_URL=your-database-url (optional)
   ```

5. **Initialize Database**:
   ```bash
   python app.py
   ```

## Usage

1. **Start the application**:
   ```bash
   python app.py
   ```

2. **Access the application**:
   - Open your browser and navigate to `http://127.0.0.1:5000`
   - Default admin credentials: username `admin`, password `admin123`

3. **User Types**:
   - **Caregiver**: Access to monitoring, history, safety zones, and training
   - **Admin**: Full system access including user management and analytics

## Project Structure

```
SafeStep/
├── app.py                      # Main Flask application
├── supabase_integration.py     # Supabase authentication and database
├── migrate_database.py         # Database migration utilities
├── setup_fresh_db.py          # Fresh database setup
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (create this)
├── static/
│   ├── css/style.css          # Custom styles
│   └── js/main.js             # JavaScript functionality
├── templates/
│   ├── base.html              # Base template
│   ├── landing.html           # Landing page
│   ├── auth/                  # Authentication templates
│   ├── caregiver/             # Caregiver dashboard templates
│   └── admin/                 # Admin dashboard templates
└── instance/
    └── safestep.db           # SQLite database (fallback)
```

## Database Models

- **User**: User accounts with role-based access
- **SeizureSession**: Seizure episode tracking
- **SafetyZone**: GPS-based safety zones
- **TrainingModule**: Educational content modules
- **TrainingProgress**: User training completion tracking
- **SupportTicket**: Support request management
- **PredictionJob**: AI prediction results

## API Endpoints

### Authentication
- `POST /login` - User authentication
- `POST /signup` - User registration
- `GET /logout` - User logout

### Caregiver Routes
- `GET /caregiver/dashboard` - Main dashboard
- `GET /caregiver/monitoring` - Real-time monitoring
- `GET /caregiver/history` - Seizure history
- `GET /caregiver/zones` - Safety zone management
- `GET /caregiver/training` - Training modules

### Admin Routes
- `GET /admin/dashboard` - Admin dashboard
- `GET /admin/users` - User management
- `POST /admin/users/delete/<id>` - Delete user
- `POST /admin/users/toggle-status/<id>` - Toggle user status

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions, please create a support ticket through the application or contact the development team.

## Development Team

- **Sai**: Dashboard and Zone Management
- **Arbaz**: Analytics and User Management
- **Ethan**: Training System
- **Issac**: Monitoring and Predictions