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