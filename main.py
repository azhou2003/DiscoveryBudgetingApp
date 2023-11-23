from census import Census
from dotenv import load_dotenv
from state_codes import state_fips #state_fips is a dictionary containing '<State>':'<fips_numeric_code>' key value pairs.
import os

load_dotenv()

#default query parameters for census api
census_state = 'Texas' 
census_year = 2022 

c = Census(os.getenv("CENSUS_API_KEY"), year = census_year)

