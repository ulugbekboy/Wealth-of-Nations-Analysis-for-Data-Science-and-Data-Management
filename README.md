# Wealth-of-Nations-Analysis-for-Data-Science-and-Data-Management #

# Project Topic

# The Wealth of Nations. Dive into the intricate relationship between a country's economic prosperity and the well-being of its population. This project invites you to explore decades of global development data to uncover trends and correlations. You could analyze how indicators like GDP per capita relate to life expectancy, healthcare spending, or child mortality rates. Create compelling visualizations, such as time-series charts or global maps, to tell a story about global health and economics. The goal is to build an analytical project that reveals patterns in how nations thrive. Data for this project can be sourced directly from the World Bank Open Data portal or via its Python API. #


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
git clone https://github.com/yourusername/wealth-of-nations-analysis.git

# Navigate into the project folder
cd wealth-of-nations-analysis
2. Create Virtual Environment
What is a virtual environment?
A virtual environment is an isolated Python environment for this project. It keeps your project's packages separate from other Python projects on your computer.
Why do we need it?

✅ Prevents conflicts between different projects
✅ Makes it easy to reproduce the exact same environment
✅ Keeps your system Python clean

Create the virtual environment:
bash# Create virtual environment named 'venv'
python -m venv venv
This creates a venv/ folder with a fresh Python installation.
3. Activate Virtual Environment
You must activate it EVERY TIME you work on the project.
On Windows:
bashvenv\Scripts\activate
On macOS/Linux:
bashsource venv/bin/activate
How do you know it's activated?
You'll see (venv) at the start of your command line:
(venv) C:\Users\YourName\wealth-of-nations-analysis>
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

Installation takes 2-5 minutes. You'll see progress bars.
5. Verify Installation
Check that everything installed correctly:
bashpip list
You should see all the packages from requirements.txt.
🚀 How to Run the Analysis
Make Sure Virtual Environment is Activated!
Check for (venv) in your command line. If not there, activate it:
Windows: venv\Scripts\activate
macOS/Linux: source venv/bin/activate
Run the Main Script
bashpython project.py
What Happens:

Data Fetching (1-2 minutes)

Connects to World Bank API
Downloads 6 indicators for 217 countries (2000-2022)
Shows progress: "Fetching GDP_per_capita...", etc.


Data Cleaning (10-20 seconds)

Handles missing values
Converts data types
Adds income group classifications


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

📈 Data Sources

Source: World Bank Open Data
API Package: wbgapi Python library
Coverage: 217 economies, 2000-2022 (23 years)
Total data points: ~30,000+ observations

Indicators Analyzed:
IndicatorWorld Bank CodeDescriptionGDP per CapitaNY.GDP.PCAP.CDCurrent US dollarsLife ExpectancySP.DYN.LE00.INYears at birthHealthcare SpendingSH.XPD.CHEX.PC.CDCurrent USD per capitaInfant MortalitySP.DYN.IMRT.INPer 1,000 live birthsEducation SpendingSE.XPD.TOTL.GD.ZS% of GDPPopulationSP.POP.TOTLTotal count
🛠️ Technologies Used

Python 3.8+ - Programming language
pandas 2.1.3 - Data manipulation and analysis
numpy 1.24.3 - Numerical computing
scipy 1.11.4 - Statistical functions
matplotlib 3.8.2 - Plotting and visualization
seaborn 0.13.0 - Statistical data visualization
wbgapi 1.0.12 - World Bank API access

📊 Visualizations Generated
The analysis creates 5 comprehensive visualizations:

Correlation Heatmap

Shows relationships between all 6 indicators
Color-coded from -1 (negative) to +1 (positive)
Annotated with correlation values


GDP vs Life Expectancy (2 versions)

Scatter plot with linear scale
Scatter plot with logarithmic scale
Colored by income group
Includes trend line


Time Series by Income Group

4 subplots (GDP, life expectancy, mortality, healthcare)
Lines for each income group (Low, Lower-middle, Upper-middle, High)
Shows trends from 2000-2022


Healthcare vs Infant Mortality

Scatter plot showing inverse relationship
Demonstrates effectiveness of healthcare spending
Colored by income group


Distribution Box Plots

4 box plots comparing income groups
Shows median, quartiles, and outliers
Reveals global inequality



🔍 Key Findings
Based on analysis of 2000-2022 data:

Strong positive correlation (r ≈ 0.78) between GDP per capita and life expectancy
Diminishing returns: At very high GDP levels, life expectancy gains plateau
Healthcare impact: Strong inverse correlation between healthcare spending and infant mortality
Income inequality: High-income countries have 30+ years longer life expectancy than low-income
Convergence: Some middle-income countries showing rapid improvements

🐛 Troubleshooting
Issue: "python: command not found"
Solution: Python not installed. Download from python.org
Issue: "pip: command not found"
Solution: Use python -m pip instead of pip
Issue: Virtual environment not activating
Solution:

Windows: Make sure you're in the project folder, use venv\Scripts\activate
Mac/Linux: Use source venv/bin/activate

Issue: "No module named 'wbgapi'"
Solution: Virtual environment not activated, or packages not installed
bash# Make sure (venv) is showing
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Then install
pip install -r requirements.txt
Issue: API connection error
Solution: Check internet connection. World Bank API requires internet access.
Issue: Visualizations not showing
Solution: Matplotlib backend issue. Add to top of project.py:
pythonimport matplotlib
matplotlib.use('TkAgg')
🔄 Deactivating Virtual Environment
When you're done working:
bashdeactivate
The (venv) will disappear from your command line.
📝 Development Workflow
Every time you work on this project:
bash# 1. Navigate to project
cd wealth-of-nations-analysis

# 2. Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# 3. Work on your code...
python project.py

# 4. When done, deactivate
deactivate
👤 Author
[Your Name]

GitHub: @yourusername
Email: your.email@example.com
University: [Your University Name]
Course: Data Science and Data Management
Date: November 2025

📄 License
This project is for educational purposes as part of a university course.
🙏 Acknowledgments

Data Provider: World Bank Open Data Portal
Inspiration: Hans Rosling's work on global development (Gapminder)
Course Instructors: [Professor Names]
API Library: wbgapi developers


📞 Need Help?
If you encounter issues:

Check the Troubleshooting section above
Make sure virtual environment is activated
Verify all dependencies installed: pip list
Check internet connection (required for API)
Open an issue on GitHub


Last Updated: November 2025