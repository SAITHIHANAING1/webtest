# SAFE-Step – Seizure Monitoring & Caregiver Support

SAFE-Step is a Flask-based web app that helps caregivers and admins coordinate safety zones, monitor activity, and manage training resources.

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

App settings are loaded from `Config` in `config.py`. Provide environment variables as needed:

- `SECRET_KEY` – Flask secret (required for sessions)
- `DATABASE_URL` – SQLAlchemy connection string (defaults to SQLite `sqlite:///safe-step.db`)

Example `.env` (optional if you export vars another way):

```

SECRET\_KEY=replace-me
DATABASE\_URL=sqlite:///safe-step.db

````

## 🚀 Getting Started

1) **Clone & enter the project**
```bash
git clone https://github.com/<your-org-or-user>/<your-repo>.git
cd <your-repo>
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

## 🧭 App Routing

* `/` – Public landing page
* Caregiver views: dashboard, monitor, zones, training
* Admin views: dashboard, zones, users, incidents, training

> The app registers `admin` and `caregiver` blueprints in `app.py`. Make sure their packages expose `routes.py` that defines `admin_bp` and `caregiver_bp`.

## 🧪 Development Notes

* UI uses Bootstrap 5 + Font Awesome via CDN (see `base.html`).
* Global styles live in `static/css/style.css`.
* Page-level behavior can go in `static/js/main.js`. A sample handler for zone delete buttons is included.

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

