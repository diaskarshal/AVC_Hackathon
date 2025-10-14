# BuildFlow ERP System
todo:
- implement create new project button in the dashboard;
- fix the "Spent: " entry in the project modal; 
- strange behaviour in projects tab: previously added projects are not shown unless one of the shown projects in the projects tab is updated; new added projects are not shown;
- add export button to project(s)/task(s)/resource(s)/budget(s) tab;
- fix import csv files
    - the output after "upload and import" shows redundant info (when importing tasks, all others are also shown with 0s).
    - the import files must be in the correct order, first should be project.csv, because if not, other table entries(tasks, budgets, resources) will use from the existing project name entries;
    - the update of the resource that was imported as said previously does not work. it does not update to the existing project that was imported later, it still chooses the old one.

BuildFlow is a ERP system for construction project management.

## Features

- **Project Management**: Create and track construction projects with timelines and budgets
- **Resource Management**: Track materials, equipment, and labor
- **Financial Control**: Monitor budgets, expenses, and cost analysis
- **Task Management**: Plan and track project tasks with dependencies
- **Analytics Dashboard**: Real-time KPIs and project insights
- **Data Import**: Import data from Excel/CSV files
- **ML Predictions**: Predict project completion dates and costs

## Tech Stack

- **Backend**: FastAPI
- **Database**: PostgreSQL
- **Frontend**: React
- **Containerization**: Docker & Docker Compose

## Quick Start

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/diaskarshal/AVC_Hackathon.git
cd buildflow
```

2. **Set up environment variables**
```bash
cd backend
cp .env.example .env

cd ..
```

3. **Start the application**
```bash
docker-compose up --build
docker-compose exec backend python -m app.utils.seed_data #run in a new terminal after the previous line
```
-----try with sudo in case of "permission denied"-----  

4. **Access the application**
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- Frontend: http://localhost:3000

## Project Structure

```
buildflow/
├── backend/
│   ├── app/
│   │   ├── models/          # Database models
│   │   ├── schemas/         # Pydantic schemas
│   │   ├── routes/          # API endpoints
│   │   ├── services/        # Business logic
│   │   ├── middleware/      # Custom middleware
│   │   ├── exceptions/      # Custom exceptions
│   │   └── utils/           # Utility functions
│   ├── tests/               # Unit tests
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/                # React frontend (to be implemented)
├── docker-compose.yml
└── README.md
```

## API Endpoints

### Projects
- `POST /api/projects/` - Create a new project
- `GET /api/projects/` - Get all projects
- `GET /api/projects/{id}` - Get project by ID
- `PUT /api/projects/{id}` - Update project
- `DELETE /api/projects/{id}` - Delete project
- `GET /api/projects/summary` - Get projects summary

### Tasks
- `POST /api/tasks/` - Create a new task
- `GET /api/tasks/` - Get all tasks (filterable by project_id, status)
- `GET /api/tasks/{id}` - Get task by ID
- `PUT /api/tasks/{id}` - Update task
- `DELETE /api/tasks/{id}` - Delete task

### Resources
- `POST /api/resources/` - Create a new resource
- `GET /api/resources/` - Get all resources (filterable)
- `GET /api/resources/{id}` - Get resource by ID
- `PUT /api/resources/{id}` - Update resource
- `DELETE /api/resources/{id}` - Delete resource

### Budgets
- `POST /api/budgets/` - Create a new budget entry
- `GET /api/budgets/` - Get all budget entries (filterable)
- `GET /api/budgets/{id}` - Get budget by ID
- `PUT /api/budgets/{id}` - Update budget
- `DELETE /api/budgets/{id}` - Delete budget

### Analytics
- `GET /api/analytics/dashboard` - Overall dashboard statistics
- `GET /api/analytics/project/{id}/kpi` - Project KPIs
- `GET /api/analytics/project/{id}/budget-breakdown` - Budget breakdown
- `GET /api/analytics/project/{id}/resource-distribution` - Resource distribution
- `GET /api/analytics/project/{id}/timeline` - Project timeline
- `GET /api/analytics/project/{id}/predict-completion` - Predict completion

### Data Import
- `POST /api/import/excel` - Import data from Excel file
- `POST /api/import/csv` - Import data from CSV file

## Development

### Running Tests
```bash
docker-compose exec backend pytest
```

### Database Migrations (Alembic)
```bash
# Generate migration
docker-compose exec backend alembic revision --autogenerate -m "description"

# Apply migration
docker-compose exec backend alembic upgrade head
```

### Access Database
```bash
docker-compose exec db psql -U buildflow -d buildflow_db
```

## Excel/CSV Import Format

### Projects Sheet/CSV
- name, description, status, start_date, end_date, total_budget, spent_amount, location

### Tasks Sheet/CSV
- project_id, name, description, status, priority, start_date, end_date, progress, assigned_to

### Resources Sheet/CSV
- project_id, name, resource_type, status, quantity, unit, unit_cost, supplier

### Budgets Sheet/CSV
- project_id, category, description, planned_amount, actual_amount