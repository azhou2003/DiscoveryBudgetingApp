# CATEGORY_MAPPING defines how banking or credit card transaction categories are mapped
# to Bureau of Labor Statistics (BLS) Consumer Expenditure Survey (CES) categories.
# 
# This mapping allows user spending data to be compared against national averages 
# from BLS datasets. It is customizable — feel free to modify or expand it to better 
# align with the specific categories returned by your financial institution or desired 
# analytical breakdowns.
CATEGORY_MAPPING = {
    'Supermarkets': [
        'Food away from home',  
        'Food prepared by consumer unit on out of town trips'
    ],
    'Groceries': [
        'Food away from home',
        'Food prepared by consumer unit on out of town trips'
    ],
    'Restaurants': ['Food away from home'],
    'Fast Food': ['Food away from home'],
    'Gasoline': ['Gasoline'],
    'Uber': ['Public and other transportation'],
    'Public Transit': ['Public and other transportation'],
    'Rent': [
        'Rented dwellings',
        'Estimated monthly rental value of owned home'
    ],
    'Utilities': [
        'Utilities, fuels, and public services',
        'Natural gas',
        'Electricity',
        'Water and other public services'
    ],
    'Clothing': ['Apparel and services'],
    'Medical': [
        'Healthcare',
        'Health insurance',
        'Medical services',
        'Drugs',
        'Medical supplies'
    ],
    'Doctor': ['Medical services'],
    'Pharmacy': ['Drugs', 'Medical supplies'],
    'Movies': ['Entertainment', 'Fees and admissions'],
    'Streaming': ['Entertainment', 'Audio and visual equipment and services'],
    'Haircut': ['Personal care products and services'],
    'Salon': ['Personal care products and services'],
    'Tuition': ['Education'],
    'Books': ['Reading', 'Education'],
    'Other': ['Miscellaneous'],
    'Services': ['Personal care products and services', 'Household operations'],
    'Merchandise': [
        'Apparel and services',
        'Household furnishings and equipment',
        'Pets, toys, hobbies, and playground equipment'
    ],
    'Travel/ Entertainment': [
        'Entertainment',
        'Fees and admissions',
        'Other lodging',
        'Food prepared by consumer unit on out of town trips'
    ]
}


SERIES_MAPPING = {}
