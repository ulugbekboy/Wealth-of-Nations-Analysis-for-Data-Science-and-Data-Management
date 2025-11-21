# importing libraries
import wbgapi as wb
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Dict, Tuple


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
        print("Cleaning data ...")
        for indicator in self.indicators.values():
            if indicator in self.data.columns:
                self.data[indicator] = pd.to_numeric(self.data[indicator], errors="coerce") ##converting to numerical data and making NaN were N/A
        
        self.data = self.data.dropna(how="all", subset=list(self.indicators.values())) ## removing completely empty colums
        countries = wb.economy.DataFrame()  ## calling the wb
        income_dict = countries["incomeLevel"].to_dict()   
        self.data["income_group"] = self.data["economy"].map(income_dict)  ## adding new column incomeLevel  

        region_dict = countries["region"].to_dict()
        self.data["region"] = self.data["economy"].map(region_dict) ## adding new column region  

        print(f"Data Cleaned ...{self.data.shape}")
        return self.data
    
    def compute_correlation(self) -> pd.DataFrame:
        all_data = list(self.indicators.values())
        correlation_matrix = self.data[all_data].corr()   # find the correlations of the indicator values
        return correlation_matrix
    
    def compute_statistics(self) -> Dict:
        stats_dict = {}      # to calculate the statistical parameters of all indicators
        for indicator in self.indicators.values():
            stats_dict[indicator] = {
                "mean": np.nanmean(self.data[indicator]),
                "median":np.nanmedian(self.data[indicator]),
                "std":np.nanstd(self.data[indicator]),
                "min":np.nanmin(self.data[indicator]),
                "max":np.nanmax(self.data[indicator])
            }
        return stats_dict
    
    def analyze_gdp_life_expectancy(self) -> Tuple[float,float]:
        filtered_data = self.data.dropna(subset = ["GDP_per_capita", "Life_expectancy"]) # choosing only colums to analyze 

        if len(filtered_data) > 0:
            correlation, p_value  = stats.pearsonr(
                filtered_data["GDP_per_capita"],
                filtered_data["Life_expectancy"],
            )
            return correlation, p_value
        return None,None

    def analyze_trends_by_income(self) -> pd.DataFrame:
        if "income_group" in self.data.columns:
            trends = self.data.groupby(['year','income_year']).agg({
               'GDP_per_capita': 'mean',
               'Life_expectancy': 'mean',
               'Infant_mortality_rate': 'mean',
               'Healthcare_spending_per_capita': 'mean'
            }).reset_index()
            return trends
        return None
    
class Visualizer():
    def __init__(self, analyzer: WealthOfNationsAnalyzer):
        self.analyzer = analyzer
        self.data = analyzer.data
        print(self.data)


    def plot_correlation_heatmap(self,save_path: str =None):

        corr_matrix = self.analyzer.compute_correlation()
        print(corr_matrix)

        plt.figure(figsize=(12,10))
        sns.heatmap(corr_matrix)

        plt.title("Correlation Matrix: Economic and Well-Being Indicators,", fontsize = 16)
        plt.tight_layout()

        if save_path:
            plt.savefig(save_path,dpi=300)

        plt.show()

    def plot_gdp_and_life_expectancy(self, save_path: str = None):
        return ""
    
    def plot_time_series_by_income(self, save_path: str = None):
        return ""
    
    def plot_health_care_and_mortality(self, save_path: str = None):
        return ""
    
    def plot_distribution_comparisons(self, save_path: str = None):
        return ""
    



def main():
    print("Analysis results")
    analyzer = WealthOfNationsAnalyzer(start_year=2000,end_year=2022)
    analyzer.fetching()
    analyzer.clean_data()
    print("-- Analysis of the indicators --")

    print("1.")
    stats = analyzer.compute_statistics()
    for indicator,values in stats.items():
        print(f"\n {indicator}:")
        for stat_name, stat_value in values.items():
            print(f"{stat_name.capitalize()}:{stat_value:,.2f}")


    print("CORRELATION ANALYSIS: GDP per Capita vs Life Expectancy")

    corr, p_value  = analyzer.analyze_gdp_life_expectancy()
    if corr is not None:
        print(f"Pearson Correlation Coefficient is {corr:.4f}")
        print(f"P-vlue is {p_value:.4e}")
        print(f"Interpretation: {'Strong' if abs(corr) > 0.7 else 'Moderate' if abs(corr) > 0.4 else 'Weak'} {'positive' if corr > 0 else 'negative'} correlation")
 
    print("VISUALIZATIONS ...")

    visualizer = Visualizer(analyzer)

    print("1. Creating correlation heatmap...")
    visualizer.plot_correlation_heatmap()

    print("2. Creating GDP vs Life Expectancy scatter plots...")
    visualizer.plot_gdp_and_life_expectancy()
  
    print("3. Creating time series by income group...")
    visualizer.plot_time_series_by_income()
  
    print("4. Creating healthcare vs mortality analysis...")
    visualizer.plot_health_care_and_mortality()
  
    print("5. Creating distribution comparisons...")
    visualizer.plot_distribution_comparisons()

    print("ANALYSIS COMPLETED!")


if __name__ == "__main__":
    main()
