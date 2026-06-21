import streamlit as st
import pandas as pd

def apply_filters(df):
    st.sidebar.header("🎛️ Dashboard Filters")
    
    # 1. [span_3](start_span)Reset / Clear Filters Button[span_3](end_span)
    if st.sidebar.button("Reset / Clear Filters"):
        st.rerun()
        
    filtered_df = df.copy()
    
    # 2. [span_4](start_span)Search / Text Filter[span_4](end_span)
    search_query = st.sidebar.text_input("🔍 Search Keyword")
    if search_query:
        # Har column mein text keyword search karne ke liye mask lagaya hai
        mask = filtered_df.astype(str).apply(lambda x: x.str.contains(search_query, case=False)).any(axis=1)
        filtered_df = filtered_df[mask]
        
    # 3. [span_5](start_span)Category Filter / Dropdown (Automatically detects 'Symbol' column)[span_5](end_span)
    cat_columns = filtered_df.select_dtypes(include=['object']).columns.tolist()
    if cat_columns:
        selected_cat_col = st.sidebar.selectbox("Select Category Column", cat_columns)
        unique_vals = filtered_df[selected_cat_col].dropna().unique().tolist()
        
        # 4. [span_6](start_span)Multi-Select Filter[span_6](end_span)
        selected_vals = st.sidebar.multiselect(f"Select Values for {selected_cat_col}", unique_vals, default=unique_vals)
        filtered_df = filtered_df[filtered_df[selected_cat_col].isin(selected_vals)]
        
    # 5. [span_7](start_span)Numerical Range Slider (For Open, High, Low, Close, Volume columns)[span_7](end_span)
    num_columns = filtered_df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    if num_columns:
        selected_num_col = st.sidebar.selectbox("Select Numerical Column to Filter", num_columns)
        min_val = float(filtered_df[selected_num_col].min())
        max_val = float(filtered_df[selected_num_col].max())
        
        if min_val != max_val:
            user_range = st.sidebar.slider(f"Range for {selected_num_col}", min_val, max_val, (min_val, max_val))
            filtered_df = filtered_df[(filtered_df[selected_num_col] >= user_range[0]) & (filtered_df[selected_num_col] <= user_range[1])]

    # 6. [span_8](start_span)Date/Time Range Filter[span_8](end_span)
    # Dataset mein Date column ko convert karne ke baad check karega
    if 'Date' in filtered_df.columns:
        min_date = filtered_df['Date'].min().date()
        max_date = filtered_df['Date'].max().date()
        
        user_date_range = st.sidebar.date_input("Select Date Range", [min_date, max_date])
        
        # Ensure user has selected both start and end date
        if isinstance(user_date_range, list) or isinstance(user_date_range, tuple):
            if len(user_date_range) == 2:
                filtered_df = filtered_df[(filtered_df['Date'].dt.date >= user_date_range[0]) & (filtered_df['Date'].dt.date <= user_date_range[1])]

    return filtered_df