from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QPushButton, QHBoxLayout, QLabel, QSizePolicy
from PyQt6.QtCore import Qt
from .style_guide import spacing, fonts
from budgeting.category_manager import CategoryManager

class BudgetTab(QWidget):
    """
    Tab for managing and editing the user's budget, including budget comparison and tips.
    """
    
    def __init__(self, main_window):
        """
        Initialize the BudgetTab with budget table, save/load buttons, and budgeting tips.
        Args:
            main_window: Reference to the main application window for callbacks.
        """
        super().__init__()
        self.main_window = main_window
        self.category_manager = CategoryManager()

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(spacing['lg'], spacing['lg'], spacing['lg'], spacing['lg'])
        main_layout.setSpacing(spacing['lg'])

        # Left: Budget comparison section
        left_vbox = QVBoxLayout()
        left_vbox.setSpacing(spacing['sm'])

        budget_header = QLabel("Budget Comparison")
        budget_header.setStyleSheet(
            f"font-size: {fonts['heading_size']}px; font-weight: {fonts['heading_weight']}; margin-bottom: {spacing['sm']}px;"
        )
        budget_header.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        budget_header.setContentsMargins(0, 0, 0, 0)
        budget_header.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        left_vbox.addWidget(budget_header)

        self.budget_table = QTableWidget()
        self.budget_table.setColumnCount(4)
        self.budget_table.setHorizontalHeaderLabels(["Category", "Weekly Budget", "Actual Avg", "Diff"])
        self.budget_table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.budget_table.setMinimumHeight(400)
        self.budget_table.setMinimumWidth(400)
        self.budget_table.setToolTip("Set your weekly budget for each category")
        self.budget_table.horizontalHeader().setStretchLastSection(True)
        self.budget_table.verticalHeader().setDefaultSectionSize(43)
        left_vbox.addWidget(self.budget_table)

        self.save_button = QPushButton("Save Config")
        self.save_button.clicked.connect(self.main_window.save_config)
        self.load_button = QPushButton("Load Config")
        self.load_button.clicked.connect(self.main_window.load_config)
        button_hbox = QHBoxLayout()
        button_hbox.setSpacing(spacing['md'])
        button_hbox.setContentsMargins(0, spacing['md'], 0, 0)
        button_hbox.addWidget(self.save_button)
        button_hbox.addWidget(self.load_button)
        left_vbox.addLayout(button_hbox)
        left_vbox.addStretch(1)

        # Right: Budgeting tips section
        tips_vbox = QVBoxLayout()
        tips_vbox.setContentsMargins(spacing['md'], spacing['md'], spacing['md'], spacing['md'])
        tips_vbox.setSpacing(spacing['sm'])
        tips_label = QLabel("Budgeting Tips")
        tips_label.setStyleSheet(
            f"font-size: {fonts['heading_size']}px; font-weight: {fonts['heading_weight']}; margin-bottom: {spacing['sm']}px;"
        )
        tips_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        tips_vbox.addWidget(tips_label)
        tips_content = QLabel("- Set realistic weekly budgets for each category.\n- Compare your actual spending to your budget.\n- Adjust your budget as needed to meet your goals.")
        tips_content.setWordWrap(True)
        tips_vbox.addWidget(tips_content)
        tips_vbox.addStretch(1)
        tips_widget = QWidget()
        tips_widget.setLayout(tips_vbox)
        tips_widget.setMinimumWidth(200)
        tips_widget.setMaximumWidth(400)
        tips_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        main_layout.addLayout(left_vbox, 3)
        main_layout.addWidget(tips_widget, 2)
        self.setLayout(main_layout)        # Responsive column resizing
        self.budget_table.horizontalHeader().setSectionResizeMode(self.budget_table.horizontalHeader().ResizeMode.Stretch)
        for col in range(self.budget_table.columnCount()):
            self.budget_table.horizontalHeader().setSectionResizeMode(col, self.budget_table.horizontalHeader().ResizeMode.Stretch)
    
    def apply_category_grouping_to_budget(self, categories_data):
        """Apply category grouping to budget data"""
        return self.category_manager.apply_grouping_to_data(categories_data)
    
    def get_grouped_categories(self, original_categories):
        """Get grouped categories for display in budget table"""
        return self.category_manager.get_grouped_categories(original_categories)