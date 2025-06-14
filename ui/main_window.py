import sys
import os
import json
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QFileDialog,
    QVBoxLayout, QLabel, QPushButton, QTabWidget, QComboBox,
    QTableWidget, QTableWidgetItem, QHBoxLayout, QLineEdit, QToolBar,
    QStatusBar, QDateEdit, QMessageBox, QCheckBox, QSizePolicy
)
from PyQt6.QtCore import Qt, QDate
from budgeting.discover_activity_processing import DiscoverActProc
from budgeting.bls_comparator import BLSComparator
from datetime import datetime
import pyqtgraph as pg

from .transactions_tab import TransactionsTab
from .trends_tab import TrendsTab
from .bls_tab import BLSTab
from .budget_tab import BudgetTab
from .theme_manager import apply_theme
from PyQt6.QtGui import QAction, QIcon
from .style_guide import spacing, colors, fonts
from .toolbar import ToolbarWidget

class BudgetApp(QMainWindow):
    """
    Main application window for the Discovery Budgeting App.
    Manages tabs, toolbar, and core UI logic.
    """
    def __init__(self):
        """
        Initialize the main window, toolbar, tabs, and status bar.
        """
        super().__init__()
        self.setWindowTitle("Discovery Budgeting App")
        self.setMinimumSize(1000, 600)
        self.resize(1200, 800)
        self.processors = []
        self.bls_comparator = None

        # Use the new ToolbarWidget
        self.toolbar = ToolbarWidget(self)
        self.addToolBar(self.toolbar)

        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.TabPosition.North)
        self.tabs.setMovable(False)
        self.tabs.setStyleSheet("QTabBar::tab { min-width: 160px; padding: 12px 24px; font-size: 15px; }")
        self.tabs.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setCentralWidget(self.tabs)

        # Instantiate tabs and pass self for callbacks/state
        self.transactions_tab = TransactionsTab(self)
        self.trends_tab = TrendsTab(self)
        self.bls_tab = BLSTab(self)
        self.budget_tab = BudgetTab(self)

        self.tabs.addTab(self.transactions_tab, "Transactions")
        self.tabs.addTab(self.trends_tab, "Trends")
        self.tabs.addTab(self.bls_tab, "BLS Comparison")
        self.tabs.addTab(self.budget_tab, "Budget Management")

        self.setStatusBar(QStatusBar())

        # Aliases for widgets used in logic methods
        self.file_selector_table = self.transactions_tab.file_selector_table
        self.trans_table = self.transactions_tab.trans_table
        self.category_selector = self.trends_tab.category_selector
        self.show_budget_checkbox = self.trends_tab.show_budget_checkbox
        self.show_bls_checkbox = self.trends_tab.show_bls_checkbox
        self.plot_widget = self.trends_tab.plot_widget
        self.bls_table = self.bls_tab.bls_table
        self.budget_table = self.budget_tab.budget_table

    def show_help_dialog(self):
        QMessageBox.information(self, "Help", "Need help? Visit the documentation or contact support.")

    def show_documentation(self):
        QMessageBox.information(self, "Documentation", "Open the user guide or documentation website.")

    def load_csv(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Bank CSV", "resources/", "CSV Files (*.csv)")
        if file_path:
            # Prompt for bank type (for now, just Discover)
            bank_type = "Discover"
            processor = DiscoverActProc(file_path, bls_comparator=self.bls_comparator)
            self.processors.append({
                'file_path': file_path,
                'processor': processor,
                'bank_type': bank_type,
                'checked': True
            })
            self.update_file_selector()
            self.statusBar().showMessage(f"CSV file loaded: {file_path}")

    def load_bls(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select BLS JSON", "data/", "JSON Files (*.json)")
        if file_path:
            self.bls_file_path = file_path
            try:
                with open(file_path, "r") as f:
                    bls_data = json.load(f)
                self.bls_comparator = BLSComparator(bls_api_key="demo")
                self.bls_comparator.bls_data = bls_data
                self.statusBar().showMessage(f"BLS file selected: {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load BLS file: {e}")
                self.bls_comparator = None
    
    def analyze_spending(self):
        checked_procs = [p['processor'] for p in self.processors if p['checked']]
        if not checked_procs:
            QMessageBox.warning(self, "No Files Selected", "Please select at least one file to analyze.")
            return

        # Aggregate date range
        all_dates = []
        for proc in checked_procs:
            all_dates += list(proc.transactions_dict.keys())
        if not all_dates:
            self.update_date_range_label(None, None)
            return
        first_date = min(all_dates)
        last_date = max(all_dates)
        self.update_date_range_label(first_date, last_date)

        # Analyze each processor for the selected date range
        start = first_date
        end = last_date
        for proc in checked_procs:
            proc.analyze_spending(
                start_date=datetime.combine(start, datetime.min.time()),
                end_date=datetime.combine(end, datetime.min.time())
            )        # Now aggregate for UI updates
        self.update_transaction_table()
        self.update_category_selector()
        self.update_trend_plot()
        self.populate_budget_table()
        if self.bls_comparator:
            self.update_bls_table()
        self.statusBar().showMessage("Analysis complete.")

    def update_bls_table(self):
        checked_procs = [p['processor'] for p in self.processors if p['checked']]
        if not checked_procs or not self.bls_comparator:
            return

        # Aggregate weekly user averages by category
        user_weekly_by_cat = {}
        count_by_cat = {}
        for proc in checked_procs:
            for cat, avg in proc.average_spending_by_category.items():
                user_weekly_by_cat[cat] = user_weekly_by_cat.get(cat, 0) + avg
                count_by_cat[cat] = count_by_cat.get(cat, 0) + 1
        for cat in user_weekly_by_cat:
            user_weekly_by_cat[cat] /= count_by_cat[cat]

        # Update the BLS tab with new methods
        self.bls_tab.populate_from_processors(self.processors)
        if hasattr(self.bls_comparator, 'bls_data'):
            self.bls_tab.set_bls_data(self.bls_comparator.bls_data)

        # Prepare BLS comparison data for legacy table (backward compatibility)
        self.bls_table.setRowCount(0)
        for cat in sorted(user_weekly_by_cat.keys()):
            user_weekly = user_weekly_by_cat[cat]
            bls_weekly = None
            if self.bls_comparator and hasattr(self.bls_comparator, 'get_bls_avg_for_user_category'):
                bls_annual = self.bls_comparator.get_bls_avg_for_user_category(cat)
                if bls_annual is not None:
                    bls_weekly = bls_annual / 52
            row = self.bls_table.rowCount()
            self.bls_table.insertRow(row)
            self.bls_table.setItem(row, 0, QTableWidgetItem(str(cat)))
            self.bls_table.setItem(row, 1, QTableWidgetItem(f"${user_weekly:.2f}"))
            if bls_weekly is not None:
                self.bls_table.setItem(row, 2, QTableWidgetItem(f"${bls_weekly:.2f}"))
                self.bls_table.setItem(row, 3, QTableWidgetItem(f"${user_weekly - bls_weekly:.2f}"))
            else:
                self.bls_table.setItem(row, 2, QTableWidgetItem("N/A"))
                self.bls_table.setItem(row, 3, QTableWidgetItem("N/A"))

    def update_transaction_table(self):
        checked_procs = [p['processor'] for p in self.processors if p['checked']]
        self.trans_table.setRowCount(0)
        all_transactions = []
        for proc in checked_procs:
            for date in sorted(proc.transactions_dict):
                for category, amount in proc.transactions_dict[date]:
                    all_transactions.append((date, category, amount))
        all_transactions.sort()
        for date, category, amount in all_transactions:
            row = self.trans_table.rowCount()
            self.trans_table.insertRow(row)
            self.trans_table.setItem(row, 0, QTableWidgetItem(date.strftime("%Y-%m-%d")))
            self.trans_table.setItem(row, 1, QTableWidgetItem(category))
            self.trans_table.setItem(row, 2, QTableWidgetItem(f"${amount:.2f}"))


    def reload_with_dates(self):
        checked_procs = [p['processor'] for p in self.processors if p['checked']]
        if not checked_procs:
            return
        # Use the current date range from the label (if available)
        # This function is now a no-op for date range, but kept for compatibility
        self.update_transaction_table()
        self.update_trend_plot()
        self.populate_budget_table()

    def save_config(self):
        config = {
            "budgets": {},
        }
        for i in range(self.budget_table.rowCount()):
            cat = self.budget_table.item(i, 0).text()
            budget_input = self.budget_table.cellWidget(i, 1)
            try:
                budget = float(budget_input.text())
                config["budgets"][cat] = budget
            except ValueError:
                continue

        file_path, _ = QFileDialog.getSaveFileName(self, "Save Config", "config.json", "JSON Files (*.json)")
        if file_path:
            with open(file_path, "w") as f:
                json.dump(config, f, indent=2)
            self.statusBar().showMessage(f"Saved config to {file_path}")

    def load_config(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Load Config", "config.json", "JSON Files (*.json)")
        if file_path:
            with open(file_path, "r") as f:
                config = json.load(f)
            budgets = config.get("budgets", {})
            for i in range(self.budget_table.rowCount()):
                cat = self.budget_table.item(i, 0).text()
                if cat in budgets:
                    self.budget_table.cellWidget(i, 1).setText(str(budgets[cat]))
            self.update_budget_comparison()
            self.statusBar().showMessage(f"Loaded config from {file_path}")

    def update_trend_plot(self):
        checked_procs = [p['processor'] for p in self.processors if p['checked']]
        if not checked_procs:
            self.plot_widget.clear()
            self.plot_widget.setTitle("No data available.")
            return

        self.plot_widget.clear()

        selected_category = self.category_selector.currentText()
        show_budget = self.show_budget_checkbox.isChecked()
        show_bls = self.show_bls_checkbox.isChecked()

        # Aggregate data
        if selected_category == "Total Spending":
            # Sum weekly spending across all checked processors
            weekly_totals = {}
            for proc in checked_procs:
                for week, val in proc.weekly_spending.items():
                    weekly_totals[week] = weekly_totals.get(week, 0) + val
            if not weekly_totals:
                self.plot_widget.setTitle("No data available.")
                return
            weeks = sorted(weekly_totals.keys())
            values = [weekly_totals[wk] for wk in weeks]
            # Convert weeks (datetime) to indices and labels for pyqtgraph
            week_labels = [wk.strftime('%Y-%m-%d') for wk in weeks]
            x_vals = list(range(len(weeks)))
            self.plot_widget.plot(x_vals, values, pen='b', symbol='o', label='User Spending')
            avg_actual = sum(values) / len(values) if values else 0

            # --- BLS aggregation for Total Spending ---
            bls_avg = None
            if self.bls_comparator and hasattr(self.bls_comparator, 'get_bls_avg_for_user_category'):
                # Aggregate all categories present in checked files
                all_categories = set()
                for proc in checked_procs:
                    all_categories.update(proc.category_series.keys())
                bls_avg = 0
                for cat in all_categories:
                    cat_bls = self.bls_comparator.get_bls_avg_for_user_category(cat)
                    if cat_bls is not None:
                        bls_avg += cat_bls / 52  # Convert annual to weekly
                if bls_avg == 0:
                    bls_avg = None
            if show_bls and bls_avg is not None:
                self.plot_widget.plot(x_vals, [bls_avg] * len(x_vals), pen=pg.mkPen('r', style=Qt.PenStyle.DashLine, width=2), label='BLS Avg')
            if show_budget:
                user_budget_total = 0
                for i in range(self.budget_table.rowCount()):
                    try:
                        val = float(self.budget_table.cellWidget(i, 1).text())
                        user_budget_total += val
                    except ValueError:
                        continue
                self.plot_widget.plot(x_vals, [user_budget_total] * len(x_vals), pen=pg.mkPen('g', style=Qt.PenStyle.DashLine, width=2), label='Budget')
        else:
            # Aggregate category series with grouping support
            category_series = {}
            for proc in checked_procs:
                # Check if this is a grouped category or original category
                if selected_category in proc.category_series:
                    # Direct match - use as is
                    for week, val in proc.category_series[selected_category].items():
                        category_series[week] = category_series.get(week, 0) + val
                else:
                    # Check if this is a grouped category by looking up original categories
                    original_cats = self.trends_tab.category_manager.get_original_categories_for_group(selected_category)
                    for orig_cat in original_cats:
                        for week, val in proc.category_series.get(orig_cat, {}).items():
                            category_series[week] = category_series.get(week, 0) + val
            if not category_series:
                self.plot_widget.setTitle("No data available.")
                return
            weeks = sorted(category_series.keys())
            values = [category_series[wk] for wk in weeks]
            week_labels = [wk.strftime('%Y-%m-%d') for wk in weeks]
            x_vals = list(range(len(weeks)))
            self.plot_widget.plot(x_vals, values, pen='b', symbol='o', label='User Spending')
            avg_actual = sum(values) / len(values) if values else 0
            bls_avg = None
            if self.bls_comparator and hasattr(self.bls_comparator, 'get_bls_avg_for_user_category'):
                bls_avg = self.bls_comparator.get_bls_avg_for_user_category(selected_category)
                if bls_avg is not None:
                    bls_avg = bls_avg / 52  # Convert annual to weekly
            if show_bls and bls_avg is not None:
                self.plot_widget.plot(x_vals, [bls_avg] * len(x_vals), pen=pg.mkPen('r', style=Qt.PenStyle.DashLine, width=2), label='BLS Avg')
            if show_budget:
                user_budget = self.get_user_budget(selected_category)
                if user_budget is not None:
                    self.plot_widget.plot(x_vals, [user_budget] * len(x_vals), pen=pg.mkPen('g', style=Qt.PenStyle.DashLine, width=2), label='Budget')

        self.plot_widget.setTitle(f"Weekly Trend: {selected_category}")
        self.plot_widget.setLabel('left', 'Amount ($)')
        self.plot_widget.setLabel('bottom', 'Week Starting')
        # Set custom x-axis ticks for week labels
        ax = self.plot_widget.getAxis('bottom')
        ax.setTicks([list(zip(x_vals, week_labels))])
        self.plot_widget.addLegend()
        self.plot_widget.setXRange(0, len(x_vals)-1, padding=0)
        self.plot_widget.setYRange(0, max(values) * 1.1, padding=0)

    def get_user_budget(self, category):
        for i in range(self.budget_table.rowCount()):
            if self.budget_table.item(i, 0).text() == category:
                budget_input = self.budget_table.cellWidget(i, 1)
                try:
                    return float(budget_input.text())
                except ValueError:
                    return None
        return None

    def populate_budget_table(self):
        checked_procs = [p['processor'] for p in self.processors if p['checked']]
        if not checked_procs:
            return

        # Aggregate average spending by category
        avg_by_cat = {}
        count_by_cat = {}
        for proc in checked_procs:
            for cat, avg in proc.average_spending_by_category.items():
                avg_by_cat[cat] = avg_by_cat.get(cat, 0) + avg
                count_by_cat[cat] = count_by_cat.get(cat, 0) + 1
        
        # Apply category grouping to budget data
        grouped_avg_by_cat = self.budget_tab.apply_category_grouping_to_budget(avg_by_cat)
        grouped_count_by_cat = self.budget_tab.apply_category_grouping_to_budget(count_by_cat)
        
        categories = sorted(grouped_avg_by_cat.keys())
        self.budget_table.setRowCount(len(categories))

        for i, cat in enumerate(categories):
            self.budget_table.setItem(i, 0, QTableWidgetItem(cat))

            # Preserve user input if it exists
            existing_widget = self.budget_table.cellWidget(i, 1)
            if existing_widget is not None:
                budget_input = existing_widget
            else:
                budget_input = QLineEdit()
                budget_input.setText("0")
                self.budget_table.setCellWidget(i, 1, budget_input)

            actual = grouped_avg_by_cat[cat] / grouped_count_by_cat[cat] if grouped_count_by_cat[cat] else 0
            self.budget_table.setItem(i, 2, QTableWidgetItem(f"${actual:.2f}"))
            self.budget_table.setItem(i, 3, QTableWidgetItem("-"))

    def update_budget_comparison(self):
        for i in range(self.budget_table.rowCount()):
            cat = self.budget_table.item(i, 0).text()
            budget_input = self.budget_table.cellWidget(i, 1)
            try:
                budget = float(budget_input.text())
            except ValueError:
                budget = 0

            actual = float(self.budget_table.item(i, 2).text().replace("$", ""))
            diff = actual - budget
            self.budget_table.setItem(i, 3, QTableWidgetItem(f"${diff:.2f}"))

    def update_file_selector(self):
        self.file_selector_table.blockSignals(True)
        self.file_selector_table.setRowCount(len(self.processors))
        for i, proc in enumerate(self.processors):
            # Checkbox
            checkbox = QCheckBox()
            checkbox.setChecked(proc['checked'])
            checkbox.stateChanged.connect(lambda state, idx=i: self.set_processor_checked(idx, state))
            self.file_selector_table.setCellWidget(i, 0, checkbox)
            # File name
            self.file_selector_table.setItem(i, 1, QTableWidgetItem(os.path.basename(proc['file_path'])))
            # Bank type
            self.file_selector_table.setItem(i, 2, QTableWidgetItem(proc['bank_type']))
        self.file_selector_table.blockSignals(False)

    def set_processor_checked(self, idx, state):
        self.processors[idx]['checked'] = bool(state)
        self.analyze_spending()

    def on_file_selector_changed(self, row, column):
        if column == 0:
            checked = self.file_selector_table.cellWidget(row, 0).isChecked()
            self.processors[row]['checked'] = checked
            self.analyze_spending()

    def update_category_selector(self):
        checked_procs = [p['processor'] for p in self.processors if p['checked']]
        categories = set()
        for proc in checked_procs:
            categories.update(proc.category_series.keys())
        
        # Apply category grouping to the category list
        grouped_categories = self.trends_tab.get_grouped_categories(list(categories))
        
        self.category_selector.clear()
        self.category_selector.addItem("Total Spending")
        for cat in sorted(grouped_categories):
            self.category_selector.addItem(cat)

    def compare_spending(self, user_spending_by_category):
        results = {}
        for user_cat, user_annual in user_spending_by_category.items():
            bls_cat = self.category_mapping.get(user_cat)
            if not bls_cat:
                continue
            bls_annual = self.bls_data.get(bls_cat)
            if bls_annual is None:
                continue
            # Convert annual BLS value to weekly
            bls_weekly = bls_annual / 52
            user_weekly = user_annual / 52  # if user_annual is also annual, otherwise just use user_annual
            results[bls_cat] = {
                "user": user_annual,  # or user_weekly if you want to compare weekly
                "bls_avg": bls_weekly,
                "difference": user_annual - bls_weekly  # or user_weekly - bls_weekly
            }
        return results

        # Aggregate weekly user averages by category
        user_weekly_by_cat = {}
        count_by_cat = {}
        for proc in checked_procs:
            for cat, avg in proc.average_spending_by_category.items():
                user_weekly_by_cat[cat] = user_weekly_by_cat.get(cat, 0) + avg
                count_by_cat[cat] = count_by_cat.get(cat, 0) + 1
        for cat in user_weekly_by_cat:
            user_weekly_by_cat[cat] /= count_by_cat[cat]

    def update_date_range_label(self, start_date, end_date):
        """
        Update the date range label in the toolbar.
        Args:
            start_date: datetime.date or None
            end_date: datetime.date or None
        """
        self.toolbar.update_date_range_label(start_date, end_date)
