import csv
from datetime import datetime, timedelta

class BankActProc:
    """
    Abstract base class for processing and analyzing bank transaction data.
    Subclasses must implement _open_file to parse their specific CSV format.
    """

    def __init__(self, file_name, bls_comparator=None):
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
        Abstract method to open and parse the CSV file.
        Should populate self.transactions_dict and set earliest/latest year.
        """
        raise NotImplementedError("Subclasses must implement _open_file()")

    def analyze_spending(self, start_date=None, end_date=None):
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
        totals = {}
        for week in self.weekly_spending_by_category.values():
            for category, amount in week.items():
                totals[category] = totals.get(category, 0) + amount
        return totals