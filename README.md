# SAFE-Step – Seizure Monitoring & Caregiver Support

SAFE-Step is a Flask-based web app that helps caregivers and admins coordinate safety zones, monitor activity, and manage training resources.
![alt text](https://github.com/user-attachments/assets/87d27ff7-186a-4ce3-9080-43d948f464dc)



## ✨ Features

### Caregivers
- Personal dashboard with quick stats (zones, incidents, training)
- Zones overview
- Training modules
- Monitoring interface

### Administrators
- Admin dashboard with summary cards and recent incidents
- Zones management (list, edit modal UI placeholder)
- User management
- Incident oversight
- Training management

> The top navigation adapts to the current role (admin vs caregiver).*

## 🧱 Tech Stack

- **Backend:** Flask
- **Config:** `Config` class (env-driven) with SQLAlchemy settings pre-wired
- **Templates:** Jinja2 + Bootstrap 5
- **Static assets:** Vanilla JS, CSS
- **(Deps):** Flask-Login, Flask-SQLAlchemy, Flask-WTF, python-dotenv

## 📁 Project Structure
```
safe-step/
├─ app.py
├─ config.py
├─ requirements.txt
├─ templates/
│  ├─ base.html
│  ├─ header.html
│  ├─ footer.html
│  ├─ landing.html
│  ├─ caregiver\_dashboard.html
│  ├─ caregiver\_zones.html
│  ├─ caregiver\_monitor.html
│  ├─ caregiver\_training.html
│  ├─ admin\_dashboard.html
│  ├─ admin\_zones.html
│  ├─ admin\_users.html
│  └─ admin\_incidents.html
└─ static/
├─ css/
│  └─ style.css
└─ js/
└─ main.js

```

## ⚙️ Configuration

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

## 🚀 Getting Started

1) **Clone & enter the project**
```bash
git clone https://github.com/SAITHIHANAING1/webtest.git
cd safestep
````

2. **Create & activate a virtual environment**

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Run the app**

```bash
python app.py
```

5. **Open in browser**

```
http://127.0.0.1:5000/
```
### Login and Access Features
Use these demo credentials:
- **Admin**: username=`admin`, password=`admin123`
- **Caregiver**: username=`demo`, password=`demo123`
- **Caregiver**: username=`caregiver`, password=`caregiver123`

## 🧭 App Routing

* `/` – Public landing page
* Caregiver views: dashboard, monitor, zones, training
* Admin views: dashboard, zones, users, incidents, training

> The app registers `admin` and `caregiver` blueprints in `app.py`. Make sure their packages expose `routes.py` that defines `admin_bp` and `caregiver_bp`.

## 🧪 Development Notes
```
```bash
# Using Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app

# Run the application
python app.py
```


## 🤝 Contributing

1. Create a feature branch
   `git checkout -b feat/short-name`
2. Commit changes
   `git commit -m "feat: add <thing>"`
3. Push & open a PR

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Development Team

- **Sai**: Dashboard and Zone Management
- **Arbaz**: Analytics and User Management
- **Ethan**: Training System
- **Issac**: Monitoring and Predictions
- **Cheng Yan**: User Authentication and Management
  
## 🆘 Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation


