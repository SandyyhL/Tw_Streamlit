import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import json
from collections import Counter

st.set_page_config(
    page_title="Tradwife Case Study",
    page_icon="📊",
    layout="centered"
)

### Introduction
st.title("Tradwife Case Study")
st.subheader("Introduction ℹ️")
st.write("Welcome to my thesis research project!")
st.write("This page is a demo of Tradwife community analysis with social computing tools. This main page shows the raw and processed data we are using.")

### Raw Data
st.subheader("Data Collection 📊")

with open("raw_data_tagged.json", 'r') as fin:
    raw_data = json.load(fin)

total_videos = len(raw_data)
creators = [video['username'] for video in raw_data]

# Count the number of videos per creator
creator_counts = Counter(creators)
total_creators = len(creator_counts)

st.write(f"We collected videos tagged with #tradwife from 2023.1.1-2024.10.12 in JSON format. In total, the data contains content from" +
         f" `{total_creators}` users, summing up to `{total_videos}` videos.")

### Top 50 most active accounts
st.subheader("Most Active Accounts 🏆")
st.write("We are interested in investigating the accounts that have been most actively engaged with #tradwife hashtag. Therefore, I decided to create a new dataframe with these accounts.")
top_50 = creator_counts.most_common(50)
# Display in a DataFrame
top_50_df = pd.DataFrame(top_50, columns=["Username", "Number of Videos"])
st.write("Here are the top 50 most active accounts in the dataset:")
st.dataframe(top_50_df)

st.write("Now, to get a holistic understanding of these most active accounts, I used TikTok API to collect all the videos they have posted over the course of 2023.1.1-2024.10.12.")
st.write("See below for the information of the our new dataset.")

with open("raw_data_cleaned_top50.json", "r") as file:
    top50_data = json.load(file)

account_video_counts = {account: len(videos) for account, videos in top50_data.items()}
top50_df = pd.DataFrame(list(account_video_counts.items()), columns=["Username", "Number of Videos"])

# Sort the DataFrame by the number of videos in descending order
top50_df = top50_df.sort_values(by="Number of Videos", ascending=False)
top50_df.reset_index(drop=True, inplace=True)

# Display the raw data
st.write("Here is the summary of the video counts for the top 50 accounts:")
st.dataframe(top50_df)

# Visualization
st.subheader("Top 50 Accounts Visualization 📊")

fig, ax = plt.subplots(figsize=(12, 8))
top50_df.plot.bar(x="Username", y="Number of Videos", ax=ax, legend=False, color="skyblue")
ax.set_title("Total Videos Posted by Top 50 Accounts")
ax.set_xlabel("Username")
ax.set_ylabel("Number of Videos")

# Rotate x-axis labels for better readability
plt.xticks(rotation=45, ha="right")

# Render the plot in Streamlit
st.pyplot(fig)

# Additional insights
st.subheader("Real Tradwives? 🥣")

st.write("I manually picked out Tradwife accounts within this new dataset. Below is the list of accounts.")

sandy_tradwives = [
    "lifetaketwo", "thymeandtenderness", "stayzontopp", "littlehouseonthepasture", 
    "thatjoyfilledhome", "senecasky", "hardmeadfarm", "jennifer__tate__", 
    "theblazed_homemaker", "mrsarialewis", "alexislester_", "mrs.blancarte", 
    "target_tradwife", "yelenamyshko", "pakistanitradwife", "ladysfarm"
]

# Load the raw data
with open("raw_data_cleaned_top50.json", "r") as fin:
    raw_data = json.load(fin)

# Filter the data for selected accounts
selected_data = {creator: raw_data[creator] for creator in sandy_tradwives if creator in raw_data}

# Count the number of videos for each selected account
tradwife_activity = {creator: len(videos) for creator, videos in selected_data.items()}

# Convert to DataFrame for visualization
tradwife_df = pd.DataFrame(list(tradwife_activity.items()), columns=["Username", "Number of Videos"])

# Sort by number of videos for better visualization
tradwife_df = tradwife_df.sort_values(by="Number of Videos", ascending=False)

# Display the data
st.write("Below is the activity data for the selected Tradwife accounts:")
st.dataframe(tradwife_df)

# Visualization
st.subheader("Tradwife Accounts Visualization 📊")
fig, ax = plt.subplots(figsize=(10, 6))
tradwife_df.plot.bar(x="Username", y="Number of Videos", ax=ax, legend=False)
ax.set_title("Activity of Selected Tradwife Accounts")
ax.set_xlabel("Username")
ax.set_ylabel("Number of Videos")

# Rotate the x-axis labels for better readability
plt.xticks(rotation=45, ha="right")
st.pyplot(fig)

st.write("With this new dataset, we can now conduct more detailed analysis. Please click the sidebar to navigate through analysis samples I created.")


# st.write("Data Preview:")
# //st.dataframe(df.head())

# sns.set(style="whitegrid")

# account_order = (
#     df.groupby(['account', 'tagged_with_tradwife'])['log_engagement']
#     .median()
#     .unstack()
#     .mean(axis=1)
#     .sort_values()
#     .index
# )

# fig, ax = plt.subplots()

# sns.boxplot(
#     data=df,
#     x='account',
#     y='log_engagement',
#     hue='tagged_with_tradwife',
#     order=account_order,  # Order accounts based on median engagement
#     showfliers=False,  # Remove outliers
#     ax = ax
# )

# ax.set_title("Combined Logged Engagement Boxplot (Sorted by Median, Without Outliers)")
# ax.set_xlabel("Account")
# ax.set_ylabel("Engagement (Likes + Comments + Shares)")
# plt.xticks(rotation=45, ha="right")

# handles, labels = plt.gca().get_legend_handles_labels()
# ax.legend(handles, ["Non-Tradwife", "Tradwife"], title="Tagged with Tradwife")

# fig_html = mpld3.fig_to_html(fig)
# #st.pyplot(fig)
# components.html(fig_html, height=600)