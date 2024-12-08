import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import mpld3
import streamlit.components.v1 as components

st.write("Hello World!")

x = st.text_input("What's your research topic?")

st.write(f"Your research topic is {x}")

df = pd.read_csv("streamlit_logged_chart_data.csv")

st.write("Data Preview:")
st.dataframe(df.head())

sns.set(style="whitegrid")

account_order = (
    df.groupby(['account', 'tagged_with_tradwife'])['log_engagement']
    .median()
    .unstack()
    .mean(axis=1)
    .sort_values()
    .index
)

fig, ax = plt.subplots()

sns.boxplot(
    data=df,
    x='account',
    y='log_engagement',
    hue='tagged_with_tradwife',
    order=account_order,  # Order accounts based on median engagement
    showfliers=False,  # Remove outliers
    ax = ax
)

ax.set_title("Combined Logged Engagement Boxplot (Sorted by Median, Without Outliers)")
ax.set_xlabel("Account")
ax.set_ylabel("Engagement (Likes + Comments + Shares)")
plt.xticks(rotation=45, ha="right")

handles, labels = plt.gca().get_legend_handles_labels()
ax.legend(handles, ["Non-Tradwife", "Tradwife"], title="Tagged with Tradwife")

fig_html = mpld3.fig_to_html(fig)
#st.pyplot(fig)
components.html(fig_html, height=600)