# 📦 Local Setup & Installation

## ✅ Prerequisites

- Python 3.10+
- Node.js (with npm)
- Git

---

## 1. Clone the Repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd visual_tagger
````

## 2. Backend Setup

 Windows
````bash
python -m venv venv
.\venv\Scripts\activate
````
 macOS/Linux
````bash
python3 -m venv venv
source venv/bin/activate
````

## 2.3 Install Dependencies
````bash
pip install -r requirements.txt
````

# 2.4 Configure Environment Variables
.env example:
```bash
APP_NAME="VisualTagger Backend"
APP_VERSION="1.0.0"
DEBUG=True

MIN_OVERALL_CONFIDENCE_FOR_TAG=0.001
HIGH_CONFIDENCE_THRESHOLD_GENERAL=0.6
MIN_CONFIDENT_TAGS_GENERAL=2
```

# 2.5 Start the FastAPI Server

```bash
uvicorn backend.src.main:app --reload
```

## Frontend Setup
# 3 Open frontend folder
```bash
cd ../frontend
```
# 3.1 Install Dependencies
```bash
npm install
```

# 3.2 Start Development Server
```bash
npm start
```

Acess http://localhost:3000


