import streamlit as st
import wbgapi as wb
import pandas as pd
import numpy as np
from scipy.stats import pearsonr
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
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
        data_frames = []
        for indicator_code, indicator_name in self.indicators.items():
            df = wb.data.DataFrame(indicator_code,
                                   time=range(self.start_year, self.end_year+1), 
                                   numericTimeKeys=True,
                                   labels=True)
            df = df.reset_index()
            df = df.melt(id_vars=["economy"], var_name="year", value_name=indicator_name)
            df["year"] = pd.to_numeric(df["year"], errors="coerce")
            data_frames.append(df)
            
        if data_frames:
            self.data = data_frames[0]
            for df in data_frames[1:]:
                self.data = pd.merge(self.data, df, on=["economy", "year"], how="outer")
        return self.data
    
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
        
        # Add ISO codes for map visualization
        iso_dict = countries.reset_index()['id'].to_dict()
        self.data["iso_code"] = self.data["economy"].map(iso_dict)
        
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
    
    def get_top_bottom_countries(self, indicator: str, year: int, n: int = 10):
        """Get 10 top and bottom countries for a specific indicator and year"""
        year_data = self.data[self.data['year'] == year].dropna(subset=[indicator])
        
        # Determine if higher is better or lower is better
        lower_is_better = indicator in ['Infant_mortality_rate']
        
        if lower_is_better:
            top = year_data.nsmallest(n, indicator)[['economy', indicator, 'income_group']].copy()
            bottom = year_data.nlargest(n, indicator)[['economy', indicator, 'income_group']].copy()
        else:
            top = year_data.nlargest(n, indicator)[['economy', indicator, 'income_group']].copy()
            bottom = year_data.nsmallest(n, indicator)[['economy', indicator, 'income_group']].copy()
        
        # Rename 'economy' column to 'Country'
        top = top.rename(columns={'economy': 'Country'})
        bottom = bottom.rename(columns={'economy': 'Country'})
        
        return top, bottom

class Visualizer:
    def __init__(self, analyzer: WealthOfNationsAnalyzer):
        self.analyzer = analyzer
        self.data = analyzer.data
    
    def plot_correlation_heatmap(self):
        corr_matrix = self.analyzer.compute_correlation()
        fig, ax = plt.subplots(figsize=(12, 10))
        sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', 
                    center=0, square=True, ax=ax, linewidths=0.5)
        ax.set_title("Correlation Matrix: Economic and Well-Being Indicators", 
                     fontsize=16, fontweight='bold')
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

    def plot_scatter_matrix(self):
        recent_year = self.data['year'].max()
        recent_data = self.data[self.data['year'] == recent_year]
        
        indicators = ['GDP_per_capita', 'Life_expectancy', 'Infant_mortality_rate', 
                     'Healthcare_spending_per_capita']
        plot_data = recent_data[indicators].dropna()
        
        fig = plt.figure(figsize=(16, 16))
        
        for i, ind1 in enumerate(indicators):
            for j, ind2 in enumerate(indicators):
                ax = plt.subplot(len(indicators), len(indicators), i * len(indicators) + j + 1)
                
                if i == j:
                    ax.hist(plot_data[ind1].dropna(), bins=30, color='skyblue', edgecolor='black')
                    ax.set_ylabel('Frequency', fontsize=8)
                else:
                    ax.scatter(plot_data[ind2], plot_data[ind1], alpha=0.5, s=20)
                
                if i == len(indicators) - 1:
                    ax.set_xlabel(ind2.replace('_', ' ').title(), fontsize=8)
                else:
                    ax.set_xticklabels([])
                
                if j == 0:
                    ax.set_ylabel(ind1.replace('_', ' ').title(), fontsize=8)
                else:
                    ax.set_yticklabels([])
                
                ax.grid(True, alpha=0.3)
        
        plt.suptitle(f'Scatter Matrix of Key Indicators ({recent_year})', 
                    fontsize=16, fontweight='bold')
        plt.tight_layout()
        return fig
    
    def create_country_trend_plot(self, selected_countries: List[str], selected_income_groups: List[str], 
                                   indicator: str, indicator_name: str):
        """Create trend plot for selected countries and income groups with visible data labels"""
        fig = go.Figure()
        
        if selected_countries:
            for country in selected_countries:
                country_data = self.data[self.data['economy'] == country].sort_values('year')
                if len(country_data) > 0:
                    fig.add_trace(go.Scatter(
                        x=country_data['year'],
                        y=country_data[indicator],
                        mode='lines+markers+text',
                        name=country,
                        text=country_data[indicator].round(2),
                        textposition='top center',
                        textfont=dict(size=9),
                        line=dict(width=2.5),
                        marker=dict(size=8),
                        legendgroup='countries',
                        legendgrouptitle_text='Countries'
                    ))
        
        # Add income group trends (aggregated)
        if selected_income_groups:
            for income_group in selected_income_groups:
                group_data = self.data[self.data['income_group'] == income_group].groupby('year')[indicator].mean().reset_index()
                if len(group_data) > 0:
                    fig.add_trace(go.Scatter(
                        x=group_data['year'],
                        y=group_data[indicator],
                        mode='lines+markers+text',
                        name=f'{income_group} (avg)',
                        text=group_data[indicator].round(2),
                        textposition='top center',
                        textfont=dict(size=9),
                        line=dict(width=3, dash='dash'),
                        marker=dict(size=6),
                        legendgroup='income_groups',
                        legendgrouptitle_text='Income Groups'
                    ))
        
        if not selected_countries and not selected_income_groups:
            # Show nothing if no selection
            fig.add_annotation(
                text="Please select countries or income groups from the sidebar",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=16)
            )
        
        fig.update_layout(
            title=f'{indicator_name} Trends Over Time',
            xaxis_title='Year',
            yaxis_title=indicator_name,
            hovermode='x unified',
            template='plotly_white',
            height=600,
            showlegend=True,
            legend=dict(orientation="v", yanchor="top", y=1, xanchor="left", x=1.02)
        )
        
        return fig
    
    def create_top_bottom_tables(self, indicator: str, year: int):
        top, bottom = self.analyzer.get_top_bottom_countries(indicator, year, n=10)
        return top, bottom

def create_indicator_tab(visualizer, indicator_key, indicator_name, selected_countries, 
                        selected_income_groups, selected_year):
        
    st.header(f"{indicator_name} Analysis")
    
    # 1. TREND PLOT
    st.subheader("Trends Over Time")
    trend_fig = visualizer.create_country_trend_plot(
        selected_countries, 
        selected_income_groups,
        indicator_key, 
        indicator_name
    )
    st.plotly_chart(trend_fig, use_container_width=True)
    
    # 2. TOP/BOTTOM TABLES
    st.subheader(f"Top 10 & Bottom 10 Countries ({selected_year})")
    top_countries, bottom_countries = visualizer.create_top_bottom_tables(indicator_key, selected_year)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("Top 10 Countries")
        st.dataframe(
            top_countries.style.background_gradient(cmap='Greens', subset=[indicator_key]),
            use_container_width=True,
            hide_index=True
        )
    
    with col2:
        st.markdown("Bottom 10 Countries")
        st.dataframe(
            bottom_countries.style.background_gradient(cmap='Reds', subset=[indicator_key]),
            use_container_width=True,
            hide_index=True
        )

def format_number(x):
    try:
        return f"{x:,.2f}".replace(",", " ")
    except:
        return x

def main():
    st.set_page_config(
        page_title="Wealth of Nations Analysis Project",
        page_icon="📈",
        layout="wide"
    )
    st.markdown("### Project #1: Economic Prosperity and Population Well-being Analysis by WBG")
    st.markdown("""
    Analysis of the relationship between economic prosperity and population well-being 
    indicators across countries using World Bank data.
    """)
    
    st.sidebar.header("Date Filter")
    start_year = st.sidebar.slider("Start Year", 2000, 2022, 2000)
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
    
    analyzer = load_data(start_year, end_year)
    visualizer = Visualizer(analyzer)
    
    st.sidebar.markdown("---")
    st.sidebar.header("Filter Options")
    
    countries_list = sorted(analyzer.data['economy'].unique().tolist())
    
    select_all_countries = st.sidebar.checkbox("Select All Countries", value=False)
    
    if select_all_countries:
        selected_countries = countries_list
        st.sidebar.info(f"All {len(countries_list)} countries selected")
    else:
        selected_countries = st.sidebar.multiselect(
            "Choose Specific Countries",
            options=countries_list,
            default=["ITA"],
            help="Select countries to compare trends over time"
        )
    
    st.sidebar.markdown("---")
    income_groups = sorted([ig for ig in analyzer.data['income_group'].unique() if pd.notna(ig)])
    
    select_all_income = st.sidebar.checkbox("Select All Income Groups", value=False)
    
    if select_all_income:
        selected_income_groups = income_groups
        st.sidebar.info(f"All {len(income_groups)} income groups selected")
    else:
        selected_income_groups = st.sidebar.multiselect(
            "Choose Income Groups",
            options=income_groups,
            default=["HIC"],
            help="Select income groups to show average trends"
        )
    
    st.sidebar.markdown("---")

    selected_year = st.sidebar.slider(
        "Select Year for Tables",
        min_value=start_year,
        max_value=end_year,
        value=end_year,
        help="Choose which year to display in top/bottom rankings"
    )
   
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "Overview",
        "Correlations", 
        "GDP per Capita",
        "Healthcare",
        "Education",
        "Population",
        "Infant Mortality"
    ])
    
    with tab1:
        st.header("Dataset Overview")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Records", f"{len(analyzer.data):,}")
        with col2:
            st.metric("Countries", analyzer.data['economy'].nunique())
        with col3:
            st.metric("Years", f"{start_year}-{end_year}")
        with col4:
            st.metric("Indicators", len(analyzer.indicators))
        
        st.subheader("Statistical Summary")
        stats = analyzer.compute_statistics()
        stats_df = pd.DataFrame(stats).T

        st.dataframe(stats_df.style.format(format_number), use_container_width=True)
        
        st.subheader("Sample Data")
        st.dataframe(analyzer.data.head(20).style.format(format_number), use_container_width=True)
    
    with tab2:
        st.header("Correlation Analysis")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("Correlation Heatmap")
            fig = visualizer.plot_correlation_heatmap()
            st.pyplot(fig)
            plt.close()
        
        with col2:
            st.subheader("Key Statistics")
            
            filtered_data = analyzer.data.dropna(subset=["GDP_per_capita", "Life_expectancy"])
            if len(filtered_data) > 0:
                corr, p_value = pearsonr(
                    filtered_data["GDP_per_capita"],
                    filtered_data["Life_expectancy"]
                )
                
                st.metric("GDP ↔ Life Expectancy", f"{corr:.4f}")
                st.metric("P-value", f"{p_value:.4e}")
                
                if abs(corr) > 0.7:
                    strength = "Strong"
                elif abs(corr) > 0.4:
                    strength = "Moderate"
                else:
                    strength = "Weak"
                
                direction = "positive" if corr > 0 else "negative"
                st.info(f"**{strength} {direction} correlation**")
        
        st.markdown("---")
        st.subheader("Correlation Heatmap Summary")
        corr_matrix = analyzer.compute_correlation()
        
        corr_flat = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
        strong_corrs = []
        for i in range(len(corr_matrix)):
            for j in range(i+1, len(corr_matrix)):
                if abs(corr_matrix.iloc[i, j]) > 0.5:
                    strong_corrs.append((
                        corr_matrix.index[i],
                        corr_matrix.columns[j],
                        corr_matrix.iloc[i, j]
                    ))
        
        strong_corrs.sort(key=lambda x: abs(x[2]), reverse=True)
        
        st.markdown(f"""
        **Key Findings from Correlation Analysis:**
        - The heatmap reveals **{len([c for c in strong_corrs if c[2] > 0.7])} strong positive correlations** (>0.7) between indicators
        - **{len([c for c in strong_corrs if c[2] < -0.7])} strong negative correlations** (<-0.7) were identified
        - GDP per capita shows the strongest correlation with life expectancy ({corr:.3f}), indicating that economic prosperity is closely linked to population health outcomes
        - Infant mortality rate exhibits strong negative correlations with GDP per capita and healthcare spending, suggesting that wealthier nations with better healthcare systems have lower infant deaths
        """)
        
        if strong_corrs:
            st.markdown("**Top 3 Strongest Correlations:**")
            for i, (ind1, ind2, corr_val) in enumerate(strong_corrs[:3], 1):
                direction = "positive" if corr_val > 0 else "negative"
                st.markdown(f"{i}. **{ind1}** ↔ **{ind2}**: {corr_val:.3f} ({direction})")
        
        st.markdown("---")
        st.subheader("Scatter Matrix")
        fig = visualizer.plot_scatter_matrix()
        st.pyplot(fig)
        plt.close()
        
        st.markdown("---")
        st.subheader("Scatter Matrix Summary")
        recent_year = analyzer.data['year'].max()
        recent_data = analyzer.data[analyzer.data['year'] == recent_year]
        indicators_list = ['GDP_per_capita', 'Life_expectancy', 'Infant_mortality_rate', 'Healthcare_spending_per_capita']
        
        st.markdown(f"""
        **Scatter Matrix Insights (Year {recent_year}):**
        - The diagonal histograms show the distribution of each indicator across all countries
        - **GDP per capita** distribution is heavily right-skewed, with most countries clustered at lower values and few high-income outliers
        - **Life expectancy** shows a more normal distribution with most countries between 65-80 years
        - **Infant mortality rate** exhibits high variance, ranging from near-zero in developed nations to over 50 per 1,000 births in developing countries
        - Off-diagonal scatter plots reveal non-linear relationships, particularly between GDP and health indicators, suggesting diminishing returns at higher income levels
        - Clear clusters emerge based on income groups, with high-income countries forming distinct groups in the upper-right quadrants
        """)
        
        st.markdown("---")
        st.subheader("Distribution Comparisons by Income Group")
        fig = visualizer.plot_distribution_comparisons()
        if fig:
            st.pyplot(fig)
            plt.close()
        
        st.markdown("---")
        st.subheader("📝 Distribution Comparisons Summary")
        st.markdown(f"""
        **Distribution Analysis by Income Group (Year {recent_year}):**
        
        **Key Insights:**
        - **Substantial inequality** exists between income groups across all indicators
        - High-income countries demonstrate consistently better outcomes: higher GDP per capita, longer life expectancy, lower infant mortality, and greater healthcare spending
        - **Within-group variance** is notable, particularly in middle-income groups, suggesting that country-specific policies and governance play significant roles beyond just income level
        - Box plots reveal **extreme outliers** in several categories:
            - Some low-income countries achieve surprisingly high life expectancy relative to GDP
            - Certain high-income nations spend disproportionately on healthcare
        - The **interquartile ranges** (IQR) are widest for middle-income groups, indicating diverse development trajectories within similar income brackets
        - Lower-middle income countries show the highest variance in infant mortality rates, highlighting uneven progress in maternal and child health services
        """)
    
    with tab3:
        create_indicator_tab(
            visualizer,
            'GDP_per_capita',
            'GDP per Capita (USD)',
            selected_countries,
            selected_income_groups,
            selected_year
        )
    
    with tab4:
        create_indicator_tab(
            visualizer,
            'Healthcare_spending_per_capita',
            'Healthcare Spending per Capita (USD)',
            selected_countries,
            selected_income_groups,
            selected_year
        )
    
    with tab5:
        create_indicator_tab(
            visualizer,
            'Education_expenditure_pct_GDP',
            'Education Expenditure (% of GDP)',
            selected_countries,
            selected_income_groups,
            selected_year
        )
    
    with tab6:
        create_indicator_tab(
            visualizer,
            'Population',
            'Total Population',
            selected_countries,
            selected_income_groups,
            selected_year
        )
    
    with tab7:
        create_indicator_tab(
            visualizer,
            'Infant_mortality_rate',
            'Infant Mortality Rate (per 1,000 births)',
            selected_countries,
            selected_income_groups,
            selected_year
        )

if __name__ == "__main__":
    main()