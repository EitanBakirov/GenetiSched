from fastapi import APIRouter, HTTPException
from typing import List, Dict
import json
from models import Employee
import os
from uuid import UUID
from scheduler import Schedule
from datetime import date
from calendar import monthcalendar

router = APIRouter()

EMPLOYEES_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "employees.json")

def load_employees() -> List[Employee]:
    try:
        if os.path.exists(EMPLOYEES_FILE):
            with open(EMPLOYEES_FILE, "r") as f:
                try:
                    data = json.load(f)
                    return [Employee(**emp) for emp in data]
                except json.JSONDecodeError:
                    # If the file is corrupted or empty, return empty list and create new file
                    save_employees([])
                    return []
        else:
            # Create the file if it doesn't exist
            save_employees([])
            return []
    except Exception as e:
        print(f"Error loading employees: {str(e)}")
        return []

def save_employees(employees: List[Employee]):
    def serialize_employee(emp):
        emp_dict = emp.model_dump()
        emp_dict['id'] = str(emp_dict['id'])  # Convert UUID to string
        return emp_dict

    with open(EMPLOYEES_FILE, "w") as f:
        json.dump([serialize_employee(emp) for emp in employees], f, indent=2)

@router.get("/employees", response_model=List[Employee])
async def get_employees():
    return load_employees()

@router.post("/employees", response_model=Employee)
async def create_employee(employee: Employee):
    employees = load_employees()
    employees.append(employee)
    save_employees(employees)
    return employee

@router.put("/employees/{employee_id}", response_model=Employee)
async def update_employee(employee_id: UUID, updated_employee: Employee):
    employees = load_employees()
    for i, emp in enumerate(employees):
        if emp.id == employee_id:
            # Preserve the ID of the existing employee
            updated_employee.id = employee_id
            employees[i] = updated_employee
            save_employees(employees)
            return updated_employee
    raise HTTPException(status_code=404, detail="Employee not found")

@router.delete("/employees/{employee_id}")
async def delete_employee(employee_id: UUID):
    employees = load_employees()
    filtered_employees = [emp for emp in employees if emp.id != employee_id]
    if len(filtered_employees) == len(employees):
        raise HTTPException(status_code=404, detail="Employee not found")
    save_employees(filtered_employees)
    return {"message": "Employee deleted successfully"}

@router.post("/schedule/generate")
async def generate_schedule():
    employees = load_employees()
    scheduler = Schedule()
    return scheduler.generate_schedule(employees)

@router.get("/validate-room/{room_number}")
async def validate_room(room_number: str):
    employees = load_employees()
    existing_senior = next((emp for emp in employees if emp.role == "senior" and emp.room_number == room_number), None)
    if existing_senior:
        raise HTTPException(
            status_code=400, 
            detail=f"Room {room_number} is already assigned to {existing_senior.name}"
        )
    return {"message": "Room is available"}

@router.get("/current-month-dates")
def get_current_month_dates():
    """Get all workdays (Sun-Thu) for the current month's first 4 weeks"""
    today = date.today()
    month_calendar = monthcalendar(today.year, today.month)
    dates = []
    
    for week_num, week in enumerate(month_calendar[:4], 1):  # Only first 4 weeks
        for day in week:
            if day != 0:  # Skip padding days
                current_date = date(today.year, today.month, day)
                if current_date.weekday() < 5:  # Only Sunday (6) to Thursday (3)
                    dates.append(current_date.isoformat())
    
    return dates

@router.post("/schedule/intern-senior/reset")
async def reset_intern_senior_schedule():
    employees = load_employees()
    scheduler = Schedule()
    # Initialize the schedule with senior availability
    initial_schedule = scheduler.initialize_intern_senior_schedule(employees)
    return {"schedule": initial_schedule}

@router.post("/schedule/rooms/reset")
async def reset_room_schedule():
    employees = load_employees()
    scheduler = Schedule()
    # Initialize rooms with their availability based on senior schedules
    result = scheduler.initialize_room_schedule(employees)
    print("Room schedule reset result:", result)  # Add debug print
    return {
        "success": True,
        "rooms": result["rooms"],
        "schedule": result["schedule"]
    }

@router.get("/test")
async def test_endpoint():
    return {"status": "ok", "message": "Backend is working"} 