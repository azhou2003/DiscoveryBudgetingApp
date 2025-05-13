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

* Import and parse Discover credit card statements (CSV)
* Weekly spending aggregation by category
* Comparison against BLS CES benchmark data
* Intelligent mapping of personal categories to public categories
* Highlight best/worst spending weeks
* Visual plots of weekly spending with user/BLS averages
* Modular design to support feature changes on the roadmap

---

## Roadmap

### Core Improvements

* Budget import and comparison against spending data
* Desktop GUI with PyQt
* Multi-bank support through a common transaction interface
* Smart budgeting assistance using basic models

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

