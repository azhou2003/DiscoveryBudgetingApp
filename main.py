from dotenv import load_dotenv
load_dotenv()
from budgeting.census_api import CensusExpenditure
from budgeting.discover_activity_processing import DiscoverActProc
from budgeting.bls_comparator import BLSComparator
from utils.plotting import plot_spending_summary

# Directly assign API keys for now (you can switch back to os.getenv if you prefer dotenv)

# Initialize BLS comparator
bls_comparator = BLSComparator(bls_api_key='-')

# Initialize Discover processor with BLS comparator
my_expend = DiscoverActProc('resources/Discover-2025-YearToDateSummary.csv', bls_comparator=bls_comparator)

# Run analysis and plot
my_expend.analyze_spending()
plot_spending_summary(my_expend)