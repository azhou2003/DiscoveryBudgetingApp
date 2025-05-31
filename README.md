# Discovery Budgeting App

A Python-based desktop budgeting application that helps users analyze personal spending habits, compare them against public benchmarks (BLS/Census), and track adherence to budget goals. Designed to support multiple banks, provide weekly insights, and eventually integrate smart budget planning tools.

---

## Project Structure

```
budgeting_app/
├── main.py                    # Entry point (initializes CLI/UI, runs processing)
├── README.md
├── requirements.txt
├── .env                       # Environment variables (e.g., API keys)
│
├── data/                      # Static or downloaded data (e.g., BLS/Census JSON)
├── resources/                 # Actual transaction data (e.g., Discover CSV exports)
├── budgeting/                 # Core business logic for processing and analysis
├── models/                    # Future ML/statistical modules
├── ui/                        # UI logic (PyQt planned)
├── tests/                     # Unit and integration tests
└── utils/                     # Shared helpers/utilities (e.g., plotting functions)
```

---

## Features

* Modular desktop GUI with separate tabs for Transactions, Trends, BLS Comparison, and Budget Management
* Import and parse credit card statements from multiple banks (e.g., Discover, others extensible)
* Weekly spending aggregation by category across all selected accounts
* Comparison against BLS Consumer Expenditure Survey (CES) benchmark data
* Intelligent mapping of personal categories to public (BLS) categories
* Visual plots of weekly spending with user and BLS averages, including budget overlays
* Highlight best/worst spending weeks
* Set, track, and compare budgets for each category
* Save and load budget configurations
* Extensible, modular design to support future features and additional data sources

---

## Roadmap

### Core Improvements

* **Budget Planning and Management:**
  * Set overall budget
  * Use a model to suggest optimal budgeting across categories based on spending patterns or goals
  * Add additional budget management features (e.g., alerts, recommendations, or visualizations)

* **Desktop GUI refinement:**
  * Improve overall layout and visual consistency
  * Add icons and tooltips for better usability
  * Enhance responsiveness and resizing behavior
  * Implement keyboard shortcuts for common actions
  * Add loading indicators and error messages for file operations
  * Support dark mode and theme customization
  * Make tables sortable and filterable
  * Add context menus for quick actions (e.g., right-click on transactions)
  * Improve accessibility (screen reader support, high-contrast mode)
  * Add onboarding/help dialogs and in-app documentation

* Multi-bank support through a common transaction interface (e.g. Chase, Bank of America, Wells Fargo, Citi, Capital One, American Express, and others)

* **BLS Data Integration:**
  * Create clear instructions for acquiring BLS Consumer Expenditure Survey data and converting it to JSON format for use in the app
  * Implement a tool within the app (or as a CLI utility) to convert raw BLS data (CSV or Excel) to the required JSON format

* **BLS Category Mapping:**
  * Provide a user-friendly way to set or edit `bls_mappings` (mapping your transaction categories to BLS categories)
  * Add instructions and/or a configuration tool for managing these mappings

* **Category Grouping and Naming:**
  * Add the ability to group similar categories together (especially when importing data from multiple banks with different naming conventions)
  * Allow users to choose which category name to keep when merging/grouping categories across sources

### Data Enhancements

* Integration with live BLS and Census APIs
* Regional spending comparisons using FIPS codes and filters

### Future Directions

* Forecasting future spending
* AI-generated budgeting tips and insights

---

## Development

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run analyzer from CLI

```bash
python main.py
```

### Run tests

```bash
pytest tests/
```

### How to Use

* In the `data/` directory, you will need to include a JSON file that maps BLS Consumer Expenditure Survey categories to their corresponding annual spending values. This is used for comparison against your own data.
* In the `resources/` directory, place your transaction history (CSV format) downloaded from Discover for the period you want to analyze.

---

## Environment Variables

Configure a `.env` file with:

```
BLS_API_KEY=your_bls_key_here
CENSUS_API_KEY=your_census_key_here
```

---

## License

MIT License

Copyright (c) 2023 azhou2003

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

