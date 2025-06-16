import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv("data/aggregated_data.csv")





# App config
st.set_page_config(page_title="March Madness 2025 Dashboard", layout="wide")
st.title("🏀 NCAA March Madness: Gender & Twitter Analysis")

# Overview
st.markdown("""
This dashboard compares **1,000 tweets** about the top men's and women's college basketball players during March Madness.
Using Text Mining Techniques, it explores sentiment, topic focus, and the most common language used by gender.
""")

# Tabs
tab1, tab2, tab3 = st.tabs(["Sentiment", "Topics", "Tweet Focus By Player"])

# --- Tab 1: Sentiment ---
with tab1:
    st.subheader("📊 Sentiment by Gender")

    # --- Average sentiment by gender ---
    sentiment_avg = df.groupby("Gender")["Sentiment Score"].mean().reset_index()
    color_map_gender = {'Men': 'blue', 'Women': 'pink'}

    fig1 = px.bar(
        sentiment_avg,
        x='Gender',
        y='Sentiment Score',
        color='Gender',
        color_discrete_map=color_map_gender,
        title="Average Sentiment Score",
        text_auto='.2f'
    )
    fig1.update_layout(
        xaxis=dict(type='category'),
        yaxis_title='Average Sentiment Score',
        xaxis_title='Gender'
    )
    st.plotly_chart(fig1, use_container_width=True)
    st.markdown("*Women’s tweets have a slightly higher average sentiment (0.19 vs 0.17), but the difference is not statistically significant (p = 0.44). This is much higher than I expected for both genders, as Twitter is often a place for critiques.*")

    # --- Sentiment category counts by gender ---
    sentiment_dist = df.groupby(["Gender", "Sentiment Category"]).size().reset_index(name='Count')
    color_map_sentiment = {
        'Negative': 'red',
        'Neutral': 'yellow',
        'Positive': 'green'
    }

    fig2 = px.bar(
        sentiment_dist,
        x='Gender',
        y='Count',
        color='Sentiment Category',
        color_discrete_map=color_map_sentiment,
        title="Sentiment Category Counts",
        barmode='group'
    )
    fig2.update_layout(
        xaxis=dict(type='category'),
        yaxis_title='Count',
        xaxis_title='Gender'
    )
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown("*The overall distribution of positive, neutral, and negative tweets is similar between genders. However, tweets about men show a noticeably higher count of negative sentiment compared to those about women.*")

    # --- Sentiment breakdown pie charts (side by side) ---
    st.subheader("🧁 Sentiment Breakdown by Gender")

    col1, col2 = st.columns(2)

    with col1:
        gender_df = df[df['Gender'] == 'Men']
        sentiment_counts = gender_df['Sentiment Category'].value_counts().reset_index()
        sentiment_counts.columns = ['Sentiment', 'Count']
        fig_men = px.pie(
            sentiment_counts,
            names='Sentiment',
            values='Count',
            color='Sentiment',
            title="Men - Sentiment Distribution",
            color_discrete_map=color_map_sentiment
        )
        st.plotly_chart(fig_men, use_container_width=True)
        st.markdown("*Just under half of the tweets about men’s players are positive (48%), with a larger portion negative (17%) compared to the tweets about women.*")

    with col2:
        gender_df = df[df['Gender'] == 'Women']
        sentiment_counts = gender_df['Sentiment Category'].value_counts().reset_index()
        sentiment_counts.columns = ['Sentiment', 'Count']
        fig_women = px.pie(
            sentiment_counts,
            names='Sentiment',
            values='Count',
            color='Sentiment',
            title="Women - Sentiment Distribution",
            color_discrete_map=color_map_sentiment
        )
        st.plotly_chart(fig_women, use_container_width=True)
        st.markdown("*Tweets about women’s players show a higher proportion of positivity (52%) and fewer negatives than men's (13%). The neutral tweets have a similiar proportion for both genders*")



# --- Tab 2: Topics ---
with tab2:
    st.subheader("🔍 Topics in Tweets")

    topic_cols = ['Topic_Performance', 'Topic_Appearance', 'Topic_Age']
    topic_descriptions = {
        'Topic_Performance': "Out of 500 tweets per gender, slightly more tweets about male players focused on performance — 115 for men vs. 105 for women.",
        'Topic_Appearance': "Tweets about women were more likely to mention appearance, with 73 appearance-related tweets compared to 49 for men.",
        'Topic_Age': "Tweets discussing player age were more common for men, with 29 tweets mentioning age for male players compared to just 13 for female players."
    }

    color_map = {'Men': 'blue', 'Women': 'pink'}
    gender_order = ['Men', 'Women']

    # Normalize Gender column just in case
    df['Gender'] = df['Gender'].str.strip()

    for topic in topic_cols:
        df_topic = df[df[topic] == 1]
        counts = df_topic.groupby('Gender').size().reset_index(name='Count')

        # Use your actual gender order but filter to those present
        categories = [g for g in gender_order if g in counts['Gender'].values]
        counts['Gender'] = pd.Categorical(counts['Gender'], categories=categories, ordered=True)

        clean_topic = topic.replace('Topic_', '')

        fig = px.bar(
            counts,
            x='Gender',
            y='Count',
            color='Gender',
            category_orders={'Gender': categories},
            color_discrete_map=color_map,
            title=f"Mentions of {clean_topic} by Gender",
            text='Count'
        )

        fig.update_layout(
            xaxis=dict(type='category'),
            yaxis_title='Number of Mentions',
            xaxis_title='Gender'
        )

        st.plotly_chart(fig, use_container_width=True)
        st.markdown(f"*{topic_descriptions[topic]}*")


# --- Tab 3: Top Words (add visualizations later) ---
with tab3:
    st.subheader("💬 Mentions of Appearance and Age by Player")

    # Horizontal bar chart for Appearance Mentions
    st.write("These are the players most frequently mentioned in the context of appearance. As you can see, there are 2 players that have significantly more appearance comments than the rest; Hailey Van Lith and Lauren Betts. Close to 30% of the tweets about them are about their appearance. Nobody on the men's side comes even close to that, capping with Mark Sears at 20%.")

    fig_appearance = px.bar(
        appearance_counts,
        x='Appearance Mentions',
        y='Player Name',
        color='Gender',
        color_discrete_map={'Men': 'blue', 'Women': 'pink'},
        orientation='h',
        title='Appearance Mentions by Player'
    )
    fig_appearance.update_layout(yaxis=dict(dtick=1))
    st.plotly_chart(fig_appearance, use_container_width=True)

    # Horizontal bar chart for Age Mentions
    st.write("These are the players most frequently mentioned in the context of age. Unlike appearance, men dominate these mentions, with both Derik Queen and Chad Baker-Mazara near 15% of tweets about their age. The top woman by age mentions is Sedona Prince, with 10%. ")

    fig_age = px.bar(
        age_counts,
        x='Age Mentions',
        y='Player Name',
        color='Gender',
        color_discrete_map={'Men': 'blue', 'Women': 'pink'},
        orientation='h',
        title='Age Mentions by Player'
    )
    fig_age.update_layout(yaxis=dict(dtick=1))
    st.plotly_chart(fig_age, use_container_width=True)

