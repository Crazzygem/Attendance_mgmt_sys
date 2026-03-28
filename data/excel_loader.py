# Excel data loader - single config file
import pandas as pd
from core.models import Employee, AttendanceRecord, Shift
import config

def get_filepath():
    return config.EXCEL_CONFIG_PATH

def load_settings():
    try:
        df = pd.read_excel(get_filepath(), sheet_name="Settings")
        settings = dict(zip(df["Key"], df["Value"]))
        return {
            "company_name": str(settings.get("company_name", "ABC Company")),
            "currency": str(settings.get("currency", "$")),
            "currency_symbol": str(settings.get("currency_symbol", "$")),
        }
    except FileNotFoundError:
        print(f"Error: {get_filepath()} not found.")
        return {"company_name": "ABC Company", "currency": "$", "currency_symbol": "$"}
    except Exception as e:
        print(f"Error loading settings: {e}")
        return {"company_name": "ABC Company", "currency": "$", "currency_symbol": "$"}

def load_shifts():
    try:
        df = pd.read_excel(get_filepath(), sheet_name="Shifts")
        shifts = {}
        for _, row in df.iterrows():
            shifts[row["Shift Name"]] = Shift(
                row["Shift Name"],
                row["Start Time"],
                row["End Time"]
            )
        return shifts
    except FileNotFoundError:
        print(f"Error: {get_filepath()} not found.")
        print("Please create the Excel file with proper data.")
        return {}
    except Exception as e:
        print(f"Error loading shifts: {e}")
        return {}

def load_employees():
    try:
        df = pd.read_excel(get_filepath(), sheet_name="Employees")
        shifts = load_shifts()
        employees = []
        for _, row in df.iterrows():
            shift_name = row["Shift"]
            shift = shifts.get(shift_name, Shift("Morning", "08:00", "17:00"))
            emp = Employee(
                emp_id=row["Employee ID"],
                name=row["Name"],
                shift=shift,
                hourly_rate=float(row["Hourly Rate"]),
                leave_balance=int(row["Leave Balance"])
            )
            employees.append(emp)
        return employees
    except FileNotFoundError:
        print(f"Error: {get_filepath()} not found.")
        return []
    except Exception as e:
        print(f"Error loading employees: {e}")
        return []

def load_attendance():
    try:
        df = pd.read_excel(get_filepath(), sheet_name="Attendance")
        records = []
        for _, row in df.iterrows():
            check_in = row["Check-in"] if pd.notna(row["Check-in"]) else None
            check_out = row["Check-out"] if pd.notna(row["Check-out"]) else None
            record = AttendanceRecord(
                emp_id=row["Employee ID"],
                date=str(row["Date"]).split(" ")[0],
                check_in=str(check_in) if check_in else None,
                check_out=str(check_out) if check_out else None
            )
            records.append(record)

        return records
    except FileNotFoundError:
        print(f"Error: {get_filepath()} not found.")
        return []
    except Exception as e:
        print(f"Error loading attendance: {e}")
        return []

def save_attendance_records(records):
    try:
        data = []
        for r in records:
            data.append({
                "Employee ID": r.emp_id,
                "Date": r.date,
                "Check-in": r.check_in,
                "Check-out": r.check_out,
            })

        df = pd.DataFrame(data)
        existing_sheets = pd.ExcelFile(get_filepath()).sheet_names
        with pd.ExcelWriter(get_filepath(), engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
            df.to_excel(writer, sheet_name="Attendance", index=False)
        return True
    except Exception as e:
        print(f"Error saving attendance: {e}")
        return False

def save_employees(employees):
    try:
        data = []
        for emp in employees:
            data.append({
                "Employee ID": emp.emp_id,
                "Name": emp.name,
                "Shift": emp.shift.name,
                "Hourly Rate": emp.hourly_rate,
                "Leave Balance": emp.leave_balance,
            })
        df = pd.DataFrame(data)
        existing_sheets = pd.ExcelFile(get_filepath()).sheet_names
        with pd.ExcelWriter(get_filepath(), engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
            df.to_excel(writer, sheet_name="Employees", index=False)
        return True
    except Exception as e:
        print(f"Error saving employees: {e}")
        return False