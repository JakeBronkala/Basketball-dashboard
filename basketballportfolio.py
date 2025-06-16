import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from scipy.stats import ttest_ind
import re
import streamlit as st


# Load your dataframe
df = pd.read_csv('top_10_women_players.csv')

# Melt the tweet columns into long format
tweet_columns = [col for col in df.columns if col.startswith('Tweet')]
long_df_women = df.melt(id_vars=['Player Name', 'Position'], 
                  value_vars=tweet_columns, 
                  var_name='Tweet #', 
                  value_name='Tweet Text')

# Optional: Clean up 'Tweet #' to just the number
long_df_women['Tweet #'] = long_df_women['Tweet #'].str.extract('(\d+)').astype(int)

#----------------------------------------------------------------------------------------

df2 = pd.read_csv('top_10_men_players.csv')

# Melt the tweet columns into long format
tweet_columns = [col for col in df.columns if col.startswith('Tweet')]
long_df_men = df2.melt(id_vars=['Player Name', 'Position'], 
                  value_vars=tweet_columns, 
                  var_name='Tweet #', 
                  value_name='Tweet Text')

# Optional: Clean up 'Tweet #' to just the number
long_df_men['Tweet #'] = long_df_men['Tweet #'].str.extract('(\d+)').astype(int)


# Assuming you have two DataFrames: df_men and df_women
long_df_men['Gender'] = 'Men'
long_df_women['Gender'] = 'Women'

long_df_men

# Combine them into one DataFrame
df_all = pd.concat([long_df_men, long_df_women], ignore_index=True)

df_all

#--------------------------------------------------------------------------------------

analyzer = SentimentIntensityAnalyzer()

def get_sentiment_score(text):
    if pd.isnull(text):
        return 0.0
    return analyzer.polarity_scores(str(text))['compound']

df_all['Sentiment Score'] = df_all['Tweet Text'].apply(get_sentiment_score)

sentiment_by_gender = df_all.groupby("Gender")["Sentiment Score"].mean().reset_index()

print(sentiment_by_gender)

# Plot sentiment by gender
plt.figure(figsize=(8, 6))
plt.bar(sentiment_by_gender["Gender"], sentiment_by_gender["Sentiment Score"], color=["blue", "orange"])
plt.title("Average Sentiment Score by Gender")
plt.xlabel("Gender")
plt.ylabel("Average Sentiment Score")
plt.show()

male_scores = df_all[df_all["Gender"] == "Men"]["Sentiment Score"]
female_scores = df_all[df_all["Gender"] == "Women"]["Sentiment Score"]
t_stat, p_val = ttest_ind(male_scores, female_scores, equal_var=False)
print(f"Welch’s t-test statistic: {t_stat:.4f}")
print(f"p-value: {p_val:.4f}")

appearance_keywords = ['appearance', 'looks', 'hot', 'ugly', 'skinny', 'beautiful', 'cute', 'pretty', 'fat',
                        'smile', 'hair', 'legs', 'butt', 'attractive', 'pale', 'fine', 'gorgeous', 'ugly', 'hairline' , 'large']
age_keywords = ['young', 'old', 'age', 'teen', 'veteran', 'freshman', 'senior', 'junior', 'sophomore', 'elder', 'aged']
performance_keywords = ['score', 'scoring', 'pass', 'rebound', 'assist', 'block', 'steal', 'defense', 'offense',
                        'speed', 'quickness', 'athletic', 'shoot', 'handle', 'dribble', 'skill', 'dunk', 'playmaking',
                        'performance', 'triple-double', 'double-double']

# Function to check if a tweet mentions any of the appearance-related keywords
def contains_appearance(tweet):
    # Convert the tweet to lowercase for case-insensitive comparison
    tweet = tweet.lower()
    # Check if any of the keywords appear in the tweet
    return any(re.search(r'\b' + re.escape(keyword) + r'\b', tweet) for keyword in appearance_keywords)

def contains_age(tweet):
    # Convert the tweet to lowercase for case-insensitive comparison
    tweet = tweet.lower()
    # Check if any of the keywords appear in the tweet
    return any(re.search(r'\b' + re.escape(keyword) + r'\b', tweet) for keyword in age_keywords)

def contains_performance(tweet):
    # Convert the tweet to lowercase for case-insensitive comparison
    tweet = tweet.lower()
    # Check if any of the keywords appear in the tweet
    return any(re.search(r'\b' + re.escape(keyword) + r'\b', tweet) for keyword in performance_keywords)

# Apply the function to each tweet and create a new column 'Appearance Mentioned'
df_all['Appearance Mentioned'] = df_all['Tweet'].apply(contains_appearance)
df_all['Age Mentioned'] = df_all['Tweet'].apply(contains_age)
df_all['Performance Mentioned'] = df_all['Tweet'].apply(contains_performance)

appearance_frequency = df_all.groupby('Gender')['Appearance Mentioned'].sum()
print(appearance_frequency)

appearance_frequency.plot(kind='bar', color=['blue', 'pink'])
plt.title('Frequency of Appearance Mentions by Gender')
plt.ylabel('Count of Appearance Mentions')
plt.xlabel('Gender')
plt.show()

age_frequency = df_all.groupby('Gender')['Age Mentioned'].sum()
print(age_frequency)

age_frequency.plot(kind='bar', color=['blue', 'pink'])
plt.title('Frequency of Age Mentions by Gender')
plt.ylabel('Count of Age Mentions')
plt.xlabel('Gender')
plt.show()

performance_frequency = df_all.groupby('Gender')['Performance Mentioned'].sum()
print(performance_frequency)

performance_frequency.plot(kind='bar', color=['blue', 'pink'])
plt.title('Frequency of Performance Mentions by Gender')
plt.ylabel('Count of Performance Mentions')
plt.xlabel('Gender')
plt.show()

appearance_frequency_by_player = df_all.groupby('Player Name')['Appearance Mentioned'].sum()
appearance_frequency_by_player = appearance_frequency_by_player.sort_values(ascending=False)
print(appearance_frequency_by_player)

appearance_frequency_by_player.head(10).plot(kind='barh', color='lightblue')
plt.title('Top 10 Players with Most Appearance Mentions')
plt.ylabel('Count of Appearance Mentions')
plt.xlabel('Player Name')
plt.xticks(rotation=90)
plt.show()

df.to_csv("basketball_dashboard/data/aggregated_data.csv", index=False)

#------------------------------------------------------------------------------

df = pd.read_csv("data/aggregated_data.csv")
print(df.columns.tolist())


def sentiment_category(score):
    if score > 0.05:
        return "Positive"
    elif score < -0.05:
        return "Negative"
    else:
        return "Neutral"

df['Sentiment Category'] = df['Sentiment Score'].apply(sentiment_category)


def contains_any(text, keywords):
    text = text.lower()
    return any(word in text for word in keywords)

df['Topic_Performance'] = df['Tweet Text'].apply(lambda x: int(contains_any(x, performance_keywords)))
df['Topic_Appearance'] = df['Tweet Text'].apply(lambda x: int(contains_any(x, appearance_keywords)))
df['Topic_Age'] = df['Tweet Text'].apply(lambda x: int(contains_any(x, age_keywords)))

df = pd.read_csv("data/aggregated_data.csv")

# Sum mentions by player and gender
appearance_counts = (
    df[df['Topic_Appearance'] == 1]
    .groupby(['Player Name', 'Gender'])
    .size()
    .reset_index(name='Appearance Mentions')
    .sort_values('Appearance Mentions', ascending=True)
)

age_counts = (
    df[df['Topic_Age'] == 1]
    .groupby(['Player Name', 'Gender'])
    .size()
    .reset_index(name='Age Mentions')
    .sort_values('Age Mentions', ascending=True)
)

df.to_csv("basketball_dashboard/data/aggregated_data.csv", index=False)

df.columns