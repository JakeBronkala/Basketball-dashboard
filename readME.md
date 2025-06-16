# 🏀 March Madness Twitter Analysis Dashboard

This project explores 1,000 tweets about the top men's and women's NCAA basketball players during March Madness 2025, using text mining and sentiment analysis to uncover patterns in how male and female athletes are discussed online.

📊 **Live Dashboard**: [Click here to view the Streamlit app](https://jakebronkala-basketball-dashboard.streamlit.app)

📄 **Full Report**: See [`MarchMadness_Report.pdf`](MarchMadness_Report.pdf)

---

## 🚀 Project Overview

Using a custom-built text classifier and sentiment analyzer, this dashboard explores:

- **Sentiment differences** between tweets about men’s and women’s players
- **Topical focus** on performance, appearance, and age
- **Player-level analysis** showing which athletes are most frequently discussed in terms of appearance and age

The dataset contains 500 tweets each for the top 10 men’s and top 10 women’s players in the 2025 NCAA tournament.

---

## 📁 Project Structure

basketball-dashboard/
│
├── data/
│ └── aggregated_data.csv # Cleaned tweet data
├── basketball_app.py # Streamlit dashboard code
├── basketballportfolio.py # Data prep and modeling
├── MarchMadness_Report.pdf # Full project write-up
└── README.md # You're here!

---

## 🧠 Tools Used

- **Python** (Pandas, Plotly, Scikit-learn, VADER, SciPy)
- **Streamlit** for interactive dashboarding
- **Git & GitHub** for version control
- **Manual labeling** + custom topic tagging for Appearance, Age, Performance

---

## 📌 Key Takeaways

- Tweets about **women’s players** were slightly more positive on average
- **Appearance** was more commonly discussed in tweets about women
- **Age** was more often mentioned for male players
- Certain players like **Hailey Van Lith** and **Lauren Betts** had unusually high appearance mentions

---

## 🧪 Future Improvements

- Add NLP-driven topic modeling
- Expand dataset to include all tournament players
- Compare tweets over time (pre- vs post-tournament)

---

## 🙋 About Me

Hi, I’m **Jake Bronkala**, a data analyst passionate about sports analytics, NLP, and building tools that communicate insights.  
📧 [Email me](mailto:jakebronkala@gmail.com) or check out more at [my GitHub](https://github.com/JakeBronkala)
