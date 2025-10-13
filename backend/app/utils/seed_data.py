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