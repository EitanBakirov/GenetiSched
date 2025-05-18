from pydantic import BaseModel, Field
from typing import List, Literal, Optional, Dict
from uuid import UUID, uuid4
from datetime import date, datetime
from calendar import monthcalendar

class Employee(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    role: Literal["intern", "senior"]
    employment: Literal[100, 80]
    room_number: Optional[str] = None
    # Monthly availability as a dict with date strings as keys and boolean as values
    availability: Dict[str, bool] = {}
    # For seniors: weekly settings for working with interns
    works_with_interns_weekly: Dict[str, bool] = {}  # Keys are week numbers (1-4)

    @staticmethod
    def get_current_month_dates() -> List[str]:
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

    def initialize_monthly_availability(self):
        """Initialize availability for all workdays in current month"""
        self.availability = {date_str: False for date_str in self.get_current_month_dates()}
        if self.role == "senior":
            self.works_with_interns_weekly = {str(week): True for week in range(1, 5)} 