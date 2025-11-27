import streamlit as st
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
    
    @st.cache_data(ttl=3600)
    def fetching(self) -> pd.DataFrame:
        data_frames = []

        for indicator_code, indicator_name in self.indicators.items():
            df = wb.data.DataFrame(indicator_code,
                                   time=range(self.start_year, self.end_year+1), 
                                   numericTimeKeys=True,
                                   labels=True
                                   )
            df = df.reset_index()
            df = df.melt(id_vars=["economy"], var_name="year", value_name=indicator_name)
            df["year"] = pd.to_numeric(df["year"], errors="coerce")
            data_frames.append(df)
            
        if data_frames:
            self.data = data_frames[0]
            for df in data_frames[1:]:
                self.data = pd.merge(
                    self.data, df, on=["economy", "year"],
                    how="outer"
                )
        return self.data
    
    @st.cache_data(ttl=3600)
    def clean_data(self) -> pd.DataFrame:
        for indicator in self.indicators.values():
            if indicator in self.data.columns:
                self.data[indicator] = pd.to_numeric(self.data[indicator], errors="coerce")
        
        self.data = self.data.dropna(how="all", subset=list(self.indicators.values()))
        countries = wb.economy.DataFrame()
        income_dict = countries["incomeLevel"].to_dict()   
        self.data["income_group"] = self.data["economy"].map(income_dict)

        region_dict = countries["region"].to_dict()
        self.data["region"] = self.data["economy"].map(region_dict)

        return self.data
    
    def compute_correlation(self) -> pd.DataFrame:
        all_data = list(self.indicators.values())
        correlation_matrix = self.data[all_data].corr()
        return correlation_matrix
    
    def compute_statistics(self) -> Dict:
        stats_dict = {}
        for indicator in self.indicators.values():
            stats_dict[indicator] = {
                "mean": np.nanmean(self.data[indicator]),
                "median": np.nanmedian(self.data[indicator]),
                "std": np.nanstd(self.data[indicator]),
                "min": np.nanmin(self.data[indicator]),
                "max": np.nanmax(self.data[indicator])
            }
        return stats_dict
    
    def analyze_gdp_life_expectancy(self) -> Tuple[float, float]:
        filtered_data = self.data.dropna(subset=["GDP_per_capita", "Life_expectancy"])

        if len(filtered_data) > 0:
            correlation, p_value = stats.pearsonr(
                filtered_data["GDP_per_capita"],
                filtered_data["Life_expectancy"],
            )
            return correlation, p_value
        return None, None

    def analyze_trends_by_income(self) -> pd.DataFrame:
        if "income_group" in self.data.columns:
            trends = self.data.groupby(['year', 'income_group']).agg({
               'GDP_per_capita': 'mean',
               'Life_expectancy': 'mean',
               'Infant_mortality_rate': 'mean',
               'Healthcare_spending_per_capita': 'mean'
            }).reset_index()
            return trends
        return None

class Visualizer:
    def __init__(self, analyzer: WealthOfNationsAnalyzer):
        self.analyzer = analyzer
        self.data = analyzer.data
    
    def plot_correlation_heatmap(self):
        corr_matrix = self.analyzer.compute_correlation()
        
        fig, ax = plt.subplots(figsize=(12, 10))
        sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', 
                    center=0, square=True, ax=ax)
        ax.set_title("Correlation Matrix: Economic and Well-Being Indicators", 
                     fontsize=16, fontweight='bold')
        plt.tight_layout()
        return fig

    def plot_gdp_and_life_expectancy(self):
        recent_year = self.data["year"].max()
        recent_data = self.data[self.data["year"] == recent_year].dropna(
            subset=["GDP_per_capita", "Life_expectancy"])
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 7))

        if "income_group" in recent_data.columns:
            for income in recent_data["income_group"].unique():
                if pd.notna(income):
                    subset = recent_data[recent_data["income_group"] == income]
                    ax1.scatter(subset["GDP_per_capita"], subset["Life_expectancy"], 
                               alpha=0.6, s=100, label=income)
        else:
            ax1.scatter(recent_data["GDP_per_capita"], recent_data["Life_expectancy"], 
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
        return fig

    def plot_time_series_by_income(self):
        trends = self.analyzer.analyze_trends_by_income()
      
        if trends is None:
            return None
      
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
        return fig
    
    def plot_health_care_and_mortality(self):
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
        return fig

    def plot_distribution_comparisons(self):
        if 'income_group' not in self.data.columns:
            return None
      
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
                bp = ax.boxplot(data_to_plot, tick_labels=labels, patch_artist=True)
              
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
        return fig

def main():
    st.set_page_config(
        page_title="Wealth of Nations Analysis",
        page_icon="🌍",
        layout="wide"
    )
    
    st.title("Project Topic: Wealth of Nations:Economic Prosperity and Population Well-being Analysis")

    st.markdown("""
    This application analyzes the relationship between economic prosperity (GDP per capita) 
    and population well-being indicators across countries from 2000-2022 using World Bank data.
    """)
    
    st.sidebar.header("Filter")
    start_year = st.sidebar.slider("Start Year", 2000, 2020, 2000)
    end_year = st.sidebar.slider("End Year", 2001, 2022, 2022)
    
    if start_year >= end_year:
        st.sidebar.error("Start year must be before end year!")
        return
    
    @st.cache_data
    def load_data(start, end):
        analyzer = WealthOfNationsAnalyzer(start_year=start, end_year=end)
        with st.spinner("Fetching data from World Bank API..."):
            analyzer.fetching()
            analyzer.clean_data()
        return analyzer
    
    try:
        analyzer = load_data(start_year, end_year)
        visualizer = Visualizer(analyzer)
        
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "Overview", 
            "Correlations", 
            "GDP vs Life Expectancy",
            "Healthcare Analysis",
            "Trends & Distributions"
        ])
        
        with tab1:
            st.header("Dataset Overview")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Records", f"{len(analyzer.data):,}")
            with col2:
                st.metric("Countries", analyzer.data['economy'].nunique())
            with col3:
                st.metric("Years Covered", f"{start_year}-{end_year}")
            
            st.subheader("Statistical Summary")
            stats = analyzer.compute_statistics()
            
            stats_df = pd.DataFrame(stats).T
            st.dataframe(stats_df.style.format("{:.2f}"), use_container_width=True)
            
            st.subheader("Sample Data")
            st.dataframe(analyzer.data.head(20), use_container_width=True)
        
        with tab2:
            st.header("Correlation Analysis")
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.subheader("Correlation Heatmap")
                fig = visualizer.plot_correlation_heatmap()
                st.pyplot(fig)
                plt.close()
            
            with col2:
                st.subheader("GDP vs Life Expectancy")
                corr, p_value = analyzer.analyze_gdp_life_expectancy()
                
                if corr is not None:
                    st.metric("Pearson Correlation", f"{corr:.4f}")
                    st.metric("P-value", f"{p_value:.4e}")
                    
                    if abs(corr) > 0.7:
                        strength = "Strong"
                    elif abs(corr) > 0.4:
                        strength = "Moderate"
                    else:
                        strength = "Weak"
                    
                    direction = "positive" if corr > 0 else "negative"
                    
                    st.info(f"**Interpretation:** {strength} {direction} correlation")
        
        with tab3:
            st.header("GDP per Capita vs Life Expectancy")
            fig = visualizer.plot_gdp_and_life_expectancy()
            st.pyplot(fig)
            plt.close()
            
            st.markdown("""
            **Key Insights:**
            - The scatter plots show the relationship between economic prosperity and life expectancy
            - The log scale plot (right) better reveals patterns for countries with lower GDP
            - Different income groups show distinct clustering patterns
            """)
        
        with tab4:
            st.header("Healthcare Spending vs Infant Mortality")
            fig = visualizer.plot_health_care_and_mortality()
            st.pyplot(fig)
            plt.close()
            
            st.markdown("""
            **Key Insights:**
            - Higher healthcare spending generally correlates with lower infant mortality
            - Income group plays a significant role in this relationship
            - Some outliers suggest other factors beyond spending affect outcomes
            """)
        
        with tab5:
            st.header("Trends Over Time")
            
            st.subheader("Time Series by Income Group")
            fig = visualizer.plot_time_series_by_income()
            if fig:
                st.pyplot(fig)
                plt.close()
            
            st.subheader("Distribution Comparisons")
            fig = visualizer.plot_distribution_comparisons()
            if fig:
                st.pyplot(fig)
                plt.close()
            
            st.markdown("""
            **Key Insights:**
            - Clear divergence between income groups over time
            - High-income countries show consistent improvement across all indicators
            - Distribution plots reveal significant inequality between income groups
            """)
        
        st.sidebar.markdown("---")
        st.sidebar.markdown("### Indicators")
        for code, name in analyzer.indicators.items():
            st.sidebar.markdown(f"- {name}")
        
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.info("Please check your internet connection and try again.")


if __name__ == "__main__":
    main()