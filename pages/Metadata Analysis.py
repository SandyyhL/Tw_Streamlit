import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import json
from collections import Counter
import plotly.express as px


st.title("Metadata Analysis")
st.write("In this page, we will walk through metadata analysis of tradwife videos.")

st.subheader("Engagement Analysis")
st.write("One research question I have is whether using #tradwife hashtag leads to more engagement of the videos, where engagement is measured by save, like and repost.")

# Load the dataset
df = pd.read_csv("/Users/sandyliu/Thesis/Streamlit/streamlit_logged_chart_data.csv")

# Display a preview of the data
st.write("### Data Preview")
st.dataframe(df.head())

# Calculate median engagement for sorting
sorted_accounts = (
    df.groupby("account")["log_engagement"]
    .median()
    .sort_values(ascending=True)
    .index
)

# Enforce the sorting order in the 'account' column
df["account"] = pd.Categorical(df["account"], categories=sorted_accounts, ordered=True)

# Create a boxplot using Plotly
st.write("### Sorted Boxplot of Logged Engagement by Account and 'Tagged with Tradwife'")
fig = px.box(
    df.sort_values("account"),  # Ensure sorted order is used
    x="account", 
    y="log_engagement", 
    color="tagged_with_tradwife", 
    labels={
        "account": "Account", 
        "log_engagement": "Logged Engagement",
        "tagged_with_tradwife": "Tagged With Tradwife"
    },
    title="Sorted Boxplot of Logged Engagement (Grouped by Account and 'Tagged With Tradwife')"
)

# Force Plotly to exclude all points (including outliers)
fig.update_traces(boxpoints=False)

# Customize layout for better readability
fig.update_layout(
    xaxis=dict(title="Account", tickangle=45),  # Rotate x-axis labels
    yaxis=dict(title="Logged Engagement"),
    boxmode="group",  # Group the boxplots side by side
    legend_title_text="Tagged With Tradwife"
)

# Display the Plotly chart
st.plotly_chart(fig, use_container_width=True)

st.write("You can reference the code snippet below on how to create this visualization.")

# Insert a code snippet illustrating the visualization process
st.write("### How to Create This Visualization")
code_snippet = """
import pandas as pd
import plotly.express as px

# Calculate median engagement for sorting
account_median = (
    df.groupby("account")["log_engagement"]
    .median()
    .sort_values(ascending=True)
)

# Enforce the sorting order based on median engagement
df["account"] = pd.Categorical(df["account"], categories=account_median.index, ordered=True)

# Create a boxplot using Plotly
fig = px.box(
    df.sort_values("account"),  # Ensure sorted order
    x="account", 
    y="log_engagement", 
    color="tagged_with_tradwife", 
    labels={
        "account": "Account", 
        "log_engagement": "Logged Engagement",
        "tagged_with_tradwife": "Tagged With Tradwife"
    },
    title="Boxplot Sorted by Median Engagement"
)

# Remove all points (no outliers, for the purpose of our practice)
fig.update_traces(boxpoints=False)

# Customize layout
fig.update_layout(
    xaxis=dict(title="Account", tickangle=45),
    yaxis=dict(title="Logged Engagement"),
    boxmode="group",
    legend_title_text="Tagged With Tradwife"
)

# Display the chart
fig.show()
"""
st.code(code_snippet, language="python")