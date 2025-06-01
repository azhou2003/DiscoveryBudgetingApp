# filepath: c:\Users\Anjie\Desktop\Projects\DiscoveryBudgetingApp\ui\category_grouping_widget.py
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QListWidget, 
                            QPushButton, QLabel, QComboBox, QMessageBox, 
                            QListWidgetItem, QGroupBox, QSplitter)
from PyQt6.QtCore import Qt, pyqtSignal
from typing import Dict, List, Set

class CategoryGroupingWidget(QWidget):
    """Widget for grouping and managing transaction categories"""
    
    categories_updated = pyqtSignal(dict)  # Emitted when category groupings change
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.category_groups = {}  # {group_name: [category_list]}
        self.original_categories = set()
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Main splitter for side-by-side layout
        splitter = QSplitter(Qt.Orientation.Horizontal)
        layout.addWidget(splitter)
        
        # Left side - Available categories
        left_widget = self.create_available_categories_widget()
        splitter.addWidget(left_widget)
        
        # Right side - Category groups
        right_widget = self.create_category_groups_widget()
        splitter.addWidget(right_widget)
        
        # Set splitter proportions
        splitter.setSizes([300, 400])
        
        # Bottom buttons
        button_layout = QHBoxLayout()
        
        self.group_button = QPushButton("Group Selected Categories")
        self.group_button.clicked.connect(self.group_selected_categories)
        self.group_button.setEnabled(False)
        button_layout.addWidget(self.group_button)
        
        self.ungroup_button = QPushButton("Ungroup Selected")
        self.ungroup_button.clicked.connect(self.ungroup_selected_categories)
        self.ungroup_button.setEnabled(False)
        button_layout.addWidget(self.ungroup_button)
        
        button_layout.addStretch()
        
        reset_button = QPushButton("Reset All Groups")
        reset_button.clicked.connect(self.reset_all_groups)
        button_layout.addWidget(reset_button)
        
        layout.addLayout(button_layout)
    
    def create_available_categories_widget(self):
        """Create the widget showing available categories to group"""
        widget = QWidget()
        main_layout = QVBoxLayout(widget)
        
        # Header
        header = QLabel("Available Categories")
        header.setStyleSheet("font-size: 14px; font-weight: bold; margin-bottom: 5px;")
        main_layout.addWidget(header)
        
        # Content container
        group_box = QGroupBox()
        group_box.setTitle("")  # Remove title since we have header above
        layout = QVBoxLayout(group_box)
        
        # Instructions
        instructions = QLabel("Select multiple categories to group them together:")
        instructions.setWordWrap(True)
        layout.addWidget(instructions)
        
        # Category list
        self.available_list = QListWidget()
        self.available_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        self.available_list.itemSelectionChanged.connect(self.on_selection_changed)
        layout.addWidget(self.available_list)
        
        # Group name selection
        group_name_layout = QHBoxLayout()
        group_name_layout.addWidget(QLabel("Group as:"))
        
        self.group_name_combo = QComboBox()
        self.group_name_combo.setEditable(True)
        self.group_name_combo.setPlaceholderText("Select or enter category name")
        group_name_layout.addWidget(self.group_name_combo)
        
        layout.addLayout(group_name_layout)
        
        main_layout.addWidget(group_box)
        return widget
        
    def create_category_groups_widget(self):
        """Create the widget showing current category groups"""
        widget = QWidget()
        main_layout = QVBoxLayout(widget)
        
        # Header
        header = QLabel("Current Category Groups")
        header.setStyleSheet("font-size: 14px; font-weight: bold; margin-bottom: 5px;")
        main_layout.addWidget(header)
        
        # Content container  
        group_box = QGroupBox()
        group_box.setTitle("")  # Remove title since we have header above
        layout = QVBoxLayout(group_box)
        
        # Instructions
        instructions = QLabel("Current groupings (select to ungroup):")
        layout.addWidget(instructions)
        
        # Groups list
        self.groups_list = QListWidget()
        self.groups_list.itemSelectionChanged.connect(self.on_groups_selection_changed)
        layout.addWidget(self.groups_list)
        
        main_layout.addWidget(group_box)
        return widget
        
    def set_categories(self, categories: List[str]):
        """Set the available categories"""
        print(f"DEBUG CategoryGroupingWidget: Setting {len(categories)} categories: {categories}")
        self.original_categories = set(categories)
        self.refresh_available_categories()
        self.update_group_name_combo()
        
    def refresh_available_categories(self):
        """Refresh the list of available categories (excluding grouped ones)"""
        self.available_list.clear()
        
        # Get categories that are not already grouped
        grouped_categories = set()
        for group_categories in self.category_groups.values():
            grouped_categories.update(group_categories)
            
        available_categories = self.original_categories - grouped_categories
        print(f"DEBUG: Refreshing categories. Original: {len(self.original_categories)}, Grouped: {len(grouped_categories)}, Available: {len(available_categories)}")
        
        for category in sorted(available_categories):
            item = QListWidgetItem(category)
            self.available_list.addItem(item)
            print(f"DEBUG: Added category to list: {category}")
    
    def update_group_name_combo(self):
        """Update the group name combo box with available categories"""
        self.group_name_combo.clear()
        # Add original categories as options
        for category in sorted(self.original_categories):
            self.group_name_combo.addItem(category)
            
    def refresh_groups_list(self):
        """Refresh the list of current category groups"""
        self.groups_list.clear()
        
        for group_name, categories in self.category_groups.items():
            item_text = f"{group_name} ← {', '.join(sorted(categories))}"
            item = QListWidgetItem(item_text)
            item.setData(Qt.ItemDataRole.UserRole, group_name)  # Store group name for reference
            self.groups_list.addItem(item)
            
    def on_selection_changed(self):
        """Handle selection changes in available categories list"""
        selected_items = self.available_list.selectedItems()
        self.group_button.setEnabled(len(selected_items) >= 2)
        
        # Update combo box with selected items
        if selected_items:
            self.group_name_combo.clear()
            for item in selected_items:
                self.group_name_combo.addItem(item.text())
            # Add original categories as well
            for category in sorted(self.original_categories):
                if self.group_name_combo.findText(category) == -1:
                    self.group_name_combo.addItem(category)
                    
    def on_groups_selection_changed(self):
        """Handle selection changes in groups list"""
        selected_items = self.groups_list.selectedItems()
        self.ungroup_button.setEnabled(len(selected_items) > 0)
        
    def group_selected_categories(self):
        """Group the selected categories under the chosen name"""
        selected_items = self.available_list.selectedItems()
        group_name = self.group_name_combo.currentText().strip()
        
        if len(selected_items) < 2:
            QMessageBox.warning(self, "Invalid Selection", 
                              "Please select at least 2 categories to group.")
            return
            
        if not group_name:
            QMessageBox.warning(self, "Invalid Group Name", 
                              "Please enter or select a group name.")
            return
            
        # Get selected category names
        selected_categories = [item.text() for item in selected_items]
        
        # Check if group name already exists
        if group_name in self.category_groups:
            reply = QMessageBox.question(
                self, "Group Exists", 
                f"Group '{group_name}' already exists. Do you want to add these categories to it?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                self.category_groups[group_name].extend(selected_categories)
                self.category_groups[group_name] = list(set(self.category_groups[group_name]))
            else:
                return
        else:
            self.category_groups[group_name] = selected_categories
            
        # Refresh displays
        self.refresh_available_categories()
        self.refresh_groups_list()
        
        # Clear selection
        self.available_list.clearSelection()
        self.group_name_combo.setCurrentText("")
        
        # Emit signal
        self.categories_updated.emit(self.get_category_mapping())
        
    def ungroup_selected_categories(self):
        """Ungroup the selected category groups"""
        selected_items = self.groups_list.selectedItems()
        
        if not selected_items:
            return
            
        for item in selected_items:
            group_name = item.data(Qt.ItemDataRole.UserRole)
            if group_name in self.category_groups:
                del self.category_groups[group_name]
                
        # Refresh displays
        self.refresh_available_categories()
        self.refresh_groups_list()
        
        # Clear selection
        self.groups_list.clearSelection()
        
        # Emit signal
        self.categories_updated.emit(self.get_category_mapping())
        
    def reset_all_groups(self):
        """Reset all category groups"""
        reply = QMessageBox.question(
            self, "Reset Groups", 
            "Are you sure you want to reset all category groups?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.category_groups.clear()
            self.refresh_available_categories()
            self.refresh_groups_list()
            self.categories_updated.emit(self.get_category_mapping())
            
    def get_category_mapping(self) -> Dict[str, str]:
        """Get the mapping from original categories to grouped categories"""
        mapping = {}
        
        # Add mappings for grouped categories
        for group_name, categories in self.category_groups.items():
            for category in categories:
                mapping[category] = group_name
                
        # Add identity mappings for ungrouped categories
        grouped_categories = set()
        for categories in self.category_groups.values():
            grouped_categories.update(categories)
            
        for category in self.original_categories:
            if category not in grouped_categories:
                mapping[category] = category
                
        return mapping
        
    def set_category_groups(self, groups: Dict[str, List[str]]):
        """Set existing category groups"""
        self.category_groups = groups.copy()
        self.refresh_available_categories()
        self.refresh_groups_list()
        
    def get_category_groups(self) -> Dict[str, List[str]]:
        """Get current category groups"""
        return self.category_groups.copy()