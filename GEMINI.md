# StayPulse: Wyndham Hotels Guest Satisfaction Analysis

## Project Overview
StayPulse is a data science project dedicated to the Exploratory Data Analysis (EDA) of guest satisfaction metrics across the Wyndham Hotels portfolio. The project analyzes 262,334 guest records to understand key performance indicators like Net Promoter Score (NPS) and Overall Satisfaction (OSAT).

### Key Technologies
- **Language:** Python 3.11+
- **Libraries:** Pandas, NumPy, Matplotlib
- **Environment:** Jupyter Notebook (`.ipynb`)
- **Data Source:** `final_data.csv` (CSV format)

### Core Analysis Features
- **NPS Classification:** Categorization of guests into Promoters (9-10), Passives (7-8), and Detractors (0-6).
- **Metric Benchmarking:** Analysis of OSAT across various service dimensions (service, cleanliness, appearance, guestroom, etc.).
- **Problem Impact Analysis:** Quantifying the correlation between "problem experienced" and NPS/OSAT scores.
- **Granular Performance Mapping:** Benchmarking individual hotels and geographic regions (states/countries).
- **Driver Analysis:** Correlation analysis to identify which service attributes most strongly influence guest loyalty.
- **Data Quality Assessment:** Comprehensive missing data and comment length analysis.

---

## Building and Running

### Prerequisites
- Python 3.11 installed.
- A virtual environment is recommended (already present in `.venv`).

### Setup
1. **Activate the Virtual Environment:**
   - Windows: `.venv\Scripts\activate`
   - Unix/macOS: `source .venv/bin/activate`

2. **Install Dependencies:**
   ```bash
   pip install pandas numpy matplotlib ipykernel
   ```

### Running the Analysis
The project is contained within a Jupyter Notebook. You can run it using:
- **Jupyter Lab/Notebook:** `jupyter notebook EDA.ipynb`
- **VS Code:** Open `EDA.ipynb` and ensure the `.venv` kernel is selected.

---

## Development Conventions

### Coding Style
- **Library Imports:** Always follow standard aliases (e.g., `import pandas as pd`, `import numpy as np`).
- **Data Processing:** Prefer vectorized Pandas operations over manual loops.
- **Visualization:** Use Matplotlib for quick exploratory plots; ensure titles and labels are present.

### Data Management
- The `final_data.csv` is the primary dataset and should be kept in the root directory.
- Avoid committing large datasets to version control if possible (use `.gitignore`).


##test re,mvoe this line
### Project Structure
- `EDA.ipynb`: Main analysis script and results.
- `final_data.csv`: Input dataset (262k+ records).
- `.venv/`: Local Python environment.
