# Payroll calculation
from core.utils import find_employee, get_total_hours

class PayrollCalculator:
    # Calculates payroll based on attendance records and hourly rates
    def __init__(self, employees, attendance_records):
        self.employees = employees
        self.attendance_records = attendance_records

    def calculate_employee_pay(self, emp_id):
        # Calculate total pay for a specific employee
        employee = find_employee(self.employees, emp_id)
        if employee is None:
            return False, f"Employee with ID '{emp_id}' not found."

        total_hours = get_total_hours(self.attendance_records, emp_id)
        total_pay = round(total_hours * employee.hourly_rate, 2)
        result = {
            "name": employee.name,
            "emp_id": emp_id,
            "total_hours": total_hours,
            "hourly_rate": employee.hourly_rate,
            "total_pay": total_pay,
        }
        return True, result

    def calculate_all_pay(self):
        # Calculate pay for all employees
        results = []
        for emp in self.employees:
            success, result = self.calculate_employee_pay(emp.emp_id)
            if success:
                results.append(result)
        return results