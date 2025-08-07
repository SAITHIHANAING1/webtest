# Arbaz's SafeStep Components Documentation

This document outlines all the components created for Arbaz's responsibilities in the SafeStep application.

## 🎯 Overview

Arbaz is responsible for three main components:
1. **Analytics Dashboard** - Business intelligence hub for staff managers
2. **AI Prediction Engine** - Backend service for risk assessment
3. **RAG AI Chatbot** - Gemini API-based intelligent assistant

---

## 📊 1. Analytics Dashboard

### Files Created/Modified:
- `templates/admin/Arbaz/analytics.html` - Main dashboard interface
- `app.py` - Backend routes and API endpoints

### Features:
- **Interactive Filters**: Date range, PWID, location filtering
- **KPI Cards**: Active Users, Monitoring Sessions, Alert Events, Avg Response Time
- **Chart Visualizations**: Usage trends with Chart.js
- **Export Functionality**: PDF export capability (WeasyPrint integration planned)

### API Endpoints:
- `GET /api/analytics/metrics` - Returns KPI data
- `GET /api/analytics/charts/trends?period=7d` - Returns trend data for charts
- `GET /api/analytics/charts/distribution` - Returns alert distribution data
- `POST /api/analytics/export-pdf` - Generates PDF reports

### Access:
- URL: `/admin/analytics`
- Requires: Admin role authentication

---

## 🧠 2. AI Prediction Engine

### Files Created:
- `prediction_engine.py` - Core prediction logic
- `test_prediction_engine.py` - Test script for demonstration

### Features:
- **Seizure Pattern Analysis**: Analyzes seizure frequency, severity, and timing
- **Risk Assessment**: Calculates risk scores and assigns risk statuses
- **Database Integration**: Works with `incidents.db` and `pwids.db`
- **Automated Updates**: Updates PWID risk profiles automatically

### Risk Assessment Logic:
- **High-Risk**: >3 seizures in 7 days, or severe seizures
- **Medium-Risk**: 2-3 seizures in 7 days
- **Low-Risk**: 0-1 seizures in 7 days

### Usage:
```python
from prediction_engine import PredictionEngine

# Initialize engine
engine = PredictionEngine('incidents.db', 'pwids.db')

# Analyze individual PWID
risk_assessment = engine.analyze_seizure_patterns(pwid_id)

# Run daily analysis for all PWIDs
summary = engine.run_daily_analysis()

# Get risk summary
risk_summary = engine.get_risk_summary()
```

### Testing:
```bash
cd SafeStep
python test_prediction_engine.py
```

---

## 🤖 3. RAG AI Chatbot

### Files Created:
- `rag_chatbot_bp.py` - Flask blueprint for chatbot backend
- `static/js/chatbot.js` - Frontend JavaScript for chat widget
- `static/css/chatbot.css` - Styling for chat widget
- `templates/admin/Arbaz/chatbot_admin.html` - Admin interface
- `app.py` - Integration and routes
- `base.html` - Chatbot widget integration

### Features:
- **Gemini API Integration**: Uses Google's Gemini Pro model
- **RAG Knowledge Base**: In-memory knowledge base with application data
- **Role-Based Access**: Different responses for admin vs caregiver users
- **Floating Chat Widget**: Available on all pages
- **Admin Interface**: Monitor and manage chatbot status

### Knowledge Base Sources:
- User data from `safestep.db`
- Training modules content
- Safety protocols and guidelines
- System information

### API Endpoints:
- `POST /api/chatbot/ask` - Process user questions
- `GET /api/chatbot/status` - Check chatbot status
- `POST /api/chatbot/reload` - Reload knowledge base

### Access:
- Chat Widget: Available on all pages (bottom-right corner)
- Admin Interface: `/admin/chatbot`
- Requires: GEMINI_API_KEY environment variable

---

## 🔧 Setup and Configuration

### Environment Variables:
```bash
# Required for chatbot
GEMINI_API_KEY=your_gemini_api_key_here

# Optional for analytics PDF export
WEASYPRINT_PATH=/path/to/weasyprint
```

### Dependencies Added:
```txt
google-generativeai==0.3.2  # For Gemini API chatbot
weasyprint==60.2           # For PDF generation
```

### Database Setup:
The prediction engine requires two SQLite databases:
- `incidents.db` - Stores seizure incident data
- `pwids.db` - Stores PWID profiles and risk assessments

### Installation:
```bash
cd SafeStep
pip install -r requirements.txt
```

---

## 🚀 Usage Examples

### 1. Running the Analytics Dashboard:
1. Start the Flask application
2. Navigate to `/admin/analytics`
3. Use filters to view different time periods
4. Export reports to PDF

### 2. Testing the Prediction Engine:
```bash
python test_prediction_engine.py
```
This will:
- Create sample data
- Run risk analysis
- Update PWID risk statuses
- Show results

### 3. Using the Chatbot:
1. Ensure `GEMINI_API_KEY` is set
2. Start the Flask application
3. Chat widget appears on all pages
4. Access admin interface at `/admin/chatbot`

---

## 🔍 Integration Points

### With Isaac's Components:
- Prediction engine reads from `incidents.db` (created by Isaac)
- Risk statuses are stored in `pwids.db` and visible in Isaac's monitoring interface

### With Sai's Components:
- Risk statuses from prediction engine appear in Sai's staff dashboard
- Analytics data can be used for staff management decisions

### With Ethan's Components:
- Training module data is included in chatbot knowledge base
- Analytics can track training completion rates

---

## 🛠️ Development Notes

### Analytics Dashboard:
- Currently uses mock data for some metrics
- Real data integration requires connecting to actual database queries
- PDF export needs WeasyPrint implementation

### Prediction Engine:
- Uses simple rule-based logic
- Can be enhanced with machine learning models
- Designed for daily batch processing

### Chatbot:
- Uses in-memory knowledge base (can be enhanced with persistent storage)
- Simple keyword-based search (can be enhanced with vector search)
- Role-based filtering for security

---

## 📝 TODO Items

### Analytics Dashboard:
- [ ] Implement real data fetching for all metrics
- [ ] Complete WeasyPrint PDF export integration
- [ ] Add more chart types (pie charts, bar charts)
- [ ] Implement data caching for performance

### Prediction Engine:
- [ ] Add machine learning model integration
- [ ] Implement real-time analysis triggers
- [ ] Add more sophisticated risk factors
- [ ] Create scheduled task integration

### Chatbot:
- [ ] Implement persistent knowledge base storage
- [ ] Add vector search capabilities
- [ ] Implement conversation history
- [ ] Add more sophisticated role-based filtering

---

## 🐛 Troubleshooting

### Chatbot Not Working:
1. Check if `GEMINI_API_KEY` is set
2. Verify internet connection for API calls
3. Check browser console for JavaScript errors

### Prediction Engine Errors:
1. Ensure `incidents.db` and `pwids.db` exist
2. Check database schema matches expected format
3. Verify file permissions

### Analytics Dashboard Issues:
1. Check if user has admin role
2. Verify API endpoints are accessible
3. Check browser console for JavaScript errors

---

## 📞 Support

For issues or questions about these components:
1. Check the troubleshooting section above
2. Review the test scripts for examples
3. Check the Flask application logs
4. Verify all dependencies are installed correctly
