# Data models
from datetime import datetime, time

class Shift:
    # Work shift with start and end times
    def __init__(self, name, start_time, end_time):
        self.name = name
        self.start_time = self._parse_time(start_time)
        self.end_time = self._parse_time(end_time)

    def _parse_time(self, time_str):
        # Convert time string to Python time object
        hour, minute = map(int, time_str.split(":"))
        return time(hour, minute)

    def get_duration_hours(self):
        # Calculate shift duration in hours
        today = datetime.today().date()
        start_dt = datetime.combine(today, self.start_time)
        end_dt = datetime.combine(today, self.end_time)

        if end_dt <= start_dt:
            from datetime import timedelta
            end_dt += timedelta(days=1)

        duration = end_dt - start_dt
        return duration.total_seconds() / 3600

    def __str__(self):
        return f"{self.name} ({self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')})"

class Employee:
    # Employee with personal and work details
    def __init__(self, emp_id, name, shift, hourly_rate, leave_balance=12):
        self.emp_id = emp_id
        self.name = name
        self.shift = shift
        self.hourly_rate = hourly_rate
        self.leave_balance = leave_balance

    def __str__(self):
        return (
            f"ID: {self.emp_id} | Name: {self.name} | "
            f"Shift: {self.shift} | Rate: ${self.hourly_rate}/hr | "
            f"Leave: {self.leave_balance} days"
        )

class AttendanceRecord:
    # Single day's check-in/out record
    def __init__(self, emp_id, date, check_in=None, check_out=None):
        self.emp_id = emp_id
        self.date = date
        self.check_in = check_in
        self.check_out = check_out

    def get_hours_worked(self):
        # Calculate hours worked from check-in and check-out times
        if self.check_in is None or self.check_out is None:
            return 0.0

        today = datetime.today().date()
        in_time = datetime.strptime(self.check_in, "%H:%M").time()
        out_time = datetime.strptime(self.check_out, "%H:%M").time()

        in_dt = datetime.combine(today, in_time)
        out_dt = datetime.combine(today, out_time)

        duration = out_dt - in_dt
        hours = duration.total_seconds() / 3600

        return round(hours, 2)

    def __str__(self):
        status = "Present" if self.check_in else "Absent"
        return (
            f"Date: {self.date} | Employee: {self.emp_id} | "
            f"In: {self.check_in or 'N/A'} | Out: {self.check_out or 'N/A'} | "
            f"Status: {status}"
        )