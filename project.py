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
    
    def fetch_data(self) -> pd.DataFrame:
        print("Fetching data from World Bank API...")
        data_frames = []
        
        for indicator_code, indicator_name in self.indicators.items():
            try:
                print(f"Fetching {indicator_name}...")
                df = wb.data.DataFrame(
                    indicator_code,
                    time=range(self.start_year, self.end_year + 1),
                    numericTimeKeys=True,
                    labels=True
                )
                
                df = df.reset_index()
                df = df.melt(id_vars=['economy'], var_name='year', value_name=indicator_name)
                df['year'] = pd.to_numeric(df['year'], errors='coerce')
                df[indicator_name] = pd.to_numeric(df[indicator_name], errors='coerce')
                data_frames.append(df)
                
            except Exception as e:
                print(f"Error fetching {indicator_name}: {str(e)}")
                continue
        
        if data_frames:
            self.data = data_frames[0]
            for df in data_frames[1:]:
                self.data = pd.merge(
                    self.data, df, 
                    on=['economy', 'year'], 
                    how='outer'
                )
        
        print(f"Data fetched successfully! Shape: {self.data.shape}")
        return self.data
    
    def clean_data(self) -> pd.DataFrame:
        print("Cleaning data...")
        
        for indicator in self.indicators.values():
            if indicator in self.data.columns:
                self.data[indicator] = pd.to_numeric(self.data[indicator], errors='coerce')
        
        self.data = self.data.dropna(how='all', subset=list(self.indicators.values()))
        
        try:
            countries = wb.economy.DataFrame()
            income_dict = countries['incomeLevel'].to_dict()
            self.data['income_group'] = self.data['economy'].map(income_dict)
        except:
            print("Could not fetch income group data")
        
        try:
            region_dict = countries['region'].to_dict()
            self.data['region'] = self.data['economy'].map(region_dict)
        except:
            print("Could not fetch region data")
        
        print(f"Data cleaned! Final shape: {self.data.shape}")
        return self.data
    
    def compute_correlations(self) -> pd.DataFrame:
        
        numeric_cols = list(self.indicators.values())
        correlation_matrix = self.data[numeric_cols].corr()
        return correlation_matrix
    
    def compute_statistics(self) -> Dict:
        
        stats_dict = {}
        
        for indicator in self.indicators.values():
            if indicator in self.data.columns:
                stats_dict[indicator] = {
                    'mean': np.nanmean(self.data[indicator]),
                    'median': np.nanmedian(self.data[indicator]),
                    'std': np.nanstd(self.data[indicator]),
                    'min': np.nanmin(self.data[indicator]),
                    'max': np.nanmax(self.data[indicator])
                }
        
        return stats_dict
    
    def analyze_gdp_life_expectancy(self) -> Tuple[float, float]:
       
        # Filter data with both values present
        filtered_data = self.data.dropna(subset=['GDP_per_capita', 'Life_expectancy'])
        
        if len(filtered_data) > 0:
            correlation, p_value = stats.pearsonr(
                filtered_data['GDP_per_capita'],
                filtered_data['Life_expectancy']
            )
            return correlation, p_value
        return None, None
    
    def analyze_trends_by_income_group(self) -> pd.DataFrame:
        
        if 'income_group' in self.data.columns:
            trends = self.data.groupby(['year', 'income_group']).agg({
                'GDP_per_capita': 'mean',
                'Life_expectancy': 'mean',
                'Infant_mortality_rate': 'mean',
                'Healthcare_spending_per_capita': 'mean'
            }).reset_index()
            return trends
        return None


class WealthVisualizer:
    
    
    def __init__(self, analyzer: WealthOfNationsAnalyzer):
        
        self.analyzer = analyzer
        self.data = analyzer.data
    
    def plot_correlation_heatmap(self, save_path: str = None):
        
        corr_matrix = self.analyzer.compute_correlations()
        
        plt.figure(figsize=(12, 10))
        sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', 
                    center=0, square=True, linewidths=1, cbar_kws={"shrink": 0.8})
        plt.title('Correlation Matrix: Economic and Well-being Indicators', 
                  fontsize=16, fontweight='bold', pad=20)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
    
    def plot_gdp_vs_life_expectancy(self, save_path: str = None):
        
        recent_year = self.data['year'].max()
        recent_data = self.data[self.data['year'] == recent_year].dropna(
            subset=['GDP_per_capita', 'Life_expectancy']
        )
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 7))
        
        if 'income_group' in recent_data.columns:
            for income in recent_data['income_group'].unique():
                if pd.notna(income):
                    subset = recent_data[recent_data['income_group'] == income]
                    ax1.scatter(subset['GDP_per_capita'], subset['Life_expectancy'], 
                              alpha=0.6, s=100, label=income)
        else:
            ax1.scatter(recent_data['GDP_per_capita'], recent_data['Life_expectancy'], 
                       alpha=0.6, s=100)
        
        ax1.set_xlabel('GDP per Capita (USD)', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Life Expectancy (years)', fontsize=12, fontweight='bold')
        ax1.set_title(f'GDP vs Life Expectancy ({recent_year})', fontsize=14, fontweight='bold')
        ax1.legend(title='Income Group')
        ax1.grid(True, alpha=0.3)
        
        if 'income_group' in recent_data.columns:
            for income in recent_data['income_group'].unique():
                if pd.notna(income):
                    subset = recent_data[recent_data['income_group'] == income]
                    ax2.scatter(subset['GDP_per_capita'], subset['Life_expectancy'], 
                              alpha=0.6, s=100, label=income)
        else:
            ax2.scatter(recent_data['GDP_per_capita'], recent_data['Life_expectancy'], 
                       alpha=0.6, s=100)
        
        ax2.set_xlabel('GDP per Capita (USD) - Log Scale', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Life Expectancy (years)', fontsize=12, fontweight='bold')
        ax2.set_title(f'GDP vs Life Expectancy - Log Scale ({recent_year})', 
                     fontsize=14, fontweight='bold')
        ax2.set_xscale('log')
        ax2.legend(title='Income Group')
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
    
    def plot_time_series_by_income(self, save_path: str = None):
        
        trends = self.analyzer.analyze_trends_by_income_group()
        
        if trends is None:
            print("Income group data not available")
            return
        
        fig, axes = plt.subplots(2, 2, figsize=(18, 14))
        
        indicators = [
            ('GDP_per_capita', 'GDP per Capita (USD)', axes[0, 0]),
            ('Life_expectancy', 'Life Expectancy (years)', axes[0, 1]),
            ('Infant_mortality_rate', 'Infant Mortality Rate (per 1,000)', axes[1, 0]),
            ('Healthcare_spending_per_capita', 'Healthcare Spending per Capita (USD)', axes[1, 1])
        ]
        
        for indicator, title, ax in indicators:
            for income in trends['income_group'].unique():
                if pd.notna(income):
                    subset = trends[trends['income_group'] == income]
                    ax.plot(subset['year'], subset[indicator], marker='o', 
                           linewidth=2, label=income, markersize=4)
            
            ax.set_xlabel('Year', fontsize=11, fontweight='bold')
            ax.set_ylabel(title, fontsize=11, fontweight='bold')
            ax.set_title(f'{title} Over Time by Income Group', fontsize=13, fontweight='bold')
            ax.legend(title='Income Group', loc='best')
            ax.grid(True, alpha=0.3)
        
        plt.suptitle('Economic and Well-being Indicators: Trends by Income Group', 
                    fontsize=16, fontweight='bold', y=1.00)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
    
    def plot_healthcare_vs_mortality(self, save_path: str = None):
        
        recent_year = self.data['year'].max()
        recent_data = self.data[self.data['year'] == recent_year].dropna(
            subset=['Healthcare_spending_per_capita', 'Infant_mortality_rate']
        )
        
        fig, ax = plt.subplots(figsize=(14, 8))
        
        if 'income_group' in recent_data.columns:
            for income in recent_data['income_group'].unique():
                if pd.notna(income):
                    subset = recent_data[recent_data['income_group'] == income]
                    ax.scatter(subset['Healthcare_spending_per_capita'], 
                             subset['Infant_mortality_rate'], 
                             alpha=0.6, s=120, label=income)
        else:
            ax.scatter(recent_data['Healthcare_spending_per_capita'], 
                      recent_data['Infant_mortality_rate'], 
                      alpha=0.6, s=120)
        
        ax.set_xlabel('Healthcare Spending per Capita (USD)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Infant Mortality Rate (per 1,000 live births)', 
                     fontsize=12, fontweight='bold')
        ax.set_title(f'Healthcare Spending vs Infant Mortality ({recent_year})', 
                    fontsize=14, fontweight='bold')
        ax.legend(title='Income Group')
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
    
    def plot_distribution_comparisons(self, save_path: str = None):
        
        if 'income_group' not in self.data.columns:
            print("Income group data not available")
            return
        
        recent_year = self.data['year'].max()
        recent_data = self.data[self.data['year'] == recent_year]
        
        fig, axes = plt.subplots(2, 2, figsize=(18, 14))
        
        indicators = [
            ('GDP_per_capita', 'GDP per Capita (USD)', axes[0, 0]),
            ('Life_expectancy', 'Life Expectancy (years)', axes[0, 1]),
            ('Infant_mortality_rate', 'Infant Mortality Rate', axes[1, 0]),
            ('Healthcare_spending_per_capita', 'Healthcare Spending per Capita (USD)', axes[1, 1])
        ]
        
        for indicator, title, ax in indicators:
            data_to_plot = []
            labels = []
            
            for income in recent_data['income_group'].unique():
                if pd.notna(income):
                    subset = recent_data[recent_data['income_group'] == income][indicator].dropna()
                    if len(subset) > 0:
                        data_to_plot.append(subset)
                        labels.append(income)
            
            if data_to_plot:
                bp = ax.boxplot(data_to_plot, labels=labels, patch_artist=True)
                
                colors = sns.color_palette("husl", len(data_to_plot))
                for patch, color in zip(bp['boxes'], colors):
                    patch.set_facecolor(color)
                    patch.set_alpha(0.7)
                
                ax.set_ylabel(title, fontsize=11, fontweight='bold')
                ax.set_title(f'{title} Distribution by Income Group ({recent_year})', 
                           fontsize=13, fontweight='bold')
                ax.tick_params(axis='x', rotation=45)
                ax.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()


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
