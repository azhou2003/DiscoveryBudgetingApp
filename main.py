from dotenv import load_dotenv
load_dotenv()
import os
from census_api import CensusExpenditure
from discover_activity_processing import DiscoverActProc
from datetime import datetime

api_key = os.getenv("CENSUS_API_KEY")

#TODO: Process CSV download of Bank Activity

my_food_expend = DiscoverActProc('Discover-AllAvailable-20231123.csv')

start_date = datetime(2023, 8, 28)
end_date = datetime(2023, 11, 8)

my_food_expend.analyze_spending(start_date, end_date)
my_food_expend.plot_spending()

#TODO: Take in input of State and Year and use to retrieve census data on food expenditure