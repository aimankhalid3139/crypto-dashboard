import streamlit as st
import pandas as pd
# Apne banaye huwe files/modules ko import kar rahe hain
from filters import apply_filters
import charts

# 1. Page Configuration & Layout Standard
st.set_page_config(page_title="Crypto Data EDA Dashboard", layout="wide")

# Dashboard Title and brief description at the top
st.title("📊 Crypto Data Visualization Dashboard")
st.caption("This interactive dashboard analyzes cryptocurrency trends using standard technical charts.")
st.markdown("---")

# 2.Data Loading Funtion
@st.cache_data
def load_data():
    df = pd.read_csv("cryptodata.csv")
    df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d %I-%p', errors='coerce')
    df = df.dropna(subset=['Date'])
    return df

# Data ko load karna
try:
    df = load_data()
except FileNotFoundError:
    st.error("❌ 'data/cryptodata.csv' nahi mili! Please check karein ke file data folder mein majood hai aur sahi named hai.")
    st.stop()

# 3. Apply Filters Sidebar (Connecting to your previous filter code)
# Filtered data simultaneously updates all charts
filtered_df = apply_filters(df)

# Check agar filter karne ke baad data khali toh nahi ho gaya
if filtered_df.empty:
    st.warning("⚠️ Selected filters ke mutabik koi data available nahi hai. Please filters adjust karein.")
else:
    # 4. KPI Summary Cards at the top
    st.subheader("📌 Key Performance Indicators (KPIs)")
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    
    with kpi1:
        st.metric(label="Total Records Loaded", value=f"{len(filtered_df):,}")
    with kpi2:
        st.metric(label="Average Close Price", value=f"${filtered_df['Close'].mean():.2f}")
    with kpi3:
        st.metric(label="Highest High Price", value=f"${filtered_df['High'].max():.2f}")
    with kpi4:
        st.metric(label="Total Volume Traded", value=f"{filtered_df['Volume'].sum():,.0f}")
        
    st.markdown("---")

    # 5. Grouping Related Charts Logically into Tabs/Sections
    st.subheader("📈 Exploratory Data Analysis & Visualizations")
    
    tab1, tab2, tab3 = st.tabs(["💰 Price Distributions", "🕒 Trend Analysis", "🔄 Relationships & Matrix"])
    
    with tab1:
        # Layout metrics: Clean columns grid
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 1. Proportional Share (Pie Chart)")
            st.pyplot(charts.plot_pie_chart(filtered_df))
        with col2:
            st.markdown("### 2. Frequency Distribution (Histogram)")
            st.pyplot(charts.plot_histogram(filtered_df))
            
        col3, col4 = st.columns(2)
        with col3:
            st.markdown("### 3. Category Frequency (Count Plot)")
            st.pyplot(charts.plot_count_plot(filtered_df))
        with col4:
            st.markdown("### 4. Data Spread & Outliers (Box Plot)")
            st.pyplot(charts.plot_box_plot(filtered_df))

    with tab2:
        col5, col6 = st.columns(2)
        with col5:
            st.markdown("### 5. Price Trend Over Time (Line Chart)")
            st.pyplot(charts.plot_line_chart(filtered_df))
        with col6:
            st.markdown("### 6. Cumulative/Spread Trend (Area Chart)")
            st.pyplot(charts.plot_area_chart(filtered_df))
            
        col7, col8 = st.columns(2)
        with col7:
            st.markdown("### 7. Price Comparison (Bar Chart)")
            st.pyplot(charts.plot_bar_chart(filtered_df))
        with col8:
            st.markdown("### 8. Probability Density (Violin Plot)")
            st.pyplot(charts.plot_violin_plot(filtered_df))

    with tab3:
        col9, col10 = st.columns(2)
        with col9:
            st.markdown("### 9. Feature Correlation (Heatmap)")
            st.pyplot(charts.plot_heatmap(filtered_df))
        with col10:
            st.markdown("### 10. Volume vs Price (Scatter Plot)")
            st.pyplot(charts.plot_scatter_plot(filtered_df))

    # Footer Info
    st.markdown("---")
    st.caption("Dashboard built strictly according to the EDA Project Guidelines.")