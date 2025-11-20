# Project Topic
"""
Wealth of Nations: Economic Prosperity and Population Well-being Analysis

This project performs comprehensive analysis of the relationship between economic
indicators and well-being metrics of a country using World Bank data.
1. As indicators I have taken following indicators:
- GDP_per_capita
- Life_expectancy
- Healthcare_spending_per_capita
- Infant_mortality_rate
- Education_expenditure_pct_GDP
- Population

"""

2. Fetching all datas from World Bank API accrging to set indicators.

1. Libraries
2. Read the datas
3. Clarify and Analysis

🌍 Wealth of Nations Analysis
A data science project analyzing the relationship between economic prosperity (GDP per capita) and population well-being indicators (life expectancy, healthcare spending, infant mortality) across countries from 2000-2022.
📊 Project Overview
This project explores global development data from the World Bank to answer:

How does GDP per capita correlate with life expectancy?
What is the relationship between healthcare spending and infant mortality?
How have these indicators evolved over time?
Are there differences between income groups?

Step-by-Step Installation
1. Clone the Repository
bash# Clone this repository to your computer
git clone https://github.com/ulugbekboy/wealth-of-nations-analysis.git

# Navigate into the project folder
cd wealth-of-nations-analysis
2. Create the virtual environment:
bash# Create virtual environment named 'venv'
python -m venv venv
This creates a venv/ folder with a fresh Python installation.
3. Activate Virtual Environment
4. Install Dependencies
Now that venv is activated, install the required packages:
bashpip install -r requirements.txt
This installs:

wbgapi (https://pypi.org/project/wbgapi/) - World Bank API access

pandas - Data manipulation
numpy - Numerical computing
scipy - Scientific computing
matplotlib - Plotting
seaborn - Statistical visualization

🚀 How to Run the Analysis

python project.py
What Happens:

Data Fetching (1-2 minutes)

Connects to World Bank API
Downloads 6 indicators for 217 countries (2000-2022)

Data Cleaning (10-20 seconds)
Statistical Analysis (5 seconds)
Computes descriptive statistics (mean, median, std)
Calculates correlations
Performs regression analysis
Visualization (20-30 seconds)
Generates 5 publication-quality plots
Saves to outputs/figures/
Displays on screen

Total runtime: 2-5 minutes (depends on internet speed)
Expected Output:

WEALTH OF NATIONS: Economic Prosperity & Well-being Analysis


Fetching data from World Bank API...
Fetching GDP_per_capita...
Fetching Life_expectancy...
...
DESCRIPTIVE STATISTICS

GDP_per_capita:
  Mean: 12,456.78
  Median: 5,234.56
...


CORRELATION ANALYSIS

Pearson Correlation: 0.7834
P-value: 2.34e-156

GENERATING VISUALIZATIONS

1. Creating correlation heatmap...
2. Creating GDP vs Life Expectancy scatter plots...
...
Output Files Created:
After running, check these folders:

outputs/figures/ - Contains 5 PNG visualization files
outputs/reports/ - Contains statistical reports (if implemented)

📈 Data Sources (https://pypi.org/project/wbgapi/) 
=
Source: World Bank Open Data
API Package: wbgapi Python library
Coverage: 217 economies, 2000-2022 (23 years)
Total data points: ~30,000+ observations

Last Updated: 30 November 2025

==1==
git init
cheking git config --list
git config --global user.name "username"
git config --global user.email "your.email@example.com"

git status
git add .
git commit -m "____"

git remote add origin https://github.com/yourusername/wealth-of-nations-analysis.git
git remote -v

git branch -M main
git push -u origin main

--activate venv envirement--
source venv/bin/activate

