# Attendance Management System

A Python CLI-based attendance management system with check-in/check-out tracking, leave management, payroll calculation, and Excel reporting.

## Features

- Employee check-in/check-out with real-time tracking
- Leave request and balance management
- Automatic payroll calculation
- Comprehensive reporting (hours, leave, payroll)
- Excel export for all reports
- All data stored in a single Excel configuration file

## Prerequisites

- Python 3.8+
- pip (Python package manager)

## Installation

1. Clone the repository:
   ```bash
   cd /path/to/project
   ```

2. Create virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate virtual environment:
   
   On Linux/Mac:
   ```bash
   source venv/bin/activate
   ```
   
   On Windows:
   ```bash
   venv\Scripts\activate
   ```

4. Install dependencies:
   ```bash
   pip install pandas openpyxl tabulate colorama
   ```

## Project Structure

```
.
├── config.py              # Minimal config (Excel path, report dir)
├── main.py                # Main CLI application
├── core/                  # Business logic
│   ├── models.py         # Data models (Employee, Shift, AttendanceRecord)
│   ├── attendance.py     # Check-in/check-out operations
│   ├── leave.py          # Leave management
│   ├── payroll.py       # Payroll calculation
│   └── utils.py         # Shared utility functions
├── data/                  # Data layer
│   ├── config.xlsx       # Single Excel config (employees, shifts, settings, attendance)
│   ├── excel_loader.py  # Excel read/write functions
│   └── sample.py        # Sample data generators (legacy, not used)
├── ui/                    # User interface
│   ├── colors.py         # Terminal color utilities
│   └── forms.py         # Input form handlers (legacy, removed)
├── reports/                # Report generation
│   └── generator.py     # Report generation with pandas
├── reports_output/         # Generated Excel reports
├── venv/                  # Virtual environment
└── .gitignore             # Git ignore rules
```

## Configuration

All configuration is stored in `data/config.xlsx` with the following sheets:

### Settings Sheet
| Key | Value |
|------|--------|
| company_name | ABC Company |
| currency | $ |
| currency_symbol | $ |

### Shifts Sheet
| Shift Name | Start Time | End Time |
|------------|-------------|-----------|
| Morning | 08:00 | 17:00 |
| Evening | 16:00 | 00:00 |
| Night | 00:00 | 08:00 |

### Employees Sheet
| Employee ID | Name | Shift | Hourly Rate | Leave Balance |
|-------------|-------|-------|-------------|---------------|
| E001 | Sokha | Morning | 5.0 | 12 |
| E002 | Channary | Evening | 6.0 | 10 |

### Attendance Sheet
| Employee ID | Date | Check-in | Check-out |
|-------------|------|----------|-----------|
| E001 | 2026-03-28 | 08:02 | 17:05 |

## Usage

### Run the Application

```bash
python main.py
```

### Main Menu

```
═════════════════════════════════════════════════
  ATTENDANCE MANAGEMENT SYSTEM
═════════════════════════════════════════════════
  1. Operation
  2. Report
  3. Export
  4. Exit
──────────────────────────────────────────────────
```

### Operation Menu

Check in/out employees and request leave. Shows today's attendance in real-time.

```
──────────────────────────────────────────────────────────
  OPERATION
──────────────────────────────────────────────────────────
+------+----------+------------+-------------+-------------+
| ID   | Name     | Check In   | Check Out   | Status      |
+======+==========+============+=============+=============+
| E001 | Sokha    | 08:02      | 17:05       | Checked Out |
| E002 | Channary | —          | —           | Absent     |
+------+----------+------------+-------------+-------------+
──────────────────────────────────────────────────────────
  1. Check-in
  2. Check-out
  3. Leave Request
  4. Back to Main Menu
```

### Report Menu

View detailed reports and summaries.

```
──────────────────────────────
  REPORT
──────────────────────────────
  1. Employee Detail
  2. All Attendance
  3. Payroll
  4. Full Summary
  5. Back to Main Menu
```

#### Report Options

1. **Employee Detail**: Shows all employees with their shift, hourly rate, and leave balance
2. **All Attendance**: Displays complete attendance history
3. **Payroll**: Shows hours worked and total pay per employee
4. **Full Summary**: Combined view of hours, leave status, and payroll

### Export

Export all reports to Excel with timestamped filenames in `reports_output/` directory.

## Data Persistence

All data is automatically saved to `data/config.xlsx` after each operation:

- **Check-in**: Saves new attendance record
- **Check-out**: Updates existing attendance record
- **Leave Request**: Updates employee leave balance

No manual data saving required.

## Troubleshooting

### Excel File Not Found
If you see "Error: data/config.xlsx not found", ensure:
- The `data/` directory exists
- `config.xlsx` file is in `data/`
- File is not corrupted (try opening in Excel)

### Import Errors
If you see module import errors:
```bash
# Reinstall dependencies
pip install --upgrade pandas openpyxl tabulate colorama
```

### Virtual Environment Issues
If venv activation fails:
```bash
# Delete and recreate venv
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install pandas openpyxl tabulate colorama
```

### Clear Compiled Python Cache
If you encounter stale bytecode issues:
```bash
find . -type d -name __pycache__ -exec rm -rf {} +
```

## Development

### Running Tests (when available)
```bash
# Run all tests
python -m pytest

# Run single test
python -m pytest -k test_name

# Run with coverage
python -m pytest --cov=. --cov-report=term-missing
```

### Code Style
This project follows the conventions documented in `AGENTS.md` for AI agents.

## License

This project is provided as-is for educational purposes.

## Support

For issues or questions, refer to `AGENTS.md` for coding guidelines and development practices.
