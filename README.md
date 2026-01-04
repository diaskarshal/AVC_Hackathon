# BuildFlow ERP System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.119.0-009688.svg)](https://fastapi.tiangolo.com)
[![React 19](https://img.shields.io/badge/React-19.2.0-61DAFB.svg)](https://reactjs.org/)


todo:
- workers should be shown the tasks their team assigned to, not the whole tasks.
- use patch(1 field - status) instead of put(updates all fields) in the workers' tasks update modal  
- «Автоматизация расчёта ресурсов для ремонта заводского оборудования» (Data Science / Аналитика);  
- Применение инновационных методов в управлении ресурсами при ремонтах заводов;  
- форма завершения: Авт. расчет ресурсов с использованием истор. данных и LLM.  

**BuildFlow** -- ERP system designed for construction project management.

![BuildFlow Dashboard](docs/dashboard.png)


---

## Features

### Core Functionality
- **Project Management**: Create, track, and manage construction projects with timelines and budgets
- **Task Management**: Plan and track project tasks with dependencies, priorities, and progress tracking
- **Resource Management**: Track materials, equipment, and labor with cost calculations
- **Financial Control**: Monitor budgets, expenses, and cost analysis with variance tracking
- **Multi-User Support**: Role-based access control (Admin, Manager, Worker)

### Analytics & Reporting
- **Real-time KPI Dashboard**: Project progress, budget utilization, task completion rates
- **Team Performance Tracking**: Monitor individual and team productivity metrics
- **Budget Breakdown Analysis**: Category-wise spending analysis with variance reporting
- **Resource Distribution**: Visualize resource allocation across projects
- **Project Timeline**: Gantt-style timeline view with milestone tracking
- **ML Predictions**: Predict project completion dates and costs using machine learning

### Data Management
- **Data Import**: Import projects, tasks, resources, and budgets from Excel/CSV files
- **Data Export**: Export any data view to CSV for further analysis
- **Bulk Operations**: Create and update multiple records efficiently

---

## Tech Stack

### Backend
- **Framework**: FastAPI 0.119.0
- **Database**: PostgreSQL 15
- **ORM**: SQLAlchemy 2.0.23
- **Authentication**: JWT
- **Password Hashing**: bcrypt with passlib
- **Data Processing**: Pandas 2.1.3
- **ML**: Scikit-learn 1.3.2
- **File Processing**: openpyxl 3.1.2

### Frontend
- **Framework**: React 19.2.0 with TypeScript 4.9.5
- **Routing**: React Router DOM 6.30.1
- **Styling**: Tailwind CSS 3.4.18
- **HTTP Client**: Axios 1.12.2
- **Charts**: Recharts 2.15.4
- **Build Tool**: React Scripts 5.0.1

### DevOps
- **Containerization**: Docker & Docker Compose
- **Web Server**: Uvicorn 0.24.0
- **Process Manager**: Uvloop 0.21.0

---

## Quick Start

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/diaskarshal/buildflow.git
cd buildflow
```

2. **Configure environment variables**
```bash
cd backend
cp .env.example .env
cd ..
```

3. **Start the application**
```bash
docker-compose up --build
```

4. **Seed the database**
```bash
docker-compose exec backend python -m app.utils.seed_data
```

5. **Access the application**
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Database**: localhost:5432

### Demo Accounts

| Role | Username | Password | Access Level |
|------|----------|----------|--------------|
| Admin | `admin` | `admin123` | Full system access |
| Manager | `manager1` | `manager123` | Projects 1-2 management |
| Worker | `worker1` | `worker123` | Own tasks only |
| Worker | `worker2` | `worker123` | Own tasks only |
| Worker | `worker3` | `worker123` | Own tasks only |

---

## Analytics
```http
GET    /api/analytics/dashboard                          # Dashboard stats
GET    /api/analytics/project/{id}/kpi                   # Project KPIs
GET    /api/analytics/project/{id}/budget-breakdown      # Budget analysis
GET    /api/analytics/project/{id}/resource-distribution # Resource stats
GET    /api/analytics/project/{id}/timeline              # Project timeline
GET    /api/analytics/project/{id}/predict-completion    # ML predictions
GET    /api/analytics/team-performance                   # Team metrics
```

### Data Import
```http
POST   /api/import/excel        # Import Excel file (Admin only)
POST   /api/import/csv          # Import CSV file (Admin only)
```

---

## Troubleshooting

### Common Issues

#### Port Already in Use
```bash
lsof -ti:3000 | xargs kill -9

lsof -ti:8000 | xargs kill -9
```

#### Database Connection Failed
```bash
docker-compose ps

docker-compose logs db

docker-compose restart db
```


#### Frontend Build Errors
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install

npm cache clean --force
```

#### Backend Import Errors
```bash
docker-compose build --no-cache backend
```

#### Database Migration Issues
```bash
docker-compose down -v
docker-compose up --build
docker-compose exec backend python -m app.utils.seed_data
```