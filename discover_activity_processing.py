import csv
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

class DiscoverActProc:
    
    def __init__(self, file_name):
        self.file_name = file_name
        self.earliest_year = float('inf')  
        self.latest_year = float('-inf')  
        self.transactions_dict = {}
        self.weekly_spending = {}
        self.max_spending_week = None
        self.min_spending_week = None
        self.start_date = None
        self.end_date = None
        self.average_spending = 0
        
        # Call _open_file in the constructor
        self._open_file()

    def _open_file(self):
        """
        Open and process a CSV file containing transaction data from Discover Activities Page.

        Description:
        This method attempts to open and process a CSV file extracted from the Discover Activities Page.
        It reads each row of the CSV file, extracts relevant information such as transaction date, year,
        and expenditure amount. The method focuses on rows related to food expenditures, specifically
        those with categories 'Restaurants' and 'Supermarkets'. The data is then organized into a dictionary,
        'transactions_dict', where keys are transaction dates, and values are lists of corresponding expenditure amounts.

        If the file is not found, a FileNotFoundError is caught and a message is printed to the console.
        If any other exception occurs during file processing, a generic exception is caught, and an error message is printed.

        Parameters: None

        Returns: None
        """
        try:
            with open(self.file_name, 'r', newline='') as file:
                csv_reader = csv.DictReader(file)

                # Read and process each row in the CSV file
                for row in csv_reader:
                    try:
                        trans_date = datetime.strptime(row['Trans. Date'], '%m/%d/%Y')
                        year = trans_date.year

                        # Set the proper year boundaries
                        self.earliest_year = min(self.earliest_year, year)
                        self.latest_year = max(self.latest_year, year)
                        
                        # Process the rows if they are food related expenditures
                        if row['Category'] in ['Restaurants', 'Supermarkets']:
                            amount = float(row['Amount'])

                            if trans_date not in self.transactions_dict:
                                self.transactions_dict[trans_date] = []

                            self.transactions_dict[trans_date].append(amount)
                    except (ValueError, KeyError) as e:
                        print(f"Error processing row: {row}. Error: {e}")
        except FileNotFoundError:
            print(f"File not found: {self.file_name}")
        except Exception as e:
            print(f"An error occurred while opening the file: {e}")
    
    def analyze_spending(self, start_date, end_date):
        """
        Analyze weekly spending over a specified date range.

        Parameters:
        - start_date (datetime): The start date of the analysis.
        - end_date (datetime): The end date of the analysis.

        Description:
        This method calculates and analyzes weekly spending over the specified date range.
        It iterates through each week, calculates the total spending for each week, and
        tracks the maximum and minimum spending weeks. The results include the average
        spending per week, the maximum spending week, and the minimum spending for a full week.

        Returns: None
        Raises: None
        """
        self.start_date = start_date
        self.end_date = end_date
        total_spent = 0
        num_weeks = 0
        current_week_start = start_date

        while current_week_start <= end_date:
            next_sunday = current_week_start + timedelta(days=(6 - current_week_start.weekday() + 7) % 7)
            current_week_end = min(next_sunday, end_date)

            # Calculate spending for the current week
            week_spending = 0
            current_day = current_week_start
            while current_day <= current_week_end:
                week_spending += sum(self.transactions_dict.get(current_day, []))
                current_day += timedelta(days=1)

            self.weekly_spending[current_week_start] = week_spending

            # Update max and min spending
            if self.max_spending_week is None or week_spending > self.max_spending_week[1]:
                self.max_spending_week = (current_week_start, week_spending)

            if (self.min_spending_week is None or week_spending < self.min_spending_week[1]) and current_week_end.weekday() == 6:
                self.min_spending_week = (current_week_start, week_spending)

            total_spent += week_spending
            num_weeks += 1

            current_week_start = current_week_end + timedelta(days=1)

        self.average_spending = total_spent / num_weeks
        
        from pprint import pprint

        # ...

        # Inside your analyze_spending method, after calculating weekly_spending
        pprint(self.weekly_spending)
        
    def plot_spending(self):
        """
        Plots the spending per week and average spending per week based on data from timeframe.
        """
        
        x_values = list(self.weekly_spending.keys())
        y_values = list(self.weekly_spending.values())

        plt.bar(x_values, y_values, width=6, color='blue', label='Weekly Spending')
        
        plt.axhline(y=self.average_spending, color='red', linestyle='--', label='Average Spending')

        plt.xlabel("Week Start Date (MM/DD/YY)")
        plt.ylabel("Spending ($)")
        plt.title(f"Weekly Spending from {self.start_date.date()} to {self.end_date.date()}")
        
        plt.xticks(rotation=45, ha="right")
        plt.xticks(x_values, [date.strftime('%m/%d/%y') for date in x_values])

        plt.legend()
        plt.tight_layout()
        plt.show()

    def get_min_week(self):
        """
        Returns the minimum week as (week, amount) pair
        """
        return self.min_spending_week
        
    def get_max_week(self):
        """
        Returns the max week as (week, amount) pair
        """
        return self.max_spending_week
        
    def get_average_spending(self):
        """
        Returns the average spending over the start_date to end_date time frame
        """
        return self.average_spending
        
        
        

