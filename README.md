# 🧬 GenetiSched - Genetic Counseling Scheduling System

A lightweight, web-based scheduling platform designed for genetic counseling departments.
The system allows managers to assign interns to senior counselors, manage room availability, and schedule office duty rotations—based on availability, employment percentage, and internal rules.

## 🚀 Features

- Add and manage employees (interns and senior counselors)
- Set employee availability and employment percentage
- Automatic schedule generation based on rules
- Room management and assignment
- Office duty rotation scheduling
- Individual schedule viewing

## 🛠️ Tech Stack

- Backend: FastAPI (Python)
- Frontend: Vue.js + TailwindCSS
- Data Storage: JSON file (can be upgraded to SQLite/PostgreSQL)
- API Communication: REST using Axios

## 📋 Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn

## 🚀 Getting Started

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the backend server:
   ```bash
   uvicorn main:app --reload
   ```

The backend will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Run the development server:
   ```bash
   npm run dev
   ```

The frontend will be available at `http://localhost:5173`

## 📁 Project Structure

```
/genetisched
├── backend/
│   ├── main.py            # FastAPI entry point
│   ├── api.py             # Employee routes
│   ├── scheduler.py       # Scheduling logic
│   ├── models.py          # Employee data model
│   └── employees.json     # Temporary employee storage
│
└── frontend/
    ├── public/
    │   └── index.html
    ├── src/
    │   ├── App.vue
    │   ├── main.js
    │   └── components/
    │       ├── EmployeeForm.vue
    │       ├── ScheduleTable.vue
    │       └── EmployeeSchedule.vue
    └── package.json
```

## 📝 License

MIT License
