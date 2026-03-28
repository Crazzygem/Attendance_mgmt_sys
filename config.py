# Minimal config - all data loaded from Excel
import os
from datetime import datetime

EXCEL_CONFIG_PATH = "data/config.xlsx"
REPORT_OUTPUT_DIR = "reports_output"


def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


def ensure_report_dir():
    if not os.path.exists(REPORT_OUTPUT_DIR):
        os.makedirs(REPORT_OUTPUT_DIR)
