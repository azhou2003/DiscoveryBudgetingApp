from budgeting.bls_mappings import CATEGORY_MAPPING, SERIES_MAPPING
import os
import json

class BLSComparator:
    def __init__(self, bls_api_key):
        self.bls_api_key = bls_api_key
        self.bls_data = {}  # {bls_category: annual amount}
        self.category_mapping = CATEGORY_MAPPING

    def fetch_bls_series_metadata(self):
        return SERIES_MAPPING

    def get_bls_example_data(self):
        path = os.path.join("data", "ces_2022_benchmarks.json")
        try:
            with open(path, "r") as f:
                self.bls_data = json.load(f)
            print(f"[BLS] Loaded {len(self.bls_data)} CES benchmark categories.")
        except FileNotFoundError:
            print(f"[BLS] CES benchmark file not found at: {path}")
        return self.bls_data

    def bulk_map(self, user_categories):
        # no-op for manual mapping
        pass

    def get_bls_avg_for_user_category(self, user_category):
        bls_categories = self.category_mapping.get(user_category, [])
        print(f"Mapping for '{user_category}': {bls_categories}")
        if not bls_categories:
            return None
        values = [self.bls_data.get(cat) for cat in bls_categories if self.bls_data.get(cat) is not None]
        if not values:
            print(f"No valid BLS data for any mapped categories: {bls_categories}")
            return None
        avg_value = sum(values) / len(values)
        print(f"BLS average for '{user_category}' (via {bls_categories}): {avg_value}")
        return avg_value
    def compare_spending(self, user_spending_by_category):
        # ensure data is loaded before comparison
        if not self.bls_data:
            self.get_bls_example_data()

        results = {}
        for ucat, amt in user_spending_by_category.items():
            bls_cat = self.category_mapping.get(ucat)
            bls_amt = self.bls_data.get(bls_cat, 0)
            if bls_cat not in results:
                results[bls_cat] = {'user': 0, 'bls_avg': bls_amt, 'difference': 0}
            results[bls_cat]['user'] += amt
            results[bls_cat]['difference'] = results[bls_cat]['user'] - results[bls_cat]['bls_avg']
        return results

