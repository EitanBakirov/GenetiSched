from typing import List, Dict, Tuple
from models import Employee
from datetime import datetime, timedelta

class Schedule:
    def __init__(self):
        self.weekdays = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday"]
        self.rooms = {}  # This will be populated dynamically based on senior employees
        self.schedule: Dict[str, Dict[str, List[str]]] = {
            day: {} for day in self.weekdays
        }
        self.office_duty: Dict[str, str] = {day: "" for day in self.weekdays}

    def get_week_number(self, day_index: int) -> str:
        """Convert day index to week number (1-4)"""
        # Week 1: Days 0-1 (Sun, Mon)
        # Week 2: Day 2 (Tue)
        # Week 3: Day 3 (Wed)
        # Week 4: Day 4 (Thu)
        week_map = {
            0: "1",  # Sunday
            1: "1",  # Monday
            2: "2",  # Tuesday
            3: "3",  # Wednesday
            4: "4",  # Thursday
        }
        return week_map[day_index]

    def generate_schedule(self, employees: List[Employee]) -> Dict:
        # Reset rooms and schedule for new generation
        seniors = [emp for emp in employees if emp.role == "senior"]
        interns = [emp for emp in employees if emp.role == "intern"]

        # Initialize rooms based on senior employees who have rooms
        self.rooms = {}
        for senior in seniors:
            if senior.room_number:  # Only include seniors with assigned rooms
                room_key = senior.room_number
                self.rooms[room_key] = senior.name

        # Initialize schedule with rooms
        self.schedule = {
            day: {room: [] for room in self.rooms.keys()} for day in self.weekdays
        }

        # For each senior who works with interns, mark their availability
        for day_index, day in enumerate(self.weekdays):
            current_week = self.get_week_number(day_index)
            
            for senior in seniors:
                if not senior.room_number:
                    continue
                
                # Check if senior works with interns this week
                works_with_interns = senior.works_with_interns_weekly.get(current_week, False)
                
                # Check if senior is available this day
                is_available = senior.availability.get(day, False)

                if works_with_interns and is_available:
                    # Mark as "Available for interns"
                    self.schedule[day][senior.room_number] = ["Available for interns"]
                elif is_available:
                    # Mark as just available
                    self.schedule[day][senior.room_number] = ["Present"]
                else:
                    # Mark as not available
                    self.schedule[day][senior.room_number] = ["Not available"]

        # Simple office duty assignment - just mark who's available
        for day in self.weekdays:
            available_seniors = [s for s in seniors if s.availability.get(day, False)]
            if available_seniors:
                # For now, just assign the first available senior
                self.office_duty[day] = available_seniors[0].name
            else:
                self.office_duty[day] = "No one available"

        return {
            "schedule": self.schedule,
            "office_duty": self.office_duty,
            "rooms": self.rooms
        }

    def initialize_intern_senior_schedule(self, employees: List[Employee]) -> Dict:
        """Initialize schedule showing which seniors are available for assignments each day"""
        seniors = [emp for emp in employees if emp.role == "senior"]
        
        # Initialize rooms and schedule structure
        rooms = {}
        schedule = {}
        
        # First, map rooms to seniors' IDs
        for senior in seniors:
            if senior.room_number:
                rooms[senior.room_number] = senior.id

        # Get the first Sunday of March 2025
        start_date = datetime(2025, 3, 2)  # This is the first Sunday in March 2025
        current_date = start_date

        # For each day, check availability and works_with_interns status
        for day_index, day in enumerate(self.weekdays):
            schedule[day] = {}
            date_str = current_date.strftime("%Y-%m-%d")
            current_week = self.get_week_number(day_index)
            
            for room_number, senior_id in rooms.items():
                senior = next(s for s in seniors if str(s.id) == str(senior_id))
                
                # First check if senior works with interns this week
                works_with_interns = senior.works_with_interns_weekly.get(current_week, False)
                
                # If they don't work with interns this week, they're not available regardless of availability
                if not works_with_interns:
                    schedule[day][room_number] = "Not Available"
                    continue
                
                # If they do work with interns this week, check their availability for this day
                is_working = senior.availability.get(date_str, False)
                
                # They are only available if they both work with interns this week AND are working this day
                schedule[day][room_number] = "Available" if is_working else "Not Available"
            
            # Move to next day
            current_date += timedelta(days=1)
        
        return {
            "rooms": rooms,
            "schedule": schedule
        }

    def initialize_room_schedule(self, employees: List[Employee]) -> Dict:
        """Initialize room schedule showing room availability based on senior schedules"""
        seniors = [emp for emp in employees if emp.role == "senior"]
        
        # Initialize rooms based on senior employees who have rooms
        rooms = {}
        room_schedule = {}
        
        # First, map rooms to seniors' IDs (not names)
        for senior in seniors:
            if senior.room_number:
                rooms[senior.room_number] = senior.id
                
        # Then, for each day, check room availability based on senior's schedule
        # Get the first Sunday of March 2025
        start_date = datetime(2025, 3, 2)  # This is the first Sunday in March 2025
        current_date = start_date
        
        # Initialize schedule for each day
        for day in self.weekdays:
            room_schedule[day] = {}
            date_str = current_date.strftime("%Y-%m-%d")
            
            for room_number, senior_id in rooms.items():
                senior = next(s for s in seniors if str(s.id) == str(senior_id))
                is_working = senior.availability.get(date_str, False)
                
                if is_working:
                    # When senior is working, room is NOT available
                    room_schedule[day][room_number] = "Not Available"
                else:
                    # When senior is NOT working, room IS available
                    room_schedule[day][room_number] = "Available"
            
            # Move to next day
            current_date += timedelta(days=1)
        
        return {
            "rooms": rooms,
            "schedule": room_schedule
        } 