import csv
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

class DiscoverActProc:
    """
    A class for processing and analyzing Discover card transaction data from a CSV file.

    Attributes:
        file_name (str): Path to the CSV file containing transaction data.
        bls_comparator (optional): An optional comparator object to compare spending against BLS data.
        earliest_year (int): The earliest year found in the transaction data.
        latest_year (int): The latest year found in the transaction data.
        transactions_dict (dict): A mapping of transaction dates to a list of (category, amount) tuples.
        weekly_spending (dict): A mapping of week start dates to total spending for that week.
        weekly_spending_by_category (dict): Weekly spending broken down by category.
        category_series (dict): Weekly time series data per category.
        max_spending_week (tuple): The week with the highest spending.
        min_spending_week (tuple): The week ending on a Sunday with the lowest spending.
        start_date (datetime): Analysis start date.
        end_date (datetime): Analysis end date.
        average_spending (float): Average spending per week.
        average_spending_by_category (dict): Average spending per category per week.
    """

    def __init__(self, file_name, bls_comparator=None):
        """
        Initializes DiscoverActProc with transaction data and optional BLS comparator.

        Args:
            file_name (str): Path to the CSV file.
            bls_comparator (optional): An object for comparing spending with BLS data.
        """
        self.file_name = file_name
        self.bls_comparator = bls_comparator
        self.earliest_year = float('inf')
        self.latest_year = float('-inf')
        self.transactions_dict = {}
        self.weekly_spending = {}
        self.weekly_spending_by_category = {}
        self.category_series = {}
        self.max_spending_week = None
        self.min_spending_week = None
        self.start_date = None
        self.end_date = None
        self.average_spending = 0
        self.average_spending_by_category = {}

        self._open_file()

    def _open_file(self):
        """
        Opens and reads the CSV file, storing transaction data.

        Populates:
            - transactions_dict with valid transaction entries.
            - earliest_year and latest_year with date range of transactions.

        Skips:
            - Any transactions with negative amounts (e.g., refunds).
            - Rows with missing or malformed data.
        """
        try:
            with open(self.file_name, 'r', newline='') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    try:
                        trans_date = datetime.strptime(row['Trans. Date'], '%m/%d/%Y')
                        year = trans_date.year
                        self.earliest_year = min(self.earliest_year, year)
                        self.latest_year = max(self.latest_year, year)

                        amount = float(row['Amount'])
                        if amount < 0:
                            continue

                        category = row['Category']
                        if trans_date not in self.transactions_dict:
                            self.transactions_dict[trans_date] = []
                        self.transactions_dict[trans_date].append((category, amount))
                    except (ValueError, KeyError) as e:
                        print(f"Error processing row: {row}. Error: {e}")
        except FileNotFoundError:
            print(f"File not found: {self.file_name}")
        except Exception as e:
            print(f"An error occurred while opening the file: {e}")

    def analyze_spending(self, start_date=None, end_date=None):
        """
        Analyzes weekly spending patterns between start and end dates.

        Computes:
            - Total and average weekly spending.
            - Weekly spending by category.
            - Time series per category.
            - Weeks with maximum and minimum spending.

        If a BLS comparator is provided, estimates a baseline average from comparable BLS categories.

        Args:
            start_date (datetime, optional): Start date for analysis. Defaults to earliest transaction date.
            end_date (datetime, optional): End date for analysis. Defaults to latest transaction date.
        """
        all_dates = sorted(self.transactions_dict.keys())
        if not all_dates:
            print("No transactions available for analysis.")
            return

        self.start_date = start_date or all_dates[0]
        self.end_date = end_date or all_dates[-1]

        total_spent = 0
        num_weeks = 0
        current_week_start = self.start_date
        category_totals_accum = {}
        category_counts = {}

        while current_week_start <= self.end_date:
            next_sunday = current_week_start + timedelta(days=(6 - current_week_start.weekday() + 7) % 7)
            current_week_end = min(next_sunday, self.end_date)

            week_spending = 0
            category_totals = {}
            current_day = current_week_start
            while current_day <= current_week_end:
                for category, amount in self.transactions_dict.get(current_day, []):
                    week_spending += amount
                    category_totals[category] = category_totals.get(category, 0) + amount
                current_day += timedelta(days=1)

            self.weekly_spending[current_week_start] = week_spending
            self.weekly_spending_by_category[current_week_start] = category_totals

            for category, amount in category_totals.items():
                if category not in self.category_series:
                    self.category_series[category] = {}
                self.category_series[category][current_week_start] = amount
                category_totals_accum[category] = category_totals_accum.get(category, 0) + amount
                category_counts[category] = category_counts.get(category, 0) + 1

            if self.max_spending_week is None or week_spending > self.max_spending_week[1]:
                self.max_spending_week = (current_week_start, week_spending)
            if (self.min_spending_week is None or week_spending < self.min_spending_week[1]) and current_week_end.weekday() == 6:
                self.min_spending_week = (current_week_start, week_spending)

            total_spent += week_spending
            num_weeks += 1
            current_week_start = current_week_end + timedelta(days=1)

        self.average_spending = total_spent / num_weeks
        for category in category_totals_accum:
            self.average_spending_by_category[category] = category_totals_accum[category] / category_counts[category]

        if self.bls_comparator:
            self.bls_comparator.get_bls_example_data()
            used_bls_categories = set()
            for user_category in category_totals_accum:
                mapped = self.bls_comparator.category_mapping.get(user_category, [])
                used_bls_categories.update(mapped)
            self.bls_weekly_avg = sum(
                self.bls_comparator.bls_data.get(cat, 0) for cat in used_bls_categories
            ) / 52

    def get_total_spending_by_category(self):
        """
        Computes total spending by category over the entire time span.

        Returns:
            dict: A mapping of category names to total spending amounts.
        """
        totals = {}
        for week in self.weekly_spending_by_category.values():
            for category, amount in week.items():
                totals[category] = totals.get(category, 0) + amount
        return totals