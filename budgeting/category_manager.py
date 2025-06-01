from typing import Dict, List, Set
import json
import os

class CategoryManager:
    """Manages category groupings and mappings"""
    
    def __init__(self, config_path: str = "data/category_groups.json"):
        self.config_path = config_path
        self.category_groups = {}
        self.load_groups()
        
    def load_groups(self):
        """Load category groups from file"""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    self.category_groups = json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading category groups: {e}")
                self.category_groups = {}
        else:
            self.category_groups = {}
            
    def save_groups(self):
        """Save category groups to file"""
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        try:
            with open(self.config_path, 'w') as f:
                json.dump(self.category_groups, f, indent=2)
        except IOError as e:
            print(f"Error saving category groups: {e}")
            
    def set_groups(self, groups: Dict[str, List[str]]):
        """Set category groups and save to file"""
        self.category_groups = groups.copy()
        self.save_groups()
        
    def get_groups(self) -> Dict[str, List[str]]:
        """Get current category groups"""
        return self.category_groups.copy()
        
    def get_category_mapping(self) -> Dict[str, str]:
        """Get mapping from original categories to grouped categories"""
        mapping = {}
        
        # Add mappings for grouped categories
        for group_name, categories in self.category_groups.items():
            for category in categories:
                mapping[category] = group_name
                
        return mapping
        
    def apply_grouping_to_data(self, data: Dict[str, float]) -> Dict[str, float]:
        """Apply category grouping to spending data"""
        mapping = self.get_category_mapping()
        grouped_data = {}
        
        for category, amount in data.items():
            grouped_category = mapping.get(category, category)
            if grouped_category in grouped_data:
                grouped_data[grouped_category] += amount
            else:
                grouped_data[grouped_category] = amount
                
        return grouped_data
        
    def get_grouped_categories(self, original_categories: Set[str]) -> Set[str]:
        """Get the set of categories after applying groupings"""
        mapping = self.get_category_mapping()
        grouped_categories = set()
        
        for category in original_categories:
            grouped_category = mapping.get(category, category)
            grouped_categories.add(grouped_category)
            
        return grouped_categories
    
    def get_original_categories_for_group(self, group_name: str) -> List[str]:
        """Get original categories that belong to a specific group"""
        if group_name in self.category_groups:
            return self.category_groups[group_name]
        else:
            # If it's not a group, return the category itself
            return [group_name]