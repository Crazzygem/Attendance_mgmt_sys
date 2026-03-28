# Shared utilities
def find_employee(employees, emp_id):
    for emp in employees:
        if emp.emp_id == emp_id:
            return emp
    return None

def get_today_records(attendance_records):
    from datetime import datetime
    today = datetime.today().strftime("%Y-%m-%d")
    return [r for r in attendance_records if r.date == today]

def find_today_record(attendance_records, emp_id):
    from datetime import datetime
    today = datetime.today().strftime("%Y-%m-%d")
    for record in attendance_records:
        if record.emp_id == emp_id and record.date == today:
            return record
    return None

def get_total_hours(attendance_records, emp_id):
    total_hours = 0.0
    for record in attendance_records:
        if record.emp_id == emp_id:
            total_hours += record.get_hours_worked()
    return round(total_hours, 2)