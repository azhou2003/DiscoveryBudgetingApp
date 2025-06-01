from dotenv import load_dotenv
load_dotenv()
from budgeting.census_api import CensusExpenditure
from budgeting.discover_activity_processing import DiscoverActProc
from budgeting.bls_comparator import BLSComparator
from utils.plotting import plot_spending_summary
from ui.theme_manager import apply_theme

# Directly assign API keys for now (you can switch back to os.getenv if you prefer dotenv)

import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import BudgetApp  # Adjust if your path is different

def main():
    app = QApplication(sys.argv)
    apply_theme(app)
    window = BudgetApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()