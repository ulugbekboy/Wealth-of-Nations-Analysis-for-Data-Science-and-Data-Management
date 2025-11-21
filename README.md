# Project Topic
Wealth of Nations: Economic Prosperity and Population Well-being Analysis

A data science project analyzing the relationship between economic prosperity (GDP per capita) and population well-being indicators (life expectancy, healthcare spending, infant mortality) across countries from 2000-2022.

# Project Overview
This project explores global development data from the World Bank to answer:

How does GDP per capita correlate with life expectancy?
What is the relationship between healthcare spending and infant mortality?
How have these indicators evolved over time?
Are there differences between income groups?

This project performs comprehensive analysis of the relationship between economic
indicators and well-being metrics of a country using World Bank data.
As indicators it was taken following indicators:
- GDP_per_capita
- Life_expectancy
- Healthcare_spending_per_capita
- Infant_mortality_rate
- Education_expenditure_pct_GDP
- Population

# Step-by-Step Installation:

1. Clone the Repository
bash# Clone this repository to your computer

git clone https://github.com/ulugbekboy/wealth-of-nations-analysis.git
cd wealth-of-nations-analysis

2. Create the virtual environment: bash# Create virtual environment named 'venv'

"python -m venv venv" This creates a venv/ folder with a fresh Python installation.

3. Activate Virtual Environment

4. Install Dependencies

Now that venv is activated, install the required packages:

pip install req.txt

- wbgapi (https://pypi.org/project/wbgapi/) - World Bank API access
- pandas - Data manipulation
- numpy - Numerical computing
- scipy - Scientific computing
- matplotlib - Plotting
- seaborn - Statistical visualization

# How to Run the Analysis

On Terminal -> python project.py

1. Data Fetching (1-2 minutes)
2. Connects to World Bank API
3. Downloads 6 indicators for 217 countries (2000-2022)
4. Data Cleaning (10-20 seconds)
5. Statistical Analysis (5 seconds)
6. Computes descriptive statistics (mean, median, std)
7. Calculates correlations
8. Performs regression analysis
9. Visualization (20-30 seconds)
10. Generates 5 plots via streamlit
11. Saves to outputs/figures/ generated visualization files

# Data Sources 
(https://pypi.org/project/wbgapi/) 

Source: World Bank Open Data
API Package: wbgapi Python library
Coverage: 217 economies, 2000-2022 (23 years)
Total data points: ~30,000+ observations

Last Updated: 30 November 2025