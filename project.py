import streamlit as st
import wbgapi as wb
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from typing import List

## class for fetching and cleaning data from wbgapi
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
            data = wb.data.fetch(
                indicator_code,
                economy='all',
                time=range(self.start_year, self.end_year + 1)
            )
            records = []
            for item in data:
                year_str = str(item['time']).replace('YR', '')
                records.append({
                    'economy': item['economy'],
                    'year': int(year_str),
                    indicator_name: item['value']
                })
            
            df = pd.DataFrame(records)
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
        country_list = list(wb.economy.list())
        code_to_name = {c['id']: c['value'] for c in country_list}
        
        self.data['country_name'] = self.data['economy'].map(code_to_name).fillna(self.data['economy'])
        
        income_dict = countries["incomeLevel"].to_dict()   
        self.data["income_group"] = self.data["economy"].map(income_dict)
        
        self.data = self.data[self.data['income_group'].notna() & (self.data['income_group'] != '')]

        return self.data
    
    def save_to_excel(self, filename: str = None):
        if self.data is None:
            raise ValueError("No data to save")
        
        if filename is None:
            filename = f'world_bank_data_{self.start_year}_{self.end_year}.xlsx'
        
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            self.data.to_excel(writer, sheet_name='All_Data', index=False)

        return filename
    
# class for all visualizations and plots
class Visualizer:
    def __init__(self, analyzer: WealthOfNationsAnalyzer):
        self.analyzer = analyzer
        self.data = analyzer.data
    
    def create_top_bottom_tables(self, indicator: str, year: int):
        year_data = self.data[self.data['year'] == year].dropna(subset=[indicator])
        
        lower_is_better = indicator in ['Infant_mortality_rate']
        
        if lower_is_better:
            top = year_data.nsmallest(10, indicator)[['economy', indicator, 'income_group']].copy()
            top = top.sort_values(by=indicator, ascending=True)
            
            bottom = year_data.nlargest(10, indicator)[['economy', indicator, 'income_group']].copy()
            
            bottom = bottom.sort_values(by=indicator, ascending=True)
        else:
            top = year_data.nlargest(10, indicator)[['economy', indicator, 'income_group']].copy()
            top = top.sort_values(by=indicator, ascending=False)
            
            bottom = year_data.nsmallest(10, indicator)[['economy', indicator, 'income_group']].copy()
            bottom = bottom.sort_values(by=indicator, ascending=False)
        
        top = top.rename(columns={'economy': 'Country'})
        bottom = bottom.rename(columns={'economy': 'Country'})
        
        return top, bottom
 
    def create_country_trend_plot(self, selected_countries: List[str], selected_income_groups: List[str], indicator: str, indicator_name: str):
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
            fig.add_annotation(
                text="Please select countries or income groups from the sidebar",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=16)
            )
        
        fig.update_layout(
            xaxis_title='Year',
            yaxis_title=indicator_name,
            hovermode='x unified',
            template='plotly_white',
            height=600,
            showlegend=True,
            legend=dict(orientation="v", yanchor="top", y=1, xanchor="left", x=1.02)
        )
        return fig

    def plot_wealth_wellbeing_correlation(self):
        data_with_years = self.data.dropna(subset=['GDP_per_capita', 'Life_expectancy', 'income_group'])
        
        fig = px.scatter(
            data_with_years,
            x='GDP_per_capita',
            y='Life_expectancy',
            animation_frame='year',
            animation_group='economy',
            size='Population',
            color='income_group',
            hover_name='economy',
            log_x=True,
            size_max=60,
            range_x=[100, 200000],
            range_y=[30, 90],
            labels={
                'GDP_per_capita': 'GDP per Capita (USD, log scale)',
                'Life_expectancy': 'Life Expectancy (years)',
                'income_group': 'Income Group'
            },
            template='plotly_white',
            height=700
        )
        fig.update_traces(marker=dict(opacity=0.7, line=dict(width=0.5, color='white')))
        return fig

# template for tabs in streamlit
def create_indicator_tab(visualizer, indicator_key, indicator_name, selected_countries,selected_income_groups, selected_year):
        
    st.header(f"{indicator_name} Analysis")
    trend_fig = visualizer.create_country_trend_plot(
        selected_countries, 
        selected_income_groups,
        indicator_key, 
        indicator_name
    )
    trend_fig.update_yaxes(tickformat=",.2f")
    st.plotly_chart(trend_fig, use_container_width=True)
    st.markdown("---")
    st.subheader(f"Top 10 Strong/Weak countries ({selected_year})")
    top_countries, bottom_countries = visualizer.create_top_bottom_tables(indicator_key, selected_year)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("Top 10 Countries")
        styled_df = (
            top_countries.style
            .background_gradient(cmap="Greens", subset=[indicator_key])
            .format({indicator_key: format_number})
        )
            
        st.dataframe(
            styled_df,
            use_container_width=True,
            hide_index=True
        )

    with col2:
        st.markdown("Bottom 10 Countries")
            
        styled_df = (
            bottom_countries.style
            .background_gradient(cmap="Reds_r", subset=[indicator_key])
            .format({indicator_key: format_number})
        )
            
        st.dataframe(
            styled_df,
            use_container_width=True,
            hide_index=True
        )


# format numbers
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
    Analysis of the relationship between economic prosperity indicators across countries using World Bank data.
    """)
    st.markdown("""
    *Author: Ulugbek Nortojiev*
    """)
    
    ##sidebar block
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
            analyzer.save_to_excel()
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
            default=[],
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
   
    ## swithing tabs
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "Overview",
        "GDP per Capita",
        "Healthcare",
        "Education",
        "Population",
        "Infant Mortality",
        "Correlations", 
    ])

    with tab1:
        st.header("Dataset Overview")
        filtered_data = analyzer.data.copy()
        
        # Apply country filter
        if not select_all_countries and selected_countries:
            filtered_data = filtered_data[filtered_data['economy'].isin(selected_countries)]
        
        # Apply income group filter
        if not select_all_income and selected_income_groups:
            filtered_data = filtered_data[filtered_data['income_group'].isin(selected_income_groups)]
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Records", f"{len(filtered_data):,}")
        with col2:
            st.metric("Countries", filtered_data['economy'].nunique())
        with col3:
            st.metric("Years", f"{start_year}-{end_year}")
        with col4:
            st.metric("Indicators", len(analyzer.indicators))
        
        st.subheader("Statistical Summary")
        
        # Compute statistics for filtered data
        filtered_stats_dict = {}
        
        for indicator in analyzer.indicators.values():
            if indicator in filtered_data.columns:
                filtered_stats_dict[indicator] = {
                    "avg": np.nanmean(filtered_data[indicator]),
                    "median": np.nanmedian(filtered_data[indicator]),
                    "std": np.nanstd(filtered_data[indicator]),
                    "min": np.nanmin(filtered_data[indicator]),
                    "max": np.nanmax(filtered_data[indicator])
                }
        filtered_stats_df = pd.DataFrame(filtered_stats_dict).T
        
        st.dataframe(filtered_stats_df.style.format(format_number), use_container_width=True)
        st.markdown("---")
        st.subheader("Sample Data")

        # Show filtered data and count
        st.markdown(f"*Displaying {len(filtered_data):,} records based on your selection*")
        st.dataframe(filtered_data, use_container_width=True, height=400)
        
        csv = filtered_data.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download data as csv",
            data=csv,
            file_name=f"filtered_wealth_data_{start_year}_{end_year}.csv",
            mime="text/csv"
        )

    with tab2:
        create_indicator_tab(
            visualizer,
            'GDP_per_capita',
            'GDP per Capita (USD)',
            selected_countries,
            selected_income_groups,
            selected_year
        )
    
    with tab3:
        create_indicator_tab(
            visualizer,
            'Healthcare_spending_per_capita',
            'Healthcare Spending per Capita (USD)',
            selected_countries,
            selected_income_groups,
            selected_year
        )
    
    with tab4:
        create_indicator_tab(
            visualizer,
            'Education_expenditure_pct_GDP',
            'Education Expenditure (% of GDP)',
            selected_countries,
            selected_income_groups,
            selected_year
        )
    
    with tab5:
        create_indicator_tab(
            visualizer,
            'Population',
            'Total Population',
            selected_countries,
            selected_income_groups,
            selected_year
        )
    
    with tab6:
        create_indicator_tab(
            visualizer,
            'Infant_mortality_rate',
            'Infant Mortality Rate (per 1,000 births)',
            selected_countries,
            selected_income_groups,
            selected_year
        )

    with tab7:
        st.header("Correlation Analysis & Country Comparison")
        st.markdown("---")
        st.subheader("Compare Two Countries")
        
        # Country selection for comparison
        countries_list = sorted(analyzer.data['economy'].unique().tolist())
        col1, col2 = st.columns(2)
        
        with col1:
            country_1 = st.selectbox(
                "Select First Country",
                options=countries_list,
                index=countries_list.index("USA") if "USA" in countries_list else 0,
                key="country_1"
            )
        
        with col2:
            country_2 = st.selectbox(
                "Select Second Country",
                options=countries_list,
                index=countries_list.index("CHN") if "CHN" in countries_list else 1,
                key="country_2"
            )
        # Filter data for selected countries
        comparison_data = analyzer.data[
            analyzer.data['economy'].isin([country_1, country_2])
        ].copy()
        
        # Show basic info
        st.info(f"Comparing **{country_1}** vs **{country_2}** ({start_year}-{end_year})")
        
        country_1_data = comparison_data[
            (comparison_data['economy'] == country_1) & 
            (comparison_data['year'] == selected_year)
        ]
        country_2_data = comparison_data[
            (comparison_data['economy'] == country_2) & 
            (comparison_data['year'] == selected_year)
        ]
        
        st.markdown("---")
        
        st.subheader(f"Key Indicators Comparison ({int(selected_year)})")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            gdp_1 = country_1_data['GDP_per_capita'].values[0] if len(country_1_data) > 0 else 0
            gdp_2 = country_2_data['GDP_per_capita'].values[0] if len(country_2_data) > 0 else 0
            st.metric(
                "GDP per Capita",
                f"${gdp_1:,.0f}",
                delta=f"{gdp_1 - gdp_2:,.0f} vs {country_2}",
                delta_color="off"
            )
            st.caption(f"{country_2}: ${gdp_2:,.0f}")
        
        with col2:
            life_1 = country_1_data['Life_expectancy'].values[0] if len(country_1_data) > 0 else 0
            life_2 = country_2_data['Life_expectancy'].values[0] if len(country_2_data) > 0 else 0
            st.metric(
                "Life Expectancy",
                f"{life_1:.1f} years",
                delta=f"{life_1 - life_2:.1f} years",
                delta_color="normal"
            )
            st.caption(f"{country_2}: {life_2:.1f} years")
        
        with col3:
            health_1 = country_1_data['Healthcare_spending_per_capita'].values[0] if len(country_1_data) > 0 else 0
            health_2 = country_2_data['Healthcare_spending_per_capita'].values[0] if len(country_2_data) > 0 else 0
            st.metric(
                "Healthcare Spending",
                f"${health_1:,.0f}",
                delta=f"${health_1 - health_2:,.0f}",
                delta_color="off"
            )
            st.caption(f"{country_2}: ${health_2:,.0f}")
        
        with col4:
            mort_1 = country_1_data['Infant_mortality_rate'].values[0] if len(country_1_data) > 0 else 0
            mort_2 = country_2_data['Infant_mortality_rate'].values[0] if len(country_2_data) > 0 else 0
            st.metric(
                "Infant Mortality",
                f"{mort_1:.1f}",
                delta=f"{mort_1 - mort_2:.1f}",
                delta_color="inverse"
            )
            st.caption(f"{country_2}: {mort_2:.1f}")
        
        st.markdown("---")
        
        # GDP vs Life Expectancy Comparison
        st.subheader("GDP per Capita vs Life Expectancy")
        
        fig_gdp_life = px.scatter(
            comparison_data,
            x='GDP_per_capita',
            y='Life_expectancy',
            color='economy',
            size='Population',
            hover_name='economy',
            hover_data={
                'year': True,
                'GDP_per_capita': ':,.0f',
                'Life_expectancy': ':.1f',
                'Population': ':,.0f'
            },
            labels={
                'GDP_per_capita': 'GDP per Capita (USD)',
                'Life_expectancy': 'Life Expectancy (years)',
                'economy': 'Country'
            },
            template='plotly_white',
            height=500,
            color_discrete_map={country_1: '#1f77b4', country_2: '#ff7f0e'}
        )
        
        fig_gdp_life.update_traces(marker=dict(opacity=0.7, line=dict(width=1, color='white')))
        st.plotly_chart(fig_gdp_life, use_container_width=True)
        
        st.markdown("---")
        
        # Healthcare vs Infant Mortality Comparison
        st.subheader("Healthcare Spending vs Infant Mortality")
        
        fig_health_mort = px.scatter(
            comparison_data,
            x='Healthcare_spending_per_capita',
            y='Infant_mortality_rate',
            color='economy',
            size='Population',
            hover_name='economy',
            hover_data={
                'year': True,
                'Healthcare_spending_per_capita': ':,.0f',
                'Infant_mortality_rate': ':.2f',
                'Population': ':,.0f'
            },
            labels={
                'Healthcare_spending_per_capita': 'Healthcare Spending per Capita (USD)',
                'Infant_mortality_rate': 'Infant Mortality Rate (per 1,000 births)',
                'economy': 'Country'
            },
            template='plotly_white',
            height=500,
            color_discrete_map={country_1: '#1f77b4', country_2: '#ff7f0e'}
        )
        
        fig_health_mort.update_traces(marker=dict(opacity=0.7, line=dict(width=1, color='white')))
        st.plotly_chart(fig_health_mort, use_container_width=True)
        
        st.markdown("---")
        
        # Time Series Comparison - All Indicators
        st.subheader("Trends Over Time Comparison")
        
        indicators_to_plot = {
            'GDP_per_capita': 'GDP per Capita (USD)',
            'Life_expectancy': 'Life Expectancy (years)',
            'Healthcare_spending_per_capita': 'Healthcare Spending per Capita (USD)',
            'Infant_mortality_rate': 'Infant Mortality Rate (per 1,000 births)',
            'Education_expenditure_pct_GDP': 'Education Expenditure (% of GDP)'
        }
        
        selected_indicator = st.selectbox(
            "Select Indicator for Time Series",
            options=list(indicators_to_plot.keys()),
            format_func=lambda x: indicators_to_plot[x],
            key="time_series_indicator"
        )
        
        fig_timeseries = go.Figure()
        
        for country in [country_1, country_2]:
            country_time_data = comparison_data[comparison_data['economy'] == country].sort_values('year')
            
            fig_timeseries.add_trace(go.Scatter(
                x=country_time_data['year'],
                y=country_time_data[selected_indicator],
                mode='lines+markers',
                name=country,
                line=dict(width=3),
                marker=dict(size=8),
                hovertemplate=f'<b>{country}</b><br>' +
                            'Year: %{x}<br>' +
                            f'{indicators_to_plot[selected_indicator]}: %{"{y:,.2f}"}' +
                            '<extra></extra>'
            ))
        
        fig_timeseries.update_layout(
            title=f'{indicators_to_plot[selected_indicator]}: {country_1} vs {country_2}',
            xaxis_title='Year',
            yaxis_title=indicators_to_plot[selected_indicator],
            hovermode='x unified',
            template='plotly_white',
            height=500,
            showlegend=True
        )
        
        st.plotly_chart(fig_timeseries, use_container_width=True)
        st.markdown("---")
        st.subheader("Detailed Statistics Comparison")
        comparison_table = []
        
        for indicator, indicator_name in analyzer.indicators.items():
            if indicator_name in comparison_data.columns:
                val_1 = country_1_data[indicator_name].values[0] if len(country_1_data) > 0 and not country_1_data[indicator_name].isna().values[0] else None
                val_2 = country_2_data[indicator_name].values[0] if len(country_2_data) > 0 and not country_2_data[indicator_name].isna().values[0] else None
                
                if val_1 is not None and val_2 is not None:
                    diff = val_1 - val_2
                    pct_diff = (diff / val_2 * 100) if val_2 != 0 else 0
                    
                    comparison_table.append({
                        'Indicator': indicator_name.replace('_', ' ').title(),
                        country_1: f"{val_1:,.2f}",
                        country_2: f"{val_2:,.2f}",
                        'Difference': f"{diff:,.2f}",
                        '% Difference': f"{pct_diff:.1f}%"
                    })
        if comparison_table:
            comparison_df = pd.DataFrame(comparison_table)
            st.dataframe(
                comparison_df.style.set_properties(**{'text-align': 'center'}),
                use_container_width=True,
                hide_index=True
            )
        st.markdown("---")    
        st.subheader("Life Expectancy among income-group countries (animated)")
        fig_animated = visualizer.plot_wealth_wellbeing_correlation()
        st.plotly_chart(fig_animated, use_container_width=True)
        
if __name__ == "__main__":
    main()