# Main CLI application
from tabulate import tabulate

from data.excel_loader import load_employees, load_attendance, load_settings
from core.attendance import AttendanceSystem
from core.leave import LeaveManager
from core.payroll import PayrollCalculator
from reports.generator import ReportGenerator
import ui.colors as colors

def input_employee_id(employees):
    while True:
        emp_id = input(f"  Enter Employee ID: ").strip().upper()
        if not emp_id:
            colors.warning("  Employee ID cannot be empty.")
            continue
        for emp in employees:
            if emp.emp_id == emp_id:
                return emp_id
        colors.error(f"  Employee '{emp_id}' not found.")

def input_number(prompt, min_val=None):
    while True:
        try:
            value = input(f"  {prompt}: ").strip()
            number = int(value)
            if min_val is not None and number < min_val:
                colors.warning(f"  Value must be at least {min_val}.")
                continue
            return number
        except ValueError:
            colors.error("  Invalid number.")

def main_menu():
    colors.separator("═", 50)
    colors.header("  ATTENDANCE MANAGEMENT SYSTEM  ")
    colors.separator("═", 50)
    colors.menu_item(1, "Operation")
    colors.menu_item(2, "Report")
    colors.menu_item(3, "Export")
    colors.menu_item(4, "Exit")
    colors.separator("─", 50)

def print_attendance_table(attendance_system):
    records = attendance_system.get_today_attendance()
    table_data = []
    for emp, status, check_in, check_out in records:
        in_time = check_in if check_in else "—"
        out_time = check_out if check_out else "—"
        table_data.append([emp.emp_id, emp.name, in_time, out_time, status])
    print(tabulate(table_data, headers=["ID", "Name", "Check In", "Check Out", "Status"], tablefmt="grid"))

def operation_menu(attendance_system):
    print()
    colors.separator("─", 65)
    colors.section("  OPERATION")
    colors.separator("─", 65)
    print_attendance_table(attendance_system)
    colors.separator("─", 65)
    colors.menu_item(1, "Check-in")
    colors.menu_item(2, "Check-out")
    colors.menu_item(3, "Leave Request")
    colors.menu_item(4, "Back to Main Menu")
    colors.separator("─", 65)

def handle_check_in(attendance_system, employees):
    colors.section("\n  CHECK-IN")
    emp_id = input_employee_id(employees)
    success, message = attendance_system.check_in(emp_id)
    if success:
        colors.success(message)
    else:
        colors.error(message)

def handle_check_out(attendance_system, employees):
    colors.section("\n  CHECK-OUT")
    emp_id = input_employee_id(employees)
    success, message = attendance_system.check_out(emp_id)
    if success:
        colors.success(message)
    else:
        colors.error(message)

def handle_leave(leave_manager, employees):
    colors.section("\n  LEAVE REQUEST")
    emp_id = input_employee_id(employees)
    days = input_number("Number of leave days", min_val=1)
    success, message = leave_manager.request_leave(emp_id, days)
    if success:
        colors.success(message)
    else:
        colors.error(message)

def report_menu():
    print()
    colors.separator("─", 30)
    colors.section("  REPORT")
    colors.separator("─", 30)
    colors.menu_item(1, "Employee Detail")
    colors.menu_item(2, "All Attendance")
    colors.menu_item(3, "Payroll")
    colors.menu_item(4, "Full Summary")
    colors.menu_item(5, "Back to Main Menu")
    colors.separator("─", 30)

def handle_employee_detail(employees):
    colors.section("\n  EMPLOYEE DETAIL")
    table_data = []
    for emp in employees:
        table_data.append([
            emp.emp_id,
            emp.name,
            emp.shift.name,
            f"${emp.hourly_rate}/hr",
            f"{emp.leave_balance} days"
        ])
    print(tabulate(table_data, headers=["ID", "Name", "Shift", "Hourly Rate", "Leave Balance"], tablefmt="grid"))

def handle_all_attendance(attendance_records):
    colors.section("\n  ALL ATTENDANCE")
    if not attendance_records:
        colors.warning("  No attendance records found.")
        return
    table_data = []
    for r in attendance_records:
        check_in = r.check_in if r.check_in else "—"
        check_out = r.check_out if r.check_out else "—"
        if r.check_out:
            status = "Checked Out"
        elif r.check_in:
            status = "Checked In"
        else:
            status = "Absent"
        table_data.append([r.emp_id, r.date, check_in, check_out, status])
    print(tabulate(table_data, headers=["ID", "Date", "Check In", "Check Out", "Status"], tablefmt="grid"))

def handle_payroll(payroll_calculator):
    colors.section("\n  PAYROLL")
    results = payroll_calculator.calculate_all_pay()
    table_data = []
    for r in results:
        table_data.append([
            r['emp_id'], r['name'], r['total_hours'],
            f"${r['hourly_rate']}", f"${r['total_pay']}"
        ])
    print(tabulate(table_data, headers=["ID", "Name", "Hours", "Rate", "Total Pay"], tablefmt="grid"))
    total = sum(r['total_pay'] for r in results)
    colors.info(f"Total Payroll: ${total:.2f}")

def handle_full_summary(report_generator):
    hours_df = report_generator.generate_hours_report()
    colors.header("\n  HOURS WORKED")
    print(tabulate(hours_df.values.tolist(), headers=hours_df.columns.tolist(), tablefmt="grid"))

    leave_df = report_generator.generate_leave_report()
    colors.header("\n  LEAVE STATUS")
    print(tabulate(leave_df.values.tolist(), headers=leave_df.columns.tolist(), tablefmt="grid"))

    payroll_df = report_generator.generate_payroll_report()
    colors.header("\n  PAYROLL")
    print(tabulate(payroll_df.values.tolist(), headers=payroll_df.columns.tolist(), tablefmt="grid"))

def handle_export(report_generator):
    colors.section("\n  EXPORT TO EXCEL")
    filepath = report_generator.export_all_reports()
    colors.success(f"  Reports exported to: {filepath}")

def operation_submenu(attendance_system, leave_manager, employees):
    while True:
        operation_menu(attendance_system)
        choice = input("  Enter choice (1-4): ").strip()

        if choice == "1":
            handle_check_in(attendance_system, employees)
        elif choice == "2":
            handle_check_out(attendance_system, employees)
        elif choice == "3":
            handle_leave(leave_manager, employees)
        elif choice == "4":
            break
        else:
            colors.warning("  Invalid choice. Enter 1-4.")

def report_submenu(employees, attendance_records, payroll_calculator, report_generator):
    while True:
        report_menu()
        choice = input("  Enter choice (1-5): ").strip()

        if choice == "1":
            handle_employee_detail(employees)
        elif choice == "2":
            handle_all_attendance(attendance_records)
        elif choice == "3":
            handle_payroll(payroll_calculator)
        elif choice == "4":
            handle_full_summary(report_generator)
        elif choice == "5":
            break
        else:
            colors.warning("  Invalid choice. Enter 1-5.")

def main():
    employees = load_employees()
    attendance_records = load_attendance()
    attendance_system = AttendanceSystem(employees, attendance_records)
    leave_manager = LeaveManager(employees)
    payroll_calculator = PayrollCalculator(employees, attendance_records)
    report_generator = ReportGenerator(employees, attendance_records)

    while True:
        main_menu()
        choice = input("  Enter choice (1-4): ").strip()

        if choice == "1":
            operation_submenu(attendance_system, leave_manager, employees)
        elif choice == "2":
            report_submenu(employees, attendance_records, payroll_calculator, report_generator)
        elif choice == "3":
            handle_export(report_generator)
        elif choice == "4":
            colors.success("\n  Goodbye!")
            break
        else:
            colors.warning("  Invalid choice. Enter 1-4.")

if __name__ == "__main__":
    main()
