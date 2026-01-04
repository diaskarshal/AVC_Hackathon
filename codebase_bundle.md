# File: ./README.md

```markdown
# BuildFlow ERP System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.119.0-009688.svg)](https://fastapi.tiangolo.com)
[![React 19](https://img.shields.io/badge/React-19.2.0-61DAFB.svg)](https://reactjs.org/)


todo:
- workers should be shown the tasks their team assigned to, not the whole tasks.
- use patch(1 field - status) instead of put(updates all fields) in the workers' tasks update modal  
«Автоматизация расчёта ресурсов для ремонта заводского оборудования» (Data Science / Аналитика);  
Применение инновационных методов в управлении ресурсами при ремонтах заводов;  
форма завершения: Авт. расчет ресурсов с использованием истор. данных и LLM.  

**BuildFlow** is a modern ERP system designed for construction project management, developed for AVC Group.

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

## Quick Start

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
cd ..
```

3. **Start the application**
```bash
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

## Project Structure

Check at the [uithub](https://uithub.com/diaskarshal/AVC_Hackathon)

---

## User Roles

### Admin
**Full system access** with the following capabilities:
- ✅ View and manage all projects
- Create, edit, and delete projects
- Manage all tasks, resources, and budgets
- View team performance metrics
- Manage user accounts
- Import/export data
- Access all system reports

### Manager
**Project-specific management** with:
- ✅ View and manage assigned projects only
- Create and assign tasks within their projects
- Manage resources for their projects
- Track budgets and expenses
- View team performance for their projects
- ❌ Cannot manage other projects
- Cannot manage users
- Limited to assigned project data

### Worker
**Task execution focus** with:
- ✅ View assigned tasks only
- Update task progress and status
- Mark tasks as complete
- View own performance metrics
- ❌ Cannot view project budgets
- Cannot manage resources
- Cannot create or delete tasks
- Limited to personal task view

---

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

---

## Development

### Backend Development

#### Setup local environment
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Run backend locally
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Database migrations
```bash
docker-compose exec backend alembic revision --autogenerate -m "description"

docker-compose exec backend alembic upgrade head

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
CORS_ORIGINS=https://somedomain.com

# Upload
MAX_UPLOAD_SIZE=10485760
ALLOWED_EXTENSIONS=.xlsx,.xls,.csv
```

#### Frontend (.env)
```env
REACT_APP_API_URL=https://api.somedomain.com
```

---

## Security

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
# Rebuild Python dependencies
docker-compose build --no-cache backend
```

#### Database Migration Issues
```bash
docker-compose down -v
docker-compose up --build
docker-compose exec backend python -m app.utils.seed_data
```
```

# File: ./docker-compose.yml

```yaml
services:
  db:
    image: postgres:15-alpine
    container_name: buildflow_db
    environment:
      POSTGRES_USER: buildflow
      POSTGRES_PASSWORD: buildflow123
      POSTGRES_DB: buildflow_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U buildflow"]
      interval: 10s
      timeout: 5s
      retries: 5

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: buildflow_backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://buildflow:buildflow123@db:5432/buildflow_db
    depends_on:
      db:
        condition: service_healthy
    volumes:
      - ./backend:/app
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: buildflow_frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend
    volumes:
      - ./frontend/src:/app/src
      - ./frontend/public:/app/public
      - /app/node_modules
    environment:
      - REACT_APP_API_URL=http://localhost:8000
      - CHOKIDAR_USEPOLLING=true
      - WDS_SOCKET_PORT=3000

volumes:
  postgres_data:
```

# File: ./.gitignore

```
__pycache__/
*.py[cod]
*.log
*.env
*.venv
.env.*
venv/
.env
.DS_Store
*.swp
*.swo
.idea/
.vscode/
*.bak
*.tmp
*.out

*.egg-info/
dist/
build/
*.spec
.mypy_cache/
.pytest_cache/
coverage/
htmlcov/

*.db
instance/
*.sqlite3

node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
.pnpm-debug.log*
package-lock.json
yarn.lock

frontend/build/
frontend/dist/
backend/__pycache__/
backend/staticfiles/
backend/media/
txts/

# docker
*.pid
*.seed
*.pid.lock
*.sock
*.tar
.env.docker
docker-compose.override.yml

Thumbs.db
ehthumbs.db
Desktop.ini
```

# File: ./test_api.sh

```bash
#!/bin/bash


BASE_URL="http://localhost:8000"
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "API Testing"
echo "========================"
echo ""

echo -n "1. Health Check... "
response=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/health")
if [ "$response" -eq 200 ]; then
    echo -e "${GREEN}✓ PASSED${NC}"
else
    echo -e "${RED}✗ FAILED (HTTP $response)${NC}"
fi

echo -n "2. Root Endpoint... "
response=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/")
if [ "$response" -eq 200 ]; then
    echo -e "${GREEN}✓ PASSED${NC}"
else
    echo -e "${RED}✗ FAILED (HTTP $response)${NC}"
fi

echo -n "3. Create Project... "
create_response=$(curl -s -X POST "$BASE_URL/api/projects/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Project",
    "description": "API Test Project",
    "status": "planning",
    "total_budget": 1000000,
    "location": "Test Location",
    "start_date": "2025-11-01T00:00:00",
    "planned_end_date": "2026-12-31T00:00:00"
  }')

project_id=$(echo $create_response | grep -o '"id":[0-9]*' | grep -o '[0-9]*')

if [ ! -z "$project_id" ]; then
    echo -e "${GREEN}✓ PASSED${NC} (Project ID: $project_id)"
else
    echo -e "${RED}✗ FAILED${NC}"
fi

echo -n "4. Get All Projects... "
response=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/api/projects/")
if [ "$response" -eq 200 ]; then
    echo -e "${GREEN}✓ PASSED${NC}"
else
    echo -e "${RED}✗ FAILED (HTTP $response)${NC}"
fi

if [ ! -z "$project_id" ]; then
    echo -n "5. Get Project by ID... "
    response=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/api/projects/$project_id")
    if [ "$response" -eq 200 ]; then
        echo -e "${GREEN}✓ PASSED${NC}"
    else
        echo -e "${RED}✗ FAILED (HTTP $response)${NC}"
    fi
fi

if [ ! -z "$project_id" ]; then
    echo -n "6. Create Task... "
    task_response=$(curl -s -X POST "$BASE_URL/api/tasks/" \
      -H "Content-Type: application/json" \
      -d "{
        \"project_id\": $project_id,
        \"name\": \"Test Task\",
        \"description\": \"API Test Task\",
        \"status\": \"not_started\",
        \"priority\": \"medium\",
        \"start_date\": \"2025-11-01T00:00:00\",
        \"planned_end_date\": \"2025-12-31T00:00:00\"
      }")
    
    task_id=$(echo $task_response | grep -o '"id":[0-9]*' | grep -o '[0-9]*')
    
    if [ ! -z "$task_id" ]; then
        echo -e "${GREEN}✓ PASSED${NC} (Task ID: $task_id)"
    else
        echo -e "${RED}✗ FAILED${NC}"
    fi
fi

if [ ! -z "$project_id" ]; then
    echo -n "7. Create Resource... "
    resource_response=$(curl -s -X POST "$BASE_URL/api/resources/" \
      -H "Content-Type: application/json" \
      -d "{
        \"project_id\": $project_id,
        \"name\": \"Test Material\",
        \"resource_type\": \"material\",
        \"status\": \"available\",
        \"quantity\": 100,
        \"unit\": \"kg\",
        \"unit_cost\": 50,
        \"supplier\": \"Test Supplier\"
      }")
    
    resource_id=$(echo $resource_response | grep -o '"id":[0-9]*' | grep -o '[0-9]*')
    
    if [ ! -z "$resource_id" ]; then
        echo -e "${GREEN}✓ PASSED${NC} (Resource ID: $resource_id)"
    else
        echo -e "${RED}✗ FAILED${NC}"
    fi
fi

if [ ! -z "$project_id" ]; then
    echo -n "8. Create Budget... "
    budget_response=$(curl -s -X POST "$BASE_URL/api/budgets/" \
      -H "Content-Type: application/json" \
      -d "{
        \"project_id\": $project_id,
        \"category\": \"Test Category\",
        \"description\": \"API Test Budget\",
        \"planned_amount\": 100000,
        \"actual_amount\": 50000
      }")
    
    budget_id=$(echo $budget_response | grep -o '"id":[0-9]*' | grep -o '[0-9]*')
    
    if [ ! -z "$budget_id" ]; then
        echo -e "${GREEN}✓ PASSED${NC} (Budget ID: $budget_id)"
    else
        echo -e "${RED}✗ FAILED${NC}"
    fi
fi

echo -n "9. Dashboard Analytics... "
response=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/api/analytics/dashboard")
if [ "$response" -eq 200 ]; then
    echo -e "${GREEN}✓ PASSED${NC}"
else
    echo -e "${RED}✗ FAILED (HTTP $response)${NC}"
fi

if [ ! -z "$project_id" ]; then
    echo -n "10. Project KPI... "
    response=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/api/analytics/project/$project_id/kpi")
    if [ "$response" -eq 200 ]; then
        echo -e "${GREEN}✓ PASSED${NC}"
    else
        echo -e "${RED}✗ FAILED (HTTP $response)${NC}"
    fi
fi

echo ""
echo "========================"
echo "Testing Complete!"
echo ""
echo -e "${YELLOW}View full API documentation at:${NC}"
echo "$BASE_URL/docs"
echo ""
```

# File: ./frontend/tailwind.config.js

```javascript
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./index.html", "./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      colors: {
        primary: {
          50: "#eff6ff",
          100: "#dbeafe",
          200: "#bfdbfe",
          300: "#93c5fd",
          400: "#60a5fa",
          500: "#3b82f6",
          600: "#2563eb",
          700: "#1d4ed8",
          800: "#1e40af",
          900: "#1e3a8a",
        },
      },
    },
  },
  plugins: [],
};
```

# File: ./frontend/.dockerignore

```
node_modules
build
.git
.gitignore
README.md
npm-debug.log*
yarn-debug.log*
yarn-error.log*
.env.local
.env.development.local
.env.test.local
.env.production.local
```

# File: ./frontend/package.json

```json
{
  "name": "buildflow_frontend",
  "version": "0.1.0",
  "private": true,
  "dependencies": {
    "@testing-library/jest-dom": "^6.9.1",
    "@testing-library/react": "^16.3.0",
    "@testing-library/user-event": "^13.5.0",
    "@types/jest": "^27.5.2",
    "@types/node": "^16.18.126",
    "@types/react": "^19.2.2",
    "@types/react-dom": "^19.2.1",
    "axios": "^1.12.2",
    "react": "^19.2.0",
    "react-dom": "^19.2.0",
    "react-router-dom": "^6.30.1",
    "react-scripts": "5.0.1",
    "recharts": "^2.15.4",
    "typescript": "^4.9.5",
    "web-vitals": "^2.1.4"
  },
  "devDependencies": {
    "@types/react-router-dom": "^5.3.3",
    "autoprefixer": "^10.4.21",
    "postcss": "^8.5.6",
    "tailwindcss": "^3.4.18"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  },
  "eslintConfig": {
    "extends": [
      "react-app",
      "react-app/jest"
    ]
  },
  "browserslist": {
    "production": [
      ">0.2%",
      "not dead",
      "not op_mini all"
    ],
    "development": [
      "last 1 chrome version",
      "last 1 firefox version",
      "last 1 safari version"
    ]
  }
}

```

# File: ./frontend/.gitignore

```
# See https://help.github.com/articles/ignoring-files/ for more about ignoring files.

# dependencies
/node_modules
/.pnp
.pnp.js

# testing
/coverage

# production
/build

# misc
.DS_Store
.env.local
.env.development.local
.env.test.local
.env.production.local

npm-debug.log*
yarn-debug.log*
yarn-error.log*

```

# File: ./frontend/Dockerfile

```
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY public ./public
COPY src ./src
COPY tsconfig.json ./
COPY tailwind.config.js ./
COPY postcss.config.js ./

EXPOSE 3000

CMD ["npm", "start"]
```

# File: ./frontend/postcss.config.js

```javascript
module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
};
```

# File: ./frontend/tsconfig.json

```json
{
  "compilerOptions": {
    "target": "es5",
    "lib": [
      "dom",
      "dom.iterable",
      "esnext"
    ],
    "allowJs": true,
    "skipLibCheck": true,
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true,
    "strict": true,
    "forceConsistentCasingInFileNames": true,
    "noFallthroughCasesInSwitch": true,
    "module": "esnext",
    "moduleResolution": "node",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx"
  },
  "include": [
    "src"
  ]
}

```

# File: ./frontend/public/manifest.json

```json
{
  "short_name": "React App",
  "name": "Create React App Sample",
  "icons": [
    {
      "src": "favicon.ico",
      "sizes": "64x64 32x32 24x24 16x16",
      "type": "image/x-icon"
    },
    {
      "src": "logo192.png",
      "type": "image/png",
      "sizes": "192x192"
    },
    {
      "src": "logo512.png",
      "type": "image/png",
      "sizes": "512x512"
    }
  ],
  "start_url": ".",
  "display": "standalone",
  "theme_color": "#000000",
  "background_color": "#ffffff"
}
```

# File: ./frontend/public/robots.txt

```
# https://www.robotstxt.org/robotstxt.html
User-agent: *
Disallow:
```

# File: ./frontend/public/index.html

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <link rel="icon" href="%PUBLIC_URL%/favicon.ico" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="theme-color" content="#000000" />
    <meta
      name="description"
      content="BuildFlow ERP - Construction Project Management System"
    />
    <link rel="apple-touch-icon" href="%PUBLIC_URL%/logo192.png" />
    <link rel="manifest" href="%PUBLIC_URL%/manifest.json" />
    <title>BuildFlow ERP</title>
  </head>
  <body>
    <noscript>You need to enable JavaScript to run this app.</noscript>
    <div id="root"></div>
  </body>
</html>
```

# File: ./frontend/src/App.css

```css
* {
  box-sizing: border-box;
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
```

# File: ./frontend/src/App.tsx

```typescript
import React from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider } from "./contexts/AuthContext";
import PrivateRoute from "./components/PrivateRoute";
import Layout from "./components/Layout";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import Projects from "./pages/Projects";
import Tasks from "./pages/Tasks";
import Resources from "./pages/Resources";
import Budgets from "./pages/Budgets";
import Import from "./pages/Import";
import Users from "./pages/Users";
import Profile from "./pages/Profile";
import TeamPerformance from "./pages/TeamPerformance";

function App() {
  return (
    <Router>
      <AuthProvider>
        <Routes>
          {/* Public Route */}
          <Route path="/login" element={<Login />} />

          {/* Admin Routes */}
          <Route
            path="/admin/dashboard"
            element={
              <PrivateRoute allowedRoles={["admin"]}>
                <Layout>
                  <Dashboard />
                </Layout>
              </PrivateRoute>
            }
          />
          <Route
            path="/users"
            element={
              <PrivateRoute allowedRoles={["admin"]}>
                <Layout>
                  <Users />
                </Layout>
              </PrivateRoute>
            }
          />

          {/* Manager Routes */}
          <Route
            path="/manager/dashboard"
            element={
              <PrivateRoute allowedRoles={["manager"]}>
                <Layout>
                  <Dashboard />
                </Layout>
              </PrivateRoute>
            }
          />
          <Route
            path="/team-performance"
            element={
              <PrivateRoute allowedRoles={["admin", "manager"]}>
                <Layout>
                  <TeamPerformance />
                </Layout>
              </PrivateRoute>
            }
          />

          {/* Worker Routes */}
          <Route
            path="/worker/dashboard"
            element={
              <PrivateRoute allowedRoles={["worker"]}>
                <Layout>
                  <Dashboard />
                </Layout>
              </PrivateRoute>
            }
          />
          <Route
            path="/worker/my-tasks"
            element={
              <PrivateRoute allowedRoles={["worker"]}>
                <Layout>
                  <Tasks />
                </Layout>
              </PrivateRoute>
            }
          />

          {/* Shared Routes (with role-based access) */}
          <Route
            path="/projects"
            element={
              <PrivateRoute allowedRoles={["admin", "manager"]}>
                <Layout>
                  <Projects />
                </Layout>
              </PrivateRoute>
            }
          />
          <Route
            path="/tasks"
            element={
              <PrivateRoute allowedRoles={["admin", "manager"]}>
                <Layout>
                  <Tasks />
                </Layout>
              </PrivateRoute>
            }
          />
          <Route
            path="/resources"
            element={
              <PrivateRoute allowedRoles={["admin", "manager"]}>
                <Layout>
                  <Resources />
                </Layout>
              </PrivateRoute>
            }
          />
          <Route
            path="/budgets"
            element={
              <PrivateRoute allowedRoles={["admin", "manager"]}>
                <Layout>
                  <Budgets />
                </Layout>
              </PrivateRoute>
            }
          />
          <Route
            path="/import"
            element={
              <PrivateRoute allowedRoles={["admin"]}>
                <Layout>
                  <Import />
                </Layout>
              </PrivateRoute>
            }
          />

          <Route
            path="/profile"
            element={
              <PrivateRoute allowedRoles={["admin", "manager", "worker"]}>
                <Layout>
                  <Profile />
                </Layout>
              </PrivateRoute>
            }
          />

          {/* Default redirect */}
          <Route path="/" element={<Navigate to="/login" replace />} />
        </Routes>
      </AuthProvider>
    </Router>
  );
}

export default App;
```

# File: ./frontend/src/index.tsx

```typescript
import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root') as HTMLElement);
root.render(<App />);

```

# File: ./frontend/src/index.css

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Roboto",
    "Oxygen", "Ubuntu", "Cantarell", "Fira Sans", "Droid Sans",
    "Helvetica Neue", sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

code {
  font-family: source-code-pro, Menlo, Monaco, Consolas, "Courier New",
    monospace;
}
```

# File: ./frontend/src/utils/export.ts

```typescript
export const exportToCSV = (data: any[], filename: string) => {
  if (data.length === 0) return;

  const headers = Object.keys(data[0]);
  const csvContent = [
    headers.join(','),
    ...data.map(row =>
      headers.map(header => {
        const value = row[header];
        if (typeof value === 'string' && value.includes(',')) {
          return `"${value}"`;
        }
        return value ?? '';
      }).join(',')
    )
  ].join('\n');

  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
  const link = document.createElement('a');
  const url = URL.createObjectURL(blob);
  
  link.setAttribute('href', url);
  link.setAttribute('download', `${filename}_${new Date().toISOString().split('T')[0]}.csv`);
  link.style.visibility = 'hidden';
  
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
};
```

# File: ./frontend/src/contexts/AuthContext.tsx

```typescript
import React, { createContext, useContext, useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { authAPI } from "../services/API";
import { AuthState, LoginCredentials } from "../types/auth";

interface AuthContextType extends AuthState {
  login: (credentials: LoginCredentials) => Promise<void>;
  logout: () => void;
  checkAuth: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const [authState, setAuthState] = useState<AuthState>({
    user: null,
    token: null,
    isAuthenticated: false,
    isLoading: true,
  });
  const navigate = useNavigate();

  // Check authentication on mount
  useEffect(() => {
    checkAuth();
  }, []);

  const checkAuth = async () => {
    const token = localStorage.getItem("token");
    const userStr = localStorage.getItem("user");

    if (token && userStr) {
      try {
        // Verify token is still valid by fetching user info
        const response = await authAPI.getCurrentUser(token);
        setAuthState({
          user: response.data,
          token,
          isAuthenticated: true,
          isLoading: false,
        });
      } catch (error) {
        // Token invalid, clear storage
        localStorage.removeItem("token");
        localStorage.removeItem("user");
        setAuthState({
          user: null,
          token: null,
          isAuthenticated: false,
          isLoading: false,
        });
      }
    } else {
      setAuthState({
        user: null,
        token: null,
        isAuthenticated: false,
        isLoading: false,
      });
    }
  };

  const login = async (credentials: LoginCredentials) => {
    try {
      const response = await authAPI.login(credentials);
      const { access_token, user } = response.data;

      localStorage.setItem("token", access_token);
      localStorage.setItem("user", JSON.stringify(user));

      setAuthState({
        user,
        token: access_token,
        isAuthenticated: true,
        isLoading: false,
      });

      if (user.role === "admin") {
        navigate("/admin/dashboard");
      } else if (user.role === "manager") {
        navigate("/manager/dashboard");
      } else if (user.role === "worker") {
        navigate("/worker/dashboard");
      }
    } catch (error: any) {
      throw new Error(
        error.response?.data?.detail || "Login failed. Please try again."
      );
    }
  };

  const logout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    setAuthState({
      user: null,
      token: null,
      isAuthenticated: false,
      isLoading: false,
    });
    navigate("/login");
  };

  return (
    <AuthContext.Provider
      value={{ ...authState, login, logout, checkAuth }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};
```

# File: ./frontend/src/components/Table.tsx

```typescript
import React from "react";

interface TableProps {
  children: React.ReactNode;
  className?: string;
}

export const Table: React.FC<TableProps> = ({ children, className = "" }) => {
  return (
    <div className="overflow-x-auto">
      <table className={`min-w-full divide-y divide-gray-200 ${className}`}>
        {children}
      </table>
    </div>
  );
};

interface TableHeaderProps {
  children: React.ReactNode;
}

export const TableHeader: React.FC<TableHeaderProps> = ({ children }) => {
  return (
    <thead className="bg-gray-50">
      <tr>{children}</tr>
    </thead>
  );
};

interface TableBodyProps {
  children: React.ReactNode;
}

export const TableBody: React.FC<TableBodyProps> = ({ children }) => {
  return <tbody className="bg-white divide-y divide-gray-200">{children}</tbody>;
};

interface TableHeadProps {
  children: React.ReactNode;
  className?: string;
}

export const TableHead: React.FC<TableHeadProps> = ({
  children,
  className = "",
}) => {
  return (
    <th
      className={`px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider ${className}`}
    >
      {children}
    </th>
  );
};

interface TableCellProps {
  children: React.ReactNode;
  className?: string;
  colSpan?: number;
}

export const TableCell: React.FC<TableCellProps> = ({
  children,
  className = "",
  colSpan,
}) => {
  return (
    <td
      className={`px-6 py-4 whitespace-nowrap text-sm ${className}`}
      {...(colSpan && { colSpan })}
    >
      {children}
    </td>
  );
};
```

# File: ./frontend/src/components/Modal.tsx

```typescript
import React from "react";

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  children: React.ReactNode;
  size?: "sm" | "md" | "lg" | "xl";
}

const Modal: React.FC<ModalProps> = ({
  isOpen,
  onClose,
  title,
  children,
  size = "md",
}) => {
  if (!isOpen) return null;

  const sizeClasses = {
    sm: "max-w-md",
    md: "max-w-lg",
    lg: "max-w-2xl",
    xl: "max-w-4xl",
  };

  return (
    <div className="fixed z-10 inset-0 overflow-y-auto">
      <div className="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        {/* Background overlay */}
        <div
          className="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"
          onClick={onClose}
        ></div>

        {/* Modal panel */}
        <div
          className={`inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:w-full ${sizeClasses[size]}`}
        >
          <div className="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-lg font-medium leading-6 text-gray-900">
                {title}
              </h3>
              <button
                onClick={onClose}
                className="text-gray-400 hover:text-gray-500"
              >
                <svg
                  className="h-6 w-6"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M6 18L18 6M6 6l12 12"
                  />
                </svg>
              </button>
            </div>
            {children}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Modal;
```

# File: ./frontend/src/components/Layout.tsx

```typescript
import React from "react";
import { Link, useLocation } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";
import UserMenu from "./UserMenu";
import Notifications from "./Notifications";

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const location = useLocation();
  const { user } = useAuth();

  const isActive = (path: string) => {
    return location.pathname === path
      ? "bg-primary-700 text-white"
      : "text-gray-300 hover:bg-primary-700 hover:text-white";
  };

  const getNavigationLinks = () => {
    if (!user) return [];

    if (user.role === "admin") {
      return [
        { path: "/admin/dashboard", label: "Dashboard" },
        { path: "/projects", label: "Projects" },
        { path: "/tasks", label: "Tasks" },
        { path: "/resources", label: "Resources" },
        { path: "/budgets", label: "Budgets" },
        { path: "/team-performance", label: "Team" },
        { path: "/users", label: "Users" },
        { path: "/import", label: "Import" },
      ];
    } else if (user.role === "manager") {
      return [
        { path: "/manager/dashboard", label: "Dashboard" },
        { path: "/projects", label: "Projects" },
        { path: "/tasks", label: "Tasks" },
        { path: "/resources", label: "Resources" },
        { path: "/budgets", label: "Budgets" },
        { path: "/team-performance", label: "Team" },
      ];
    } else {
      return [
        { path: "/worker/dashboard", label: "Dashboard" },
        { path: "/worker/my-tasks", label: "My Tasks" },
      ];
    }
  };

  const navLinks = getNavigationLinks();

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Navigation */}
      <nav className="bg-primary-600 shadow-lg">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center">
              <Link
                to="/"
                className="flex-shrink-0 text-white text-xl font-bold"
              >
                BuildFlow
              </Link>
              <div className="hidden md:block">
                <div className="ml-10 flex items-baseline space-x-4">
                  {navLinks.map((link) => (
                    <Link
                      key={link.path}
                      to={link.path}
                      className={`px-3 py-2 rounded-md text-sm font-medium ${isActive(
                        link.path
                      )}`}
                    >
                      {link.label}
                    </Link>
                  ))}
                </div>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <Notifications />
              <UserMenu />
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        {children}
      </main>
    </div>
  );
};

export default Layout;
```

# File: ./frontend/src/components/TextArea.tsx

```typescript
import React from "react";

interface TextAreaProps {
  label?: string;
  name: string;
  value: string;
  onChange: (e: React.ChangeEvent<HTMLTextAreaElement>) => void;
  placeholder?: string;
  required?: boolean;
  disabled?: boolean;
  rows?: number;
  className?: string;
  error?: string;
}

const TextArea: React.FC<TextAreaProps> = ({
  label,
  name,
  value,
  onChange,
  placeholder,
  required = false,
  disabled = false,
  rows = 3,
  className = "",
  error,
}) => {
  return (
    <div className={className}>
      {label && (
        <label
          htmlFor={name}
          className="block text-sm font-medium text-gray-700 mb-1"
        >
          {label}
          {required && <span className="text-red-500 ml-1">*</span>}
        </label>
      )}
      <textarea
        id={name}
        name={name}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        required={required}
        disabled={disabled}
        rows={rows}
        className={`block w-full px-3 py-2 border ${
          error ? "border-red-300" : "border-gray-300"
        } rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm ${
          disabled ? "bg-gray-100 cursor-not-allowed" : ""
        }`}
      />
      {error && <p className="mt-1 text-sm text-red-600">{error}</p>}
    </div>
  );
};

export default TextArea;
```

# File: ./frontend/src/components/UserMenu.tsx

```typescript
import React, { useState } from "react";
import { useAuth } from "../contexts/AuthContext";
import { Link } from "react-router-dom";

const UserMenu: React.FC = () => {
  const { user, logout } = useAuth();
  const [isOpen, setIsOpen] = useState(false);

  if (!user) return null;

  const getRoleBadgeColor = (role: string) => {
    switch (role) {
      case "admin":
        return "bg-red-100 text-red-800";
      case "manager":
        return "bg-blue-100 text-blue-800";
      case "worker":
        return "bg-green-100 text-green-800";
      default:
        return "bg-gray-100 text-gray-800";
    }
  };

  return (
    <div className="relative">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center space-x-3 focus:outline-none"
      >
        <div className="text-right">
          <div className="text-sm font-medium text-white">{user.name}</div>
          <div
            className={`text-xs px-2 py-0.5 rounded-full inline-block ${getRoleBadgeColor(user.role)}`}
          >
            {user.role}
          </div>
        </div>
        <div className="w-10 h-10 rounded-full bg-white flex items-center justify-center text-primary-600 font-bold">
          {user.name.charAt(0)}
        </div>
      </button>

      {isOpen && (
        <>
          <div
            className="fixed inset-0 z-10"
            onClick={() => setIsOpen(false)}
          ></div>
          <div className="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg py-1 z-20">
            <div className="px-4 py-2 border-b border-gray-200">
              <div className="text-sm font-medium text-gray-900">
                {user.name}
              </div>
              <div className="text-xs text-gray-500">{user.email}</div>
            </div>
            
            {/* ADD PROFILE LINK */}
            <Link
              to="/profile"
              onClick={() => setIsOpen(false)}
              className="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
            >
              My Profile
            </Link>
            
            <button
              onClick={logout}
              className="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
            >
              Logout
            </button>
          </div>
        </>
      )}
    </div>
  );
};

export default UserMenu;
```

# File: ./frontend/src/components/Select.tsx

```typescript
import React from "react";

interface SelectProps {
  label?: string;
  name: string;
  value: string;
  onChange: (e: React.ChangeEvent<HTMLSelectElement>) => void;
  options: { value: string; label: string }[];
  required?: boolean;
  disabled?: boolean;
  className?: string;
  error?: string;
}

const Select: React.FC<SelectProps> = ({
  label,
  name,
  value,
  onChange,
  options,
  required = false,
  disabled = false,
  className = "",
  error,
}) => {
  return (
    <div className={className}>
      {label && (
        <label
          htmlFor={name}
          className="block text-sm font-medium text-gray-700 mb-1"
        >
          {label}
          {required && <span className="text-red-500 ml-1">*</span>}
        </label>
      )}
      <select
        id={name}
        name={name}
        value={value}
        onChange={onChange}
        required={required}
        disabled={disabled}
        className={`block w-full px-3 py-2 border ${
          error ? "border-red-300" : "border-gray-300"
        } rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm ${
          disabled ? "bg-gray-100 cursor-not-allowed" : ""
        }`}
      >
        {options.map((option) => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
      {error && <p className="mt-1 text-sm text-red-600">{error}</p>}
    </div>
  );
};

export default Select;
```

# File: ./frontend/src/components/PrivateRoute.tsx

```typescript
import React from "react";
import { Navigate } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";

interface PrivateRouteProps {
  children: React.ReactNode;
  allowedRoles?: string[];
}

const PrivateRoute: React.FC<PrivateRouteProps> = ({
  children,
  allowedRoles,
}) => {
  const { isAuthenticated, isLoading, user } = useAuth();

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-gray-500">Loading...</div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  if (allowedRoles && user && !allowedRoles.includes(user.role)) {
    if (user.role === "admin") {
      return <Navigate to="/admin/dashboard" replace />;
    } else if (user.role === "manager") {
      return <Navigate to="/manager/dashboard" replace />;
    } else {
      return <Navigate to="/worker/dashboard" replace />;
    }
  }

  return <>{children}</>;
};

export default PrivateRoute;
```

# File: ./frontend/src/components/Button.tsx

```typescript
import React from "react";

interface ButtonProps {
  children: React.ReactNode;
  onClick?: () => void;
  type?: "button" | "submit" | "reset";
  variant?: "primary" | "secondary" | "danger" | "success";
  size?: "sm" | "md" | "lg";
  disabled?: boolean;
  className?: string;
}

const Button: React.FC<ButtonProps> = ({
  children,
  onClick,
  type = "button",
  variant = "primary",
  size = "md",
  disabled = false,
  className = "",
}) => {
  const baseClasses =
    "font-medium rounded-md focus:outline-none focus:ring-2 focus:ring-offset-2 transition-colors";

  const variantClasses = {
    primary:
      "bg-primary-600 text-white hover:bg-primary-700 focus:ring-primary-500",
    secondary:
      "bg-gray-200 text-gray-900 hover:bg-gray-300 focus:ring-gray-500",
    danger: "bg-red-600 text-white hover:bg-red-700 focus:ring-red-500",
    success:
      "bg-green-600 text-white hover:bg-green-700 focus:ring-green-500",
  };

  const sizeClasses = {
    sm: "px-3 py-1.5 text-sm",
    md: "px-4 py-2 text-sm",
    lg: "px-6 py-3 text-base",
  };

  const disabledClasses = disabled ? "opacity-50 cursor-not-allowed" : "";

  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled}
      className={`${baseClasses} ${variantClasses[variant]} ${sizeClasses[size]} ${disabledClasses} ${className}`}
    >
      {children}
    </button>
  );
};

export default Button;
```

# File: ./frontend/src/components/KPIReports.tsx

```typescript
import React from "react";
import { Card, CardHeader, CardBody } from "./Card";

interface KPIData {
  label: string;
  value: string | number;
  change?: number;
  trend?: "up" | "down" | "neutral";
  format?: "currency" | "percentage" | "number";
}

interface KPIReportsProps {
  title: string;
  kpis: KPIData[];
}

const KPIReports: React.FC<KPIReportsProps> = ({ title, kpis }) => {
  const formatValue = (value: string | number, format?: string) => {
    if (typeof value === "number") {
      if (format === "currency") {
        return new Intl.NumberFormat("en-US", {
          style: "currency",
          currency: "USD",
        }).format(value);
      } else if (format === "percentage") {
        return `${value.toFixed(1)}%`;
      } else {
        return value.toLocaleString();
      }
    }
    return value;
  };

  const getTrendIcon = (trend?: "up" | "down" | "neutral") => {
    if (trend === "up") {
      return (
        <svg
          className="h-5 w-5 text-green-500"
          fill="currentColor"
          viewBox="0 0 20 20"
        >
          <path
            fillRule="evenodd"
            d="M5.293 9.707a1 1 0 010-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 01-1.414 1.414L11 7.414V15a1 1 0 11-2 0V7.414L6.707 9.707a1 1 0 01-1.414 0z"
            clipRule="evenodd"
          />
        </svg>
      );
    } else if (trend === "down") {
      return (
        <svg
          className="h-5 w-5 text-red-500"
          fill="currentColor"
          viewBox="0 0 20 20"
        >
          <path
            fillRule="evenodd"
            d="M14.707 10.293a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 111.414-1.414L9 12.586V5a1 1 0 012 0v7.586l2.293-2.293a1 1 0 011.414 0z"
            clipRule="evenodd"
          />
        </svg>
      );
    }
    return null;
  };

  return (
    <Card>
      <CardHeader>
        <h3 className="text-lg font-medium leading-6 text-gray-900">{title}</h3>
      </CardHeader>
      <CardBody>
        <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
          {kpis.map((kpi, index) => (
            <div key={index} className="bg-gray-50 p-4 rounded-lg">
              <div className="flex items-center justify-between">
                <div className="text-sm font-medium text-gray-600">
                  {kpi.label}
                </div>
                {kpi.trend && getTrendIcon(kpi.trend)}
              </div>
              <div className="mt-2 flex items-baseline">
                <div className="text-2xl font-semibold text-gray-900">
                  {formatValue(kpi.value, kpi.format)}
                </div>
                {kpi.change !== undefined && (
                  <div
                    className={`ml-2 text-sm ${
                      kpi.change >= 0 ? "text-green-600" : "text-red-600"
                    }`}
                  >
                    {kpi.change >= 0 ? "+" : ""}
                    {kpi.change.toFixed(1)}%
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      </CardBody>
    </Card>
  );
};

export default KPIReports;
```

# File: ./frontend/src/components/Notifications.tsx

```typescript
import React, { useState, useEffect, useCallback } from "react";
import { useAuth } from "../contexts/AuthContext";
import { tasksAPI, Task } from "../services/API";

const Notifications: React.FC = () => {
  const { user } = useAuth();
  const [isOpen, setIsOpen] = useState(false);
  const [overdueTasks, setOverdueTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(false);

  const fetchNotifications = useCallback(async () => {
    if (!user) return;

    setLoading(true);
    try {
      const response = await tasksAPI.getAll({});
      const tasks = response.data;

      let filtered = tasks.filter((task) => task.is_overdue);

      if (user.role === "worker") {
        filtered = filtered.filter(
          (task) => task.assigned_to === user.worker_name
        );
      } else if (user.role === "manager") {
        const managedProjects = user.managed_projects || [];
        filtered = filtered.filter((task) =>
          managedProjects.includes(task.project_id)
        );
      }

      setOverdueTasks(filtered);
    } catch (err) {
      console.error("Failed to fetch notifications:", err);
    } finally {
      setLoading(false);
    }
  }, [user]);

  useEffect(() => {
    if (isOpen && user) {
      fetchNotifications();
    }
  }, [isOpen, user, fetchNotifications]);

  if (!user) return null;

  const notificationCount = overdueTasks.length;

  return (
    <div className="relative">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="relative p-2 text-white hover:bg-primary-700 rounded-md focus:outline-none"
      >
        <svg
          className="h-6 w-6"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"
          />
        </svg>
        {notificationCount > 0 && (
          <span className="absolute top-0 right-0 inline-flex items-center justify-center px-2 py-1 text-xs font-bold leading-none text-white transform translate-x-1/2 -translate-y-1/2 bg-red-600 rounded-full">
            {notificationCount}
          </span>
        )}
      </button>

      {isOpen && (
        <>
          <div
            className="fixed inset-0 z-10"
            onClick={() => setIsOpen(false)}
          ></div>
          <div className="absolute right-0 mt-2 w-80 bg-white rounded-md shadow-lg py-1 z-20 max-h-96 overflow-y-auto">
            <div className="px-4 py-2 border-b border-gray-200">
              <div className="text-sm font-semibold text-gray-900">
                Notifications
              </div>
            </div>

            {loading ? (
              <div className="px-4 py-8 text-center text-gray-500">
                Loading...
              </div>
            ) : overdueTasks.length > 0 ? (
              <div className="divide-y divide-gray-200">
                {overdueTasks.slice(0, 5).map((task) => (
                  <div key={task.id} className="px-4 py-3 hover:bg-gray-50">
                    <div className="flex items-start">
                      <div className="flex-shrink-0">
                        <svg
                          className="h-5 w-5 text-red-600"
                          fill="currentColor"
                          viewBox="0 0 20 20"
                        >
                          <path
                            fillRule="evenodd"
                            d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                            clipRule="evenodd"
                          />
                        </svg>
                      </div>
                      <div className="ml-3 flex-1">
                        <p className="text-sm font-medium text-gray-900">
                          {task.name}
                        </p>
                        <p className="text-xs text-red-600 mt-1">
                          Overdue since{" "}
                          {task.planned_end_date
                            ? new Date(
                                task.planned_end_date
                              ).toLocaleDateString()
                            : "N/A"}
                        </p>
                        {task.assigned_to && (
                          <p className="text-xs text-gray-500 mt-1">
                            Assigned to: {task.assigned_to}
                          </p>
                        )}
                      </div>
                    </div>
                  </div>
                ))}
                {overdueTasks.length > 5 && (
                  <div className="px-4 py-2 text-center text-sm text-primary-600 hover:bg-gray-50">
                    +{overdueTasks.length - 5} more overdue tasks
                  </div>
                )}
              </div>
            ) : (
              <div className="px-4 py-8 text-center text-gray-500">
                <svg
                  className="mx-auto h-12 w-12 text-gray-400"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
                <p className="mt-2 text-sm">No overdue tasks!</p>
              </div>
            )}
          </div>
        </>
      )}
    </div>
  );
};

export default Notifications;
```

# File: ./frontend/src/components/Card.tsx

```typescript
import React from "react";

interface CardProps {
  children: React.ReactNode;
  className?: string;
}

export const Card: React.FC<CardProps> = ({ children, className = "" }) => {
  return (
    <div
      className={`bg-white overflow-hidden shadow rounded-lg ${className}`}
    >
      {children}
    </div>
  );
};

interface CardHeaderProps {
  children: React.ReactNode;
  className?: string;
}

export const CardHeader: React.FC<CardHeaderProps> = ({
  children,
  className = "",
}) => {
  return (
    <div className={`px-4 py-5 border-b border-gray-200 sm:px-6 ${className}`}>
      {children}
    </div>
  );
};

interface CardBodyProps {
  children: React.ReactNode;
  className?: string;
}

export const CardBody: React.FC<CardBodyProps> = ({
  children,
  className = "",
}) => {
  return <div className={`px-4 py-5 sm:p-6 ${className}`}>{children}</div>;
};
```

# File: ./frontend/src/components/ActivityLog.tsx

```typescript
import React from "react";
import { Card, CardHeader, CardBody } from "./Card";

interface Activity {
  id: number;
  user: string;
  action: string;
  timestamp: string;
  details: string;
}

interface ActivityLogProps {
  activities: Activity[];
}

const ActivityLog: React.FC<ActivityLogProps> = ({ activities }) => {
  const getActivityIcon = (action: string) => {
    if (action.includes("create")) return "➕";
    if (action.includes("update")) return "✏️";
    if (action.includes("delete")) return "🗑️";
    if (action.includes("login")) return "🔐";
    return "📝";
  };

  return (
    <Card>
      <CardHeader>
        <h3 className="text-lg font-medium leading-6 text-gray-900">
          Recent Activity
        </h3>
      </CardHeader>
      <CardBody>
        {activities.length > 0 ? (
          <div className="flow-root">
            <ul className="-mb-8">
              {activities.map((activity, idx) => (
                <li key={activity.id}>
                  <div className="relative pb-8">
                    {idx !== activities.length - 1 && (
                      <span
                        className="absolute top-4 left-4 -ml-px h-full w-0.5 bg-gray-200"
                        aria-hidden="true"
                      />
                    )}
                    <div className="relative flex space-x-3">
                      <div>
                        <span className="h-8 w-8 rounded-full bg-primary-100 flex items-center justify-center text-lg">
                          {getActivityIcon(activity.action)}
                        </span>
                      </div>
                      <div className="flex-1 min-w-0">
                        <div>
                          <p className="text-sm text-gray-900">
                            <span className="font-medium">{activity.user}</span>{" "}
                            {activity.action}
                          </p>
                          <p className="text-xs text-gray-500 mt-0.5">
                            {new Date(activity.timestamp).toLocaleString()}
                          </p>
                        </div>
                        {activity.details && (
                          <p className="text-sm text-gray-600 mt-1">
                            {activity.details}
                          </p>
                        )}
                      </div>
                    </div>
                  </div>
                </li>
              ))}
            </ul>
          </div>
        ) : (
          <div className="text-center py-8 text-gray-500">
            <p>No recent activity</p>
          </div>
        )}
      </CardBody>
    </Card>
  );
};

export default ActivityLog;
```

# File: ./frontend/src/components/Input.tsx

```typescript
import React from "react";

interface InputProps {
  label?: string;
  type?: string;
  name: string;
  value: string | number;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  placeholder?: string;
  required?: boolean;
  disabled?: boolean;
  className?: string;
  error?: string;
}

const Input: React.FC<InputProps> = ({
  label,
  type = "text",
  name,
  value,
  onChange,
  placeholder,
  required = false,
  disabled = false,
  className = "",
  error,
}) => {
  return (
    <div className={className}>
      {label && (
        <label
          htmlFor={name}
          className="block text-sm font-medium text-gray-700 mb-1"
        >
          {label}
          {required && <span className="text-red-500 ml-1">*</span>}
        </label>
      )}
      <input
        type={type}
        id={name}
        name={name}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        required={required}
        disabled={disabled}
        className={`block w-full px-3 py-2 border ${
          error ? "border-red-300" : "border-gray-300"
        } rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm ${
          disabled ? "bg-gray-100 cursor-not-allowed" : ""
        }`}
      />
      {error && <p className="mt-1 text-sm text-red-600">{error}</p>}
    </div>
  );
};

export default Input;
```

# File: ./frontend/src/components/dashboards/AdminDashboard.tsx

```typescript
import React from "react";
import { Link } from "react-router-dom";
import { Card, CardHeader, CardBody } from "../Card";
import { DashboardStats } from "../../services/API";

interface AdminDashboardProps {
  stats: DashboardStats;
  onRefresh: () => void;
}

const AdminDashboard: React.FC<AdminDashboardProps> = ({
  stats,
  onRefresh,
}) => {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">
            Admin Dashboard
          </h1>
          <p className="text-gray-600 mt-1">
            Complete overview of all projects and resources
          </p>
        </div>
        <button
          onClick={onRefresh}
          className="px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700"
        >
          Refresh
        </button>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        {/* Total Projects */}
        <Card>
          <CardBody>
            <div className="flex items-center">
              <div className="flex-shrink-0 bg-primary-500 rounded-md p-3">
                <svg
                  className="h-6 w-6 text-white"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"
                  />
                </svg>
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">
                    Total Projects
                  </dt>
                  <dd className="text-2xl font-semibold text-gray-900">
                    {stats.total_projects}
                  </dd>
                </dl>
              </div>
            </div>
            <div className="mt-2 text-sm text-gray-500">
              {stats.active_projects} active,{" "}
              {stats.completed_projects} completed
            </div>
          </CardBody>
        </Card>

        {/* Budget */}
        <Card>
          <CardBody>
            <div className="flex items-center">
              <div className="flex-shrink-0 bg-green-500 rounded-md p-3">
                <svg
                  className="h-6 w-6 text-white"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">
                    Total Budget
                  </dt>
                  <dd className="text-2xl font-semibold text-gray-900">
                    ${(stats.total_budget / 1000000).toFixed(1)}M
                  </dd>
                </dl>
              </div>
            </div>
            <div className="mt-2 text-sm text-gray-500">
              ${(stats.total_spent / 1000000).toFixed(1)}M spent (
              {stats.budget_utilization.toFixed(1)}%)
            </div>
          </CardBody>
        </Card>

        {/* Tasks */}
        <Card>
          <CardBody>
            <div className="flex items-center">
              <div className="flex-shrink-0 bg-blue-500 rounded-md p-3">
                <svg
                  className="h-6 w-6 text-white"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
                  />
                </svg>
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">
                    Total Tasks
                  </dt>
                  <dd className="text-2xl font-semibold text-gray-900">
                    {stats.total_tasks}
                  </dd>
                </dl>
              </div>
            </div>
            <div className="mt-2 text-sm text-gray-500">
              {stats.completed_tasks} completed (
              {stats.task_completion_rate.toFixed(1)}%)
            </div>
          </CardBody>
        </Card>

        {/* Overdue Tasks */}
        <Card>
          <CardBody>
            <div className="flex items-center">
              <div className="flex-shrink-0 bg-red-500 rounded-md p-3">
                <svg
                  className="h-6 w-6 text-white"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">
                    Overdue Tasks
                  </dt>
                  <dd className="text-2xl font-semibold text-gray-900">
                    {stats.overdue_tasks}
                  </dd>
                </dl>
              </div>
            </div>
            <div className="mt-2 text-sm text-gray-500">
              Requires attention
            </div>
          </CardBody>
        </Card>
      </div>

      {/* Quick Actions */}
      <Card>
        <CardHeader>
          <h3 className="text-lg font-medium leading-6 text-gray-900">
            Quick Actions
          </h3>
        </CardHeader>
        <CardBody>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-4">
            <Link
              to="/projects"
              className="flex items-center justify-center px-4 py-3 border border-transparent text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700"
            >
              Manage Projects
            </Link>
            <Link
              to="/tasks"
              className="flex items-center justify-center px-4 py-3 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700"
            >
              View All Tasks
            </Link>
            <Link
              to="/import"
              className="flex items-center justify-center px-4 py-3 border border-transparent text-sm font-medium rounded-md text-white bg-green-600 hover:bg-green-700"
            >
              Import Data
            </Link>
            <Link
              to="/users"
              className="flex items-center justify-center px-4 py-3 border border-transparent text-sm font-medium rounded-md text-white bg-purple-600 hover:bg-purple-700"
            >
              Manage Users
            </Link>
          </div>
        </CardBody>
      </Card>

      {/* System Health */}
      <div className="grid grid-cols-1 gap-5 lg:grid-cols-2">
        <Card>
          <CardHeader>
            <h3 className="text-lg font-medium leading-6 text-gray-900">
              Budget Overview
            </h3>
          </CardHeader>
          <CardBody>
            <div className="space-y-4">
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span className="text-gray-600">Budget Utilization</span>
                  <span className="font-semibold">
                    {stats.budget_utilization.toFixed(1)}%
                  </span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className={`h-2 rounded-full ${
                      stats.budget_utilization > 90
                        ? "bg-red-600"
                        : stats.budget_utilization > 75
                        ? "bg-yellow-500"
                        : "bg-green-500"
                    }`}
                    style={{
                      width: `${Math.min(stats.budget_utilization, 100)}%`,
                    }}
                  ></div>
                </div>
              </div>
              <div className="grid grid-cols-2 gap-4 pt-4 border-t">
                <div>
                  <p className="text-sm text-gray-600">Total Budget</p>
                  <p className="text-lg font-semibold">
                    ${(stats.total_budget / 1000000).toFixed(2)}M
                  </p>
                </div>
                <div>
                  <p className="text-sm text-gray-600">Total Spent</p>
                  <p className="text-lg font-semibold">
                    ${(stats.total_spent / 1000000).toFixed(2)}M
                  </p>
                </div>
              </div>
            </div>
          </CardBody>
        </Card>

        <Card>
          <CardHeader>
            <h3 className="text-lg font-medium leading-6 text-gray-900">
              Task Completion
            </h3>
          </CardHeader>
          <CardBody>
            <div className="space-y-4">
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span className="text-gray-600">Completion Rate</span>
                  <span className="font-semibold">
                    {stats.task_completion_rate.toFixed(1)}%
                  </span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className="bg-blue-600 h-2 rounded-full"
                    style={{
                      width: `${Math.min(stats.task_completion_rate, 100)}%`,
                    }}
                  ></div>
                </div>
              </div>
              <div className="grid grid-cols-3 gap-4 pt-4 border-t">
                <div>
                  <p className="text-sm text-gray-600">Total</p>
                  <p className="text-lg font-semibold">{stats.total_tasks}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-600">Completed</p>
                  <p className="text-lg font-semibold text-green-600">
                    {stats.completed_tasks}
                  </p>
                </div>
                <div>
                  <p className="text-sm text-gray-600">Overdue</p>
                  <p className="text-lg font-semibold text-red-600">
                    {stats.overdue_tasks}
                  </p>
                </div>
              </div>
            </div>
          </CardBody>
        </Card>
      </div>
    </div>
  );
};

export default AdminDashboard;
```

# File: ./frontend/src/components/dashboards/WorkerDashboard.tsx

```typescript
import React from "react";
import { Link } from "react-router-dom";
import { Card, CardHeader, CardBody } from "../Card";

interface WorkerStats {
  total_tasks: number;
  completed_tasks: number;
  in_progress_tasks: number;
  not_started_tasks: number;
  overdue_tasks: number;
  upcoming_tasks: number;
  task_completion_rate: number;
}

interface WorkerDashboardProps {
  stats: WorkerStats;
  onRefresh: () => void;
}

const WorkerDashboard: React.FC<WorkerDashboardProps> = ({
  stats,
  onRefresh,
}) => {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">
            Worker Dashboard
          </h1>
          <p className="text-gray-600 mt-1">Manage your assigned tasks</p>
        </div>
        <button
          onClick={onRefresh}
          className="px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700"
        >
          Refresh
        </button>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardBody>
            <div className="flex items-center">
              <div className="flex-shrink-0 bg-blue-500 rounded-md p-3">
                <svg
                  className="h-6 w-6 text-white"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
                  />
                </svg>
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">
                    My Tasks
                  </dt>
                  <dd className="text-2xl font-semibold text-gray-900">
                    {stats.total_tasks}
                  </dd>
                </dl>
              </div>
            </div>
            <div className="mt-2 text-sm text-gray-500">Total assigned</div>
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <div className="flex items-center">
              <div className="flex-shrink-0 bg-green-500 rounded-md p-3">
                <svg
                  className="h-6 w-6 text-white"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M5 13l4 4L19 7"
                  />
                </svg>
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">
                    Completed
                  </dt>
                  <dd className="text-2xl font-semibold text-gray-900">
                    {stats.completed_tasks}
                  </dd>
                </dl>
              </div>
            </div>
            <div className="mt-2 text-sm text-gray-500">
              {stats.task_completion_rate.toFixed(0)}% rate
            </div>
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <div className="flex items-center">
              <div className="flex-shrink-0 bg-yellow-500 rounded-md p-3">
                <svg
                  className="h-6 w-6 text-white"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">
                    In Progress
                  </dt>
                  <dd className="text-2xl font-semibold text-gray-900">
                    {stats.in_progress_tasks}
                  </dd>
                </dl>
              </div>
            </div>
            <div className="mt-2 text-sm text-gray-500">Currently working</div>
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <div className="flex items-center">
              <div className="flex-shrink-0 bg-red-500 rounded-md p-3">
                <svg
                  className="h-6 w-6 text-white"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">
                    Overdue
                  </dt>
                  <dd className="text-2xl font-semibold text-gray-900">
                    {stats.overdue_tasks}
                  </dd>
                </dl>
              </div>
            </div>
            <div className="mt-2 text-sm text-gray-500">Need attention</div>
          </CardBody>
        </Card>
      </div>

      {/* Quick Actions */}
      <Card>
        <CardHeader>
          <h3 className="text-lg font-medium leading-6 text-gray-900">
            Quick Actions
          </h3>
        </CardHeader>
        <CardBody>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <Link
              to="/worker/my-tasks"
              className="flex items-center justify-center px-4 py-3 border border-transparent text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700"
            >
              View My Tasks
            </Link>
            <Link
              to="/worker/my-tasks?filter=overdue"
              className="flex items-center justify-center px-4 py-3 border border-transparent text-sm font-medium rounded-md text-white bg-red-600 hover:bg-red-700"
            >
              View Overdue Tasks
            </Link>
          </div>
        </CardBody>
      </Card>

      {/* Task Status Overview */}
      <div className="grid grid-cols-1 gap-5 lg:grid-cols-2">
        <Card>
          <CardHeader>
            <h3 className="text-lg font-medium leading-6 text-gray-900">
              Task Status
            </h3>
          </CardHeader>
          <CardBody>
            <div className="space-y-3">
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-600">Completed</span>
                <div className="flex items-center">
                  <div className="w-32 bg-gray-200 rounded-full h-2 mr-2">
                    <div
                      className="bg-green-500 h-2 rounded-full"
                      style={{
                        width: `${
                          stats.total_tasks > 0
                            ? (stats.completed_tasks / stats.total_tasks) * 100
                            : 0
                        }%`,
                      }}
                    ></div>
                  </div>
                  <span className="text-sm font-semibold">
                    {stats.completed_tasks}
                  </span>
                </div>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-600">In Progress</span>
                <div className="flex items-center">
                  <div className="w-32 bg-gray-200 rounded-full h-2 mr-2">
                    <div
                      className="bg-yellow-500 h-2 rounded-full"
                      style={{
                        width: `${
                          stats.total_tasks > 0
                            ? (stats.in_progress_tasks / stats.total_tasks) *
                              100
                            : 0
                        }%`,
                      }}
                    ></div>
                  </div>
                  <span className="text-sm font-semibold">
                    {stats.in_progress_tasks}
                  </span>
                </div>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-600">Not Started</span>
                <div className="flex items-center">
                  <div className="w-32 bg-gray-200 rounded-full h-2 mr-2">
                    <div
                      className="bg-gray-400 h-2 rounded-full"
                      style={{
                        width: `${
                          stats.total_tasks > 0
                            ? (stats.not_started_tasks / stats.total_tasks) *
                              100
                            : 0
                        }%`,
                      }}
                    ></div>
                  </div>
                  <span className="text-sm font-semibold">
                    {stats.not_started_tasks}
                  </span>
                </div>
              </div>
            </div>
          </CardBody>
        </Card>

        <Card>
          <CardHeader>
            <h3 className="text-lg font-medium leading-6 text-gray-900">
              Upcoming Deadlines
            </h3>
          </CardHeader>
          <CardBody>
            <div className="text-center py-8">
              <svg
                className="mx-auto h-12 w-12 text-gray-400"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
                />
              </svg>
              <h3 className="mt-2 text-sm font-medium text-gray-900">
                Tasks Due Soon
              </h3>
              <p className="mt-1 text-sm text-gray-500">
                You have {stats.upcoming_tasks} task(s) due in the next 7 days
              </p>
              <div className="mt-6">
                <Link
                  to="/worker/my-tasks?filter=upcoming"
                  className="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700"
                >
                  View Upcoming Tasks
                </Link>
              </div>
            </div>
          </CardBody>
        </Card>
      </div>
    </div>
  );
};

export default WorkerDashboard;
```

# File: ./frontend/src/components/dashboards/ManagerDashboard.tsx

```typescript
import React from "react";
import { Link } from "react-router-dom";
import { Card, CardHeader, CardBody } from "../Card";
import { DashboardStats } from "../../services/API";

interface ManagerDashboardProps {
  stats: DashboardStats;
  onRefresh: () => void;
}

const ManagerDashboard: React.FC<ManagerDashboardProps> = ({
  stats,
  onRefresh,
}) => {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">
            Manager Dashboard
          </h1>
          <p className="text-gray-600 mt-1">
            Manage your assigned projects and team
          </p>
        </div>
        <button
          onClick={onRefresh}
          className="px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700"
        >
          Refresh
        </button>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardBody>
            <div className="flex items-center">
              <div className="flex-shrink-0 bg-primary-500 rounded-md p-3">
                <svg
                  className="h-6 w-6 text-white"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"
                  />
                </svg>
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">
                    My Projects
                  </dt>
                  <dd className="text-2xl font-semibold text-gray-900">
                    {stats.total_projects}
                  </dd>
                </dl>
              </div>
            </div>
            <div className="mt-2 text-sm text-gray-500">
              {stats.active_projects} active
            </div>
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <div className="flex items-center">
              <div className="flex-shrink-0 bg-green-500 rounded-md p-3">
                <svg
                  className="h-6 w-6 text-white"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">
                    Budget
                  </dt>
                  <dd className="text-2xl font-semibold text-gray-900">
                    {stats.budget_utilization.toFixed(0)}%
                  </dd>
                </dl>
              </div>
            </div>
            <div className="mt-2 text-sm text-gray-500">
              ${(stats.total_spent / 1000000).toFixed(1)}M spent
            </div>
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <div className="flex items-center">
              <div className="flex-shrink-0 bg-blue-500 rounded-md p-3">
                <svg
                  className="h-6 w-6 text-white"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
                  />
                </svg>
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">
                    Tasks
                  </dt>
                  <dd className="text-2xl font-semibold text-gray-900">
                    {stats.total_tasks}
                  </dd>
                </dl>
              </div>
            </div>
            <div className="mt-2 text-sm text-gray-500">
              {stats.task_completion_rate.toFixed(0)}% complete
            </div>
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <div className="flex items-center">
              <div className="flex-shrink-0 bg-red-500 rounded-md p-3">
                <svg
                  className="h-6 w-6 text-white"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">
                    Issues
                  </dt>
                  <dd className="text-2xl font-semibold text-gray-900">
                    {stats.overdue_tasks}
                  </dd>
                </dl>
              </div>
            </div>
            <div className="mt-2 text-sm text-gray-500">Overdue tasks</div>
          </CardBody>
        </Card>
      </div>

      {/* Quick Actions for Manager */}
      <Card>
        <CardHeader>
          <h3 className="text-lg font-medium leading-6 text-gray-900">
            Quick Actions
          </h3>
        </CardHeader>
        <CardBody>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
            <Link
              to="/projects"
              className="flex items-center justify-center px-4 py-3 border border-transparent text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700"
            >
              View Projects
            </Link>
            <Link
              to="/tasks"
              className="flex items-center justify-center px-4 py-3 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700"
            >
              Manage Tasks
            </Link>
            <Link
              to="/resources"
              className="flex items-center justify-center px-4 py-3 border border-transparent text-sm font-medium rounded-md text-white bg-green-600 hover:bg-green-700"
            >
              Track Resources
            </Link>
          </div>
        </CardBody>
      </Card>

      {/* Performance Overview */}
      <div className="grid grid-cols-1 gap-5 lg:grid-cols-2">
        <Card>
          <CardHeader>
            <h3 className="text-lg font-medium leading-6 text-gray-900">
              Budget Performance
            </h3>
          </CardHeader>
          <CardBody>
            <div className="space-y-4">
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span className="text-gray-600">Budget Utilization</span>
                  <span className="font-semibold">
                    {stats.budget_utilization.toFixed(1)}%
                  </span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className={`h-2 rounded-full ${
                      stats.budget_utilization > 90
                        ? "bg-red-600"
                        : stats.budget_utilization > 75
                        ? "bg-yellow-500"
                        : "bg-green-500"
                    }`}
                    style={{
                      width: `${Math.min(stats.budget_utilization, 100)}%`,
                    }}
                  ></div>
                </div>
              </div>
              <div className="grid grid-cols-2 gap-4 pt-4 border-t">
                <div>
                  <p className="text-sm text-gray-600">Allocated</p>
                  <p className="text-lg font-semibold">
                    ${(stats.total_budget / 1000000).toFixed(2)}M
                  </p>
                </div>
                <div>
                  <p className="text-sm text-gray-600">Spent</p>
                  <p className="text-lg font-semibold">
                    ${(stats.total_spent / 1000000).toFixed(2)}M
                  </p>
                </div>
              </div>
            </div>
          </CardBody>
        </Card>

        <Card>
          <CardHeader>
            <h3 className="text-lg font-medium leading-6 text-gray-900">
              Team Progress
            </h3>
          </CardHeader>
          <CardBody>
            <div className="space-y-4">
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span className="text-gray-600">Task Completion</span>
                  <span className="font-semibold">
                    {stats.task_completion_rate.toFixed(1)}%
                  </span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className="bg-blue-600 h-2 rounded-full"
                    style={{
                      width: `${Math.min(stats.task_completion_rate, 100)}%`,
                    }}
                  ></div>
                </div>
              </div>
              <div className="grid grid-cols-3 gap-4 pt-4 border-t">
                <div>
                  <p className="text-sm text-gray-600">Total</p>
                  <p className="text-lg font-semibold">{stats.total_tasks}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-600">Done</p>
                  <p className="text-lg font-semibold text-green-600">
                    {stats.completed_tasks}
                  </p>
                </div>
                <div>
                  <p className="text-sm text-gray-600">Overdue</p>
                  <p className="text-lg font-semibold text-red-600">
                    {stats.overdue_tasks}
                  </p>
                </div>
              </div>
            </div>
          </CardBody>
        </Card>
      </div>
    </div>
  );
};

export default ManagerDashboard;
```

# File: ./frontend/src/services/API.ts

```typescript
import axios from "axios";

const API_BASE_URL =
  process.env.REACT_APP_API_URL || "http://localhost:8000";

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid
      localStorage.removeItem("token");
      localStorage.removeItem("user");
      window.location.href = "/login";
    }
    return Promise.reject(error);
  }
);

export interface Project {
  id: number;
  name: string;
  description?: string;
  status: string;
  start_date?: string;
  planned_end_date?: string;
  actual_end_date?: string;
  total_budget: number;
  spent_amount: number;
  budget_utilization: number;
  remaining_budget: number;
  location?: string;
  created_at: string;
  updated_at: string;
}

export interface Task {
  id: number;
  project_id: number;
  name: string;
  description?: string;
  status: string;
  priority: string;
  start_date?: string;
  planned_end_date?: string;
  actual_end_date?: string;
  progress_percentage: number;
  assigned_to?: string;
  is_overdue: boolean;
  created_at: string;
  updated_at: string;
}

export interface Resource {
  id: number;
  project_id: number;
  name: string;
  resource_type: string;
  status: string;
  quantity: number;
  unit?: string;
  unit_cost: number;
  total_cost: number;
  supplier?: string;
  allocated_date: string;
  created_at: string;
  updated_at: string;
}

export interface Budget {
  id: number;
  project_id: number;
  category: string;
  description?: string;
  planned_amount: number;
  actual_amount: number;
  variance: number;
  variance_percentage: number;
  budget_date: string;
  created_at: string;
  updated_at: string;
}

export interface DashboardStats {
  total_projects: number;
  active_projects: number;
  completed_projects: number;
  total_budget: number;
  total_spent: number;
  budget_utilization: number;
  total_tasks: number;
  completed_tasks: number;
  overdue_tasks: number;
  task_completion_rate: number;
}

export interface TeamMember {
  username: string;
  role: string;
  name: string;
  email: string;
  worker_name?: string;
  managed_projects?: number[];
}

export interface TeamPerformance {
  worker_name: string;
  total_tasks: number;
  completed_tasks: number;
  avg_progress: number;
  completion_rate: number;
}

export interface ActivityLog {
  id: number;
  user: string;
  action: string;
  timestamp: string;
  details: string;
}

export interface WorkerStats {
  total_tasks: number;
  completed_tasks: number;
  in_progress_tasks: number;
  not_started_tasks: number;
  overdue_tasks: number;
  upcoming_tasks: number;
  task_completion_rate: number;
}

// Projects
export const projectsAPI = {
  getAll: () => api.get<Project[]>("/api/projects/"),
  getById: (id: number) => api.get<Project>(`/api/projects/${id}`),
  create: (data: Partial<Project>) =>
    api.post<Project>("/api/projects/", data),
  update: (id: number, data: Partial<Project>) =>
    api.put<Project>(`/api/projects/${id}`, data),
  delete: (id: number) => api.delete(`/api/projects/${id}`),
  getSummary: () => api.get("/api/projects/summary"),
};

// Tasks
export const tasksAPI = {
  getAll: (params?: { project_id?: number; status?: string }) =>
    api.get<Task[]>("/api/tasks/", { params }),
  getById: (id: number) => api.get<Task>(`/api/tasks/${id}`),
  create: (data: Partial<Task>) => api.post<Task>("/api/tasks/", data),
  update: (id: number, data: Partial<Task>) =>
    api.put<Task>(`/api/tasks/${id}`, data),
  delete: (id: number) => api.delete(`/api/tasks/${id}`),
  getOverdue: (projectId: number) =>
    api.get<Task[]>(`/api/tasks/project/${projectId}/overdue`),
};

// Resources
export const resourcesAPI = {
  getAll: (params?: {
    project_id?: number;
    resource_type?: string;
  }) => api.get<Resource[]>("/api/resources/", { params }),
  getById: (id: number) => api.get<Resource>(`/api/resources/${id}`),
  create: (data: Partial<Resource>) =>
    api.post<Resource>("/api/resources/", data),
  update: (id: number, data: Partial<Resource>) =>
    api.put<Resource>(`/api/resources/${id}`, data),
  delete: (id: number) => api.delete(`/api/resources/${id}`),
};

// Budgets
export const budgetsAPI = {
  getAll: (params?: { project_id?: number; category?: string }) =>
    api.get<Budget[]>("/api/budgets/", { params }),
  getById: (id: number) => api.get<Budget>(`/api/budgets/${id}`),
  create: (data: Partial<Budget>) =>
    api.post<Budget>("/api/budgets/", data),
  update: (id: number, data: Partial<Budget>) =>
    api.put<Budget>(`/api/budgets/${id}`, data),
  delete: (id: number) => api.delete(`/api/budgets/${id}`),
};

export const usersAPI = {
  getAll: () => api.get<TeamMember[]>("/api/users/"),
  getProfile: () => api.get<TeamMember>("/api/users/profile"),
  updateProfile: (data: Partial<TeamMember>) =>
    api.put<TeamMember>("/api/users/profile", data),
  getTeam: () => api.get<TeamMember[]>("/api/users/team"),
  getActivityLog: (limit: number = 50) =>
    api.get<ActivityLog[]>(`/api/users/activity-log?limit=${limit}`),
};

export const analyticsAPI = {
  getDashboard: () => api.get<DashboardStats>("/api/analytics/dashboard"),
  getProjectKPI: (projectId: number) =>
    api.get(`/api/analytics/project/${projectId}/kpi`),
  getBudgetBreakdown: (projectId: number) =>
    api.get(`/api/analytics/project/${projectId}/budget-breakdown`),
  getResourceDistribution: (projectId: number) =>
    api.get(`/api/analytics/project/${projectId}/resource-distribution`),
  getTimeline: (projectId: number) =>
    api.get(`/api/analytics/project/${projectId}/timeline`),
  predictCompletion: (projectId: number) =>
    api.get(`/api/analytics/project/${projectId}/predict-completion`),
  getTeamPerformance: (projectId?: number) =>
    api.get<{ team_members: number; performance: TeamPerformance[] }>(
      `/api/analytics/team-performance${projectId ? `?project_id=${projectId}` : ""}`
    ),
};

export const importAPI = {
  uploadExcel: (file: File) => {
    const formData = new FormData();
    formData.append("file", file);
    return api.post("/api/import/excel", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
  },
  uploadCSV: (file: File) => {
    const formData = new FormData();
    formData.append("file", file);
    return api.post("/api/import/csv", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
  },
};

export const authAPI = {
  login: (credentials: { username: string; password: string }) =>
    api.post("/api/auth/login", credentials),
  getCurrentUser: (token: string) =>
    api.get("/api/auth/me", {
      headers: { Authorization: `Bearer ${token}` },
    }),
  getDemoUsers: () => api.get("/api/auth/demo-users"),
};



export default api;
```

# File: ./frontend/src/types/auth.tsx

```typescript
export interface User {
  username: string;
  name: string;
  email: string;
  role: "admin" | "manager" | "worker";
  worker_name?: string;
  managed_projects?: number[];
}

export interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
}

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface DemoUser {
  username: string;
  role: string;
  name: string;
  hint: string;
}
```

# File: ./frontend/src/pages/Dashboard.tsx

```typescript
import React, { useEffect, useState } from "react";
import { analyticsAPI, DashboardStats, WorkerStats } from "../services/API";
import { useAuth } from "../contexts/AuthContext";
import AdminDashboard from "../components/dashboards/AdminDashboard";
import ManagerDashboard from "../components/dashboards/ManagerDashboard";
import WorkerDashboard from "../components/dashboards/WorkerDashboard";

const Dashboard: React.FC = () => {
  const { user } = useAuth();
  const [stats, setStats] = useState<DashboardStats | WorkerStats | null>(
    null
  );
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchDashboard();
  }, []);

  const fetchDashboard = async () => {
    try {
      setLoading(true);
      const response = await analyticsAPI.getDashboard();
      setStats(response.data);
      setError(null);
    } catch (err: any) {
      setError(err.message || "Failed to fetch dashboard data");
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-gray-500">Loading dashboard...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-400 text-red-700 px-4 py-3 rounded">
        Error: {error}
      </div>
    );
  }

  if (!stats || !user) return null;

  if (user.role === "admin") {
    return (
      <AdminDashboard
        stats={stats as DashboardStats}
        onRefresh={fetchDashboard}
      />
    );
  } else if (user.role === "manager") {
    return (
      <ManagerDashboard
        stats={stats as DashboardStats}
        onRefresh={fetchDashboard}
      />
    );
  } else {
    return (
      <WorkerDashboard
        stats={stats as WorkerStats}
        onRefresh={fetchDashboard}
      />
    );
  }
};

export default Dashboard;
```

# File: ./frontend/src/pages/Tasks.tsx

```typescript
import React, { useEffect, useState } from "react";
import { Card, CardBody } from "../components/Card";
import { Table, TableHeader, TableBody, TableHead, TableCell } from "../components/Table";
import Button from "../components/Button";
import Modal from "../components/Modal";
import Input from "../components/Input";
import Select from "../components/Select";
import TextArea from "../components/TextArea";
import { exportToCSV } from '../utils/export';
import { tasksAPI, projectsAPI, Task, Project } from "../services/API";

const Tasks: React.FC = () => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [filterProject, setFilterProject] = useState<string>("");
  const [filterStatus, setFilterStatus] = useState<string>("");

  const [formData, setFormData] = useState({
    project_id: "",
    name: "",
    description: "",
    status: "not_started",
    priority: "medium",
    start_date: "",
    planned_end_date: "",
    progress_percentage: 0,
    assigned_to: "",
  });

  useEffect(() => {
    fetchTasks();
    fetchProjects();
  }, []);

  const fetchTasks = async () => {
    try {
      setLoading(true);
      const response = await tasksAPI.getAll();
      setTasks(response.data);
      setError(null);
    } catch (err: any) {
      setError(err.message || "Failed to fetch tasks");
    } finally {
      setLoading(false);
    }
  };

  const fetchProjects = async () => {
    try {
      const response = await projectsAPI.getAll();
      setProjects(response.data);
    } catch (err) {
      console.error("Failed to fetch projects:", err);
    }
  };

  const handleInputChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const submitData: any = {
        project_id: parseInt(formData.project_id),
        name: formData.name,
        description: formData.description || undefined,
        status: formData.status,
        priority: formData.priority,
        progress_percentage: parseFloat(formData.progress_percentage.toString()),
        assigned_to: formData.assigned_to || undefined,
      };

      // Only include dates if they are filled
      if (formData.start_date) {
        submitData.start_date = new Date(formData.start_date).toISOString();
      }
      if (formData.planned_end_date) {
        submitData.planned_end_date = new Date(formData.planned_end_date).toISOString();
      }

      if (editingTask) {
        await tasksAPI.update(editingTask.id, submitData);
      } else {
        await tasksAPI.create(submitData);
      }
      setIsModalOpen(false);
      resetForm();
      fetchTasks();
    } catch (err: any) {
      const errorMsg = err.response?.data?.detail 
        ? JSON.stringify(err.response.data.detail)
        : err.message || "Failed to save task";
      alert(errorMsg);
    }
  };

  const handleDelete = async (id: number) => {
    if (window.confirm("Are you sure you want to delete this task?")) {
      try {
        await tasksAPI.delete(id);
        fetchTasks();
      } catch (err: any) {
        alert(err.message || "Failed to delete task");
      }
    }
  };

  const handleExport = () => {
    const exportData = filteredTasks.map((task) => ({
      ID: task.id,
      "Project ID": task.project_id,
      Name: task.name,
      Status: task.status,
      Priority: task.priority,
      "Assigned To": task.assigned_to || "Unassigned",
      "Start Date": task.start_date
        ? new Date(task.start_date).toLocaleDateString()
        : "N/A",
      "End Date": task.planned_end_date
        ? new Date(task.planned_end_date).toLocaleDateString()
        : "N/A",
      "Progress %": task.progress_percentage,
      Overdue: task.is_overdue ? "Yes" : "No",
    }));

    exportToCSV(exportData, "tasks");
  };

  const openEditModal = (task: Task) => {
    setEditingTask(task);
    setFormData({
      project_id: task.project_id.toString(),
      name: task.name,
      description: task.description || "",
      status: task.status,
      priority: task.priority,
      start_date: task.start_date?.split("T")[0] || "",
      planned_end_date: task.planned_end_date?.split("T")[0] || "",
      progress_percentage: task.progress_percentage,
      assigned_to: task.assigned_to || "",
    });
    setIsModalOpen(true);
  };

  const resetForm = () => {
    setFormData({
      project_id: "",
      name: "",
      description: "",
      status: "not_started",
      priority: "medium",
      start_date: "",
      planned_end_date: "",
      progress_percentage: 0,
      assigned_to: "",
    });
    setEditingTask(null);
  };

  const getStatusColor = (status: string) => {
    const colors: Record<string, string> = {
      not_started: "bg-gray-100 text-gray-800",
      in_progress: "bg-blue-100 text-blue-800",
      completed: "bg-green-100 text-green-800",
      delayed: "bg-yellow-100 text-yellow-800",
      blocked: "bg-red-100 text-red-800",
    };
    return colors[status] || "bg-gray-100 text-gray-800";
  };

  const getPriorityColor = (priority: string) => {
    const colors: Record<string, string> = {
      low: "text-gray-600",
      medium: "text-blue-600",
      high: "text-orange-600",
      critical: "text-red-600",
    };
    return colors[priority] || "text-gray-600";
  };

  const filteredTasks = tasks.filter((task) => {
    if (filterProject && task.project_id.toString() !== filterProject) return false;
    if (filterStatus && task.status !== filterStatus) return false;
    return true;
  });

  // Calculate statistics
  const totalTasks = filteredTasks.length;
  const completedTasks = filteredTasks.filter(t => t.status === "completed").length;
  const inProgressTasks = filteredTasks.filter(t => t.status === "in_progress").length;
  const overdueTasks = filteredTasks.filter(t => t.is_overdue).length;
  const completionRate = totalTasks > 0 ? (completedTasks / totalTasks * 100) : 0;

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-gray-500">Loading tasks...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-400 text-red-700 px-4 py-3 rounded">
        Error: {error}
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-900">Tasks</h1>
        <div className="flex space-x-3">
          <Button variant="secondary" onClick={handleExport}>
            📥 Export
          </Button>
          <Button onClick={() => setIsModalOpen(true)}>Add New Task</Button>
        </div>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card>
          <CardBody>
            <div className="text-sm text-gray-500">Total Tasks</div>
            <div className="text-2xl font-bold text-gray-900">{totalTasks}</div>
          </CardBody>
        </Card>
        <Card>
          <CardBody>
            <div className="text-sm text-gray-500">Completed</div>
            <div className="text-2xl font-bold text-green-600">{completedTasks}</div>
            <div className="text-xs text-gray-500 mt-1">
              {completionRate.toFixed(1)}% completion rate
            </div>
          </CardBody>
        </Card>
        <Card>
          <CardBody>
            <div className="text-sm text-gray-500">In Progress</div>
            <div className="text-2xl font-bold text-blue-600">{inProgressTasks}</div>
          </CardBody>
        </Card>
        <Card>
          <CardBody>
            <div className="text-sm text-gray-500">Overdue</div>
            <div className="text-2xl font-bold text-red-600">{overdueTasks}</div>
          </CardBody>
        </Card>
      </div>

      {/* Filters */}
      <Card>
        <CardBody>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Select
              label="Filter by Project"
              name="filterProject"
              value={filterProject}
              onChange={(e) => setFilterProject(e.target.value)}
              options={[
                { value: "", label: "All Projects" },
                ...projects.map((p) => ({ value: p.id.toString(), label: p.name })),
              ]}
            />
            <Select
              label="Filter by Status"
              name="filterStatus"
              value={filterStatus}
              onChange={(e) => setFilterStatus(e.target.value)}
              options={[
                { value: "", label: "All Statuses" },
                { value: "not_started", label: "Not Started" },
                { value: "in_progress", label: "In Progress" },
                { value: "completed", label: "Completed" },
                { value: "delayed", label: "Delayed" },
                { value: "blocked", label: "Blocked" },
              ]}
            />
            <div className="flex items-end">
              <Button
                variant="secondary"
                onClick={() => {
                  setFilterProject("");
                  setFilterStatus("");
                }}
                className="w-full"
              >
                Clear Filters
              </Button>
            </div>
          </div>
        </CardBody>
      </Card>

      {/* Tasks Table */}
      <Card>
        <Table>
          <TableHeader>
            <TableHead>Task Name</TableHead>
            <TableHead>Project</TableHead>
            <TableHead>Status</TableHead>
            <TableHead>Priority</TableHead>
            <TableHead>Progress</TableHead>
            <TableHead>Assigned To</TableHead>
            <TableHead>Due Date</TableHead>
            <TableHead>Actions</TableHead>
          </TableHeader>
          <TableBody>
            {filteredTasks.map((task) => (
              <tr key={task.id}>
                <TableCell>
                  <div className="font-medium text-gray-900">{task.name}</div>
                  {task.description && (
                    <div className="text-gray-500 text-xs mt-1 truncate max-w-xs">
                      {task.description}
                    </div>
                  )}
                </TableCell>
                <TableCell>
                  <div className="text-gray-900">
                    {projects.find((p) => p.id === task.project_id)?.name || `Project #${task.project_id}`}
                  </div>
                </TableCell>
                <TableCell>
                  <span
                    className={`px-2 py-1 text-xs font-semibold rounded-full ${getStatusColor(task.status)}`}
                  >
                    {task.status.replace("_", " ")}
                  </span>
                </TableCell>
                <TableCell>
                  <span className={`font-semibold capitalize ${getPriorityColor(task.priority)}`}>
                    {task.priority}
                  </span>
                </TableCell>
                <TableCell>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className="bg-primary-600 h-2 rounded-full"
                      style={{ width: `${task.progress_percentage}%` }}
                    ></div>
                  </div>
                  <div className="text-xs text-gray-500 mt-1">
                    {task.progress_percentage}%
                  </div>
                </TableCell>
                <TableCell>
                  {task.assigned_to || <span className="text-gray-400">Unassigned</span>}
                </TableCell>
                <TableCell>
                  {task.planned_end_date ? (
                    <div>
                      <div className="text-gray-900">
                        {new Date(task.planned_end_date).toLocaleDateString()}
                      </div>
                      {task.is_overdue && (
                        <span className="text-xs text-red-600 font-semibold">Overdue</span>
                      )}
                    </div>
                  ) : (
                    <span className="text-gray-400">No date</span>
                  )}
                </TableCell>
                <TableCell>
                  <div className="flex space-x-2">
                    <button
                      onClick={() => openEditModal(task)}
                      className="text-primary-600 hover:text-primary-900"
                    >
                      Edit
                    </button>
                    <button
                      onClick={() => handleDelete(task.id)}
                      className="text-red-600 hover:text-red-900"
                    >
                      Delete
                    </button>
                  </div>
                </TableCell>
              </tr>
            ))}
          </TableBody>
        </Table>
        {filteredTasks.length === 0 && (
          <div className="text-center py-12 text-gray-500">No tasks found</div>
        )}
      </Card>

      {/* Create/Edit Modal */}
      <Modal
        isOpen={isModalOpen}
        onClose={() => {
          setIsModalOpen(false);
          resetForm();
        }}
        title={editingTask ? "Edit Task" : "Create New Task"}
        size="lg"
      >
        <form onSubmit={handleSubmit} className="space-y-4">
          <Select
            label="Project"
            name="project_id"
            value={formData.project_id}
            onChange={handleInputChange}
            options={[
              { value: "", label: "Select a project" },
              ...projects.map((p) => ({ value: p.id.toString(), label: p.name })),
            ]}
            required
          />

          <Input
            label="Task Name"
            name="name"
            value={formData.name}
            onChange={handleInputChange}
            required
          />

          <TextArea
            label="Description"
            name="description"
            value={formData.description}
            onChange={handleInputChange}
            rows={3}
          />

          <div className="grid grid-cols-2 gap-4">
            <Select
              label="Status"
              name="status"
              value={formData.status}
              onChange={handleInputChange}
              options={[
                { value: "not_started", label: "Not Started" },
                { value: "in_progress", label: "In Progress" },
                { value: "completed", label: "Completed" },
                { value: "delayed", label: "Delayed" },
                { value: "blocked", label: "Blocked" },
              ]}
              required
            />

            <Select
              label="Priority"
              name="priority"
              value={formData.priority}
              onChange={handleInputChange}
              options={[
                { value: "low", label: "Low" },
                { value: "medium", label: "Medium" },
                { value: "high", label: "High" },
                { value: "critical", label: "Critical" },
              ]}
              required
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <Input
              label="Start Date"
              type="date"
              name="start_date"
              value={formData.start_date}
              onChange={handleInputChange}
            />

            <Input
              label="Planned End Date"
              type="date"
              name="planned_end_date"
              value={formData.planned_end_date}
              onChange={handleInputChange}
            />
          </div>

          <Input
            label="Progress (%)"
            type="number"
            name="progress_percentage"
            value={formData.progress_percentage}
            onChange={handleInputChange}
            placeholder="0-100"
          />

          <Input
            label="Assigned To"
            name="assigned_to"
            value={formData.assigned_to}
            onChange={handleInputChange}
            placeholder="Team member name"
          />

          <div className="flex justify-end space-x-3 pt-4">
            <Button
              type="button"
              variant="secondary"
              onClick={() => {
                setIsModalOpen(false);
                resetForm();
              }}
            >
              Cancel
            </Button>
            <Button type="submit">
              {editingTask ? "Update Task" : "Create Task"}
            </Button>
          </div>
        </form>
      </Modal>
    </div>
  );
};

export default Tasks;
```

# File: ./frontend/src/pages/Resources.tsx

```typescript
import React, { useEffect, useState } from "react";
import { Card, CardBody } from "../components/Card";
import { Table, TableHeader, TableBody, TableHead, TableCell } from "../components/Table";
import Button from "../components/Button";
import Modal from "../components/Modal";
import Input from "../components/Input";
import Select from "../components/Select";
import { exportToCSV } from '../utils/export';
import { resourcesAPI, projectsAPI, Resource, Project } from "../services/API";

const Resources: React.FC = () => {
  const [resources, setResources] = useState<Resource[]>([]);
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingResource, setEditingResource] = useState<Resource | null>(null);
  const [filterProject, setFilterProject] = useState<string>("");
  const [filterType, setFilterType] = useState<string>("");

  const [formData, setFormData] = useState({
    project_id: "",
    name: "",
    resource_type: "material",
    status: "available",
    quantity: 0,
    unit: "",
    unit_cost: 0,
    supplier: "",
  });

  useEffect(() => {
    fetchResources();
    fetchProjects();
  }, []);

  const fetchResources = async () => {
    try {
      setLoading(true);
      const response = await resourcesAPI.getAll();
      setResources(response.data);
      setError(null);
    } catch (err: any) {
      setError(err.message || "Failed to fetch resources");
    } finally {
      setLoading(false);
    }
  };

  const fetchProjects = async () => {
    try {
      const response = await projectsAPI.getAll();
      setProjects(response.data);
    } catch (err) {
      console.error("Failed to fetch projects:", err);
    }
  };

  const handleInputChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
  e.preventDefault();
  try {
    const submitData = {
      ...formData,
      project_id: parseInt(formData.project_id),
      quantity: parseFloat(formData.quantity.toString()),
      unit_cost: parseFloat(formData.unit_cost.toString()),
    };

    if (editingResource) {
      await resourcesAPI.update(editingResource.id, submitData);
    } else {
      await resourcesAPI.create(submitData);
    }
    setIsModalOpen(false);
    resetForm();
    fetchResources();
  } catch (err: any) {
    alert(err.message || "Failed to save resource");
  }
};

  const handleDelete = async (id: number) => {
    if (window.confirm("Are you sure you want to delete this resource?")) {
      try {
        await resourcesAPI.delete(id);
        fetchResources();
      } catch (err: any) {
        alert(err.message || "Failed to delete resource");
      }
    }
  };

  const handleExport = () => {
    const exportData = filteredResources.map((resource) => ({
      ID: resource.id,
      "Project ID": resource.project_id,
      Name: resource.name,
      Type: resource.resource_type,
      Status: resource.status,
      Quantity: resource.quantity,
      Unit: resource.unit || "N/A",
      "Unit Cost": resource.unit_cost,
      "Total Cost": resource.total_cost,
      Supplier: resource.supplier || "N/A",
      "Allocated Date": new Date(resource.allocated_date).toLocaleDateString(),
    }));

    exportToCSV(exportData, "resources");
  };

  const openEditModal = (resource: Resource) => {
    setEditingResource(resource);
    setFormData({
      project_id: resource.project_id.toString(),
      name: resource.name,
      resource_type: resource.resource_type,
      status: resource.status,
      quantity: resource.quantity,
      unit: resource.unit || "",
      unit_cost: resource.unit_cost,
      supplier: resource.supplier || "",
    });
    setIsModalOpen(true);
  };

  const resetForm = () => {
    setFormData({
      project_id: "",
      name: "",
      resource_type: "material",
      status: "available",
      quantity: 0,
      unit: "",
      unit_cost: 0,
      supplier: "",
    });
    setEditingResource(null);
  };

  const getStatusColor = (status: string) => {
    const colors: Record<string, string> = {
      available: "bg-green-100 text-green-800",
      in_use: "bg-blue-100 text-blue-800",
      depleted: "bg-red-100 text-red-800",
      maintenance: "bg-yellow-100 text-yellow-800",
    };
    return colors[status] || "bg-gray-100 text-gray-800";
  };

  const getTypeIcon = (type: string) => {
    const icons: Record<string, string> = {
      material: "🧱",
      equipment: "⚙️",
      labor: "👷",
    };
    return icons[type] || "📦";
  };

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat("en-US", {
      style: "currency",
      currency: "USD",
    }).format(amount);
  };

  const filteredResources = resources.filter((resource) => {
    if (filterProject && resource.project_id.toString() !== filterProject) return false;
    if (filterType && resource.resource_type !== filterType) return false;
    return true;
  });

  // Calculate totals
  const totalCost = filteredResources.reduce((sum, r) => sum + r.total_cost, 0);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-gray-500">Loading resources...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-400 text-red-700 px-4 py-3 rounded">
        Error: {error}
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-900">Resources</h1>
        <div className="flex space-x-3">
          <Button variant="secondary" onClick={handleExport}>
            📥 Export
          </Button>
          <Button onClick={() => setIsModalOpen(true)}>
            Add New Resource
          </Button>
        </div>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card>
          <CardBody>
            <div className="text-sm text-gray-500">Total Resources</div>
            <div className="text-2xl font-bold text-gray-900">{filteredResources.length}</div>
          </CardBody>
        </Card>
        <Card>
          <CardBody>
            <div className="text-sm text-gray-500">Total Cost</div>
            <div className="text-2xl font-bold text-gray-900">{formatCurrency(totalCost)}</div>
          </CardBody>
        </Card>
        <Card>
          <CardBody>
            <div className="text-sm text-gray-500">Available Resources</div>
            <div className="text-2xl font-bold text-gray-900">
              {filteredResources.filter((r) => r.status === "available").length}
            </div>
          </CardBody>
        </Card>
      </div>

      {/* Filters */}
      <Card>
        <CardBody>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Select
              label="Filter by Project"
              name="filterProject"
              value={filterProject}
              onChange={(e) => setFilterProject(e.target.value)}
              options={[
                { value: "", label: "All Projects" },
                ...projects.map((p) => ({ value: p.id.toString(), label: p.name })),
              ]}
            />
            <Select
              label="Filter by Type"
              name="filterType"
              value={filterType}
              onChange={(e) => setFilterType(e.target.value)}
              options={[
                { value: "", label: "All Types" },
                { value: "material", label: "Material" },
                { value: "equipment", label: "Equipment" },
                { value: "labor", label: "Labor" },
              ]}
            />
            <div className="flex items-end">
              <Button
                variant="secondary"
                onClick={() => {
                  setFilterProject("");
                  setFilterType("");
                }}
                className="w-full"
              >
                Clear Filters
              </Button>
            </div>
          </div>
        </CardBody>
      </Card>

      {/* Resources Table */}
      <Card>
        <Table>
          <TableHeader>
            <TableHead>Resource</TableHead>
            <TableHead>Project</TableHead>
            <TableHead>Type</TableHead>
            <TableHead>Status</TableHead>
            <TableHead>Quantity</TableHead>
            <TableHead>Unit Cost</TableHead>
            <TableHead>Total Cost</TableHead>
            <TableHead>Supplier</TableHead>
            <TableHead>Actions</TableHead>
          </TableHeader>
          <TableBody>
            {filteredResources.map((resource) => (
              <tr key={resource.id}>
                <TableCell>
                  <div className="flex items-center">
                    <span className="text-2xl mr-2">{getTypeIcon(resource.resource_type)}</span>
                    <div className="font-medium text-gray-900">{resource.name}</div>
                  </div>
                </TableCell>
                <TableCell>
                  {projects.find((p) => p.id === resource.project_id)?.name || `Project #${resource.project_id}`}
                </TableCell>
                <TableCell>
                  <span className="capitalize">{resource.resource_type}</span>
                </TableCell>
                <TableCell>
                  <span
                    className={`px-2 py-1 text-xs font-semibold rounded-full ${getStatusColor(resource.status)}`}
                  >
                    {resource.status.replace("_", " ")}
                  </span>
                </TableCell>
                <TableCell>
                  {resource.quantity} {resource.unit}
                </TableCell>
                <TableCell>{formatCurrency(resource.unit_cost)}</TableCell>
                <TableCell>
                  <span className="font-semibold">{formatCurrency(resource.total_cost)}</span>
                </TableCell>
                <TableCell>
                  {resource.supplier || <span className="text-gray-400">N/A</span>}
                </TableCell>
                <TableCell>
                  <div className="flex space-x-2">
                    <button
                      onClick={() => openEditModal(resource)}
                      className="text-primary-600 hover:text-primary-900"
                    >
                      Edit
                    </button>
                    <button
                      onClick={() => handleDelete(resource.id)}
                      className="text-red-600 hover:text-red-900"
                    >
                      Delete
                    </button>
                  </div>
                </TableCell>
              </tr>
            ))}
          </TableBody>
        </Table>
        {filteredResources.length === 0 && (
          <div className="text-center py-12 text-gray-500">No resources found</div>
        )}
      </Card>

      {/* Create/Edit Modal */}
      <Modal
        isOpen={isModalOpen}
        onClose={() => {
          setIsModalOpen(false);
          resetForm();
        }}
        title={editingResource ? "Edit Resource" : "Add New Resource"}
        size="lg"
      >
        <form onSubmit={handleSubmit} className="space-y-4">
          <Select
            label="Project"
            name="project_id"
            value={formData.project_id}
            onChange={handleInputChange}
            options={[
              { value: "", label: "Select a project" },
              ...projects.map((p) => ({ value: p.id.toString(), label: p.name })),
            ]}
            required
          />

          <Input
            label="Resource Name"
            name="name"
            value={formData.name}
            onChange={handleInputChange}
            required
          />

          <div className="grid grid-cols-2 gap-4">
            <Select
              label="Type"
              name="resource_type"
              value={formData.resource_type}
              onChange={handleInputChange}
              options={[
                { value: "material", label: "Material" },
                { value: "equipment", label: "Equipment" },
                { value: "labor", label: "Labor" },
              ]}
              required
            />

            <Select
              label="Status"
              name="status"
              value={formData.status}
              onChange={handleInputChange}
              options={[
                { value: "available", label: "Available" },
                { value: "in_use", label: "In Use" },
                { value: "depleted", label: "Depleted" },
                { value: "maintenance", label: "Maintenance" },
              ]}
              required
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <Input
              label="Quantity"
              type="number"
              name="quantity"
              value={formData.quantity}
              onChange={handleInputChange}
              required
            />

            <Input
              label="Unit"
              name="unit"
              value={formData.unit}
              onChange={handleInputChange}
              placeholder="kg, m³, hours, etc."
            />
          </div>

          <Input
            label="Unit Cost"
            type="number"
            name="unit_cost"
            value={formData.unit_cost}
            onChange={handleInputChange}
            placeholder="0.00"
            required
          />

          <Input
            label="Supplier"
            name="supplier"
            value={formData.supplier}
            onChange={handleInputChange}
            placeholder="Supplier name"
          />

          <div className="bg-gray-50 px-4 py-3 rounded">
            <div className="text-sm text-gray-600">
              Total Cost:{" "}
              <span className="font-semibold text-gray-900">
                {formatCurrency(Number(formData.quantity) * Number(formData.unit_cost))}
              </span>
            </div>
          </div>

          <div className="flex justify-end space-x-3 pt-4">
            <Button
              type="button"
              variant="secondary"
              onClick={() => {
                setIsModalOpen(false);
                resetForm();
              }}
            >
              Cancel
            </Button>
            <Button type="submit">
              {editingResource ? "Update Resource" : "Add Resource"}
            </Button>
          </div>
        </form>
      </Modal>
    </div>
  );
};

export default Resources;
```

# File: ./frontend/src/pages/Profile.tsx

```typescript
import React, { useState, useEffect } from "react";
import { Card, CardHeader, CardBody } from "../components/Card";
import Input from "../components/Input";
import Button from "../components/Button";
import { useAuth } from "../contexts/AuthContext";
import { usersAPI } from "../services/API";

const Profile: React.FC = () => {
  const { user } = useAuth();
  const [formData, setFormData] = useState({
    name: "",
    email: "",
  });
  const [isEditing, setIsEditing] = useState(false);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState<{
    type: "success" | "error";
    text: string;
  } | null>(null);

  useEffect(() => {
    if (user) {
      setFormData({
        name: user.name,
        email: user.email,
      });
    }
  }, [user]);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setMessage(null);

    try {
      await usersAPI.updateProfile(formData);
      setMessage({
        type: "success",
        text: "Profile updated successfully! Please log in again to see changes.",
      });
      setIsEditing(false);
    } catch (err: any) {
      setMessage({
        type: "error",
        text: err.message || "Failed to update profile",
      });
    } finally {
      setLoading(false);
    }
  };

  if (!user) return null;

  const getRoleBadgeColor = (role: string) => {
    switch (role) {
      case "admin":
        return "bg-red-100 text-red-800";
      case "manager":
        return "bg-blue-100 text-blue-800";
      case "worker":
        return "bg-green-100 text-green-800";
      default:
        return "bg-gray-100 text-gray-800";
    }
  };

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">My Profile</h1>
        <p className="text-gray-600 mt-1">Manage your account information</p>
      </div>

      {message && (
        <div
          className={`px-4 py-3 rounded ${
            message.type === "success"
              ? "bg-green-50 border border-green-400 text-green-700"
              : "bg-red-50 border border-red-400 text-red-700"
          }`}
        >
          {message.text}
        </div>
      )}

      {/* Profile Overview */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <h3 className="text-lg font-medium leading-6 text-gray-900">
              Profile Information
            </h3>
            {!isEditing && (
              <Button onClick={() => setIsEditing(true)} size="sm">
                Edit Profile
              </Button>
            )}
          </div>
        </CardHeader>
        <CardBody>
          <div className="flex items-center mb-6">
            <div className="h-20 w-20 rounded-full bg-primary-100 flex items-center justify-center text-primary-600 font-bold text-3xl">
              {user.name.charAt(0)}
            </div>
            <div className="ml-6">
              <h2 className="text-2xl font-bold text-gray-900">{user.name}</h2>
              <span
                className={`mt-1 inline-block px-3 py-1 text-sm font-semibold rounded-full ${getRoleBadgeColor(user.role)}`}
              >
                {user.role.charAt(0).toUpperCase() + user.role.slice(1)}
              </span>
            </div>
          </div>

          {isEditing ? (
            <form onSubmit={handleSubmit} className="space-y-4">
              <Input
                label="Name"
                name="name"
                value={formData.name}
                onChange={handleInputChange}
                required
              />
              <Input
                label="Email"
                type="email"
                name="email"
                value={formData.email}
                onChange={handleInputChange}
                required
              />

              <div className="flex justify-end space-x-3 pt-4">
                <Button
                  type="button"
                  variant="secondary"
                  onClick={() => {
                    setIsEditing(false);
                    setFormData({
                      name: user.name,
                      email: user.email,
                    });
                  }}
                >
                  Cancel
                </Button>
                <Button type="submit" disabled={loading}>
                  {loading ? "Saving..." : "Save Changes"}
                </Button>
              </div>
            </form>
          ) : (
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700">
                  Username
                </label>
                <p className="mt-1 text-gray-900">{user.username}</p>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">
                  Email
                </label>
                <p className="mt-1 text-gray-900">{user.email}</p>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">
                  Role
                </label>
                <p className="mt-1 text-gray-900 capitalize">{user.role}</p>
              </div>
              {user.worker_name && (
                <div>
                  <label className="block text-sm font-medium text-gray-700">
                    Worker Name
                  </label>
                  <p className="mt-1 text-gray-900">{user.worker_name}</p>
                </div>
              )}
              {user.managed_projects && user.managed_projects.length > 0 && (
                <div>
                  <label className="block text-sm font-medium text-gray-700">
                    Managed Projects
                  </label>
                  <p className="mt-1 text-gray-900">
                    {user.managed_projects.length} project(s)
                  </p>
                </div>
              )}
            </div>
          )}
        </CardBody>
      </Card>

      {/* Account Information */}
      <Card>
        <CardHeader>
          <h3 className="text-lg font-medium leading-6 text-gray-900">
            Account Details
          </h3>
        </CardHeader>
        <CardBody>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="bg-gray-50 p-4 rounded-lg">
              <div className="text-sm text-gray-600">Account Type</div>
              <div className="text-lg font-semibold text-gray-900 mt-1">
                {user.role === "admin"
                  ? "Administrator"
                  : user.role === "manager"
                  ? "Project Manager"
                  : "Worker"}
              </div>
            </div>
            <div className="bg-gray-50 p-4 rounded-lg">
              <div className="text-sm text-gray-600">Access Level</div>
              <div className="text-lg font-semibold text-gray-900 mt-1">
                {user.role === "admin"
                  ? "Full Access"
                  : user.role === "manager"
                  ? "Project Management"
                  : "Task Execution"}
              </div>
            </div>
          </div>
        </CardBody>
      </Card>

      {/* Permissions */}
      <Card>
        <CardHeader>
          <h3 className="text-lg font-medium leading-6 text-gray-900">
            Permissions & Access
          </h3>
        </CardHeader>
        <CardBody>
          <div className="space-y-3">
            {user.role === "admin" && (
              <>
                <PermissionItem
                  icon="✅"
                  text="Full system administration"
                  granted
                />
                <PermissionItem
                  icon="✅"
                  text="User management"
                  granted
                />
                <PermissionItem
                  icon="✅"
                  text="All projects access"
                  granted
                />
                <PermissionItem
                  icon="✅"
                  text="Budget and financial data"
                  granted
                />
                <PermissionItem
                  icon="✅"
                  text="Data import/export"
                  granted
                />
              </>
            )}
            {user.role === "manager" && (
              <>
                <PermissionItem
                  icon="✅"
                  text="Manage assigned projects"
                  granted
                />
                <PermissionItem
                  icon="✅"
                  text="Create and assign tasks"
                  granted
                />
                <PermissionItem
                  icon="✅"
                  text="View team performance"
                  granted
                />
                <PermissionItem
                  icon="✅"
                  text="Budget tracking"
                  granted
                />
                <PermissionItem
                  icon="❌"
                  text="System administration"
                  granted={false}
                />
              </>
            )}
            {user.role === "worker" && (
              <>
                <PermissionItem
                  icon="✅"
                  text="View assigned tasks"
                  granted
                />
                <PermissionItem
                  icon="✅"
                  text="Update task progress"
                  granted
                />
                <PermissionItem
                  icon="❌"
                  text="Project management"
                  granted={false}
                />
                <PermissionItem
                  icon="❌"
                  text="Budget information"
                  granted={false}
                />
                <PermissionItem
                  icon="❌"
                  text="Resource management"
                  granted={false}
                />
              </>
            )}
          </div>
        </CardBody>
      </Card>
    </div>
  );
};

interface PermissionItemProps {
  icon: string;
  text: string;
  granted: boolean;
}

const PermissionItem: React.FC<PermissionItemProps> = ({
  icon,
  text,
  granted,
}) => (
  <div className="flex items-center">
    <span className="text-xl mr-3">{icon}</span>
    <span className={granted ? "text-gray-900" : "text-gray-400"}>
      {text}
    </span>
  </div>
);

export default Profile;
```

# File: ./frontend/src/pages/Login.tsx

```typescript
import React, { useState, useEffect } from "react";
import { useAuth } from "../contexts/AuthContext";
import { authAPI } from "../services/API";
import { DemoUser } from "../types/auth";
import Button from "../components/Button";
import Input from "../components/Input";

const Login: React.FC = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [demoUsers, setDemoUsers] = useState<DemoUser[]>([]);
  const { login } = useAuth();

  useEffect(() => {
    fetchDemoUsers();
  }, []);

  const fetchDemoUsers = async () => {
    try {
      const response = await authAPI.getDemoUsers();
      setDemoUsers(response.data);
    } catch (err) {
      console.error("Failed to fetch demo users:", err);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      await login({ username, password });
    } catch (err: any) {
      setError(err.message || "Login failed");
    } finally {
      setLoading(false);
    }
  };

  const quickLogin = (user: DemoUser) => {
    setUsername(user.username);
    // Extract password from hint (e.g., "Password: admin123")
    const passwordMatch = user.hint.match(/Password: (\w+)/);
    if (passwordMatch) {
      setPassword(passwordMatch[1]);
    }
  };

  const getRoleBadgeColor = (role: string) => {
    switch (role) {
      case "admin":
        return "bg-red-100 text-red-800";
      case "manager":
        return "bg-blue-100 text-blue-800";
      case "worker":
        return "bg-green-100 text-green-800";
      default:
        return "bg-gray-100 text-gray-800";
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 to-primary-100 flex items-center justify-center px-4">
      <div className="max-w-6xl w-full grid md:grid-cols-2 gap-8">
        {/* Login Form */}
        <div className="bg-white rounded-lg shadow-xl p-8">
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">
              BuildFlow ERP
            </h1>
            <p className="text-gray-600">
              Construction Project Management System
            </p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            <Input
              label="Username"
              name="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Enter username"
              required
            />

            <Input
              label="Password"
              type="password"
              name="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter password"
              required
            />

            {error && (
              <div className="bg-red-50 border border-red-400 text-red-700 px-4 py-3 rounded">
                {error}
              </div>
            )}

            <Button
              type="submit"
              className="w-full"
              disabled={loading}
            >
              {loading ? "Logging in..." : "Login"}
            </Button>
          </form>

          <div className="mt-6 text-center text-sm text-gray-600">
            <p>Demo accounts available →</p>
          </div>
        </div>

        {/* Demo Users Panel */}
        <div className="bg-white rounded-lg shadow-xl p-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">
            Demo Accounts
          </h2>
          <p className="text-gray-600 mb-6">
            Click any account to quick-fill the login form
          </p>

          <div className="space-y-3">
            {demoUsers.map((user) => (
              <button
                key={user.username}
                onClick={() => quickLogin(user)}
                className="w-full text-left p-4 border-2 border-gray-200 rounded-lg hover:border-primary-500 hover:bg-primary-50 transition-colors"
              >
                <div className="flex items-center justify-between mb-2">
                  <span className="font-semibold text-gray-900">
                    {user.name}
                  </span>
                  <span
                    className={`px-2 py-1 text-xs font-semibold rounded-full ${getRoleBadgeColor(user.role)}`}
                  >
                    {user.role}
                  </span>
                </div>
                <div className="text-sm text-gray-600">
                  <div>Username: {user.username}</div>
                  <div className="text-xs text-gray-500 mt-1">
                    {user.hint}
                  </div>
                </div>
              </button>
            ))}
          </div>

          <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
            <h3 className="font-semibold text-blue-900 mb-2">
              Role Descriptions:
            </h3>
            <ul className="text-sm text-blue-800 space-y-1">
              <li>
                <strong>Admin:</strong> Full system access
              </li>
              <li>
                <strong>Manager:</strong> Manage assigned projects
              </li>
              <li>
                <strong>Worker:</strong> View and update own tasks
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;
```

# File: ./frontend/src/pages/TeamPerformance.tsx

```typescript
import React, { useEffect, useState, useCallback } from "react";
import { Card, CardHeader, CardBody } from "../components/Card";
import {
  Table,
  TableHeader,
  TableBody,
  TableHead,
  TableCell,
} from "../components/Table";
import Select from "../components/Select";
import {
  analyticsAPI,
  projectsAPI,
  Project,
  TeamPerformance,
} from "../services/API";

const TeamPerformancePage: React.FC = () => {
  const [performance, setPerformance] = useState<TeamPerformance[]>([]);
  const [projects, setProjects] = useState<Project[]>([]);
  const [selectedProject, setSelectedProject] = useState<string>("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchProjects = async () => {
    try {
      const response = await projectsAPI.getAll();
      setProjects(response.data);
    } catch (err) {
      console.error("Failed to fetch projects:", err);
    }
  };

    const fetchPerformance = useCallback(async () => {
    try {
      setLoading(true);
      const projectId = selectedProject ? parseInt(selectedProject) : undefined;
      const response = await analyticsAPI.getTeamPerformance(projectId);
      setPerformance(response.data.performance);
      setError(null);
    } catch (err: any) {
      setError(err.message || "Failed to fetch team performance");
    } finally {
      setLoading(false);
    }
  }, [selectedProject]);

  useEffect(() => {
    fetchProjects();
  }, []);

  useEffect(() => {
    fetchPerformance();
  }, [fetchPerformance]);

  const getPerformanceColor = (rate: number) => {
    if (rate >= 80) return "text-green-600";
    if (rate >= 60) return "text-yellow-600";
    return "text-red-600";
  };

  const getPerformanceBadge = (rate: number) => {
    if (rate >= 80) return { label: "Excellent", color: "bg-green-100 text-green-800" };
    if (rate >= 60) return { label: "Good", color: "bg-yellow-100 text-yellow-800" };
    if (rate >= 40) return { label: "Fair", color: "bg-orange-100 text-orange-800" };
    return { label: "Needs Improvement", color: "bg-red-100 text-red-800" };
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-gray-500">Loading team performance...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-400 text-red-700 px-4 py-3 rounded">
        Error: {error}
      </div>
    );
  }

  // Calculate overall stats
  const totalTasks = performance.reduce((sum, p) => sum + p.total_tasks, 0);
  const totalCompleted = performance.reduce(
    (sum, p) => sum + p.completed_tasks,
    0
  );
  const avgCompletion =
    performance.length > 0
      ? performance.reduce((sum, p) => sum + p.completion_rate, 0) /
        performance.length
      : 0;

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">
            Team Performance
          </h1>
          <p className="text-gray-600 mt-1">
            Track team member productivity and task completion
          </p>
        </div>
        <button
          onClick={fetchPerformance}
          className="px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700"
        >
          Refresh
        </button>
      </div>

      {/* Filter */}
      <Card>
        <CardBody>
          <Select
            label="Filter by Project"
            name="selectedProject"
            value={selectedProject}
            onChange={(e) => setSelectedProject(e.target.value)}
            options={[
              { value: "", label: "All Projects" },
              ...projects.map((p) => ({
                value: p.id.toString(),
                label: p.name,
              })),
            ]}
          />
        </CardBody>
      </Card>

      {/* Summary Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card>
          <CardBody>
            <div className="text-sm text-gray-500">Team Members</div>
            <div className="text-2xl font-bold text-gray-900">
              {performance.length}
            </div>
          </CardBody>
        </Card>
        <Card>
          <CardBody>
            <div className="text-sm text-gray-500">Total Tasks</div>
            <div className="text-2xl font-bold text-gray-900">{totalTasks}</div>
          </CardBody>
        </Card>
        <Card>
          <CardBody>
            <div className="text-sm text-gray-500">Completed</div>
            <div className="text-2xl font-bold text-green-600">
              {totalCompleted}
            </div>
          </CardBody>
        </Card>
        <Card>
          <CardBody>
            <div className="text-sm text-gray-500">Avg. Completion Rate</div>
            <div className={`text-2xl font-bold ${getPerformanceColor(avgCompletion)}`}>
              {avgCompletion.toFixed(1)}%
            </div>
          </CardBody>
        </Card>
      </div>

      {/* Performance Table */}
      <Card>
        <Table>
          <TableHeader>
            <TableHead>Worker</TableHead>
            <TableHead>Total Tasks</TableHead>
            <TableHead>Completed</TableHead>
            <TableHead>Avg. Progress</TableHead>
            <TableHead>Completion Rate</TableHead>
            <TableHead>Performance</TableHead>
          </TableHeader>
          <TableBody>
            {performance.length > 0 ? (
              performance.map((member) => {
                const badge = getPerformanceBadge(member.completion_rate);
                return (
                  <tr key={member.worker_name}>
                    <TableCell>
                      <div className="flex items-center">
                        <div className="h-10 w-10 rounded-full bg-primary-100 flex items-center justify-center text-primary-600 font-bold mr-3">
                          {member.worker_name.charAt(0)}
                        </div>
                        <div className="font-medium text-gray-900">
                          {member.worker_name}
                        </div>
                      </div>
                    </TableCell>
                    <TableCell>
                      <span className="font-semibold">{member.total_tasks}</span>
                    </TableCell>
                    <TableCell>
                      <span className="font-semibold text-green-600">
                        {member.completed_tasks}
                      </span>
                    </TableCell>
                    <TableCell>
                      <div className="flex items-center">
                        <div className="w-24 bg-gray-200 rounded-full h-2 mr-2">
                          <div
                            className="bg-blue-600 h-2 rounded-full"
                            style={{ width: `${member.avg_progress}%` }}
                          ></div>
                        </div>
                        <span className="text-sm font-semibold">
                          {member.avg_progress.toFixed(0)}%
                        </span>
                      </div>
                    </TableCell>
                    <TableCell>
                      <div className="flex items-center">
                        <div className="w-24 bg-gray-200 rounded-full h-2 mr-2">
                          <div
                            className={`h-2 rounded-full ${
                              member.completion_rate >= 80
                                ? "bg-green-500"
                                : member.completion_rate >= 60
                                ? "bg-yellow-500"
                                : "bg-red-500"
                            }`}
                            style={{ width: `${member.completion_rate}%` }}
                          ></div>
                        </div>
                        <span
                          className={`text-sm font-semibold ${getPerformanceColor(member.completion_rate)}`}
                        >
                          {member.completion_rate.toFixed(0)}%
                        </span>
                      </div>
                    </TableCell>
                    <TableCell>
                      <span
                        className={`px-2 py-1 text-xs font-semibold rounded-full ${badge.color}`}
                      >
                        {badge.label}
                      </span>
                    </TableCell>
                  </tr>
                );
              })
            ) : (
              <tr>
                <TableCell colSpan={6}>
                  <div className="text-center py-8 text-gray-500">
                    No performance data available
                  </div>
                </TableCell>
              </tr>
            )}
          </TableBody>
        </Table>
      </Card>

      {/* Performance Insights */}
      {performance.length > 0 && (
        <div className="grid grid-cols-1 gap-5 lg:grid-cols-3">
          <Card>
            <CardHeader>
              <h3 className="text-lg font-medium leading-6 text-gray-900">
                Top Performers
              </h3>
            </CardHeader>
            <CardBody>
              <div className="space-y-3">
                {[...performance]
                  .sort((a, b) => b.completion_rate - a.completion_rate)
                  .slice(0, 3)
                  .map((member, index) => (
                    <div
                      key={member.worker_name}
                      className="flex items-center justify-between"
                    >
                      <div className="flex items-center">
                        <span className="text-2xl mr-2">
                          {index === 0 ? "🥇" : index === 1 ? "🥈" : "🥉"}
                        </span>
                        <span className="text-sm font-medium">
                          {member.worker_name}
                        </span>
                      </div>
                      <span className="text-sm font-semibold text-green-600">
                        {member.completion_rate.toFixed(0)}%
                      </span>
                    </div>
                  ))}
              </div>
            </CardBody>
          </Card>

          <Card>
            <CardHeader>
              <h3 className="text-lg font-medium leading-6 text-gray-900">
                Most Active
              </h3>
            </CardHeader>
            <CardBody>
              <div className="space-y-3">
                {[...performance]
                  .sort((a, b) => b.total_tasks - a.total_tasks)
                  .slice(0, 3)
                  .map((member) => (
                    <div
                      key={member.worker_name}
                      className="flex items-center justify-between"
                    >
                      <span className="text-sm font-medium">
                        {member.worker_name}
                      </span>
                      <span className="text-sm font-semibold text-blue-600">
                        {member.total_tasks} tasks
                      </span>
                    </div>
                  ))}
              </div>
            </CardBody>
          </Card>

          <Card>
            <CardHeader>
              <h3 className="text-lg font-medium leading-6 text-gray-900">
                Needs Support
              </h3>
            </CardHeader>
            <CardBody>
              <div className="space-y-3">
                {[...performance]
                  .filter((p) => p.completion_rate < 60)
                  .sort((a, b) => a.completion_rate - b.completion_rate)
                  .slice(0, 3)
                  .map((member) => (
                    <div
                      key={member.worker_name}
                      className="flex items-center justify-between"
                    >
                      <span className="text-sm font-medium">
                        {member.worker_name}
                      </span>
                      <span className="text-sm font-semibold text-red-600">
                        {member.completion_rate.toFixed(0)}%
                      </span>
                    </div>
                  ))}
                {performance.filter((p) => p.completion_rate < 60).length ===
                  0 && (
                  <div className="text-center text-sm text-gray-500">
                    All team members performing well! 🎉
                  </div>
                )}
              </div>
            </CardBody>
          </Card>
        </div>
      )}
    </div>
  );
};

export default TeamPerformancePage;
```

# File: ./frontend/src/pages/Import.tsx

```typescript
import React, { useState } from "react";
import { Card, CardHeader, CardBody } from "../components/Card";
import Button from "../components/Button";
import { importAPI } from "../services/API";

const Import: React.FC = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setSelectedFile(e.target.files[0]);
      setResult(null);
      setError(null);
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setError("Please select a file first");
      return;
    }

    setUploading(true);
    setError(null);
    setResult(null);

    try {
      let response;
      if (
        selectedFile.name.endsWith(".xlsx") ||
        selectedFile.name.endsWith(".xls")
      ) {
        response = await importAPI.uploadExcel(selectedFile);
      } else if (selectedFile.name.endsWith(".csv")) {
        response = await importAPI.uploadCSV(selectedFile);
      } else {
        throw new Error(
          "Invalid file type. Please upload .xlsx, .xls, or .csv files"
        );
      }

      setResult(response.data);
      setSelectedFile(null);
      // Reset file input
      const fileInput = document.getElementById(
        "file-upload"
      ) as HTMLInputElement;
      if (fileInput) fileInput.value = "";
    } catch (err: any) {
      setError(
        err.response?.data?.detail ||
          err.message ||
          "Failed to upload file"
      );
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-900">Import Data</h1>
      </div>

      <Card>
        <CardHeader>
          <h3 className="text-lg font-medium leading-6 text-gray-900">
            Upload Excel or CSV File
          </h3>
        </CardHeader>
        <CardBody className="space-y-4">
          <p className="text-sm text-gray-600">
            Import projects(always first), tasks, resources, and budget data from Excel or
            CSV files. The file should contain sheets/columns matching the
            required format.
          </p>

          <div className="border-2 border-dashed border-gray-300 rounded-lg p-6">
            <div className="text-center">
              <svg
                className="mx-auto h-12 w-12 text-gray-400"
                stroke="currentColor"
                fill="none"
                viewBox="0 0 48 48"
              >
                <path
                  d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02"
                  strokeWidth={2}
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
              </svg>
              <div className="mt-4">
                <label
                  htmlFor="file-upload"
                  className="cursor-pointer bg-white rounded-md font-medium text-primary-600 hover:text-primary-500 focus-within:outline-none focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-primary-500"
                >
                  <span>Upload a file</span>
                  <input
                    id="file-upload"
                    name="file-upload"
                    type="file"
                    className="sr-only"
                    accept=".xlsx,.xls,.csv"
                    onChange={handleFileChange}
                  />
                </label>
                <p className="pl-1 text-sm text-gray-600">
                  or drag and drop
                </p>
              </div>
              <p className="text-xs text-gray-500 mt-2">
                XLSX, XLS, or CSV up to 10MB
              </p>
            </div>
          </div>

          {selectedFile && (
            <div className="flex items-center justify-between bg-gray-50 p-4 rounded-md">
              <div className="flex items-center">
                <svg
                  className="h-5 w-5 text-gray-400 mr-2"
                  fill="currentColor"
                  viewBox="0 0 20 20"
                >
                  <path
                    fillRule="evenodd"
                    d="M8 4a3 3 0 00-3 3v4a5 5 0 0010 0V7a1 1 0 112 0v4a7 7 0 11-14 0V7a5 5 0 0110 0v4a3 3 0 11-6 0V7a1 1 0 012 0v4a1 1 0 102 0V7a3 3 0 00-3-3z"
                    clipRule="evenodd"
                  />
                </svg>
                <span className="text-sm text-gray-900">
                  {selectedFile.name}
                </span>
                <span className="ml-2 text-xs text-gray-500">
                  ({(selectedFile.size / 1024).toFixed(2)} KB)
                </span>
              </div>
              <Button
                variant="secondary"
                size="sm"
                onClick={() => {
                  setSelectedFile(null);
                  const fileInput = document.getElementById(
                    "file-upload"
                  ) as HTMLInputElement;
                  if (fileInput) fileInput.value = "";
                }}
              >
                Remove
              </Button>
            </div>
          )}

          <div className="flex justify-end">
            <Button
              onClick={handleUpload}
              disabled={!selectedFile || uploading}
            >
              {uploading ? "Uploading..." : "Upload and Import"}
            </Button>
          </div>

          {error && (
            <div className="bg-red-50 border border-red-400 text-red-700 px-4 py-3 rounded">
              {error}
            </div>
          )}

          {result && (
            <div className="bg-green-50 border border-green-400 text-green-700 px-4 py-3 rounded">
              <h4 className="font-semibold mb-2">Import Successful!</h4>
              <div className="text-sm space-y-1">
                {result.stats?.projects !== undefined && (
                  <p>Projects imported: {result.stats.projects}</p>
                )}
                {result.stats?.tasks !== undefined && (
                  <p>Tasks imported: {result.stats.tasks}</p>
                )}
                {result.stats?.resources !== undefined && (
                  <p>Resources imported: {result.stats.resources}</p>
                )}
                {result.stats?.budgets !== undefined && (
                  <p>Budgets imported: {result.stats.budgets}</p>
                )}
              </div>
            </div>
          )}
        </CardBody>
      </Card>

      <Card>
        <CardHeader>
          <h3 className="text-lg font-medium leading-6 text-gray-900">
            Import Format Guide
          </h3>
        </CardHeader>
        <CardBody>
          <div className="space-y-4">
            <div>
              <h4 className="font-semibold text-gray-900 mb-2">
                Excel Format (Multi-sheet)
              </h4>
              <p className="text-sm text-gray-600 mb-2">
                Create separate sheets for each data type:
              </p>
              <ul className="list-disc list-inside text-sm text-gray-600 space-y-1">
              <li>
                <strong>Projects:</strong> name (or project_name), description, status,
                start_date, end_date, total_budget, spent_amount, location
              </li>
              <li>
                <strong>Tasks:</strong> project_id OR project_name, name (or task_name), description,
                status, priority, start_date, end_date, progress,
                assigned_to
              </li>
              <li>
                <strong>Resources:</strong> project_id OR project_name, name (or resource_name),
                resource_type, status, quantity, unit, unit_cost, supplier
              </li>
              <li>
                <strong>Budgets:</strong> project_id OR project_name, category,
                description, planned_amount, actual_amount
              </li>
            </ul>
            </div>

            <div>
              <h4 className="font-semibold text-gray-900 mb-2">
                CSV Format (Single entity type)
              </h4>
              <p className="text-sm text-gray-600">
                CSV files should contain columns matching one of the formats
                above. The system will auto-detect the entity type based on
                the columns.
              </p>
            </div>
          </div>
        </CardBody>
      </Card>
    </div>
  );
};

export default Import;
```

# File: ./frontend/src/pages/Budgets.tsx

```typescript
import React, { useEffect, useState } from "react";
import { Card, CardBody } from "../components/Card";
import {
  Table,
  TableHeader,
  TableBody,
  TableHead,
  TableCell,
} from "../components/Table";
import Button from "../components/Button";
import Modal from "../components/Modal";
import Input from "../components/Input";
import Select from "../components/Select";
import TextArea from "../components/TextArea";
import { exportToCSV } from '../utils/export';
import { budgetsAPI, projectsAPI, Budget, Project } from "../services/API";

const Budgets: React.FC = () => {
  const [budgets, setBudgets] = useState<Budget[]>([]);
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingBudget, setEditingBudget] = useState<Budget | null>(null);
  const [filterProject, setFilterProject] = useState<string>("");

  const [formData, setFormData] = useState({
    project_id: "",
    category: "",
    description: "",
    planned_amount: 0,
    actual_amount: 0,
  });

  useEffect(() => {
    fetchBudgets();
    fetchProjects();
  }, []);

  const fetchBudgets = async () => {
    try {
      setLoading(true);
      const response = await budgetsAPI.getAll();
      setBudgets(response.data);
      setError(null);
    } catch (err: any) {
      setError(err.message || "Failed to fetch budgets");
    } finally {
      setLoading(false);
    }
  };

  const fetchProjects = async () => {
    try {
      const response = await projectsAPI.getAll();
      setProjects(response.data);
    } catch (err) {
      console.error("Failed to fetch projects:", err);
    }
  };

  const handleInputChange = (
    e: React.ChangeEvent<
      HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement
    >
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const submitData = {
        ...formData,
        project_id: parseInt(formData.project_id),
        planned_amount: parseFloat(formData.planned_amount.toString()),
        actual_amount: parseFloat(formData.actual_amount.toString()),
      };

      if (editingBudget) {
        await budgetsAPI.update(editingBudget.id, submitData);
      } else {
        await budgetsAPI.create(submitData);
      }
      setIsModalOpen(false);
      resetForm();
      fetchBudgets();
    } catch (err: any) {
      alert(err.message || "Failed to save budget");
    }
  };

  const handleDelete = async (id: number) => {
    if (
      window.confirm("Are you sure you want to delete this budget entry?")
    ) {
      try {
        await budgetsAPI.delete(id);
        fetchBudgets();
      } catch (err: any) {
        alert(err.message || "Failed to delete budget");
      }
    }
  };

  const openEditModal = (budget: Budget) => {
    setEditingBudget(budget);
    setFormData({
      project_id: budget.project_id.toString(),
      category: budget.category,
      description: budget.description || "",
      planned_amount: budget.planned_amount,
      actual_amount: budget.actual_amount,
    });
    setIsModalOpen(true);
  };

  const handleExport = () => {
    const exportData = filteredBudgets.map((budget) => ({
      ID: budget.id,
      "Project ID": budget.project_id,
      Category: budget.category,
      Description: budget.description || "N/A",
      "Planned Amount": budget.planned_amount,
      "Actual Amount": budget.actual_amount,
      Variance: budget.variance,
      "Variance %": budget.variance_percentage.toFixed(2),
      Date: new Date(budget.budget_date).toLocaleDateString(),
    }));

    exportToCSV(exportData, "budgets");
  };

  const resetForm = () => {
    setFormData({
      project_id: "",
      category: "",
      description: "",
      planned_amount: 0,
      actual_amount: 0,
    });
    setEditingBudget(null);
  };

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat("en-US", {
      style: "currency",
      currency: "USD",
    }).format(amount);
  };

  const getVarianceColor = (variance: number) => {
    if (variance > 0) return "text-green-600";
    if (variance < 0) return "text-red-600";
    return "text-gray-600";
  };

  const filteredBudgets = budgets.filter((budget) => {
    if (filterProject && budget.project_id.toString() !== filterProject)
      return false;
    return true;
  });

  // Calculate totals
  const totalPlanned = filteredBudgets.reduce(
    (sum, b) => sum + b.planned_amount,
    0
  );
  const totalActual = filteredBudgets.reduce(
    (sum, b) => sum + b.actual_amount,
    0
  );
  const totalVariance = totalPlanned - totalActual;
  const variancePercentage =
    totalPlanned > 0 ? (totalVariance / totalPlanned) * 100 : 0;

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-gray-500">Loading budgets...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-400 text-red-700 px-4 py-3 rounded">
        Error: {error}
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-900">Budgets</h1>
        <div className="flex space-x-3">
          <Button variant="secondary" onClick={handleExport}>
            📥 Export
          </Button>
          <Button onClick={() => setIsModalOpen(true)}>
            Add Budget Entry
          </Button>
        </div>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card>
          <CardBody>
            <div className="text-sm text-gray-500">Total Planned</div>
            <div className="text-2xl font-bold text-gray-900">
              {formatCurrency(totalPlanned)}
            </div>
          </CardBody>
        </Card>
        <Card>
          <CardBody>
            <div className="text-sm text-gray-500">Total Actual</div>
            <div className="text-2xl font-bold text-gray-900">
              {formatCurrency(totalActual)}
            </div>
          </CardBody>
        </Card>
        <Card>
          <CardBody>
            <div className="text-sm text-gray-500">Variance</div>
            <div
              className={`text-2xl font-bold ${getVarianceColor(totalVariance)}`}
            >
              {formatCurrency(totalVariance)}
            </div>
          </CardBody>
        </Card>
        <Card>
          <CardBody>
            <div className="text-sm text-gray-500">Variance %</div>
            <div
              className={`text-2xl font-bold ${getVarianceColor(totalVariance)}`}
            >
              {variancePercentage.toFixed(1)}%
            </div>
          </CardBody>
        </Card>
      </div>

      {/* Filter */}
      <Card>
        <CardBody>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Select
              label="Filter by Project"
              name="filterProject"
              value={filterProject}
              onChange={(e) => setFilterProject(e.target.value)}
              options={[
                { value: "", label: "All Projects" },
                ...projects.map((p) => ({
                  value: p.id.toString(),
                  label: p.name,
                })),
              ]}
            />
            <div className="flex items-end">
              <Button
                variant="secondary"
                onClick={() => setFilterProject("")}
                className="w-full"
              >
                Clear Filter
              </Button>
            </div>
          </div>
        </CardBody>
      </Card>

      {/* Budgets Table */}
      <Card>
        <Table>
          <TableHeader>
            <TableHead>Category</TableHead>
            <TableHead>Project</TableHead>
            <TableHead>Description</TableHead>
            <TableHead>Planned Amount</TableHead>
            <TableHead>Actual Amount</TableHead>
            <TableHead>Variance</TableHead>
            <TableHead>Variance %</TableHead>
            <TableHead>Actions</TableHead>
          </TableHeader>
          <TableBody>
            {filteredBudgets.map((budget) => (
              <tr key={budget.id}>
                <TableCell>
                  <div className="font-medium text-gray-900">
                    {budget.category}
                  </div>
                </TableCell>
                <TableCell>
                  {projects.find((p) => p.id === budget.project_id)?.name ||
                    `Project #${budget.project_id}`}
                </TableCell>
                <TableCell>
                  <div className="text-gray-600 max-w-xs truncate">
                    {budget.description || (
                      <span className="text-gray-400">No description</span>
                    )}
                  </div>
                </TableCell>
                <TableCell>
                  <span className="font-semibold">
                    {formatCurrency(budget.planned_amount)}
                  </span>
                </TableCell>
                <TableCell>
                  <span className="font-semibold">
                    {formatCurrency(budget.actual_amount)}
                  </span>
                </TableCell>
                <TableCell>
                  <span
                    className={`font-semibold ${getVarianceColor(budget.variance)}`}
                  >
                    {formatCurrency(budget.variance)}
                  </span>
                </TableCell>
                <TableCell>
                  <span
                    className={`font-semibold ${getVarianceColor(budget.variance)}`}
                  >
                    {budget.variance_percentage.toFixed(1)}%
                  </span>
                </TableCell>
                <TableCell>
                  <div className="flex space-x-2">
                    <button
                      onClick={() => openEditModal(budget)}
                      className="text-primary-600 hover:text-primary-900"
                    >
                      Edit
                    </button>
                    <button
                      onClick={() => handleDelete(budget.id)}
                      className="text-red-600 hover:text-red-900"
                    >
                      Delete
                    </button>
                  </div>
                </TableCell>
              </tr>
            ))}
          </TableBody>
        </Table>
        {filteredBudgets.length === 0 && (
          <div className="text-center py-12 text-gray-500">
            No budget entries found
          </div>
        )}
      </Card>

      {/* Create/Edit Modal */}
      <Modal
        isOpen={isModalOpen}
        onClose={() => {
          setIsModalOpen(false);
          resetForm();
        }}
        title={editingBudget ? "Edit Budget Entry" : "Add Budget Entry"}
      >
        <form onSubmit={handleSubmit} className="space-y-4">
          <Select
            label="Project"
            name="project_id"
            value={formData.project_id}
            onChange={handleInputChange}
            options={[
              { value: "", label: "Select a project" },
              ...projects.map((p) => ({
                value: p.id.toString(),
                label: p.name,
              })),
            ]}
            required
          />

          <Input
            label="Category"
            name="category"
            value={formData.category}
            onChange={handleInputChange}
            placeholder="e.g., Materials, Labor, Equipment"
            required
          />

          <TextArea
            label="Description"
            name="description"
            value={formData.description}
            onChange={handleInputChange}
            rows={3}
          />

          <div className="grid grid-cols-2 gap-4">
            <Input
              label="Planned Amount"
              type="number"
              name="planned_amount"
              value={formData.planned_amount}
              onChange={handleInputChange}
              placeholder="0.00"
              required
            />

            <Input
              label="Actual Amount"
              type="number"
              name="actual_amount"
              value={formData.actual_amount}
              onChange={handleInputChange}
              placeholder="0.00"
              required
            />
          </div>

          <div className="bg-gray-50 px-4 py-3 rounded">
            <div className="text-sm text-gray-600">
              Variance:{" "}
              <span
                className={`font-semibold ${getVarianceColor(
                  parseFloat(formData.planned_amount.toString()) -
                    parseFloat(formData.actual_amount.toString())
                )}`}
              >
                {formatCurrency(
                  parseFloat(formData.planned_amount.toString()) -
                    parseFloat(formData.actual_amount.toString())
                )}
              </span>
            </div>
          </div>

          <div className="flex justify-end space-x-3 pt-4">
            <Button
              type="button"
              variant="secondary"
              onClick={() => {
                setIsModalOpen(false);
                resetForm();
              }}
            >
              Cancel
            </Button>
            <Button type="submit">
              {editingBudget ? "Update Budget" : "Add Budget"}
            </Button>
          </div>
        </form>
      </Modal>
    </div>
  );
};

export default Budgets;
```

# File: ./frontend/src/pages/Users.tsx

```typescript
import React, { useEffect, useState } from "react";
import { Card, CardHeader, CardBody } from "../components/Card";
import {
  Table,
  TableHeader,
  TableBody,
  TableHead,
  TableCell,
} from "../components/Table";
import { usersAPI, TeamMember } from "../services/API";

const Users: React.FC = () => {
  const [users, setUsers] = useState<TeamMember[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    try {
      setLoading(true);
      const response = await usersAPI.getAll();
      setUsers(response.data);
      setError(null);
    } catch (err: any) {
      setError(err.message || "Failed to fetch users");
    } finally {
      setLoading(false);
    }
  };

  const getRoleBadgeColor = (role: string) => {
    switch (role) {
      case "admin":
        return "bg-red-100 text-red-800";
      case "manager":
        return "bg-blue-100 text-blue-800";
      case "worker":
        return "bg-green-100 text-green-800";
      default:
        return "bg-gray-100 text-gray-800";
    }
  };

  const getRoleIcon = (role: string) => {
    switch (role) {
      case "admin":
        return "👑";
      case "manager":
        return "📊";
      case "worker":
        return "👷";
      default:
        return "👤";
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-gray-500">Loading users...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-400 text-red-700 px-4 py-3 rounded">
        Error: {error}
      </div>
    );
  }

  // Group users by role
  const adminUsers = users.filter((u) => u.role === "admin");
  const managerUsers = users.filter((u) => u.role === "manager");
  const workerUsers = users.filter((u) => u.role === "worker");

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">User Management</h1>
          <p className="text-gray-600 mt-1">
            Manage system users and their roles
          </p>
        </div>
        <button
          onClick={fetchUsers}
          className="px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700"
        >
          Refresh
        </button>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card>
          <CardBody>
            <div className="text-sm text-gray-500">Total Users</div>
            <div className="text-2xl font-bold text-gray-900">
              {users.length}
            </div>
          </CardBody>
        </Card>
        <Card>
          <CardBody>
            <div className="text-sm text-gray-500">Administrators</div>
            <div className="text-2xl font-bold text-red-600">
              {adminUsers.length}
            </div>
          </CardBody>
        </Card>
        <Card>
          <CardBody>
            <div className="text-sm text-gray-500">Managers</div>
            <div className="text-2xl font-bold text-blue-600">
              {managerUsers.length}
            </div>
          </CardBody>
        </Card>
        <Card>
          <CardBody>
            <div className="text-sm text-gray-500">Workers</div>
            <div className="text-2xl font-bold text-green-600">
              {workerUsers.length}
            </div>
          </CardBody>
        </Card>
      </div>

      {/* Administrators */}
      <Card>
        <CardHeader>
          <h3 className="text-lg font-medium leading-6 text-gray-900">
            ADMIN
          </h3>
        </CardHeader>
        <Table>
          <TableHeader>
            <TableHead>User</TableHead>
            <TableHead>Username</TableHead>
            <TableHead>Email</TableHead>
            <TableHead>Role</TableHead>
          </TableHeader>
          <TableBody>
            {adminUsers.map((user) => (
              <tr key={user.username}>
                <TableCell>
                  <div className="flex items-center">
                    <div className="h-10 w-10 rounded-full bg-red-100 flex items-center justify-center text-red-600 font-bold mr-3">
                      {user.name.charAt(0)}
                    </div>
                    <div className="font-medium text-gray-900">
                      {user.name}
                    </div>
                  </div>
                </TableCell>
                <TableCell>{user.username}</TableCell>
                <TableCell>{user.email}</TableCell>
                <TableCell>
                  <span
                    className={`px-2 py-1 text-xs font-semibold rounded-full ${getRoleBadgeColor(user.role)}`}
                  >
                    {getRoleIcon(user.role)} {user.role}
                  </span>
                </TableCell>
              </tr>
            ))}
          </TableBody>
        </Table>
      </Card>

      {/* Managers */}
      <Card>
        <CardHeader>
          <h3 className="text-lg font-medium leading-6 text-gray-900">
            📊 Project Managers
          </h3>
        </CardHeader>
        <Table>
          <TableHeader>
            <TableHead>User</TableHead>
            <TableHead>Username</TableHead>
            <TableHead>Email</TableHead>
            <TableHead>Managed Projects</TableHead>
            <TableHead>Role</TableHead>
          </TableHeader>
          <TableBody>
            {managerUsers.map((user) => (
              <tr key={user.username}>
                <TableCell>
                  <div className="flex items-center">
                    <div className="h-10 w-10 rounded-full bg-blue-100 flex items-center justify-center text-blue-600 font-bold mr-3">
                      {user.name.charAt(0)}
                    </div>
                    <div className="font-medium text-gray-900">
                      {user.name}
                    </div>
                  </div>
                </TableCell>
                <TableCell>{user.username}</TableCell>
                <TableCell>{user.email}</TableCell>
                <TableCell>
                  {user.managed_projects && user.managed_projects.length > 0 ? (
                    <span className="text-sm text-gray-600">
                      {user.managed_projects.length} project(s)
                    </span>
                  ) : (
                    <span className="text-sm text-gray-400">
                      No projects assigned
                    </span>
                  )}
                </TableCell>
                <TableCell>
                  <span
                    className={`px-2 py-1 text-xs font-semibold rounded-full ${getRoleBadgeColor(user.role)}`}
                  >
                    {getRoleIcon(user.role)} {user.role}
                  </span>
                </TableCell>
              </tr>
            ))}
          </TableBody>
        </Table>
      </Card>

      {/* Workers */}
      <Card>
        <CardHeader>
          <h3 className="text-lg font-medium leading-6 text-gray-900">
            👷 Workers
          </h3>
        </CardHeader>
        <Table>
          <TableHeader>
            <TableHead>User</TableHead>
            <TableHead>Username</TableHead>
            <TableHead>Email</TableHead>
            <TableHead>Worker Name</TableHead>
            <TableHead>Role</TableHead>
          </TableHeader>
          <TableBody>
            {workerUsers.map((user) => (
              <tr key={user.username}>
                <TableCell>
                  <div className="flex items-center">
                    <div className="h-10 w-10 rounded-full bg-green-100 flex items-center justify-center text-green-600 font-bold mr-3">
                      {user.name.charAt(0)}
                    </div>
                    <div className="font-medium text-gray-900">
                      {user.name}
                    </div>
                  </div>
                </TableCell>
                <TableCell>{user.username}</TableCell>
                <TableCell>{user.email}</TableCell>
                <TableCell>
                  <span className="text-sm text-gray-600">
                    {user.worker_name || "N/A"}
                  </span>
                </TableCell>
                <TableCell>
                  <span
                    className={`px-2 py-1 text-xs font-semibold rounded-full ${getRoleBadgeColor(user.role)}`}
                  >
                    {getRoleIcon(user.role)} {user.role}
                  </span>
                </TableCell>
              </tr>
            ))}
          </TableBody>
        </Table>
      </Card>
    </div>
  );
};

export default Users;
```

# File: ./frontend/src/pages/Projects.tsx

```typescript
import React, { useEffect, useState } from "react";
import { Card, CardBody } from "../components/Card";
import Modal from "../components/Modal";
import Input from "../components/Input";
import Select from "../components/Select";
import TextArea from "../components/TextArea";
import Button from "../components/Button";
import { exportToCSV } from '../utils/export';
import { projectsAPI, Project } from "../services/API";

const Projects: React.FC = () => {
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isDetailModalOpen, setIsDetailModalOpen] = useState(false);
  const [editingProject, setEditingProject] = useState<Project | null>(null);
  const [selectedProject, setSelectedProject] = useState<Project | null>(null);

  const [formData, setFormData] = useState({
    name: "",
    description: "",
    status: "planning",
    start_date: "",
    planned_end_date: "",
    total_budget: 0,
    location: "",
  });

  useEffect(() => {
    fetchProjects();
  }, []);

  const fetchProjects = async () => {
    try {
      setLoading(true);
      const response = await projectsAPI.getAll();
      setProjects(response.data);
      setError(null);
    } catch (err: any) {
      setError(err.message || "Failed to fetch projects");
    } finally {
      setLoading(false);
    }
  };
  const handleInputChange = (
      e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>
    ) => {
      const { name, value } = e.target;
      setFormData((prev) => ({ ...prev, [name]: value }));
    };

    const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const submitData: any = {
        ...formData,
        total_budget: parseFloat(formData.total_budget.toString()),
      };

      // Only include dates if they are valid
      if (formData.start_date) {
        try {
          submitData.start_date = new Date(formData.start_date).toISOString();
        } catch (err) {
          console.error("Invalid start_date:", err);
        }
      }
      
      if (formData.planned_end_date) {
        try {
          submitData.planned_end_date = new Date(
            formData.planned_end_date
          ).toISOString();
        } catch (err) {
          console.error("Invalid planned_end_date:", err);
        }
      }

      if (editingProject) {
        await projectsAPI.update(editingProject.id, submitData);
      } else {
        await projectsAPI.create(submitData);
      }
      setIsModalOpen(false);
      resetForm();
      fetchProjects();
    } catch (err: any) {
      alert(
        err.response?.data?.detail || err.message || "Failed to save project"
      );
    }
  };

  const handleDelete = async (id: number) => {
    if (window.confirm("Are you sure you want to delete this project? This will also delete all associated tasks, resources, and budgets.")) {
      try {
        await projectsAPI.delete(id);
        setIsDetailModalOpen(false);
        fetchProjects();
      } catch (err: any) {
        alert(err.message || "Failed to delete project");
      }
    }
  };

  const openCreateModal = () => {
    resetForm();
    setIsModalOpen(true);
  };

  const openEditModal = (project: Project) => {
    setEditingProject(project);
    setFormData({
      name: project.name,
      description: project.description || "",
      status: project.status,
      start_date: project.start_date?.split("T")[0] || "",
      planned_end_date: project.planned_end_date?.split("T")[0] || "",
      total_budget: project.total_budget,
      location: project.location || "",
    });
    setIsDetailModalOpen(false);
    setIsModalOpen(true);
  };

  const openDetailModal = (project: Project) => {
    setSelectedProject(project);
    setIsDetailModalOpen(true);
  };

  const resetForm = () => {
    setFormData({
      name: "",
      description: "",
      status: "planning",
      start_date: "",
      planned_end_date: "",
      total_budget: 0,
      location: "",
    });
    setEditingProject(null);
  };

  const getStatusColor = (status: string) => {
    const colors: Record<string, string> = {
      planning: "bg-gray-100 text-gray-800",
      in_progress: "bg-blue-100 text-blue-800",
      on_hold: "bg-yellow-100 text-yellow-800",
      completed: "bg-green-100 text-green-800",
      cancelled: "bg-red-100 text-red-800",
    };
    return colors[status] || "bg-gray-100 text-gray-800";
  };

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat("en-US", {
      style: "currency",
      currency: "USD",
      minimumFractionDigits: 0,
    }).format(amount);
  };

  const formatDate = (dateString?: string) => {
    if (!dateString) return "N/A";
    return new Date(dateString).toLocaleDateString();
  };

  const handleExport = () => {
    const exportData = projects.map((project) => ({
      ID: project.id,
      Name: project.name,
      Status: project.status,
      "Start Date": project.start_date
        ? new Date(project.start_date).toLocaleDateString()
        : "N/A",
      "End Date": project.planned_end_date
        ? new Date(project.planned_end_date).toLocaleDateString()
        : "N/A",
      "Total Budget": project.total_budget,
      "Spent Amount": project.spent_amount,
      "Budget Utilization %": project.budget_utilization.toFixed(2),
      Location: project.location || "N/A",
    }));

    exportToCSV(exportData, "projects");
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-gray-500">Loading projects...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-400 text-red-700 px-4 py-3 rounded">
        Error: {error}
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-900">Projects</h1>
        <div className="flex space-x-3">
          <Button variant="secondary" onClick={handleExport}>
            📥 Export
          </Button>
          <Button onClick={() => setIsModalOpen(true)}>
            Add New Project
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
        {projects.map((project) => (
          <Card key={project.id} className="cursor-pointer hover:shadow-lg transition-shadow">
            <CardBody className="space-y-4">
              <div onClick={() => openDetailModal(project)}>
                <div className="text-lg font-semibold text-gray-900 hover:text-primary-600">
                  {project.name}
                </div>
                <p className="mt-1 text-sm text-gray-500 line-clamp-2">
                  {project.description}
                </p>
              </div>

              <div>
                <span
                  className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getStatusColor(project.status)}`}
                >
                  {project.status.replace("_", " ")}
                </span>
              </div>

              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span className="text-gray-500">Budget:</span>
                  <span className="font-medium text-gray-900">
                    {formatCurrency(project.total_budget)}
                  </span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-500">Spent:</span>
                  <span className="font-medium text-gray-900">
                    {formatCurrency(project.spent_amount)}
                  </span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className={`h-2 rounded-full ${
                      project.budget_utilization > 90
                        ? "bg-red-500"
                        : project.budget_utilization > 75
                          ? "bg-yellow-500"
                          : "bg-green-500"
                    }`}
                    style={{
                      width: `${Math.min(project.budget_utilization, 100)}%`,
                    }}
                  ></div>
                </div>
                <div className="text-xs text-gray-500 text-right">
                  {project.budget_utilization.toFixed(1)}% utilized
                </div>
              </div>

              {project.location && (
                <div className="text-sm text-gray-500">
                  📍 {project.location}
                </div>
              )}
            </CardBody>
          </Card>
        ))}
      </div>

      {projects.length === 0 && (
        <Card>
          <CardBody className="text-center py-12">
            <p className="text-gray-500">No projects found</p>
            <Button onClick={openCreateModal} className="mt-4">
              Create Your First Project
            </Button>
          </CardBody>
        </Card>
      )}

      {/* Create/Edit Modal */}
      <Modal
        isOpen={isModalOpen}
        onClose={() => {
          setIsModalOpen(false);
          resetForm();
        }}
        title={editingProject ? "Edit Project" : "Create New Project"}
        size="lg"
      >
        <form onSubmit={handleSubmit} className="space-y-4">
          <Input
            label="Project Name"
            name="name"
            value={formData.name}
            onChange={handleInputChange}
            required
          />

          <TextArea
            label="Description"
            name="description"
            value={formData.description}
            onChange={handleInputChange}
            rows={3}
          />

          <Select
            label="Status"
            name="status"
            value={formData.status}
            onChange={handleInputChange}
            options={[
              { value: "planning", label: "Planning" },
              { value: "in_progress", label: "In Progress" },
              { value: "on_hold", label: "On Hold" },
              { value: "completed", label: "Completed" },
              { value: "cancelled", label: "Cancelled" },
            ]}
            required
          />

          <div className="grid grid-cols-2 gap-4">
            <Input
              label="Start Date"
              type="date"
              name="start_date"
              value={formData.start_date}
              onChange={handleInputChange}
            />

            <Input
              label="Planned End Date"
              type="date"
              name="planned_end_date"
              value={formData.planned_end_date}
              onChange={handleInputChange}
            />
          </div>

          <Input
            label="Total Budget"
            type="number"
            name="total_budget"
            value={formData.total_budget}
            onChange={handleInputChange}
            placeholder="0.00"
            required
          />

          <Input
            label="Location"
            name="location"
            value={formData.location}
            onChange={handleInputChange}
            placeholder="Project location"
          />

          <div className="flex justify-end space-x-3 pt-4">
            <Button
              type="button"
              variant="secondary"
              onClick={() => {
                setIsModalOpen(false);
                resetForm();
              }}
            >
              Cancel
            </Button>
            <Button type="submit">
              {editingProject ? "Update Project" : "Create Project"}
            </Button>
          </div>
        </form>
      </Modal>

      {/* Project Detail Modal */}
      <Modal
        isOpen={isDetailModalOpen}
        onClose={() => setIsDetailModalOpen(false)}
        title={selectedProject?.name || "Project Details"}
        size="xl"
      >
        {selectedProject && (
          <div className="space-y-6">
            <div>
              <h4 className="text-sm font-medium text-gray-500">Description</h4>
              <p className="mt-1 text-gray-900">{selectedProject.description || "No description"}</p>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <h4 className="text-sm font-medium text-gray-500">Status</h4>
                <span
                  className={`mt-1 inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getStatusColor(selectedProject.status)}`}
                >
                  {selectedProject.status.replace("_", " ")}
                </span>
              </div>
              <div>
                <h4 className="text-sm font-medium text-gray-500">Location</h4>
                <p className="mt-1 text-gray-900">{selectedProject.location || "N/A"}</p>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <h4 className="text-sm font-medium text-gray-500">Start Date</h4>
                <p className="mt-1 text-gray-900">{formatDate(selectedProject.start_date)}</p>
              </div>
              <div>
                <h4 className="text-sm font-medium text-gray-500">Planned End Date</h4>
                <p className="mt-1 text-gray-900">{formatDate(selectedProject.planned_end_date)}</p>
              </div>
            </div>

            <div>
              <h4 className="text-sm font-medium text-gray-500">Budget Information</h4>
              <div className="mt-2 space-y-2">
                <div className="flex justify-between">
                  <span>Total Budget:</span>
                  <span className="font-semibold">{formatCurrency(selectedProject.total_budget)}</span>
                </div>
                <div className="flex justify-between">
                  <span>Spent Amount:</span>
                  <span className="font-semibold">{formatCurrency(selectedProject.spent_amount)}</span>
                </div>
                <div className="flex justify-between">
                  <span>Remaining:</span>
                  <span className="font-semibold">{formatCurrency(selectedProject.remaining_budget)}</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className={`h-2 rounded-full ${
                      selectedProject.budget_utilization > 90
                        ? "bg-red-500"
                        : selectedProject.budget_utilization > 75
                          ? "bg-yellow-500"
                          : "bg-green-500"
                    }`}
                    style={{
                      width: `${Math.min(selectedProject.budget_utilization, 100)}%`,
                    }}
                  ></div>
                </div>
                <div className="text-sm text-gray-500 text-right">
                  {selectedProject.budget_utilization.toFixed(1)}% utilized
                </div>
              </div>
            </div>

            <div className="flex justify-end space-x-3 pt-4 border-t">
              <Button
                variant="secondary"
                onClick={() => setIsDetailModalOpen(false)}
              >
                Close
              </Button>
              <Button
                variant="primary"
                onClick={() => openEditModal(selectedProject)}
              >
                Edit Project
              </Button>
              <Button
                variant="danger"
                onClick={() => handleDelete(selectedProject.id)}
              >
                Delete Project
              </Button>
            </div>
          </div>
        )}
      </Modal>
    </div>
  );
};

export default Projects;
```

# File: ./backend/.gitgnore

```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Environment
.env
.env.local
.venv

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Database
*.db
*.sqlite
*.sqlite3

# Logs
*.log
logs/

# OS
.DS_Store
Thumbs.db

# Docker
docker-compose.override.yml

# Testing
.coverage
htmlcov/
.pytest_cache/
.tox/

# Alembic
alembic/versions/*.pyc
```

# File: ./backend/requirements.txt

```
alembic==1.12.1
annotated-types==0.7.0
anyio==3.7.1
bcrypt==4.1.2
certifi==2025.10.5
cffi==2.0.0
click==8.3.0
cryptography==46.0.2
dnspython==2.8.0
ecdsa==0.19.1
email-validator==2.3.0
et_xmlfile==2.0.0
fastapi==0.119.0
fastapi-cli==0.0.13
fastapi-cloud-cli==0.3.1
greenlet==3.2.4
h11==0.16.0
httpcore==1.0.9
httptools==0.7.1
httpx==0.28.1
idna==3.10
iniconfig==2.1.0
Jinja2==3.1.6
joblib==1.5.2
Mako==1.3.10
markdown-it-py==4.0.0
MarkupSafe==3.0.3
mdurl==0.1.2
numpy==1.26.2
openpyxl==3.1.2
packaging==25.0
pandas==2.1.3
passlib==1.7.4
pluggy==1.6.0
psycopg2-binary==2.9.9
pyasn1==0.6.1
pycparser==2.23
pydantic==2.5.0
pydantic-settings==2.1.0
pydantic_core==2.14.1
Pygments==2.19.2
pytest==7.4.3
pytest-asyncio==0.21.1
python-dateutil==2.8.2
python-dotenv==1.0.0
python-jose==3.3.0
python-multipart==0.0.20
pytz==2025.2
PyYAML==6.0.3
rich==14.2.0
rich-toolkit==0.15.1
rignore==0.7.0
rsa==4.9.1
scikit-learn==1.3.2
scipy==1.16.2
sentry-sdk==2.41.0
shellingham==1.5.4
six==1.17.0
sniffio==1.3.1
SQLAlchemy==2.0.23
starlette==0.48.0
threadpoolctl==3.6.0
typer==0.19.2
typing_extensions==4.15.0
tzdata==2025.2
urllib3==2.5.0
uvicorn==0.24.0
uvloop==0.21.0
watchfiles==1.1.0
websockets==15.0.1

```

# File: ./backend/Dockerfile

```
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

# File: ./backend/app/__init__.py

```python
from . import config, database, main

__all__ = ["config", "database", "main"]
```

# File: ./backend/app/config.py

```python
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    APP_NAME: str = "BuildFlow ERP"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    DATABASE_URL: str = (
        "postgresql://buildflow:buildflow123@db:5432/buildflow_db"
    )
    
    # store as strings, convert via properties
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:5173"
    ALLOWED_EXTENSIONS: str = ".xlsx,.xls,.csv"
    
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    
    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
    
    @property
    def allowed_extensions_set(self) -> set[str]:
        return {ext.strip() for ext in self.ALLOWED_EXTENSIONS.split(",") if ext.strip()}
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
```

# File: ./backend/app/database.py

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    Base.metadata.create_all(bind=engine)
```

# File: ./backend/app/main.py

```python
# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from app.config import settings
# from app.database import init_db
# from app.routes import (
#     projects,
#     resources,
#     tasks,
#     budgets,
#     analytics,
#     import_data,
# )
# from app.middleware.error_handler import add_exception_handlers

# app = FastAPI(
#     title=settings.APP_NAME, version=settings.APP_VERSION, debug=settings.DEBUG
# )

# app.add_middleware(
#     CORSMiddleware,
#     # allow_origins=settings.cors_origins_list,  # use the property from the config.py
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# add_exception_handlers(app)

# app.include_router(projects.router, prefix="/api/projects", tags=["Projects"])
# app.include_router(tasks.router, prefix="/api/tasks", tags=["Tasks"])
# app.include_router(
#     resources.router, prefix="/api/resources", tags=["Resources"]
# )
# app.include_router(budgets.router, prefix="/api/budgets", tags=["Budgets"])
# app.include_router(
#     analytics.router, prefix="/api/analytics", tags=["Analytics"]
# )
# app.include_router(import_data.router, prefix="/api/import", tags=["Import"])


# @app.on_event("startup")
# async def startup_event():
#     """Initialize database on startup"""
#     init_db()


# @app.get("/")
# async def root():
#     """Root endpoint"""
#     return {
#         "message": "Welcome to BuildFlow ERP API",
#         "version": settings.APP_VERSION,
#         "docs": "/docs",
#     }


# @app.get("/health")
# async def health_check():
#     """Health check endpoint"""
#     return {"status": "healthy", "service": settings.APP_NAME}


from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import init_db
from app.routes import (
    auth,
    users,
    projects,
    resources,
    tasks,
    budgets,
    analytics,
    import_data,
)
from app.middleware.error_handler import add_exception_handlers


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events"""
    init_db()
    yield

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

add_exception_handlers(app)

app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(projects.router, prefix="/api/projects", tags=["Projects"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["Tasks"])
app.include_router(
    resources.router, prefix="/api/resources", tags=["Resources"]
)
app.include_router(budgets.router, prefix="/api/budgets", tags=["Budgets"])
app.include_router(
    analytics.router, prefix="/api/analytics", tags=["Analytics"]
)
app.include_router(import_data.router, prefix="/api/import", tags=["Import"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to BuildFlow ERP API",
        "version": settings.APP_VERSION,
        "docs": "/docs",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": settings.APP_NAME}
```

# File: ./backend/app/auth/__init__.py

```python
from app.auth.jwt_handler import create_access_token, verify_token
from app.auth.dependencies import get_current_user, require_role
from app.auth.demo_users import DEMO_USERS, get_user_by_username

__all__ = [
    "create_access_token",
    "verify_token",
    "get_current_user",
    "require_role",
    "DEMO_USERS",
    "get_user_by_username",
]
```

# File: ./backend/app/auth/demo_users.py

```python
from typing import Dict, Optional
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

_DEMO_USER_PASSWORDS = {
    "admin": "admin123",
    "manager1": "manager123",
    "worker1": "worker123",
    "worker2": "worker123",
    "worker3": "worker123",
}

DEMO_USERS = {
    "admin": {
        "username": "admin",
        "role": "admin",
        "name": "John Admin",
        "email": "admin@buildflow.com",
        "worker_name": None,
        "managed_projects": [],
    },
    "manager1": {
        "username": "manager1",
        "role": "manager",
        "name": "Sarah Manager",
        "email": "sarah@buildflow.com",
        "worker_name": None,
        "managed_projects": [1, 2],
    },
    "worker1": {
        "username": "worker1",
        "role": "worker",
        "name": "Mike Construction",
        "email": "mike@buildflow.com",
        "worker_name": "Mike Construction",
        "managed_projects": [],
    },
    "worker2": {
        "username": "worker2",
        "role": "worker",
        "name": "Lisa Field",
        "email": "lisa@buildflow.com",
        "worker_name": "Lisa Field",
        "managed_projects": [],
    },
    "worker3": {
        "username": "worker3",
        "role": "worker",
        "name": "Construction Team A",
        "email": "teama@buildflow.com",
        "worker_name": "Construction Team A",
        "managed_projects": [],
    },
}


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)


def get_user_by_username(username: str) -> Optional[Dict]:
    """Get user by username"""
    return DEMO_USERS.get(username)


def authenticate_user(username: str, password: str) -> Optional[Dict]:
    """Authenticate a user"""
    user = get_user_by_username(username)
    if not user:
        return None
    
    # Check against demo password - simple string comparison for demo
    demo_password = _DEMO_USER_PASSWORDS.get(username)
    if not demo_password:
        return None
    
    # Direct string comparison for simplicity in demo
    if password != demo_password:
        return None
    
    # Return user copy without password
    return user.copy()
```

# File: ./backend/app/auth/dependencies.py

```python
from typing import List
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.auth.jwt_handler import verify_token
from app.auth.demo_users import get_user_by_username

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    """Get current authenticated user from JWT token"""
    token = credentials.credentials
    payload = verify_token(token)
    
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    username: str = payload.get("sub")
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )
    
    user = get_user_by_username(username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    
    # Return user without password hash
    user_copy = user.copy()
    user_copy.pop("password_hash", None)
    return user_copy


def require_role(*allowed_roles: str):
    """Dependency to check if user has required role"""
    async def role_checker(current_user: dict = Depends(get_current_user)):
        if current_user["role"] not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required role: {', '.join(allowed_roles)}",
            )
        return current_user
    return role_checker
```

# File: ./backend/app/auth/jwt_handler.py

```python
from datetime import datetime, timedelta
from typing import Optional, Dict
from jose import JWTError, jwt
from app.config import settings


def create_access_token(
    data: dict, expires_delta: Optional[timedelta] = None
) -> str:
    """Create JWT access token"""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def verify_token(token: str) -> Optional[Dict]:
    """Verify and decode JWT token"""
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError:
        return None
```

# File: ./backend/app/utils/__init__.py

```python
from app.utils.seed_data import seed_database

__all__ = ["seed_database"]
```

# File: ./backend/app/utils/seed_data.py

```python
"""
Seed script to populate database with sample data for demo purposes.
Run with: docker-compose exec backend python -m app.utils.seed_data in a new terminal after the docker-compose is up
"""

from datetime import datetime, timedelta
from app.database import SessionLocal
from app.models import (
    Project, ProjectStatus,
    Task, TaskStatus, TaskPriority,
    Resource, ResourceType, ResourceStatus,
    Budget
)


def seed_database():
    db = SessionLocal()
    
    try:
        print("🌱 Starting database seeding...")
        
        # Create Projects
        projects_data = [
            {
                "name": "Residential Complex Alpha",
                "description": "Modern 10-story residential building with 120 apartments",
                "status": ProjectStatus.IN_PROGRESS,
                "start_date": datetime(2025, 9, 1),
                "planned_end_date": datetime(2026, 12, 31),
                "total_budget": 8500000.0,
                "spent_amount": 3200000.0,
                "location": "Astana, Esil District"
            },
            {
                "name": "Business Center Omega",
                "description": "15-story office building with retail on ground floor",
                "status": ProjectStatus.IN_PROGRESS,
                "start_date": datetime(2025, 7, 15),
                "planned_end_date": datetime(2027, 6, 30),
                "total_budget": 15000000.0,
                "spent_amount": 4500000.0,
                "location": "Almaty, Bostandyk District"
            },
            {
                "name": "Shopping Mall Gamma",
                "description": "3-story shopping center with parking",
                "status": ProjectStatus.PLANNING,
                "start_date": datetime(2025, 12, 1),
                "planned_end_date": datetime(2027, 3, 31),
                "total_budget": 12000000.0,
                "spent_amount": 0.0,
                "location": "Shymkent, City Center"
            }
        ]
        
        projects = []
        for proj_data in projects_data:
            project = Project(**proj_data)
            db.add(project)
            projects.append(project)
        
        db.commit()
        print(f"✅ Created {len(projects)} projects")
        
        # Refresh to get IDs
        for proj in projects:
            db.refresh(proj)
        
        # Create Tasks for Project 1
        tasks_project1 = [
            {
                "project_id": projects[0].id,
                "name": "Site Preparation and Excavation",
                "description": "Clear site and excavate foundation",
                "status": TaskStatus.COMPLETED,
                "priority": TaskPriority.HIGH,
                "start_date": datetime(2025, 9, 1),
                "planned_end_date": datetime(2025, 10, 15),
                "actual_end_date": datetime(2025, 10, 12),
                "progress_percentage": 100.0,
                "assigned_to": "Construction Team A"
            },
            {
                "project_id": projects[0].id,
                "name": "Foundation Construction",
                "description": "Pour concrete foundation",
                "status": TaskStatus.COMPLETED,
                "priority": TaskPriority.CRITICAL,
                "start_date": datetime(2025, 10, 16),
                "planned_end_date": datetime(2025, 11, 30),
                "actual_end_date": datetime(2025, 11, 28),
                "progress_percentage": 100.0,
                "assigned_to": "Foundation Specialists"
            },
            {
                "project_id": projects[0].id,
                "name": "Structural Framework (Floors 1-5)",
                "description": "Build structural columns and beams",
                "status": TaskStatus.IN_PROGRESS,
                "priority": TaskPriority.HIGH,
                "start_date": datetime(2025, 12, 1),
                "planned_end_date": datetime(2026, 3, 31),
                "progress_percentage": 65.0,
                "assigned_to": "Structural Team"
            },
            {
                "project_id": projects[0].id,
                "name": "Structural Framework (Floors 6-10)",
                "description": "Build upper floors structure",
                "status": TaskStatus.NOT_STARTED,
                "priority": TaskPriority.HIGH,
                "start_date": datetime(2026, 4, 1),
                "planned_end_date": datetime(2026, 7, 31),
                "progress_percentage": 0.0,
                "assigned_to": "Structural Team"
            },
            {
                "project_id": projects[0].id,
                "name": "Electrical Systems Installation",
                "description": "Install wiring and electrical panels",
                "status": TaskStatus.NOT_STARTED,
                "priority": TaskPriority.MEDIUM,
                "start_date": datetime(2026, 6, 1),
                "planned_end_date": datetime(2026, 9, 30),
                "progress_percentage": 0.0,
                "assigned_to": "Electrical Team"
            }
        ]
        
        # Create Tasks for Project 2
        tasks_project2 = [
            {
                "project_id": projects[1].id,
                "name": "Demolition of Old Structure",
                "description": "Safe demolition and debris removal",
                "status": TaskStatus.COMPLETED,
                "priority": TaskPriority.HIGH,
                "start_date": datetime(2025, 7, 15),
                "planned_end_date": datetime(2025, 8, 31),
                "actual_end_date": datetime(2025, 8, 28),
                "progress_percentage": 100.0,
                "assigned_to": "Demolition Crew"
            },
            {
                "project_id": projects[1].id,
                "name": "Deep Foundation Work",
                "description": "Pile driving and foundation reinforcement",
                "status": TaskStatus.IN_PROGRESS,
                "priority": TaskPriority.CRITICAL,
                "start_date": datetime(2025, 9, 1),
                "planned_end_date": datetime(2026, 1, 15),
                "progress_percentage": 45.0,
                "assigned_to": "Foundation Specialists"
            }
        ]
        
        all_tasks = tasks_project1 + tasks_project2
        for task_data in all_tasks:
            task = Task(**task_data)
            db.add(task)
        
        db.commit()
        print(f"✅ Created {len(all_tasks)} tasks")
        
        # Create Resources for Project 1
        resources_project1 = [
            {
                "project_id": projects[0].id,
                "name": "Concrete M300",
                "resource_type": ResourceType.MATERIAL,
                "status": ResourceStatus.IN_USE,
                "quantity": 5000.0,
                "unit": "m³",
                "unit_cost": 12000.0,
                "supplier": "Astana Concrete Ltd"
            },
            {
                "project_id": projects[0].id,
                "name": "Steel Reinforcement Bars",
                "resource_type": ResourceType.MATERIAL,
                "status": ResourceStatus.IN_USE,
                "quantity": 80000.0,
                "unit": "kg",
                "unit_cost": 250.0,
                "supplier": "Kazakhstan Steel"
            },
            {
                "project_id": projects[0].id,
                "name": "Tower Crane",
                "resource_type": ResourceType.EQUIPMENT,
                "status": ResourceStatus.IN_USE,
                "quantity": 2.0,
                "unit": "units",
                "unit_cost": 150000.0,
                "supplier": "Heavy Equipment Rentals"
            },
            {
                "project_id": projects[0].id,
                "name": "Construction Workers",
                "resource_type": ResourceType.LABOR,
                "status": ResourceStatus.AVAILABLE,
                "quantity": 50.0,
                "unit": "workers",
                "unit_cost": 2500.0,
                "supplier": "BuildForce Agency"
            }
        ]
        
        resources_project2 = [
            {
                "project_id": projects[1].id,
                "name": "High-Grade Concrete M400",
                "resource_type": ResourceType.MATERIAL,
                "status": ResourceStatus.IN_USE,
                "quantity": 8000.0,
                "unit": "m³",
                "unit_cost": 15000.0,
                "supplier": "Premium Concrete Co"
            },
            {
                "project_id": projects[1].id,
                "name": "Excavator CAT 320",
                "resource_type": ResourceType.EQUIPMENT,
                "status": ResourceStatus.IN_USE,
                "quantity": 3.0,
                "unit": "units",
                "unit_cost": 80000.0,
                "supplier": "Heavy Machinery Rental"
            }
        ]
        
        all_resources = resources_project1 + resources_project2
        for resource_data in all_resources:
            resource = Resource(**resource_data)
            resource.calculate_total_cost()
            db.add(resource)
        
        db.commit()
        print(f"✅ Created {len(all_resources)} resources")
        
        # Create Budget entries
        budgets = [
            # Project 1
            {
                "project_id": projects[0].id,
                "category": "Materials",
                "description": "Concrete, steel, bricks, etc.",
                "planned_amount": 3500000.0,
                "actual_amount": 1800000.0
            },
            {
                "project_id": projects[0].id,
                "category": "Labor",
                "description": "Construction workers, engineers",
                "planned_amount": 2500000.0,
                "actual_amount": 950000.0
            },
            {
                "project_id": projects[0].id,
                "category": "Equipment",
                "description": "Cranes, excavators, tools",
                "planned_amount": 1500000.0,
                "actual_amount": 450000.0
            },
            {
                "project_id": projects[0].id,
                "category": "Permits and Insurance",
                "description": "Legal and safety requirements",
                "planned_amount": 500000.0,
                "actual_amount": 0.0
            },
            # Project 2
            {
                "project_id": projects[1].id,
                "category": "Materials",
                "description": "Premium construction materials",
                "planned_amount": 6000000.0,
                "actual_amount": 2100000.0
            },
            {
                "project_id": projects[1].id,
                "category": "Labor",
                "description": "Specialized construction teams",
                "planned_amount": 4500000.0,
                "actual_amount": 1500000.0
            },
            {
                "project_id": projects[1].id,
                "category": "Equipment",
                "description": "Heavy machinery and tools",
                "planned_amount": 2500000.0,
                "actual_amount": 900000.0
            }
        ]
        
        for budget_data in budgets:
            budget = Budget(**budget_data)
            db.add(budget)
        
        db.commit()
        print(f"✅ Created {len(budgets)} budget entries")
        
        print("\n🎉 Database seeding completed successfully!")
        print(f"📊 Summary:")
        print(f"   - Projects: {len(projects)}")
        print(f"   - Tasks: {len(all_tasks)}")
        print(f"   - Resources: {len(all_resources)}")
        print(f"   - Budget Entries: {len(budgets)}")
        
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
```

# File: ./backend/app/models/resource.py

```python
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.database import Base


class ResourceType(str, enum.Enum):
    MATERIAL = "material"
    EQUIPMENT = "equipment"
    LABOR = "labor"


class ResourceStatus(str, enum.Enum):
    AVAILABLE = "available"
    IN_USE = "in_use"
    DEPLETED = "depleted"
    MAINTENANCE = "maintenance"


class Resource(Base):
    __tablename__ = "resources"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    
    name = Column(String(255), nullable=False)
    resource_type = Column(Enum(ResourceType), nullable=False)
    status = Column(Enum(ResourceStatus), default=ResourceStatus.AVAILABLE)
    
    quantity = Column(Float, default=0.0)
    unit = Column(String(50))  # kg, m3, hours, pieces, etc.
    
    unit_cost = Column(Float, default=0.0)
    total_cost = Column(Float, default=0.0)
    
    supplier = Column(String(255))
    
    allocated_date = Column(DateTime, default=datetime.utcnow)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    project = relationship("Project", back_populates="resources")
    
    def calculate_total_cost(self):
        self.total_cost = self.quantity * self.unit_cost
        return self.total_cost
```

# File: ./backend/app/models/project.py

```python
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.database import Base


class ProjectStatus(str, enum.Enum):
    PLANNING = "planning"
    IN_PROGRESS = "in_progress"
    ON_HOLD = "on_hold"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    status = Column(Enum(ProjectStatus), default=ProjectStatus.PLANNING)
    
    start_date = Column(DateTime)
    planned_end_date = Column(DateTime)
    actual_end_date = Column(DateTime, nullable=True)
    
    total_budget = Column(Float, default=0.0)
    spent_amount = Column(Float, default=0.0)
    
    location = Column(String(255))
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")
    resources = relationship("Resource", back_populates="project", cascade="all, delete-orphan")
    budgets = relationship("Budget", back_populates="project", cascade="all, delete-orphan")
    
    @property
    def budget_utilization(self):
        if self.total_budget == 0:
            return 0
        return (self.spent_amount / self.total_budget) * 100
    
    @property
    def remaining_budget(self):
        return self.total_budget - self.spent_amount
```

# File: ./backend/app/models/__init__.py

```python
from app.models.project import Project, ProjectStatus
from app.models.task import Task, TaskStatus, TaskPriority
from app.models.resource import Resource, ResourceType, ResourceStatus
from app.models.budget import Budget

__all__ = [
    "Project", "ProjectStatus",
    "Task", "TaskStatus", "TaskPriority",
    "Resource", "ResourceType", "ResourceStatus",
    "Budget"
]
```

# File: ./backend/app/models/task.py

```python
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.database import Base


class TaskStatus(str, enum.Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    DELAYED = "delayed"
    BLOCKED = "blocked"


class TaskPriority(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    
    name = Column(String(255), nullable=False)
    description = Column(Text)
    status = Column(Enum(TaskStatus), default=TaskStatus.NOT_STARTED)
    priority = Column(Enum(TaskPriority), default=TaskPriority.MEDIUM)
    
    start_date = Column(DateTime)
    planned_end_date = Column(DateTime)
    actual_end_date = Column(DateTime, nullable=True)
    
    progress_percentage = Column(Float, default=0.0)
    
    assigned_to = Column(String(255))
    
    depends_on_task_id = Column(Integer, ForeignKey("tasks.id"), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    project = relationship("Project", back_populates="tasks")
    dependencies = relationship("Task", remote_side=[id])
    
    @property
    def is_overdue(self):
        if self.status != TaskStatus.COMPLETED and self.planned_end_date:
            return datetime.utcnow() > self.planned_end_date
        return False
```

# File: ./backend/app/models/budget.py

```python
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Budget(Base):
    __tablename__ = "budgets"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    
    category = Column(String(255), nullable=False)  # Materials, Labor, Equipment, etc.
    description = Column(Text)
    
    planned_amount = Column(Float, default=0.0)
    actual_amount = Column(Float, default=0.0)
    
    budget_date = Column(DateTime, default=datetime.utcnow)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    project = relationship("Project", back_populates="budgets")
    
    @property
    def variance(self):
        return self.planned_amount - self.actual_amount
    
    @property
    def variance_percentage(self):
        if self.planned_amount == 0:
            return 0
        return (self.variance / self.planned_amount) * 100
```

# File: ./backend/app/schemas/resource.py

```python
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.resource import ResourceType, ResourceStatus


class ResourceBase(BaseModel):
    project_id: int
    name: str = Field(..., min_length=1, max_length=255)
    resource_type: ResourceType
    status: ResourceStatus = ResourceStatus.AVAILABLE
    quantity: float = Field(default=0.0, ge=0)
    unit: Optional[str] = Field(None, max_length=50)
    unit_cost: float = Field(default=0.0, ge=0)
    supplier: Optional[str] = None


class ResourceCreate(ResourceBase):
    pass


class ResourceUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    resource_type: Optional[ResourceType] = None
    status: Optional[ResourceStatus] = None
    quantity: Optional[float] = Field(None, ge=0)
    unit: Optional[str] = Field(None, max_length=50)
    unit_cost: Optional[float] = Field(None, ge=0)
    supplier: Optional[str] = None


class ResourceResponse(ResourceBase):
    id: int
    total_cost: float
    allocated_date: datetime
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
```

# File: ./backend/app/schemas/project.py

```python
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.project import ProjectStatus


class ProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    status: ProjectStatus = ProjectStatus.PLANNING
    start_date: Optional[datetime] = None
    planned_end_date: Optional[datetime] = None
    total_budget: float = Field(default=0.0, ge=0)
    location: Optional[str] = None


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    status: Optional[ProjectStatus] = None
    start_date: Optional[datetime] = None
    planned_end_date: Optional[datetime] = None
    actual_end_date: Optional[datetime] = None
    total_budget: Optional[float] = Field(None, ge=0)
    spent_amount: Optional[float] = Field(None, ge=0)
    location: Optional[str] = None


class ProjectResponse(ProjectBase):
    id: int
    spent_amount: float
    actual_end_date: Optional[datetime] = None
    budget_utilization: float
    remaining_budget: float
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ProjectSummary(BaseModel):
    id: int
    name: str
    status: ProjectStatus
    budget_utilization: float
    progress: float = 0.0
    
    class Config:
        from_attributes = True
```

# File: ./backend/app/schemas/__init__.py

```python
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse, ProjectSummary
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.schemas.resource import ResourceCreate, ResourceUpdate, ResourceResponse
from app.schemas.budget import BudgetCreate, BudgetUpdate, BudgetResponse

__all__ = [
    "ProjectCreate", "ProjectUpdate", "ProjectResponse", "ProjectSummary",
    "TaskCreate", "TaskUpdate", "TaskResponse",
    "ResourceCreate", "ResourceUpdate", "ResourceResponse",
    "BudgetCreate", "BudgetUpdate", "BudgetResponse"
]
```

# File: ./backend/app/schemas/task.py

```python
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.task import TaskStatus, TaskPriority


class TaskBase(BaseModel):
    project_id: int
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.NOT_STARTED
    priority: TaskPriority = TaskPriority.MEDIUM
    start_date: Optional[datetime] = None
    planned_end_date: Optional[datetime] = None
    progress_percentage: float = Field(default=0.0, ge=0, le=100)
    assigned_to: Optional[str] = None
    depends_on_task_id: Optional[int] = None


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    start_date: Optional[datetime] = None
    planned_end_date: Optional[datetime] = None
    actual_end_date: Optional[datetime] = None
    progress_percentage: Optional[float] = Field(None, ge=0, le=100)
    assigned_to: Optional[str] = None
    depends_on_task_id: Optional[int] = None


class TaskResponse(TaskBase):
    id: int
    actual_end_date: Optional[datetime] = None
    is_overdue: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
```

# File: ./backend/app/schemas/budget.py

```python
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class BudgetBase(BaseModel):
    project_id: int
    category: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    planned_amount: float = Field(default=0.0, ge=0)
    actual_amount: float = Field(default=0.0, ge=0)


class BudgetCreate(BudgetBase):
    pass


class BudgetUpdate(BaseModel):
    category: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    planned_amount: Optional[float] = Field(None, ge=0)
    actual_amount: Optional[float] = Field(None, ge=0)


class BudgetResponse(BudgetBase):
    id: int
    variance: float
    variance_percentage: float
    budget_date: datetime
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
```

# File: ./backend/app/routes/tasks.py

```python
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models.task import Task, TaskStatus
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.auth.dependencies import get_current_user, require_role

router = APIRouter()

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db)
):
    db_task = Task(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


@router.get("/", response_model=List[TaskResponse])
async def get_tasks(
    project_id: Optional[int] = Query(None),
    status: Optional[TaskStatus] = Query(None),
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    query = db.query(Task)
    
    if project_id:
        query = query.filter(Task.project_id == project_id)
    if status:
        query = query.filter(Task.status == status)
    
    return query.offset(skip).limit(limit).all()


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    return task


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_update: TaskUpdate,
    db: Session = Depends(get_db)
):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    
    update_data = task_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_task, field, value)
    
    db.commit()
    db.refresh(db_task)
    return db_task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    
    db.delete(db_task)
    db.commit()
    return None


@router.get("/project/{project_id}/overdue", response_model=List[TaskResponse])
async def get_overdue_tasks(
    project_id: int,
    db: Session = Depends(get_db)
):
    from datetime import datetime
    tasks = db.query(Task).filter(
        Task.project_id == project_id,
        Task.status != TaskStatus.COMPLETED,
        Task.planned_end_date < datetime.utcnow()
    ).all()
    return tasks

def check_task_access(current_user: dict, task: Task) -> bool:
    """Check if user has access to this task"""
    if current_user["role"] == "admin":
        return True
    elif current_user["role"] == "manager":
        managed_projects = current_user.get("managed_projects", [])
        return task.project_id in managed_projects
    elif current_user["role"] == "worker":
        return task.assigned_to == current_user.get("worker_name")
    return False


@router.get("/", response_model=List[TaskResponse])
async def get_tasks(
    project_id: Optional[int] = Query(None),
    status: Optional[TaskStatus] = Query(None),
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Get tasks filtered by user role"""
    query = db.query(Task)
    
    # Filter based on user role
    if current_user["role"] == "worker":
        # Workers see only their assigned tasks
        worker_name = current_user.get("worker_name")
        query = query.filter(Task.assigned_to == worker_name)
    elif current_user["role"] == "manager":
        # Managers see tasks from their projects
        managed_projects = current_user.get("managed_projects", [])
        query = query.filter(Task.project_id.in_(managed_projects))
    
    if project_id:
        query = query.filter(Task.project_id == project_id)
    if status:
        query = query.filter(Task.status == status)
    
    return query.offset(skip).limit(limit).all()


@router.post(
    "/",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_role("admin", "manager"))],
)
async def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    # Check manager permissions
    if current_user["role"] == "manager":
        managed_projects = current_user.get("managed_projects", [])
        if task.project_id not in managed_projects:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only create tasks for your managed projects",
            )
    
    db_task = Task(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_update: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Update task - role-based permissions"""
    db_task = db.query(Task).filter(Task.id == task_id).first()
    
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found",
        )
    
    if not check_task_access(current_user, db_task):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this task",
        )
    
    # Workers can only update specific fields
    if current_user["role"] == "worker":
        allowed_fields = {"status", "progress_percentage", "actual_end_date"}
        update_data = task_update.model_dump(
            exclude_unset=True, include=allowed_fields
        )
    else:
        update_data = task_update.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(db_task, field, value)
    
    db.commit()
    db.refresh(db_task)
    return db_task


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_role("admin", "manager"))],
)
async def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Delete task - admin and manager only"""
    db_task = db.query(Task).filter(Task.id == task_id).first()
    
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found",
        )
    
    if current_user["role"] == "manager":
        managed_projects = current_user.get("managed_projects", [])
        if db_task.project_id not in managed_projects:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only delete tasks from your managed projects",
            )
    
    db.delete(db_task)
    db.commit()
    return None
```

# File: ./backend/app/routes/projects.py

```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.project import Project
from app.schemas.project import (
    ProjectCreate,
    ProjectUpdate,
    ProjectResponse,
    ProjectSummary,
)
from app.services.project_service import ProjectService
from app.auth.dependencies import get_current_user, require_role

router = APIRouter()


@router.post(
    "/",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_role("admin"))],
)
async def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    service = ProjectService(db)
    return service.create_project(project)


@router.get("/", response_model=List[ProjectResponse])
async def get_projects(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Get projects based on user role"""
    service = ProjectService(db)
    
    # Managers see only their assigned projects
    if current_user["role"] == "manager":
        managed_project_ids = current_user.get("managed_projects", [])
        projects = service.get_projects(skip=skip, limit=limit)
        return [p for p in projects if p.id in managed_project_ids]
    
    # Admin and workers see all projects
    return service.get_projects(skip=skip, limit=limit)


@router.get("/summary", response_model=List[ProjectSummary])
async def get_projects_summary(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    service = ProjectService(db)
    summaries = service.get_projects_summary()
    
    if current_user["role"] == "manager":
        managed_project_ids = current_user.get("managed_projects", [])
        return [s for s in summaries if s["id"] in managed_project_ids]
    
    return summaries


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    service = ProjectService(db)
    project = service.get_project_by_id(project_id)
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with id {project_id} not found",
        )
    
    # Check manager permissions
    if current_user["role"] == "manager":
        managed_project_ids = current_user.get("managed_projects", [])
        if project_id not in managed_project_ids:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have access to this project",
            )
    
    return project


@router.put(
    "/{project_id}",
    response_model=ProjectResponse,
    dependencies=[Depends(require_role("admin", "manager"))],
)
async def update_project(
    project_id: int,
    project_update: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    # Check manager permissions
    if current_user["role"] == "manager":
        managed_project_ids = current_user.get("managed_projects", [])
        if project_id not in managed_project_ids:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have access to this project",
            )
    
    service = ProjectService(db)
    project = service.update_project(project_id, project_update)
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with id {project_id} not found",
        )
    
    return project


@router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_role("admin"))],  # Admin only
)
async def delete_project(project_id: int, db: Session = Depends(get_db)):
    service = ProjectService(db)
    success = service.delete_project(project_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with id {project_id} not found",
        )
    
    return None
```

# File: ./backend/app/routes/auth.py

```python
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from datetime import timedelta
from app.auth.demo_users import authenticate_user
from app.auth.jwt_handler import create_access_token
from app.auth.dependencies import get_current_user
from app.config import settings

router = APIRouter()


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: dict


@router.post("/login", response_model=LoginResponse)
async def login(credentials: LoginRequest):
    """Login endpoint - authenticate user and return JWT token"""
    user = authenticate_user(credentials.username, credentials.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    access_token = create_access_token(
        data={"sub": user["username"], "role": user["role"]},
        expires_delta=access_token_expires,
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user,
    }


@router.get("/me")
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """Get current authenticated user information"""
    return current_user


@router.get("/demo-users")
async def get_demo_users():
    """Get list of demo users for login page (for presentation purposes)"""
    from app.auth.demo_users import DEMO_USERS, _DEMO_USER_PASSWORDS
    
    demo_info = []
    for username, user_data in DEMO_USERS.items():
        # Get the actual password from the password dict
        actual_password = _DEMO_USER_PASSWORDS.get(username, "")
        demo_info.append({
            "username": username,
            "role": user_data["role"],
            "name": user_data["name"],
            "hint": f"Password: {actual_password}"
        })
    
    return demo_info
```

# File: ./backend/app/routes/import_data.py

```python
from fastapi import (
    APIRouter,
    Depends,
    UploadFile,
    File,
    HTTPException,
    status,
)
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.import_service import ImportService
from app.config import settings
from app.auth.dependencies import require_role

router = APIRouter()


@router.post("/excel", dependencies=[Depends(require_role("admin"))])
async def import_from_excel(
    file: UploadFile = File(...), db: Session = Depends(get_db)
):
    """Import from Excel - admin only"""
    if not any(
        file.filename.endswith(ext) for ext in settings.allowed_extensions_set
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type. Allowed: {', '.join(settings.allowed_extensions_set)}",
        )
    
    contents = await file.read()
    if len(contents) > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File too large. Max size: {settings.MAX_UPLOAD_SIZE / (1024*1024)}MB",
        )
    
    service = ImportService(db)
    try:
        result = service.import_from_excel(contents, file.filename)
        return {"message": "Import successful", "stats": result}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Import failed: {str(e)}",
        )


@router.post("/csv", dependencies=[Depends(require_role("admin"))])
async def import_from_csv(
    file: UploadFile = File(...), db: Session = Depends(get_db)
):
    """Import from CSV - admin only"""
    if not file.filename.endswith(".csv"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Only CSV files allowed",
        )
    
    contents = await file.read()
    if len(contents) > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File too large. Max size: {settings.MAX_UPLOAD_SIZE / (1024*1024)}MB",
        )
    
    service = ImportService(db)
    try:
        result = service.import_from_csv(contents)
        return {"message": "Import successful", "stats": result}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Import failed: {str(e)}",
        )
```

# File: ./backend/app/routes/__init__.py

```python
from . import auth, projects, resources, tasks, budgets, analytics, import_data

__all__ = ["auth", "projects", "resources", "tasks", "budgets", "analytics", "import_data"]
```

# File: ./backend/app/routes/budgets.py

```python
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models.budget import Budget
from app.schemas.budget import BudgetCreate, BudgetUpdate, BudgetResponse
from app.auth.dependencies import get_current_user, require_role

router = APIRouter()


@router.post(
    "/",
    response_model=BudgetResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_role("admin", "manager"))],
)
async def create_budget(
    budget: BudgetCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Create budget - admin and manager only"""
    # Check manager permissions
    if current_user["role"] == "manager":
        managed_projects = current_user.get("managed_projects", [])
        if budget.project_id not in managed_projects:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only create budgets for your managed projects",
            )
    
    db_budget = Budget(**budget.model_dump())
    db.add(db_budget)
    db.commit()
    db.refresh(db_budget)
    return db_budget


@router.get("/", response_model=List[BudgetResponse])
async def get_budgets(
    project_id: Optional[int] = Query(None),
    category: Optional[str] = Query(None),
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Get budgets filtered by user role"""
    query = db.query(Budget)
    
    # Filter based on user role
    if current_user["role"] == "manager":
        managed_projects = current_user.get("managed_projects", [])
        query = query.filter(Budget.project_id.in_(managed_projects))
    elif current_user["role"] == "worker":
        # Workers can't access budgets - return empty
        return []
    
    if project_id:
        query = query.filter(Budget.project_id == project_id)
    if category:
        query = query.filter(Budget.category.ilike(f"%{category}%"))
    
    return query.offset(skip).limit(limit).all()


@router.get("/{budget_id}", response_model=BudgetResponse)
async def get_budget(
    budget_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Get single budget"""
    budget = db.query(Budget).filter(Budget.id == budget_id).first()
    
    if not budget:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Budget with id {budget_id} not found",
        )
    
    # Check permissions
    if current_user["role"] == "manager":
        managed_projects = current_user.get("managed_projects", [])
        if budget.project_id not in managed_projects:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have access to this budget",
            )
    elif current_user["role"] == "worker":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Workers cannot access budget details",
        )
    
    return budget


@router.put(
    "/{budget_id}",
    response_model=BudgetResponse,
    dependencies=[Depends(require_role("admin", "manager"))],
)
async def update_budget(
    budget_id: int,
    budget_update: BudgetUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Update budget - admin and manager only"""
    db_budget = db.query(Budget).filter(Budget.id == budget_id).first()
    
    if not db_budget:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Budget with id {budget_id} not found",
        )
    
    # Check manager permissions
    if current_user["role"] == "manager":
        managed_projects = current_user.get("managed_projects", [])
        if db_budget.project_id not in managed_projects:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only update budgets in your managed projects",
            )
    
    update_data = budget_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_budget, field, value)
    
    db.commit()
    db.refresh(db_budget)
    return db_budget


@router.delete(
    "/{budget_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_role("admin", "manager"))],
)
async def delete_budget(
    budget_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Delete budget - admin and manager only"""
    db_budget = db.query(Budget).filter(Budget.id == budget_id).first()
    
    if not db_budget:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Budget with id {budget_id} not found",
        )
    
    # Check manager permissions
    if current_user["role"] == "manager":
        managed_projects = current_user.get("managed_projects", [])
        if db_budget.project_id not in managed_projects:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only delete budgets from your managed projects",
            )
    
    db.delete(db_budget)
    db.commit()
    return None
```

# File: ./backend/app/routes/users.py

```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.auth.dependencies import require_role, get_current_user
from app.auth.demo_users import DEMO_USERS, get_user_by_username
from passlib.context import CryptContext

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.get("/", dependencies=[Depends(require_role("admin"))])
async def get_all_users(db: Session = Depends(get_db)):
    users = []
    for username, user_data in DEMO_USERS.items():
        user_copy = user_data.copy()
        user_copy.pop("password_hash", None)
        user_copy["username"] = username
        users.append(user_copy)
    return users


@router.get("/profile")
async def get_user_profile(current_user: dict = Depends(get_current_user)):
    return current_user


@router.put("/profile")
async def update_user_profile(
    profile_data: dict,
    current_user: dict = Depends(get_current_user),
):
    updated_user = current_user.copy()
    
    allowed_fields = ["name", "email"]
    for field in allowed_fields:
        if field in profile_data:
            updated_user[field] = profile_data[field]
    
    return updated_user


@router.get("/team", dependencies=[Depends(require_role("admin", "manager"))])
async def get_team_members(
    current_user: dict = Depends(get_current_user),
):
    """Get team members based on role"""
    if current_user["role"] == "admin":
        team = []
        for username, user_data in DEMO_USERS.items():
            user_copy = user_data.copy()
            user_copy.pop("password_hash", None)
            user_copy["username"] = username
            team.append(user_copy)
        return team
    elif current_user["role"] == "manager":
        managed_projects = current_user.get("managed_projects", [])
        team = []
        for username, user_data in DEMO_USERS.items():
            if user_data["role"] == "worker":
                user_copy = user_data.copy()
                user_copy.pop("password_hash", None)
                user_copy["username"] = username
                team.append(user_copy)
        return team
    
    return []


@router.get("/activity-log", dependencies=[Depends(require_role("admin"))])
async def get_activity_log(
    limit: int = 50,
    db: Session = Depends(get_db),
):
    return {
        "message": "Activity logging not yet implemented",
        "activities": []
    }
```

# File: ./backend/app/routes/analytics.py

```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.analytics_service import AnalyticsService
from app.auth.dependencies import get_current_user

router = APIRouter()

@router.get("/dashboard")
async def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    service = AnalyticsService(db)
    
    if current_user["role"] == "manager":
        managed_projects = current_user.get("managed_projects", [])
        stats = service.get_manager_dashboard_stats(managed_projects)
    elif current_user["role"] == "worker":
        worker_name = current_user.get("worker_name")
        stats = service.get_worker_dashboard_stats(worker_name)
    else:
        stats = service.get_dashboard_stats()
    
    return stats


@router.get("/team-performance")
async def get_team_performance(
    project_id: int = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    if current_user["role"] == "worker":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Workers cannot access team performance data"
        )
    
    if current_user["role"] == "manager" and project_id:
        managed_projects = current_user.get("managed_projects", [])
        if project_id not in managed_projects:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have access to this project"
            )
    
    service = AnalyticsService(db)
    return service.get_team_performance(project_id)


@router.get("/project/{project_id}/kpi")
async def get_project_kpi(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    if current_user["role"] == "manager":
        managed_projects = current_user.get("managed_projects", [])
        if project_id not in managed_projects:
            from fastapi import HTTPException, status
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have access to this project",
            )
    
    service = AnalyticsService(db)
    return service.get_project_kpi(project_id)


@router.get("/project/{project_id}/budget-breakdown")
async def get_budget_breakdown(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Get budget breakdown - admin and manager only"""
    if current_user["role"] == "worker":
        from fastapi import HTTPException, status
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Workers cannot access budget information",
        )
    
    # Check manager permissions
    if current_user["role"] == "manager":
        managed_projects = current_user.get("managed_projects", [])
        if project_id not in managed_projects:
            from fastapi import HTTPException, status
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have access to this project",
            )
    
    service = AnalyticsService(db)
    return service.get_budget_breakdown(project_id)


@router.get("/project/{project_id}/resource-distribution")
async def get_resource_distribution(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Get resource distribution - admin and manager only"""
    if current_user["role"] == "worker":
        from fastapi import HTTPException, status
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Workers cannot access resource information",
        )
    
    # Check manager permissions
    if current_user["role"] == "manager":
        managed_projects = current_user.get("managed_projects", [])
        if project_id not in managed_projects:
            from fastapi import HTTPException, status
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have access to this project",
            )
    
    service = AnalyticsService(db)
    return service.get_resource_distribution(project_id)


@router.get("/project/{project_id}/timeline")
async def get_project_timeline(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Get project timeline with milestones"""
    # Check manager permissions
    if current_user["role"] == "manager":
        managed_projects = current_user.get("managed_projects", [])
        if project_id not in managed_projects:
            from fastapi import HTTPException, status
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have access to this project",
            )
    
    service = AnalyticsService(db)
    return service.get_project_timeline(project_id)


@router.get("/project/{project_id}/predict-completion")
async def predict_completion(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Predict project completion date and cost using ML"""
    # Check manager permissions
    if current_user["role"] == "manager":
        managed_projects = current_user.get("managed_projects", [])
        if project_id not in managed_projects:
            from fastapi import HTTPException, status
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have access to this project",
            )
    
    service = AnalyticsService(db)
    return service.predict_completion(project_id)
```

# File: ./backend/app/routes/resources.py

```python
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models.resource import Resource, ResourceType
from app.schemas.resource import (
    ResourceCreate,
    ResourceUpdate,
    ResourceResponse,
)
from app.auth.dependencies import get_current_user, require_role

router = APIRouter()


@router.post(
    "/",
    response_model=ResourceResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_role("admin", "manager"))],
)
async def create_resource(
    resource: ResourceCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Create resource - admin and manager only"""
    # Check manager permissions
    if current_user["role"] == "manager":
        managed_projects = current_user.get("managed_projects", [])
        if resource.project_id not in managed_projects:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only create resources for your managed projects",
            )
    
    db_resource = Resource(**resource.model_dump())
    db_resource.calculate_total_cost()
    db.add(db_resource)
    db.commit()
    db.refresh(db_resource)
    return db_resource


@router.get("/", response_model=List[ResourceResponse])
async def get_resources(
    project_id: Optional[int] = Query(None),
    resource_type: Optional[ResourceType] = Query(None),
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Get resources filtered by user role"""
    query = db.query(Resource)
    
    if current_user["role"] == "manager":
        managed_projects = current_user.get("managed_projects", [])
        query = query.filter(Resource.project_id.in_(managed_projects))
    elif current_user["role"] == "worker":
        return []
    
    if project_id:
        query = query.filter(Resource.project_id == project_id)
    if resource_type:
        query = query.filter(Resource.resource_type == resource_type)
    
    return query.offset(skip).limit(limit).all()


@router.get("/{resource_id}", response_model=ResourceResponse)
async def get_resource(
    resource_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Get single resource"""
    resource = db.query(Resource).filter(Resource.id == resource_id).first()
    
    if not resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resource with id {resource_id} not found",
        )
    
    # Check permissions
    if current_user["role"] == "manager":
        managed_projects = current_user.get("managed_projects", [])
        if resource.project_id not in managed_projects:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have access to this resource",
            )
    elif current_user["role"] == "worker":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Workers cannot access resource details",
        )
    
    return resource


@router.put(
    "/{resource_id}",
    response_model=ResourceResponse,
    dependencies=[Depends(require_role("admin", "manager"))],
)
async def update_resource(
    resource_id: int,
    resource_update: ResourceUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Update resource - admin and manager only"""
    db_resource = (
        db.query(Resource).filter(Resource.id == resource_id).first()
    )
    
    if not db_resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resource with id {resource_id} not found",
        )
    
    # Check manager permissions
    if current_user["role"] == "manager":
        managed_projects = current_user.get("managed_projects", [])
        if db_resource.project_id not in managed_projects:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only update resources in your managed projects",
            )
    
    update_data = resource_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_resource, field, value)
    
    db_resource.calculate_total_cost()
    db.commit()
    db.refresh(db_resource)
    return db_resource


@router.delete(
    "/{resource_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_role("admin", "manager"))],
)
async def delete_resource(
    resource_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Delete resource - admin and manager only"""
    db_resource = (
        db.query(Resource).filter(Resource.id == resource_id).first()
    )
    
    if not db_resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resource with id {resource_id} not found",
        )
    
    # Check manager permissions
    if current_user["role"] == "manager":
        managed_projects = current_user.get("managed_projects", [])
        if db_resource.project_id not in managed_projects:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only delete resources from your managed projects",
            )
    
    db.delete(db_resource)
    db.commit()
    return None
```

# File: ./backend/app/services/project_service.py

```python
from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.project import Project
from app.models.task import Task, TaskStatus
from app.schemas.project import ProjectCreate, ProjectUpdate
from datetime import datetime


class ProjectService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_project(self, project: ProjectCreate) -> Project:
        db_project = Project(**project.model_dump())
        self.db.add(db_project)
        self.db.commit()
        self.db.refresh(db_project)
        return db_project
    
    def get_projects(self, skip: int = 0, limit: int = 10) -> List[Project]:
        return self.db.query(Project).offset(skip).limit(limit).all()
    
    def get_project_by_id(self, project_id: int) -> Optional[Project]:
        return self.db.query(Project).filter(Project.id == project_id).first()
    
    def update_project(self, project_id: int, project_update: ProjectUpdate) -> Optional[Project]:
        db_project = self.get_project_by_id(project_id)
        if not db_project:
            return None
        
        update_data = project_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_project, field, value)
        
        db_project.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(db_project)
        return db_project
    
    def delete_project(self, project_id: int) -> bool:
        db_project = self.get_project_by_id(project_id)
        if not db_project:
            return False
        
        self.db.delete(db_project)
        self.db.commit()
        return True
    
    def get_projects_summary(self) -> List[dict]:
        """Get projects summary + progress"""
        projects = self.db.query(Project).all()
        summaries = []
        
        for project in projects:
            # Calculate progress based on completed tasks
            total_tasks = self.db.query(Task).filter(Task.project_id == project.id).count()
            completed_tasks = self.db.query(Task).filter(
                Task.project_id == project.id,
                Task.status == TaskStatus.COMPLETED
            ).count()
            
            progress = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
            
            summaries.append({
                "id": project.id,
                "name": project.name,
                "status": project.status,
                "budget_utilization": project.budget_utilization,
                "progress": round(progress, 2)
            })
        
        return summaries
```

# File: ./backend/app/services/__init__.py

```python
from app.services.project_service import ProjectService
from app.services.analytics_service import AnalyticsService  
from app.services.import_service import ImportService

__all__ = ["ProjectService", "AnalyticsService", "ImportService"]
```

# File: ./backend/app/services/analytics_service.py

```python
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.project import Project, ProjectStatus
from app.models.task import Task, TaskStatus
from app.models.resource import Resource, ResourceType
from app.models.budget import Budget
from datetime import datetime, timedelta
from typing import Dict, List


class AnalyticsService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_dashboard_stats(self) -> Dict:
        total_projects = self.db.query(Project).count()
        active_projects = self.db.query(Project).filter(
            Project.status == ProjectStatus.IN_PROGRESS
        ).count()
        
        total_budget = self.db.query(func.sum(Project.total_budget)).scalar() or 0
        total_spent = self.db.query(func.sum(Project.spent_amount)).scalar() or 0
        
        total_tasks = self.db.query(Task).count()
        completed_tasks = self.db.query(Task).filter(
            Task.status == TaskStatus.COMPLETED
        ).count()
        overdue_tasks = self.db.query(Task).filter(
            Task.status != TaskStatus.COMPLETED,
            Task.planned_end_date < datetime.utcnow()
        ).count()
        
        return {
            "total_projects": total_projects,
            "active_projects": active_projects,
            "completed_projects": self.db.query(Project).filter(
                Project.status == ProjectStatus.COMPLETED
            ).count(),
            "total_budget": round(total_budget, 2),
            "total_spent": round(total_spent, 2),
            "budget_utilization": round((total_spent / total_budget * 100) if total_budget > 0 else 0, 2),
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "overdue_tasks": overdue_tasks,
            "task_completion_rate": round((completed_tasks / total_tasks * 100) if total_tasks > 0 else 0, 2)
        }
    
    def get_project_kpi(self, project_id: int) -> Dict:
        """Get KPIs for a specific project"""
        project = self.db.query(Project).filter(Project.id == project_id).first()
        if not project:
            return {}
        
        tasks = self.db.query(Task).filter(Task.project_id == project_id).all()
        total_tasks = len(tasks)
        completed_tasks = len([t for t in tasks if t.status == TaskStatus.COMPLETED])
        overdue_tasks = len([t for t in tasks if t.is_overdue])
        
        resources = self.db.query(Resource).filter(Resource.project_id == project_id).all()
        total_resource_cost = sum(r.total_cost for r in resources)
        
        return {
            "project_name": project.name,
            "status": project.status.value,
            "progress": round((completed_tasks / total_tasks * 100) if total_tasks > 0 else 0, 2),
            "budget_total": project.total_budget,
            "budget_spent": project.spent_amount,
            "budget_remaining": project.remaining_budget,
            "budget_utilization": round(project.budget_utilization, 2),
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "in_progress_tasks": len([t for t in tasks if t.status == TaskStatus.IN_PROGRESS]),
            "overdue_tasks": overdue_tasks,
            "total_resources": len(resources),
            "resource_cost": round(total_resource_cost, 2),
            "start_date": project.start_date.isoformat() if project.start_date else None,
            "planned_end": project.planned_end_date.isoformat() if project.planned_end_date else None,
            "actual_end": project.actual_end_date.isoformat() if project.actual_end_date else None
        }
    
    def get_budget_breakdown(self, project_id: int) -> List[Dict]:
        """Get budget breakdown by category"""
        budgets = self.db.query(Budget).filter(Budget.project_id == project_id).all()
        
        breakdown = []
        for budget in budgets:
            breakdown.append({
                "category": budget.category,
                "planned": budget.planned_amount,
                "actual": budget.actual_amount,
                "variance": budget.variance,
                "variance_percentage": round(budget.variance_percentage, 2)
            })
        
        return breakdown
    
    def get_resource_distribution(self, project_id: int) -> Dict:
        """Get resource distribution by type"""
        resources = self.db.query(Resource).filter(Resource.project_id == project_id).all()
        
        distribution = {
            ResourceType.MATERIAL.value: {"count": 0, "total_cost": 0},
            ResourceType.EQUIPMENT.value: {"count": 0, "total_cost": 0},
            ResourceType.LABOR.value: {"count": 0, "total_cost": 0}
        }
        
        for resource in resources:
            dist_key = resource.resource_type.value
            distribution[dist_key]["count"] += 1
            distribution[dist_key]["total_cost"] += resource.total_cost
        
        return distribution
    
    def get_project_timeline(self, project_id: int) -> Dict:
        project = self.db.query(Project).filter(Project.id == project_id).first()
        if not project:
            return {}
        
        tasks = self.db.query(Task).filter(Task.project_id == project_id).order_by(Task.start_date).all()
        
        timeline = []
        for task in tasks:
            timeline.append({
                "id": task.id,
                "name": task.name,
                "status": task.status.value,
                "start_date": task.start_date.isoformat() if task.start_date else None,
                "planned_end": task.planned_end_date.isoformat() if task.planned_end_date else None,
                "actual_end": task.actual_end_date.isoformat() if task.actual_end_date else None,
                "progress": task.progress_percentage,
                "is_overdue": task.is_overdue
            })
        
        return {
            "project_name": project.name,
            "project_start": project.start_date.isoformat() if project.start_date else None,
            "project_end": project.planned_end_date.isoformat() if project.planned_end_date else None,
            "tasks": timeline
        }
    
    def predict_completion(self, project_id: int) -> Dict:
        """Simple prediction of completion date and cost"""
        project = self.db.query(Project).filter(Project.id == project_id).first()
        if not project:
            return {}
        
        tasks = self.db.query(Task).filter(Task.project_id == project_id).all()
        completed = len([t for t in tasks if t.status == TaskStatus.COMPLETED])
        total = len(tasks)
        
        if total == 0 or completed == 0:
            return {
                "predicted_completion_date": None,
                "predicted_total_cost": project.total_budget,
                "confidence": "low"
            }
        
        # Simple linear projection
        progress_rate = completed / total
        
        if project.start_date and progress_rate > 0:
            days_elapsed = (datetime.utcnow() - project.start_date).days
            estimated_total_days = days_elapsed / progress_rate
            predicted_date = project.start_date + timedelta(days=estimated_total_days)
        else:
            predicted_date = project.planned_end_date
        
        # Cost prediction
        if project.spent_amount > 0:
            predicted_cost = project.spent_amount / progress_rate
        else:
            predicted_cost = project.total_budget
        
        return {
            "predicted_completion_date": predicted_date.isoformat() if predicted_date else None,
            "predicted_total_cost": round(predicted_cost, 2),
            "current_progress": round(progress_rate * 100, 2),
            "cost_overrun": round(predicted_cost - project.total_budget, 2),
            "confidence": "medium" if completed > 3 else "low"
        }
    
    def get_manager_dashboard_stats(self, managed_project_ids: List[int]) -> Dict:
        """Get dashboard stats filtered for manager's projects"""
        if not managed_project_ids:
            return {
                "total_projects": 0,
                "active_projects": 0,
                "completed_projects": 0,
                "total_budget": 0,
                "total_spent": 0,
                "budget_utilization": 0,
                "total_tasks": 0,
                "completed_tasks": 0,
                "overdue_tasks": 0,
                "task_completion_rate": 0
            }
        
        total_projects = self.db.query(Project).filter(
            Project.id.in_(managed_project_ids)
        ).count()
        
        active_projects = self.db.query(Project).filter(
            Project.id.in_(managed_project_ids),
            Project.status == ProjectStatus.IN_PROGRESS
        ).count()
        
        total_budget = self.db.query(func.sum(Project.total_budget)).filter(
            Project.id.in_(managed_project_ids)
        ).scalar() or 0
        
        total_spent = self.db.query(func.sum(Project.spent_amount)).filter(
            Project.id.in_(managed_project_ids)
        ).scalar() or 0
        
        total_tasks = self.db.query(Task).filter(
            Task.project_id.in_(managed_project_ids)
        ).count()
        
        completed_tasks = self.db.query(Task).filter(
            Task.project_id.in_(managed_project_ids),
            Task.status == TaskStatus.COMPLETED
        ).count()
        
        overdue_tasks = self.db.query(Task).filter(
            Task.project_id.in_(managed_project_ids),
            Task.status != TaskStatus.COMPLETED,
            Task.planned_end_date < datetime.utcnow()
        ).count()
        
        return {
            "total_projects": total_projects,
            "active_projects": active_projects,
            "completed_projects": self.db.query(Project).filter(
                Project.id.in_(managed_project_ids),
                Project.status == ProjectStatus.COMPLETED
            ).count(),
            "total_budget": round(total_budget, 2),
            "total_spent": round(total_spent, 2),
            "budget_utilization": round(
                (total_spent / total_budget * 100) if total_budget > 0 else 0, 2
            ),
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "overdue_tasks": overdue_tasks,
            "task_completion_rate": round(
                (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0, 2
            )
        }


    def get_worker_dashboard_stats(self, worker_name: str) -> Dict:
        """Get dashboard stats for a specific worker"""
        total_tasks = self.db.query(Task).filter(
            Task.assigned_to == worker_name
        ).count()
        
        completed_tasks = self.db.query(Task).filter(
            Task.assigned_to == worker_name,
            Task.status == TaskStatus.COMPLETED
        ).count()
        
        in_progress_tasks = self.db.query(Task).filter(
            Task.assigned_to == worker_name,
            Task.status == TaskStatus.IN_PROGRESS
        ).count()
        
        overdue_tasks = self.db.query(Task).filter(
            Task.assigned_to == worker_name,
            Task.status != TaskStatus.COMPLETED,
            Task.planned_end_date < datetime.utcnow()
        ).count()
        
        # Tasks due in next 7 days
        upcoming_deadline = datetime.utcnow() + timedelta(days=7)
        upcoming_tasks = self.db.query(Task).filter(
            Task.assigned_to == worker_name,
            Task.status != TaskStatus.COMPLETED,
            Task.planned_end_date.between(datetime.utcnow(), upcoming_deadline)
        ).count()
        
        return {
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "in_progress_tasks": in_progress_tasks,
            "not_started_tasks": self.db.query(Task).filter(
                Task.assigned_to == worker_name,
                Task.status == TaskStatus.NOT_STARTED
            ).count(),
            "overdue_tasks": overdue_tasks,
            "upcoming_tasks": upcoming_tasks,
            "task_completion_rate": round(
                (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0, 2
            )
        }

    def get_team_performance(self, project_id: int = None) -> Dict:
        """Get team performance metrics"""
        from sqlalchemy import case
        
        query = self.db.query(
            Task.assigned_to,
            func.count(Task.id).label("total_tasks"),
            func.sum(
                case(
                    (Task.status == TaskStatus.COMPLETED, 1),
                    else_=0
                )
            ).label("completed_tasks"),
            func.avg(Task.progress_percentage).label("avg_progress")
        ).filter(Task.assigned_to.isnot(None))
        
        if project_id:
            query = query.filter(Task.project_id == project_id)
        
        results = query.group_by(Task.assigned_to).all()
        
        team_stats = []
        for result in results:
            completion_rate = (
                (result.completed_tasks / result.total_tasks * 100)
                if result.total_tasks > 0 else 0
            )
            team_stats.append({
                "worker_name": result.assigned_to,
                "total_tasks": result.total_tasks,
                "completed_tasks": result.completed_tasks,
                "avg_progress": round(result.avg_progress or 0, 2),
                "completion_rate": round(completion_rate, 2)
            })
        
        return {
            "team_members": len(team_stats),
            "performance": team_stats
        }
```

# File: ./backend/app/services/import_service.py

```python
from sqlalchemy.orm import Session
import pandas as pd
from io import BytesIO
from app.models.project import Project, ProjectStatus
from app.models.task import Task, TaskStatus, TaskPriority
from app.models.resource import Resource, ResourceType, ResourceStatus
from app.models.budget import Budget
from datetime import datetime
from typing import Dict, Optional


class ImportService:
    def __init__(self, db: Session):
        self.db = db
        self._project_name_to_id: Dict[str, int] = {}
    
    def _build_project_mapping(self):
        """Build a mapping of project names to IDs"""
        projects = self.db.query(Project).all()
        self._project_name_to_id = {
            project.name.lower().strip(): project.id 
            for project in projects
        }
    
    def _get_project_id(
        self, 
        row: pd.Series, 
        row_index: int
    ) -> Optional[int]:
        """
        Get project_id from row, supporting both project_id and project_name
        """
        # Try project_id first
        if pd.notna(row.get('project_id')):
            try:
                project_id = int(row.get('project_id'))
                # Verify this project exists
                exists = self.db.query(Project).filter(
                    Project.id == project_id
                ).first()
                if exists:
                    return project_id
                else:
                    print(
                        f"Row {row_index}: project_id {project_id} "
                        f"not found in database"
                    )
            except:
                print(f"Row {row_index}: Invalid project_id format")
        
        # Try project_name
        if pd.notna(row.get('project_name')):
            project_name = str(row.get('project_name')).lower().strip()
            if project_name in self._project_name_to_id:
                return self._project_name_to_id[project_name]
            else:
                print(
                    f"Row {row_index}: project_name '{project_name}' "
                    f"not found in database"
                )
        
        return None
    
    def import_from_excel(self, file_content: bytes, filename: str) -> Dict:
        """Import data from Excel file with multiple sheets"""
        try:
            excel_file = BytesIO(file_content)
            
            # Reads all sheets
            sheets = pd.read_excel(
                excel_file, sheet_name=None, engine='openpyxl'
            )
            
            stats = {
                "projects": 0,
                "tasks": 0,
                "resources": 0,
                "budgets": 0
            }
            
            # Import projects first
            if 'Projects' in sheets or 'projects' in sheets:
                sheet_name = 'Projects' if 'Projects' in sheets else 'projects'
                stats["projects"] = self._import_projects(sheets[sheet_name])
            
            # Rebuild project mapping after importing projects
            self._build_project_mapping()
            
            # Then import dependent entities
            if 'Tasks' in sheets or 'tasks' in sheets:
                sheet_name = 'Tasks' if 'Tasks' in sheets else 'tasks'
                stats["tasks"] = self._import_tasks(sheets[sheet_name])
            
            if 'Resources' in sheets or 'resources' in sheets:
                sheet_name = (
                    'Resources' if 'Resources' in sheets else 'resources'
                )
                stats["resources"] = self._import_resources(
                    sheets[sheet_name]
                )
            
            if 'Budgets' in sheets or 'budgets' in sheets:
                sheet_name = 'Budgets' if 'Budgets' in sheets else 'budgets'
                stats["budgets"] = self._import_budgets(sheets[sheet_name])
            
            return stats
        
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Error importing Excel: {str(e)}")
    
    def import_from_csv(self, file_content: bytes) -> Dict:
        try:
            df = None
            for delimiter in [',', ';', '\t']:
                try:
                    df = pd.read_csv(BytesIO(file_content), delimiter=delimiter)
                    if len(df.columns) > 1:
                        break
                except:
                    continue
            
            if df is None or len(df.columns) <= 1:
                raise Exception("Unable to parse CSV file")
            
            df.columns = df.columns.str.strip().str.lower()
            columns = set(df.columns)
            
            # Check for BUDGETS first (most specific - has category + planned_amount)
            if 'category' in columns and 'planned_amount' in columns:
                self._build_project_mapping()
                count = self._import_budgets(df)
                return {
                    "projects": 0,
                    "tasks": 0,
                    "resources": 0,
                    "budgets": count
                }
            
            # Check for RESOURCES (has resource_type or resource_name)
            elif 'resource_name' in columns or 'resource_type' in columns:
                self._build_project_mapping()
                count = self._import_resources(df)
                return {
                    "projects": 0,
                    "tasks": 0,
                    "resources": count,
                    "budgets": 0
                }
            
            # Check for TASKS (has task_name or task-specific columns)
            elif 'task_name' in columns or (
                'name' in columns and (
                    'assigned_to' in columns or 
                    'priority' in columns or
                    'progress' in columns or
                    'progress_percentage' in columns
                )
            ):
                self._build_project_mapping()
                count = self._import_tasks(df)
                return {
                    "projects": 0,
                    "tasks": count,
                    "resources": 0,
                    "budgets": 0
                }
            
            # Check for PROJECTS last (most general - can have project_name or basic columns)
            elif 'project_name' in columns or (
                'name' in columns and 'total_budget' in columns
            ):
                count = self._import_projects(df)
                return {
                    "projects": count,
                    "tasks": 0,
                    "resources": 0,
                    "budgets": 0
                }
            
            else:
                raise Exception(
                    f"Unable to determine CSV data type. "
                    f"Columns found: {', '.join(columns)}"
                )
        
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Error importing CSV: {str(e)}")
    
    def _import_projects(self, df: pd.DataFrame) -> int:
        """Import projects from dataframe"""
        count = 0
        df.columns = df.columns.str.strip().str.lower()
        
        for index, row in df.iterrows():
            try:
                # Handle different column name variations
                name = row.get('name') or row.get('project_name')
                if pd.isna(name):
                    print(f"Skipping row {index}: missing project name")
                    continue
                
                name = str(name).strip()
                if not name:
                    print(f"Skipping row {index}: empty project name")
                    continue
                
                # Parse description
                description = ''
                if pd.notna(row.get('description')):
                    description = str(row.get('description')).strip()
                
                # Parse dates
                start_date = None
                if pd.notna(row.get('start_date')):
                    try:
                        start_date = pd.to_datetime(row.get('start_date'))
                    except:
                        print(
                            f"Row {index}: Invalid start_date, skipping"
                        )
                
                planned_end_date = None
                end_date_field = row.get('end_date') or row.get(
                    'planned_end_date'
                )
                if pd.notna(end_date_field):
                    try:
                        planned_end_date = pd.to_datetime(end_date_field)
                    except:
                        print(
                            f"Row {index}: Invalid end_date, skipping"
                        )
                
                # Parse budget
                total_budget = 0.0
                if pd.notna(row.get('total_budget')):
                    try:
                        total_budget = float(row.get('total_budget'))
                    except:
                        print(
                            f"Row {index}: Invalid total_budget, using 0.0"
                        )
                
                spent_amount = 0.0
                if pd.notna(row.get('spent_amount')):
                    try:
                        spent_amount = float(row.get('spent_amount'))
                    except:
                        print(
                            f"Row {index}: Invalid spent_amount, using 0.0"
                        )
                
                # Parse location
                location = ''
                if pd.notna(row.get('location')):
                    location = str(row.get('location')).strip()
                
                project = Project(
                    name=name,
                    description=description,
                    status=self._parse_project_status(
                        row.get('status', 'planning')
                    ),
                    start_date=start_date,
                    planned_end_date=planned_end_date,
                    total_budget=total_budget,
                    spent_amount=spent_amount,
                    location=location
                )
                self.db.add(project)
                self.db.flush()  # Flush to get the ID
                count += 1
            except Exception as e:
                print(f"Error importing project row {index}: {e}")
                continue
        
        self.db.commit()
        return count
    
    def _import_tasks(self, df: pd.DataFrame) -> int:
        """Import tasks from dataframe"""
        count = 0
        df.columns = df.columns.str.strip().str.lower()
        
        for index, row in df.iterrows():
            try:
                # Validate required fields
                name = row.get('name') or row.get('task_name')
                if pd.isna(name):
                    print(f"Skipping row {index}: missing task name")
                    continue
                
                name = str(name).strip()
                if not name:
                    print(f"Skipping row {index}: empty task name")
                    continue
                
                # Get project_id using enhanced method
                project_id = self._get_project_id(row, index)
                if project_id is None:
                    print(
                        f"Skipping row {index}: could not resolve project. "
                        f"Use 'project_id' or 'project_name' column."
                    )
                    continue
                
                # Parse description
                description = ''
                if pd.notna(row.get('description')):
                    description = str(row.get('description')).strip()
                
                # Parse dates
                start_date = None
                if pd.notna(row.get('start_date')):
                    try:
                        start_date = pd.to_datetime(row.get('start_date'))
                    except:
                        print(f"Row {index}: Invalid start_date")
                
                planned_end_date = None
                end_date_field = row.get('end_date') or row.get(
                    'planned_end_date'
                )
                if pd.notna(end_date_field):
                    try:
                        planned_end_date = pd.to_datetime(end_date_field)
                    except:
                        print(f"Row {index}: Invalid end_date")
                
                # Parse progress
                progress = 0.0
                progress_field = row.get('progress') or row.get(
                    'progress_percentage'
                )
                if pd.notna(progress_field):
                    try:
                        progress = float(progress_field)
                        progress = max(0.0, min(100.0, progress))
                    except:
                        print(
                            f"Row {index}: Invalid progress, using 0.0"
                        )
                
                # Parse assigned_to
                assigned_to = ''
                if pd.notna(row.get('assigned_to')):
                    assigned_to = str(row.get('assigned_to')).strip()
                
                task = Task(
                    project_id=project_id,
                    name=name,
                    description=description,
                    status=self._parse_task_status(
                        row.get('status', 'not_started')
                    ),
                    priority=self._parse_task_priority(
                        row.get('priority', 'medium')
                    ),
                    start_date=start_date,
                    planned_end_date=planned_end_date,
                    progress_percentage=progress,
                    assigned_to=assigned_to
                )
                self.db.add(task)
                count += 1
            except Exception as e:
                print(f"Error importing task row {index}: {e}")
                continue
        
        self.db.commit()
        return count
    
    def _import_resources(self, df: pd.DataFrame) -> int:
        """Import resources from dataframe"""
        count = 0
        df.columns = df.columns.str.strip().str.lower()
        
        for index, row in df.iterrows():
            try:
                # Validate required fields
                name = row.get('name') or row.get('resource_name')
                if pd.isna(name):
                    print(f"Skipping row {index}: missing resource name")
                    continue
                
                name = str(name).strip()
                if not name:
                    print(f"Skipping row {index}: empty resource name")
                    continue
                
                # Get project_id using enhanced method
                project_id = self._get_project_id(row, index)
                if project_id is None:
                    print(
                        f"Skipping row {index}: could not resolve project. "
                        f"Use 'project_id' or 'project_name' column."
                    )
                    continue
                
                # Parse quantity
                quantity = 0.0
                if pd.notna(row.get('quantity')):
                    try:
                        quantity = float(row.get('quantity'))
                        quantity = max(0.0, quantity)
                    except:
                        print(f"Row {index}: Invalid quantity, using 0.0")
                
                # Parse unit
                unit = 'units'
                if pd.notna(row.get('unit')):
                    unit = str(row.get('unit')).strip()
                
                # Parse unit_cost
                unit_cost = 0.0
                if pd.notna(row.get('unit_cost')):
                    try:
                        unit_cost = float(row.get('unit_cost'))
                        unit_cost = max(0.0, unit_cost)
                    except:
                        print(f"Row {index}: Invalid unit_cost, using 0.0")
                
                # Parse supplier
                supplier = ''
                if pd.notna(row.get('supplier')):
                    supplier = str(row.get('supplier')).strip()
                
                resource = Resource(
                    project_id=project_id,
                    name=name,
                    resource_type=self._parse_resource_type(
                        row.get('resource_type', 'material')
                    ),
                    status=self._parse_resource_status(
                        row.get('status', 'available')
                    ),
                    quantity=quantity,
                    unit=unit,
                    unit_cost=unit_cost,
                    supplier=supplier
                )
                resource.calculate_total_cost()
                self.db.add(resource)
                count += 1
            except Exception as e:
                print(f"Error importing resource row {index}: {e}")
                continue
        
        self.db.commit()
        return count
    
    def _import_budgets(self, df: pd.DataFrame) -> int:
        """Import budgets from dataframe"""
        count = 0
        df.columns = df.columns.str.strip().str.lower()
        
        for index, row in df.iterrows():
            try:
                # Validate required fields
                category = row.get('category')
                if pd.isna(category):
                    print(f"Skipping row {index}: missing category")
                    continue
                
                category = str(category).strip()
                if not category:
                    print(f"Skipping row {index}: empty category")
                    continue
                
                # Get project_id using enhanced method
                project_id = self._get_project_id(row, index)
                if project_id is None:
                    print(
                        f"Skipping row {index}: could not resolve project. "
                        f"Use 'project_id' or 'project_name' column."
                    )
                    continue
                
                # Parse description
                description = ''
                if pd.notna(row.get('description')):
                    description = str(row.get('description')).strip()
                
                # Parse planned_amount
                planned_amount = 0.0
                if pd.notna(row.get('planned_amount')):
                    try:
                        planned_amount = float(row.get('planned_amount'))
                        planned_amount = max(0.0, planned_amount)
                    except:
                        print(
                            f"Row {index}: Invalid planned_amount, using 0.0"
                        )
                
                # Parse actual_amount
                actual_amount = 0.0
                if pd.notna(row.get('actual_amount')):
                    try:
                        actual_amount = float(row.get('actual_amount'))
                        actual_amount = max(0.0, actual_amount)
                    except:
                        print(
                            f"Row {index}: Invalid actual_amount, using 0.0"
                        )
                
                budget = Budget(
                    project_id=project_id,
                    category=category,
                    description=description,
                    planned_amount=planned_amount,
                    actual_amount=actual_amount
                )
                self.db.add(budget)
                count += 1
            except Exception as e:
                print(f"Error importing budget row {index}: {e}")
                continue
        
        self.db.commit()
        return count
    
    # Helper methods to parse enum values
    def _parse_project_status(self, status: str) -> ProjectStatus:
        if pd.isna(status):
            return ProjectStatus.PLANNING
        
        status_map = {
            'planning': ProjectStatus.PLANNING,
            'in_progress': ProjectStatus.IN_PROGRESS,
            'active': ProjectStatus.IN_PROGRESS,
            'on_hold': ProjectStatus.ON_HOLD,
            'completed': ProjectStatus.COMPLETED,
            'cancelled': ProjectStatus.CANCELLED
        }
        return status_map.get(
            str(status).lower().strip(), ProjectStatus.PLANNING
        )
    
    def _parse_task_status(self, status: str) -> TaskStatus:
        if pd.isna(status):
            return TaskStatus.NOT_STARTED
        
        status_map = {
            'not_started': TaskStatus.NOT_STARTED,
            'in_progress': TaskStatus.IN_PROGRESS,
            'active': TaskStatus.IN_PROGRESS,
            'completed': TaskStatus.COMPLETED,
            'delayed': TaskStatus.DELAYED,
            'blocked': TaskStatus.BLOCKED
        }
        return status_map.get(
            str(status).lower().strip(), TaskStatus.NOT_STARTED
        )
    
    def _parse_task_priority(self, priority: str) -> TaskPriority:
        if pd.isna(priority):
            return TaskPriority.MEDIUM
        
        priority_map = {
            'low': TaskPriority.LOW,
            'medium': TaskPriority.MEDIUM,
            'high': TaskPriority.HIGH,
            'critical': TaskPriority.CRITICAL
        }
        return priority_map.get(
            str(priority).lower().strip(), TaskPriority.MEDIUM
        )
    
    def _parse_resource_type(self, resource_type: str) -> ResourceType:
        if pd.isna(resource_type):
            return ResourceType.MATERIAL
        
        type_map = {
            'material': ResourceType.MATERIAL,
            'equipment': ResourceType.EQUIPMENT,
            'labor': ResourceType.LABOR,
            'human': ResourceType.LABOR
        }
        return type_map.get(
            str(resource_type).lower().strip(), ResourceType.MATERIAL
        )
    
    def _parse_resource_status(self, status: str) -> ResourceStatus:
        if pd.isna(status):
            return ResourceStatus.AVAILABLE
        
        status_map = {
            'available': ResourceStatus.AVAILABLE,
            'in_use': ResourceStatus.IN_USE,
            'active': ResourceStatus.IN_USE,
            'depleted': ResourceStatus.DEPLETED,
            'maintenance': ResourceStatus.MAINTENANCE,
            'ordered': ResourceStatus.AVAILABLE,
            'retired': ResourceStatus.DEPLETED
        }
        return status_map.get(
            str(status).lower().strip(), ResourceStatus.AVAILABLE
        )
```

# File: ./backend/app/middleware/__init__.py

```python
from app.middleware.error_handler import add_exception_handlers

__all__ = ["add_exception_handlers"]
```

# File: ./backend/app/middleware/error_handler.py

```python
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.exceptions.custom_exceptions import BuildFlowException
import logging

logger = logging.getLogger(__name__)


def add_exception_handlers(app: FastAPI):
    
    @app.exception_handler(BuildFlowException)
    async def buildflow_exception_handler(request: Request, exc: BuildFlowException):
        logger.error(f"BuildFlow error: {exc.message}")
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.message, "error_type": type(exc).__name__}
        )
    
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        logger.error(f"Validation error: {exc.errors()}")
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": exc.errors(), "error_type": "ValidationError"}
        )
    
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        logger.error(f"Unexpected error: {str(exc)}", exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Internal server error", "error_type": "ServerError"}
        )
```

# File: ./backend/app/exceptions/__init__.py

```python
from app.exceptions.custom_exceptions import (
    BuildFlowException,
    ResourceNotFoundException,
    ValidationException,
    FileUploadException,
    DatabaseException
)

__all__ = [
    "BuildFlowException",
    "ResourceNotFoundException",
    "ValidationException",
    "FileUploadException",
    "DatabaseException"
]
```

# File: ./backend/app/exceptions/custom_exceptions.py

```python
class BuildFlowException(Exception):
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class ResourceNotFoundException(BuildFlowException):
    def __init__(self, resource: str, resource_id: int):
        message = f"{resource} with id {resource_id} not found"
        super().__init__(message, status_code=404)


class ValidationException(BuildFlowException):
    def __init__(self, message: str):
        super().__init__(message, status_code=400)


class FileUploadException(BuildFlowException):
    def __init__(self, message: str):
        super().__init__(message, status_code=400)


class DatabaseException(BuildFlowException):
    def __init__(self, message: str = "Database operation failed"):
        super().__init__(message, status_code=500)
```

