# Report generation
import pandas as pd
import config
from core.utils import get_total_hours
from data.excel_loader import load_settings, load_employees


# Generates analytical reports using pandas DataFrames
class ReportGenerator:
    def __init__(self, employees, attendance_records):
        self.employees = employees
        self.attendance_records = attendance_records

    # Generate report showing total hours worked per employee
    def generate_hours_report(self):
        data = []
        for emp in self.employees:
            total_hours = get_total_hours(self.attendance_records, emp.emp_id)
            data.append({
                "Employee ID": emp.emp_id,
                "Name": emp.name,
                "Total Hours Worked": total_hours,
            })
        df = pd.DataFrame(data)
        return df
    
    # Generate report showing leave information per employee
    def generate_leave_report(self):
        employees = load_employees()
        emp_balances = {e.emp_id: e.leave_balance for e in employees}
        data = []
        for emp in self.employees:
            initial = emp_balances.get(emp.emp_id, emp.leave_balance)
            leaves_taken = initial - emp.leave_balance

            data.append({
                "Employee ID": emp.emp_id,
                "Name": emp.name,
                "Leaves Taken": leaves_taken,
                "Leaves Remaining": emp.leave_balance,
            })

        df = pd.DataFrame(data)
        return df

    # Generate payroll report with hours, rate, and pay
    def generate_payroll_report(self):
        data = []
        for emp in self.employees:
            total_hours = get_total_hours(self.attendance_records, emp.emp_id)
            total_pay = round(total_hours * emp.hourly_rate, 2)

            data.append({
                "Employee ID": emp.emp_id,
                "Name": emp.name,
                "Shift": emp.shift.name,
                "Hourly Rate ($)": emp.hourly_rate,
                "Total Hours": total_hours,
                "Total Pay ($)": total_pay,
            })

        df = pd.DataFrame(data)
        return df
    
    # Generate complete summary combining hours, leaves, and payroll
    def generate_full_summary(self):
        employees = load_employees()
        emp_balances = {e.emp_id: e.leave_balance for e in employees}
        data = []
        for emp in self.employees:
            total_hours = get_total_hours(self.attendance_records, emp.emp_id)
            total_pay = round(total_hours * emp.hourly_rate, 2)
            initial = emp_balances.get(emp.emp_id, emp.leave_balance)
            leaves_taken = initial - emp.leave_balance

            data.append({
                "Employee ID": emp.emp_id,
                "Name": emp.name,
                "Shift": emp.shift.name,
                "Hours Worked": total_hours,
                "Leaves Taken": leaves_taken,
                "Leaves Left": emp.leave_balance,
                "Rate ($/hr)": emp.hourly_rate,
                "Total Pay ($)": total_pay,
            })

        df = pd.DataFrame(data)
        return df

    # Export multiple DataFrames to Excel file
    def export_to_excel(self, reports_dict, filename=None):
        try:
            import openpyxl
        except ImportError:
            return "Error: openpyxl not installed. Run: pip install openpyxl"

        config.ensure_report_dir()
        if filename is None:
            filename = f"report_{config.get_timestamp()}.xlsx"

        filepath = f"{config.REPORT_OUTPUT_DIR}/{filename}"
        
        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            for sheet_name, df in reports_dict.items():
                df.to_excel(writer, sheet_name=sheet_name, index=False)

        return filepath

    # Generate and export all reports to Excel
    def export_all_reports(self):
        reports = {
            "Hours Worked": self.generate_hours_report(),
            "Leave Status": self.generate_leave_report(),
            "Payroll": self.generate_payroll_report(),
            "Full Summary": self.generate_full_summary(),
        }
        return self.export_to_excel(reports)