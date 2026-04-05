# MediScan AI Pro

> Hybrid Disease Identifier with Offline Engine + Online AI Intelligence

## Overview

MediScan AI Pro is a Python-based web application that identifies possible diseases using an offline symptom-matching system while integrating advanced AI and real-time health intelligence APIs when internet is available.

**This application does NOT provide medical diagnosis. Always consult a licensed medical professional.**

---

## Features

### Offline Mode (Core)
- Symptom checker with local SQLite database
- Disease matching algorithm with percentage scoring
- 15+ preloaded diseases with symptoms, treatments, and prevention
- Full functionality without internet

### Online Mode (Enhanced)
- **AI Medical Assistant** via OpenRouter API (Medical LLM)
- **Weather-based Risk Assessment** via Open-Meteo API
- **Disease Outbreak Alerts** via CMU Delphi Epidata API
- **Location-based Insights** via Geoapify API
- Smart alerts combining weather + outbreak data

### UI/UX
- Fully responsive (mobile + desktop)
- Dark mode / Light mode toggle
- Animated cards, transitions, and hover effects
- Card-based modern interface
- PWA support for offline caching

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Backend | Python + FastAPI |
| Database | SQLite + SQLAlchemy ORM |
| Frontend | HTML, CSS, JavaScript |
| AI API | OpenRouter |
| Weather API | Open-Meteo |
| Epidata API | CMU Delphi Epidata |
| Location API | Geoapify |

---

## Quick Start

### 1. Setup

```bash
# Windows
setup.bat

# Manual
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure API Keys (Optional)

Copy `.env.example` to `.env` and add your API keys:

```bash
cd backend
copy .env.example .env
```

Edit `.env`:
```
OPENROUTER_API_KEY=your_key_here
GEOAPIFY_API_KEY=your_key_here
```

**Note:** The app works fully offline without API keys. Online features activate automatically when keys are configured.

### 3. Run

```bash
# Windows
start.bat

# Manual
cd backend
venv\Scripts\activate
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Open **http://localhost:8000** in your browser.

---

## Project Structure

```
dese/
├── backend/
│   ├── app/
│   │   ├── models/
│   │   │   └── models.py          # SQLAlchemy models
│   │   ├── routes/
│   │   │   ├── offline.py         # Offline API endpoints
│   │   │   └── online.py          # Online API endpoints
│   │   ├── services/
│   │   │   ├── offline_engine.py  # Symptom matching engine
│   │   │   └── online_services.py # AI + external APIs
│   │   ├── database.py            # DB config
│   │   └── seed.py                # Database seeder
│   ├── main.py                    # FastAPI app entry
│   └── requirements.txt
├── frontend/
│   ├── index.html                 # Main HTML
│   ├── css/
│   │   └── styles.css             # All styles
│   ├── js/
│   │   └── app.js                 # All frontend logic
│   ├── manifest.json              # PWA manifest
│   └── sw.js                      # Service worker
├── setup.bat                      # Setup script
└── start.bat                      # Start script
```

---

## API Endpoints

### Offline Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/symptoms` | Get all symptoms |
| GET | `/api/diseases` | Get all diseases |
| GET | `/api/diseases/search?q=` | Search diseases |
| POST | `/api/match` | Match symptoms to diseases |
| GET | `/api/disease/{id}` | Get disease details |

### Online Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/online/chat` | AI medical assistant |
| GET | `/api/online/weather?lat=&lon=` | Weather + risk |
| GET | `/api/online/outbreaks` | Outbreak data |
| GET | `/api/online/location?lat=&lon=` | Reverse geocode |
| POST | `/api/online/risk-assessment` | Full risk assessment |

---

## Database Schema

### diseases
- id, name, description, causes, prevention, created_at

### symptoms
- id, name

### disease_symptoms (junction table)
- disease_id, symptom_id

### treatments
- id, disease_id, immediate_action, medications

---

## Matching Algorithm

```
score = (matched_symptoms / total_disease_symptoms) * 100
```

- Returns top 3-5 diseases ranked by match percentage
- Handles partial symptom input gracefully
- Shows matched vs unmatched symptoms

---

## Preloaded Diseases

1. Malaria
2. Influenza (Flu)
3. Dengue Fever
4. Typhoid Fever
5. Common Cold
6. Pneumonia
7. Cholera
8. Tuberculosis (TB)
9. Hepatitis A
10. Asthma
11. Diabetes (Type 2)
12. Hypertension
13. Gastroenteritis
14. Migraine
15. Anemia

---

## Medical Disclaimer

**This application does NOT provide medical diagnosis.** All outputs are labeled as "Possible Conditions" with "Estimated Match" percentages. The system never presents certainty. Always consult a licensed medical professional for proper diagnosis and treatment.

---

## License

© 2026 SifunaCodex

---

## Built For

- Rural areas with limited internet access
- Early health risk awareness
- Preventive healthcare decisions
- Educational health information
