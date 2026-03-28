# Leave management
from core.utils import find_employee
from data.excel_loader import save_employees

class LeaveManager:
    def __init__(self, employees):
        self.employees = employees

    def request_leave(self, emp_id, days):
        employee = find_employee(self.employees, emp_id)
        if employee is None:
            return False, f"Employee with ID '{emp_id}' not found."

        if days <= 0:
            return False, "Leave days must be a positive number."

        if employee.leave_balance < days:
            return False, (
                f"Not enough leave balance. {employee.name} has "
                f"{employee.leave_balance} days available, but requested {days} days."
            )

        employee.leave_balance -= days
        save_employees(self.employees)

        return True, (
            f"Leave approved for {employee.name}. "
            f"Days taken: {days}. "
            f"Remaining balance: {employee.leave_balance} days."
        )

    def get_leave_balances(self):
        return [(emp, emp.leave_balance) for emp in self.employees]
