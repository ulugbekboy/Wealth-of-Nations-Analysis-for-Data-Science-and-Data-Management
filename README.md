# Project Topic
Wealth of Nations: Economic Prosperity and Population Well-being Analysis

A data science project analyzing the relationship between economic prosperity (GDP per capita) and population well-being indicators (life expectancy, healthcare spending, infant mortality) across countries from 2000-2022.

# Project Overview
This project is an interactive Streamlit application designed to analyze the relationship between economic prosperity and population well-being across countries using World Bank open data.

The dashboard provides visual insights for key indicators such as:

- GDP per capita
- Life expectancy
- Healthcare spending per capita
- Infant mortality rate
- Education spending
- Population
- Users can explore data through maps, trends, correlations, bar charts, and ranked tables.

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

To run the project: // streamlit run project.py //

- streamlit (https://pypi.org/project/streamlit/) - For Interactive Dashboards
- wbgapi (https://pypi.org/project/wbgapi/) - World Bank API access
- pandas - Data manipulation
- numpy - Numerical computing
- scipy - Scientific computing
- matplotlib - Plotting
- seaborn - Statistical visualization

# How to Run the Analysis

On Terminal -> python project.py

1. Data Fetching (10-20 minutes)
2. Data Cleaning (10–20 seconds)
3. Statistical Analysis (5 seconds)
4. Computes descriptive statistics (mean, median, std)
5. Visualization (20–30 seconds)
6. Displays all charts inside Streamlit

# Data Sources 
(https://pypi.org/project/wbgapi/) 

Source: World Bank Open Data
API Package: wbgapi Python library
Coverage: 265 economies, 2000-2022 (22 years)
Total data points: ~30,000+ observations

Last Updated: 30 November 2025
Author: Ulugbek Nortojiev