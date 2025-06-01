from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, 
                            QLabel, QPushButton, QTableWidget, QTableWidgetItem,
                            QSplitter, QGroupBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from .category_grouping_widget import CategoryGroupingWidget
from budgeting.category_manager import CategoryManager

class BLSTab(QWidget):
    """BLS Comparison tab with category grouping functionality"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.category_manager = CategoryManager()
        self.current_data = {}
        self.bls_data = {}
        self.setup_ui()
        
        # For backward compatibility with main window
        self.bls_table = self.comparison_table
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Create tab widget for BLS functionality
        tab_widget = QTabWidget()
        layout.addWidget(tab_widget)
        
        # BLS Comparison tab
        comparison_tab = self.create_comparison_tab()
        tab_widget.addTab(comparison_tab, "BLS Comparison")
        
        # Category Grouping tab
        grouping_tab = self.create_grouping_tab()
        tab_widget.addTab(grouping_tab, "Category Grouping")
        
    def create_comparison_tab(self):
        """Create the BLS comparison tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Title
        title = QLabel("BLS Consumer Expenditure Survey Comparison")
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(title)
          # Table for comparison data (full width)
        self.comparison_table = QTableWidget()
        self.comparison_table.setColumnCount(5)
        self.comparison_table.setHorizontalHeaderLabels([
            "Category", "Your Spending", "BLS Average", "Difference", "Difference (%)"
        ])
        
        # Set table to stretch to full width with equal column widths
        header = self.comparison_table.horizontalHeader()
        for i in range(5):
            header.setSectionResizeMode(i, header.ResizeMode.Stretch)
        
        layout.addWidget(self.comparison_table)
        
        return widget
        
    def create_grouping_tab(self):
        """Create the category grouping tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Category grouping widget
        self.grouping_widget = CategoryGroupingWidget()
        self.grouping_widget.categories_updated.connect(self.on_categories_updated)
        layout.addWidget(self.grouping_widget)
        
        # Load existing groups
        existing_groups = self.category_manager.get_groups()
        self.grouping_widget.set_category_groups(existing_groups)
        
        return widget
        
    def set_transaction_data(self, categories):
        """Set the transaction categories for grouping"""
        category_list = list(categories.keys()) if isinstance(categories, dict) else list(categories)
        self.grouping_widget.set_categories(category_list)
        self.current_data = categories if isinstance(categories, dict) else {}
        self.update_comparison()
        
    def set_bls_data(self, bls_data):
        """Set the BLS comparison data"""
        self.bls_data = bls_data
        self.update_comparison()
        
    def on_categories_updated(self, category_mapping):
        """Handle category grouping updates"""
        # Save the groups to the category manager
        groups = self.grouping_widget.get_category_groups()
        self.category_manager.set_groups(groups)
        
        # Update the comparison with grouped data
        self.update_comparison()
        
    def update_comparison(self):
        """Update the BLS comparison table"""
        if not self.current_data or not self.bls_data:
            return
            
        # Apply category grouping to current data
        grouped_data = self.category_manager.apply_grouping_to_data(self.current_data)
        
        # Update table
        self.update_comparison_table(grouped_data)
        
    def update_comparison_table(self, grouped_data):
        """Update the comparison table with grouped data"""
        self.comparison_table.setRowCount(len(grouped_data))
        
        row = 0
        for category, your_spending in grouped_data.items():
            # Category name
            self.comparison_table.setItem(row, 0, QTableWidgetItem(category))
            
            # Your spending
            self.comparison_table.setItem(row, 1, QTableWidgetItem(f"${your_spending:.2f}"))
              # BLS average (if available)
            bls_amount = self.bls_data.get(category, 0)
            self.comparison_table.setItem(row, 2, QTableWidgetItem(f"${bls_amount:.2f}"))
            
            # Raw difference
            raw_diff = your_spending - bls_amount
            diff_item = QTableWidgetItem(f"${raw_diff:+.2f}")
            if raw_diff > 0:
                diff_item.setBackground(QColor(255, 200, 200))  # Light red
            elif raw_diff < 0:
                diff_item.setBackground(QColor(200, 255, 200))  # Light green
            self.comparison_table.setItem(row, 3, diff_item)
            
            # Percentage difference
            if bls_amount > 0:
                diff_pct = (raw_diff / bls_amount) * 100
                pct_text = f"{diff_pct:+.1f}%"
                pct_item = QTableWidgetItem(pct_text)
                if diff_pct > 0:
                    pct_item.setBackground(QColor(255, 200, 200))  # Light red
                elif diff_pct < 0:
                    pct_item.setBackground(QColor(200, 255, 200))  # Light green
                self.comparison_table.setItem(row, 4, pct_item)
            else:
                self.comparison_table.setItem(row, 4, QTableWidgetItem("N/A"))                
            row += 1
        
    def update_bls_table(self, user_weekly_by_cat, bls_comparator):
        """Update BLS table - for compatibility with main window"""
        # Apply category grouping to user data
        grouped_data = self.category_manager.apply_grouping_to_data(user_weekly_by_cat)
        
        # Update internal data
        self.current_data = grouped_data
        if bls_comparator and hasattr(bls_comparator, 'bls_data'):
            self.bls_data = bls_comparator.bls_data
            
        # Update the comparison
        self.update_comparison()
        
    def populate_from_processors(self, processors):
        """Populate category data from transaction processors"""
        if not processors:
            print("DEBUG: No processors provided")
            return
            
        # Extract all categories from processors
        all_categories = set()
        category_totals = {}
        
        print(f"DEBUG: Processing {len(processors)} processors")
        for proc_info in processors:
            print(f"DEBUG: Processor info: {proc_info.keys()}")
            if not proc_info.get('checked', False):
                print(f"DEBUG: Processor not checked, skipping")
                continue
                
            processor = proc_info['processor']
            print(f"DEBUG: Processor has average_spending_by_category: {hasattr(processor, 'average_spending_by_category')}")
            if hasattr(processor, 'average_spending_by_category'):
                categories = processor.average_spending_by_category
                print(f"DEBUG: Found {len(categories)} categories: {list(categories.keys())}")
                for cat, amount in categories.items():
                    all_categories.add(cat)
                    if cat in category_totals:
                        category_totals[cat] += amount
                    else:
                        category_totals[cat] = amount
        
        print(f"DEBUG: Total categories found: {len(all_categories)}")
        print(f"DEBUG: Categories: {list(all_categories)}")
        
        # Set categories for grouping widget
        self.grouping_widget.set_categories(list(all_categories))
        self.current_data = category_totals
        self.update_comparison()