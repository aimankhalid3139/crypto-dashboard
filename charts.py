import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# Matplotlib ki styling global set kar rahe hain taake dashboard responsive aur clean lage
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')

# 1. PIE CHART (Proportional distribution of Volume by Symbol/Date)
def plot_pie_chart(df):
    fig, ax = plt.subplots(figsize=(6, 4))
    # Agar multiple symbols hain toh unka volume share, warna status distribution
    data = df.groupby('Symbol')['Volume'].sum()
    if data.empty or len(data) == 1:
        # Fallback agar sirf ek hi symbol ho pura data mein
        df['Price_Range'] = pd.qcut(df['Close'], q=3, labels=['Low', 'Medium', 'High'], duplicates='drop')
        data = df['Price_Range'].value_counts()
    
    ax.pie(data, labels=data.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette('pastel'))
    ax.set_title("Proportional Distribution (Market Share/Segments)", fontsize=12, fontweight='bold')
    return fig

# 2. HISTOGRAM (Frequency distribution of Close Price)
def plot_histogram(df):
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.histplot(df['Close'], bins=20, kde=True, ax=ax, color='skyblue')
    ax.set_title("Frequency Distribution of Close Price", fontsize=12, fontweight='bold')
    ax.set_xlabel("Close Price")
    ax.set_ylabel("Frequency")
    return fig

# 3. LINE CHART (Trends over time)
def plot_line_chart(df):
    fig, ax = plt.subplots(figsize=(6, 4))
    # Date ko sort karke line plot banana
    df_sorted = df.sort_values('Date')
    ax.plot(df_sorted['Date'], df_sorted['Close'], color='green', marker='o', linestyle='-', markersize=2)
    ax.set_title("Price Trend Over Time", fontsize=12, fontweight='bold')
    ax.set_xlabel("Date")
    ax.set_ylabel("Close Price")
    plt.xticks(rotation=45)
    return fig

# 4. BAR CHART (Compare averages across categories)
def plot_bar_chart(df):
    fig, ax = plt.subplots(figsize=(6, 4))
    # High vs Low price comparison or average close price per group
    df_melted = df.melt(id_vars=['Date'], value_vars=['Open', 'Close'], var_name='Price_Type', value_name='Price')
    sns.barplot(data=df_melted, x='Price_Type', y='Price', ax=ax, palette='muted', errorbar=None)
    ax.set_title("Comparison of Average Open vs Close Price", fontsize=12, fontweight='bold')
    ax.set_xlabel("Price Type")
    ax.set_ylabel("Average Price")
    return fig

# 5. SCATTER PLOT (Relationship between Volume and Close Price)
def plot_scatter_plot(df):
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.scatterplot(data=df, x='Volume', y='Close', ax=ax, color='purple', alpha=0.7)
    ax.set_title("Relationship: Volume vs Close Price", fontsize=12, fontweight='bold')
    ax.set_xlabel("Volume")
    ax.set_ylabel("Close Price")
    return fig

# 6. BOX PLOT (Data spread and outliers)
def plot_box_plot(df):
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.boxplot(data=df[['Open', 'High', 'Low', 'Close']], ax=ax, palette='Set2')
    ax.set_title("Data Spread & Outliers Detection", fontsize=12, fontweight='bold')
    ax.set_ylabel("Price Value")
    return fig

# 7. HEATMAP (Correlation matrix of features)
def plot_heatmap(df):
    fig, ax = plt.subplots(figsize=(6, 4))
    numeric_df = df[['Open', 'High', 'Low', 'Close', 'Volume']].corr()
    sns.heatmap(numeric_df, annot=True, cmap='coolwarm', fmt=".2f", ax=ax, linewidths=0.5)
    ax.set_title("Feature Correlation Matrix", fontsize=12, fontweight='bold')
    return fig

# 8. AREA CHART (Cumulative trends over time)
def plot_area_chart(df):
    fig, ax = plt.subplots(figsize=(6, 4))
    df_sorted = df.sort_values('Date')
    ax.fill_between(df_sorted['Date'], df_sorted['High'], df_sorted['Low'], color="orange", alpha=0.4, label='High-Low Range')
    ax.plot(df_sorted['Date'], df_sorted['Close'], color="darkorange", label='Close')
    ax.set_title("Cumulative / Spread Trend Over Time", fontsize=12, fontweight='bold')
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.legend()
    plt.xticks(rotation=45)
    return fig

# 9. COUNT PLOT (Frequency count of categorical variables)
def plot_count_plot(df):
    fig, ax = plt.subplots(figsize=(6, 4))
    # Agar unique symbols kam hain toh unka count, warna simple categorize karke count
    if 'Price_Range' not in df.columns:
        df['Price_Range'] = pd.qcut(df['Close'], q=3, labels=['Low Price Tier', 'Medium Price Tier', 'High Price Tier'], duplicates='drop')
    sns.countplot(data=df, x='Price_Range', ax=ax, palette='Set3')
    ax.set_title("Frequency Count of Price Categories", fontsize=12, fontweight='bold')
    ax.set_xlabel("Price Tier")
    ax.set_ylabel("Count")
    return fig

# 10. VIOLIN PLOT (Distribution and probability density)
def plot_violin_plot(df):
    fig, ax = plt.subplots(figsize=(6, 4))
    # Reshaping for visualization
    df_melted = df.melt(value_vars=['High', 'Low'], var_name='Metrics', value_name='Price')
    sns.violinplot(data=df_melted, x='Metrics', y='Price', ax=ax, palette='Pastel1')
    ax.set_title("Probability Density & Distribution", fontsize=12, fontweight='bold')
    ax.set_xlabel("Metrics")
    ax.set_ylabel("Price Value")
    return fig
plt.tight_layout()