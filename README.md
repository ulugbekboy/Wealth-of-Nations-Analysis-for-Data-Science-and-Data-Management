# Project Topic

### The Wealth of Nations. Dive into the intricate relationship between a country's economic prosperity and the well-being of its population. This project invites you to explore decades of global development data to uncover trends and correlations. You could analyze how indicators like GDP per capita relate to life expectancy, healthcare spending, or child mortality rates. Create compelling visualizations, such as time-series charts or global maps, to tell a story about global health and economics. The goal is to build an analytical project that reveals patterns in how nations thrive. Data for this project can be sourced directly from the World Bank Open Data portal or via its Python API.


1. Libraries
2. Read the datas
3. Clarify and 



🌍 Wealth of Nations Analysis
A data science project analyzing the relationship between economic prosperity (GDP per capita) and population well-being indicators (life expectancy, healthcare spending, infant mortality) across countries from 2000-2022.
📊 Project Overview
This project explores global development data from the World Bank to answer:

How does GDP per capita correlate with life expectancy?
What is the relationship between healthcare spending and infant mortality?
How have these indicators evolved over time?
Are there differences between income groups?

📁 Project Structure
wealth-of-nations-analysis/
│
├── project.py              # Main analysis script (run this!)
├── requirements.txt        # Python dependencies list
├── .gitignore             # Git ignore rules (excludes venv, data, outputs)
├── README.md              # This documentation file
├── task explanation.md    # Project assignment description
│
├── venv/                  # Virtual environment (NOT in Git)
│
├── data/                  # Data directory (created automatically)
│   ├── raw/              # Raw data from World Bank API
│   └── processed/        # Cleaned and processed data
│
└── outputs/              # Generated outputs (created automatically)
    ├── figures/         # Visualization outputs (.png files)
    └── reports/         # Statistical reports (.txt, .json)
Note: venv/, data/, and outputs/ folders are NOT tracked in Git because:

venv/ - Each user creates their own virtual environment
data/ - Data is fetched from API (don't need to store it)
outputs/ - Results are generated when you run the code

🔧 Setup Instructions
Prerequisites

Python 3.8 or higher (Download here)
Internet connection (for World Bank API access)
Git (Download here)

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

wbgapi - World Bank API access
pandas - Data manipulation
numpy - Numerical computing
scipy - Scientific computing
matplotlib - Plotting
seaborn - Statistical visualization

5. Verify Installation
Check that everything installed correctly:
bashpip list

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

======================================================================
WEALTH OF NATIONS: Economic Prosperity & Well-being Analysis
======================================================================

Fetching data from World Bank API...
Fetching GDP_per_capita...
Fetching Life_expectancy...
...

======================================================================
DESCRIPTIVE STATISTICS
======================================================================

GDP_per_capita:
  Mean: 12,456.78
  Median: 5,234.56
...

======================================================================
CORRELATION ANALYSIS
======================================================================
Pearson Correlation: 0.7834
P-value: 2.34e-156

======================================================================
GENERATING VISUALIZATIONS
======================================================================
1. Creating correlation heatmap...
2. Creating GDP vs Life Expectancy scatter plots...
...
Output Files Created:
After running, check these folders:

outputs/figures/ - Contains 5 PNG visualization files
outputs/reports/ - Contains statistical reports (if implemented)

📈 Data Sources (https://pypi.org/project/wbgapi/) 

Source: World Bank Open Data
API Package: wbgapi Python library
Coverage: 217 economies, 2000-2022 (23 years)
Total data points: ~30,000+ observations

Last Updated: 30 November 2025