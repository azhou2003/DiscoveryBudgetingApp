from budgeting.bls_mappings import CATEGORY_MAPPING, SERIES_MAPPING
import os
import json

class BLSComparator:
    """
    A class to compare user spending categories against benchmark data from the BLS (Bureau of Labor Statistics).

    Attributes:
        bls_api_key (str): API key for future expansion (currently unused).
        bls_data (dict): Dictionary mapping BLS category codes to annual benchmark amounts.
        category_mapping (dict): Mapping from user-defined categories to BLS categories.
    """
    def __init__(self, bls_api_key):
        """
        Initializes the BLSComparator with an API key and empty data containers.

        Args:
            bls_api_key (str): The API key to use for future BLS API requests.
        """
        self.bls_api_key = bls_api_key
        self.bls_data = {}  # {bls_category: annual amount}
        self.category_mapping = CATEGORY_MAPPING

    def fetch_bls_series_metadata(self):
        """
        Returns static BLS series metadata.

        Returns:
            dict: A mapping of internal BLS series codes to descriptive metadata.
        """
        return SERIES_MAPPING

    def get_bls_example_data(self):
        """
        Loads example BLS CES (Consumer Expenditure Survey) benchmark data from a local JSON file.

        Returns:
            dict: A dictionary of BLS categories and their benchmark annual values.
        """
        path = os.path.join("data", "ces_2022_benchmarks.json")
        try:
            with open(path, "r") as f:
                self.bls_data = json.load(f)
            print(f"[BLS] Loaded {len(self.bls_data)} CES benchmark categories.")
        except FileNotFoundError:
            print(f"[BLS] CES benchmark file not found at: {path}")
        return self.bls_data

    def bulk_map(self, user_categories):
        """
        Stub method for future batch category mapping logic. Currently a no-op.

        Args:
            user_categories (list[str]): List of user-defined category names.
        """
        pass

    def get_bls_avg_for_user_category(self, user_category):
        """
        Computes the average BLS benchmark spending for a given user-defined category.

        Args:
            user_category (str): The user-defined spending category.

        Returns:
            float or None: The average BLS value if mapping is successful; otherwise None.
        """
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
        """
        Compares user spending to BLS benchmark data across mapped categories.

        Args:
            user_spending_by_category (dict): Mapping of user-defined categories to total spending.

        Returns:
            dict: A dictionary mapping BLS categories to a breakdown of:
                  - user: total user spending mapped to this BLS category
                  - bls_avg: BLS average value
                  - difference: user spending minus BLS average
        """
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

