# Attendance management
from datetime import datetime
from core.models import AttendanceRecord
from core.utils import find_employee, get_today_records, find_today_record
from data.excel_loader import save_attendance_records

class AttendanceSystem:
    def __init__(self, employees, attendance_records):
        self.employees = employees
        self.attendance_records = attendance_records

    def check_in(self, emp_id):
        employee = find_employee(self.employees, emp_id)
        if employee is None:
            return False, f"Employee with ID '{emp_id}' not found."

        existing_record = find_today_record(self.attendance_records, emp_id)
        if existing_record is not None:
            return False, f"{employee.name} has already checked in today at {existing_record.check_in}."

        today = datetime.today().strftime("%Y-%m-%d")
        now = datetime.now().strftime("%H:%M")

        new_record = AttendanceRecord(emp_id, today, check_in=now, check_out=None)
        self.attendance_records.append(new_record)
        save_attendance_records(self.attendance_records)

        return True, f"{employee.name} checked in successfully at {now}."

    def check_out(self, emp_id):
        employee = find_employee(self.employees, emp_id)
        if employee is None:
            return False, f"Employee with ID '{emp_id}' not found."

        record = find_today_record(self.attendance_records, emp_id)
        if record is None:
            return False, f"{employee.name} has not checked in today."

        if record.check_out is not None:
            return False, f"{employee.name} has already checked out today at {record.check_out}."

        now = datetime.now().strftime("%H:%M")
        record.check_out = now
        save_attendance_records(self.attendance_records)

        hours = record.get_hours_worked()
        return True, f"{employee.name} checked out successfully at {now}. Hours worked: {hours}"

    def get_today_attendance(self):
        today_records = get_today_records(self.attendance_records)
        record_dict = {r.emp_id: r for r in today_records}

        result = []
        for emp in self.employees:
            if emp.emp_id in record_dict:
                record = record_dict[emp.emp_id]
                if record.check_out:
                    status = "Checked Out"
                else:
                    status = "Checked In"
                result.append((emp, status, record.check_in, record.check_out))
            else:
                result.append((emp, "Absent", None, None))

        return result
