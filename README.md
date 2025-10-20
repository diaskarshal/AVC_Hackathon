# BuildFlow ERP System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.119.0-009688.svg)](https://fastapi.tiangolo.com)
[![React 19](https://img.shields.io/badge/React-19.2.0-61DAFB.svg)](https://reactjs.org/)


todo:
- workers should be shown the tasks their team assigned to, not the whole tasks.

**BuildFlow** is a modern ERP system designed for construction project management, developed for AVC Group.

![BuildFlow Dashboard](docs/dashboard.png)


---

## ✨ Features

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

### User Interface
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Intuitive Navigation**: Role-based navigation tailored to user permissions
- **Real-time Notifications**: Get alerted about overdue tasks and critical updates
- **Dark Mode Ready**: UI components prepared for dark theme support

---

## 🛠 Tech Stack

### Backend
- **Framework**: FastAPI 0.119.0
- **Database**: PostgreSQL 15
- **ORM**: SQLAlchemy 2.0.23
- **Authentication**: JWT (python-jose)
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

## 🚀 Quick Start

### Prerequisites

- Docker 20.10+ and Docker Compose 2.0+

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
# Edit .env with your settings
cd ..
```

3. **Start the application**
```bash
# Build and start all services
docker-compose up --build
```

4. **Seed the database** (in a new terminal)
```bash
docker-compose exec backend python -m app.utils.seed_data
```

5. **Access the application**
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Database**: localhost:5432 (credentials in docker-compose.yml)

### Demo Accounts

| Role | Username | Password | Access Level |
|------|----------|----------|--------------|
| Admin | `admin` | `admin123` | Full system access |
| Manager | `manager1` | `manager123` | Projects 1-2 management |
| Worker | `worker1` | `worker123` | Own tasks only |
| Worker | `worker2` | `worker123` | Own tasks only |
| Worker | `worker3` | `worker123` | Own tasks only |

---

## 📁 Project Structure

Check at the [uithub link.](https://uithub.com/diaskarshal/AVC_Hackathon)

---

## 👥 User Roles

### Admin
**Full system access** with the following capabilities:
- ✅ View and manage all projects
- ✅ Create, edit, and delete projects
- ✅ Manage all tasks, resources, and budgets
- ✅ View team performance metrics
- ✅ Manage user accounts
- ✅ Import/export data
- ✅ Access all system reports

### Manager
**Project-specific management** with:
- ✅ View and manage assigned projects only
- ✅ Create and assign tasks within their projects
- ✅ Manage resources for their projects
- ✅ Track budgets and expenses
- ✅ View team performance for their projects
- ❌ Cannot manage other projects
- ❌ Cannot manage users
- ❌ Limited to assigned project data

### Worker
**Task execution focus** with:
- ✅ View assigned tasks only
- ✅ Update task progress and status
- ✅ Mark tasks as complete
- ✅ View own performance metrics
- ❌ Cannot view project budgets
- ❌ Cannot manage resources
- ❌ Cannot create or delete tasks
- ❌ Limited to personal task view

---

## 📚 API Documentation

### Base URL
```
Development: http://localhost:8000
Production: https://your-domain.com
```

### Authentication

All protected endpoints require a JWT token in the Authorization header:
```
Authorization: Bearer <your_jwt_token>
```

### Endpoints Overview

#### Authentication
```http
POST   /api/auth/login          # Login and get JWT token
GET    /api/auth/me             # Get current user info
GET    /api/auth/demo-users     # Get demo users list
```

#### Projects
```http
POST   /api/projects/           # Create project (Admin only)
GET    /api/projects/           # List projects (filtered by role)
GET    /api/projects/{id}       # Get project details
PUT    /api/projects/{id}       # Update project (Admin/Manager)
DELETE /api/projects/{id}       # Delete project (Admin only)
GET    /api/projects/summary    # Get projects summary
```

#### Tasks
```http
POST   /api/tasks/              # Create task (Admin/Manager)
GET    /api/tasks/              # List tasks (filtered by role)
GET    /api/tasks/{id}          # Get task details
PUT    /api/tasks/{id}          # Update task (role-dependent)
DELETE /api/tasks/{id}          # Delete task (Admin/Manager)
```

#### Resources
```http
POST   /api/resources/          # Create resource (Admin/Manager)
GET    /api/resources/          # List resources
GET    /api/resources/{id}      # Get resource details
PUT    /api/resources/{id}      # Update resource (Admin/Manager)
DELETE /api/resources/{id}      # Delete resource (Admin/Manager)
```

#### Budgets
```http
POST   /api/budgets/            # Create budget (Admin/Manager)
GET    /api/budgets/            # List budgets
GET    /api/budgets/{id}        # Get budget details
PUT    /api/budgets/{id}        # Update budget (Admin/Manager)
DELETE /api/budgets/{id}        # Delete budget (Admin/Manager)
```

#### Analytics
```http
GET    /api/analytics/dashboard                          # Dashboard stats
GET    /api/analytics/project/{id}/kpi                   # Project KPIs
GET    /api/analytics/project/{id}/budget-breakdown      # Budget analysis
GET    /api/analytics/project/{id}/resource-distribution # Resource stats
GET    /api/analytics/project/{id}/timeline              # Project timeline
GET    /api/analytics/project/{id}/predict-completion    # ML predictions
GET    /api/analytics/team-performance                   # Team metrics
```

#### Data Import
```http
POST   /api/import/excel        # Import Excel file (Admin only)
POST   /api/import/csv          # Import CSV file (Admin only)
```

#### Users
```http
GET    /api/users/              # List all users (Admin only)
GET    /api/users/profile       # Get own profile
PUT    /api/users/profile       # Update own profile
GET    /api/users/team          # Get team members (Admin/Manager)
```

---

## 💻 Development

### Backend Development

#### Setup local environment
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### Run backend locally
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Database migrations
```bash
# Create migration
docker-compose exec backend alembic revision --autogenerate -m "description"

# Apply migration
docker-compose exec backend alembic upgrade head

# Rollback migration
docker-compose exec backend alembic downgrade -1
```

#### Access database directly
```bash
docker-compose exec db psql -U buildflow -d buildflow_db
```

### Frontend Development

#### Setup local environment
```bash
cd frontend
npm install
```


---
### Environment Variables

#### Backend (.env)
```env
# Application
APP_NAME=BuildFlow ERP
APP_VERSION=1.0.0
DEBUG=False

# Database
DATABASE_URL=postgresql://user:password@host:port/database

# Security
SECRET_KEY=your-super-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
CORS_ORIGINS=https://yourdomain.com

# Upload
MAX_UPLOAD_SIZE=10485760
ALLOWED_EXTENSIONS=.xlsx,.xls,.csv
```

#### Frontend (.env)
```env
REACT_APP_API_URL=https://api.yourdomain.com
```

---

## 🔒 Security

### Authentication & Authorization
- JWT-based authentication with configurable expiration
- Role-based access control (RBAC)
- Secure password hashing with bcrypt
- Token refresh mechanism

### Data Security
- SQL injection prevention via SQLAlchemy ORM
- XSS protection in frontend
- CSRF protection for state-changing operations
- Input validation and sanitization

---

## 🐛 Troubleshooting

### Common Issues

#### Port Already in Use
```bash
# Find and kill process using port 3000
lsof -ti:3000 | xargs kill -9

# Find and kill process using port 8000
lsof -ti:8000 | xargs kill -9
```

#### Database Connection Failed
```bash
# Check if PostgreSQL container is running
docker-compose ps

# View PostgreSQL logs
docker-compose logs db

# Restart database
docker-compose restart db
```

#### Permission Denied (Linux/Mac)
```bash
# Run with sudo
sudo docker-compose up --build
```

#### Frontend Build Errors
```bash
# Clear node_modules and reinstall
cd frontend
rm -rf node_modules package-lock.json
npm install

# Clear cache
npm cache clean --force
```

#### Backend Import Errors
```bash
# Rebuild Python dependencies
docker-compose build --no-cache backend
```

#### Database Migration Issues
```bash
# Reset database (⚠️ destroys all data)
docker-compose down -v
docker-compose up --build
docker-compose exec backend python -m app.utils.seed_data
```