# Hackersbridge

**Hackersbridge** is a Django-powered web platform designed to enhance the hackathon experience by streamlining the management, execution, and evaluation of both individual and team-based competitions. It offers real-time communication, face detection-based proctoring, and flexible evaluation systems to ensure fairness, engagement, and transparency throughout the event.

---

## 🚀 Features

### 🛠️ Hackathon Management
- Create and configure hackathons with:
  - Event name, description, and schedule
  - Themes and problem statements
  - Evaluation strategies (for both individual and team contests)
- Manage participants and judge workflows

### 👨‍💻 Individual Contests
- Online coding environment with test case-based automatic grading
- Integrated face detection for proctoring to help monitor contest integrity

### 👥 Team-Based Events
- Project-based submissions for teams
- Evaluations based on criteria such as innovation, implementation, and impact
- Virtual team collaboration through screen sharing and video calls (WebRTC)

### 📢 Real-Time Communication
- Live Q&A sessions using WebSockets
- Team chat and announcements
- Workshop scheduling and resource sharing

### 🔍 Proctoring via Face Detection
- Implements a TensorFlow-based face detection model
- Monitors participant presence and flags potential issues
- Helps organizers maintain competition integrity

### 📊 Analytics & Leaderboards
- Live leaderboard for real-time contest standings
- Organizer dashboards with:
  - Participant statistics
  - Submission tracking
  - Engagement heatmaps and activity insights

---

## 💡 Objectives

Hackersbridge aims to:
- Ensure fair and transparent hackathons using reliable monitoring tools
- Promote teamwork, creativity, and problem-solving
- Provide a full-stack event management platform for both organizers and participants
- Enable smooth communication and collaboration in virtual settings

---

## 🧰 Tech Stack

- **Backend**: Django
- **Frontend**: HTML, CSS, JavaScript (via Django templates)
- **Face Detection**: TensorFlow with a custom trained face detection model
- **WebSockets**: Django Channels
- **Video & Audio Communication**: WebRTC
- **Database**: PostgreSQL / SQLite
- **Deployment**: Docker / Heroku-compatible

---

## 📦 Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/hackersbridge.git
   cd hackersbridge
Create and activate a virtual environment

bash
Copy
Edit
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
Install dependencies

bash
Copy
Edit
pip install -r requirements.txt
Run migrations

bash
Copy
Edit
python manage.py migrate
Create a superuser

bash
Copy
Edit
python manage.py createsuperuser
Start the development server

bash
Copy
Edit
python manage.py runserver
Open in browser

Visit: http://127.0.0.1:8000/

