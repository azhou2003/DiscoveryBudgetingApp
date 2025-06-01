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
* Modern, accessible design system with unified colors, spacing, and typography
* Consistent toolbar with improved button sizing, icons, and a user-readable date range display
* All tables feature visually integrated section headers, improved row heights, and left-aligned headers
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

## UI Modernization & Refactoring

- All UI code is modularized: toolbar logic is in `ui/toolbar.py`, each tab in its own file, and design tokens in `ui/style_guide.py`.
- Toolbar is now a dedicated widget with clear, accessible button sizing and a non-editable, user-friendly date range label.
- Table section headers are visually part of the tables (not separate labels), using merged header rows for clarity and accessibility.
- Consistent spacing, margins, and font sizes across all UI elements.
- All code is organized with docstrings and best practices for maintainability.

---

## Roadmap

### 1. Foundational Features

- **Multi-bank Support**
  - Implement a common transaction interface (e.g., Chase, Bank of America, Wells Fargo, Citi, Capital One, American Express, etc.)

- **Category Grouping and Naming**
  - Add ability to group similar categories (especially when importing from different banks)
  - Let users choose preferred category names when merging/grouping across sources

- **BLS Data Integration**
  - Create clear instructions for acquiring BLS Consumer Expenditure Survey data and converting it to JSON
  - Implement a CLI tool or in-app utility to convert raw BLS data (CSV or Excel) to the required JSON format

- **BLS Category Mapping**
  - Provide a user-friendly tool for managing `bls_mappings` (mapping your transaction categories to BLS categories)


### 2. Core Budgeting Capabilities

- **Budget Planning and Management**
  - Set an overall budget
  - Use a model to suggest optimal budgets by category based on spending patterns or user-defined goals
  - Add smart features like alerts, visualizations, and tailored recommendations


### 3. Interface and Usability Improvements

- **Desktop GUI Refinement**
  - Refine layout with improved icons, spacing, and visual consistency
  - Add tooltips, onboarding/help dialogs, and in-app documentation
  - Enhance layout behavior and theme support:
    - Responsive resizing
    - Dark mode 
  - Add loading indicators and error messages for file operations
  - Make tables sortable and filterable
  - Add context menus (e.g., right-click actions on transactions)


### 4. Data Enhancements

- **External Data Integration**
  - Integrate live BLS and Census APIs
  - Enable regional spending comparisons using FIPS codes and filters

### 5. Future Directions

- **Smart Insights & Predictions**
  - Forecast future spending
  - Generate AI-powered budgeting tips and insights


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

