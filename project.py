"""
Wealth of Nations: Economic Prosperity and Population Well-being Analysis

This module performs comprehensive analysis of the relationship between economic
indicators and well-being metrics using World Bank data.
As Indicators i have taken :
- GDP_per_capita
- Life_expectancy
- Healthcare_spending_per_capita
- Infant_mortality_rate
- Education_expenditure_pct_GDP
- Population

"""

import wbgapi as wb
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Dict, Tuple

plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")


class WealthOfNationsAnalyzer:
    def __init__(self, start_year: int = 2000, end_year: int = 2022):
        self.start_year = start_year
        self.end_year = end_year
        self.data = None
        self.indicators = {
            'NY.GDP.PCAP.CD': 'GDP_per_capita',
            'SP.DYN.LE00.IN': 'Life_expectancy',
            'SH.XPD.CHEX.PC.CD': 'Healthcare_spending_per_capita',
            'SP.DYN.IMRT.IN': 'Infant_mortality_rate',
            'SE.XPD.TOTL.GD.ZS': 'Education_expenditure_pct_GDP',
            'SP.POP.TOTL': 'Population'
        }

    def fetching(self) -> pd.DataFrame:
        print("Fetching data from World Bank API...")
        data_frames = []

        for indicator_code, indicator_name in self.indicators.items():
            print(f"Started fetching {indicator_name} ...")
            df = wb.data.DataFrame(indicator_code,
                                   time = range(self.start_year, self.end_year+1), 
                                   numericTimeKeys = True, # to make dates integer
                                   labels = True # to make labels as indicator names
                                   )
            df = df.reset_index() # to make all colums as regular ones
            df = df.melt(id_vars = ["economy"], var_name = "year", value_name= indicator_name) # reshaping the table
            df["year"] = pd.to_numeric(df["year"], errors="coerce")
            ##df[indicator_name] = pd.to_numeric(df[indicator_name], errors="coerce")
            data_frames.append(df)
            
        if data_frames:
            self.data = data_frames[0]
            for df in data_frames[1:]:
                self.data = pd.merge(
                    self.data,df,on=["economy", "year"],
                    how="outer"
                ) # the loop is used for merging all indicator tables into one table
        print(f"Fetched successfully {self.data.shape}")
        return self.data
    

    def clean_data(self) -> pd.DataFrame:
        return ""
    

    def compute_correlation(self) -> pd.DataFrame:
        return ""
    
    def compute_statistics(self) -> Dict:
        return ""
    
    def analyze_gdp_life_expectancy(self) -> Tuple[float,float]:
        return ""
    
    def analyze_trends_by_income(self) -> pd.DataFrame:
        return ""

class Visualizer():
    pass

def main():
    

    print("WEALTH OF NATIONS: Economic Prosperity & Well-being Analysis")
    
    analyzer = WealthOfNationsAnalyzer(start_year=2000, end_year=2022)
    
    try:
        analyzer.fetch_data()
        analyzer.clean_data()
    except Exception as e:
        print(f"Error loading data: {str(e)}")
        return
    
    print("\n" + "=" * 70)
    print("DESCRIPTIVE STATISTICS")
    print("=" * 70)
    stats = analyzer.compute_statistics()
    for indicator, values in stats.items():
        print(f"\n{indicator}:")
        for stat_name, stat_value in values.items():
            print(f"  {stat_name.capitalize()}: {stat_value:,.2f}")
    
    print("\n" + "=" * 70)
    print("CORRELATION ANALYSIS: GDP per Capita vs Life Expectancy")
    print("=" * 70)
    corr, p_val = analyzer.analyze_gdp_life_expectancy()
    if corr is not None:
        print(f"Pearson Correlation Coefficient: {corr:.4f}")
        print(f"P-value: {p_val:.4e}")
        print(f"Interpretation: {'Strong' if abs(corr) > 0.7 else 'Moderate' if abs(corr) > 0.4 else 'Weak'} {'positive' if corr > 0 else 'negative'} correlation")
    
    print("\n" + "=" * 70)
    print("GENERATING VISUALIZATIONS")
    print("=" * 70)
    
    visualizer = WealthVisualizer(analyzer)
    
    print("\n1. Creating correlation heatmap...")
    visualizer.plot_correlation_heatmap()
    
    print("\n2. Creating GDP vs Life Expectancy scatter plots...")
    visualizer.plot_gdp_vs_life_expectancy()
    
    print("\n3. Creating time series by income group...")
    visualizer.plot_time_series_by_income()
    
    print("\n4. Creating healthcare vs mortality analysis...")
    visualizer.plot_healthcare_vs_mortality()
    
    print("\n5. Creating distribution comparisons...")
    visualizer.plot_distribution_comparisons()
    
    print("\n" + "=" * 70)
    print("ANALYSIS COMPLETE!")
    print("=" * 70)


if __name__ == "__main__":
    main()
