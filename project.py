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
    print("Analysis result")
    analyzer = WealthOfNationsAnalyzer(start_year=2000,end_year=2022)
    analyzer.fetching()
    print("hello")

if __name__ == "__main__":
    main()
