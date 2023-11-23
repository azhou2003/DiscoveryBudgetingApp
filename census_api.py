from census import Census
from state_codes import state_fips #state_fips is a dictionary containing '<State>':'<fips_numeric_code>' key value pairs.
import os

class CensusExpenditure:
    
    api_key = os.getenv("CENSUS_API_KEY")
    
    def __init__(self, state = 'Texas', year = 2022):
        self.census_state = state
        self.census_year = year
        self.c = Census(api_key, year = self.census_year)
        self.census_state_fips = state_fips[self.census_state]
    
    #TODO: actual implementation of data retrieval from census API
    
    
    
    
    




