# HealthKart Influencer Campaign Dashboard

## 🧠 Context

HealthKart runs influencer campaigns across platforms like Instagram, YouTube, and Twitter to promote brands such as **MuscleBlaze**, **HKVitals**, and **Gritzo**. Influencers may be paid based on posts or per order.

This dashboard helps track:
- Campaign performance
- Influencer-level insights
- ROI and Incremental ROAS
- Payouts

---

## 🎯 Objective

Build an interactive dashboard that allows marketers to:
- Upload or ingest influencer campaign data
- Analyze post and influencer performance
- Filter by brand, product, platform, influencer type
- Gain actionable insights
- Export filtered data if needed

---

## 📁 Project Structure
HealthKart_dashboard/
├── data/
│ ├── influencers.csv
│ ├── posts.csv
│ ├── tracking_data.csv
│ └── payouts.csv
├── analysis.ipynb # EDA and insight generation
├── dashboard.py # Streamlit dashboard code
├── requirements.txt # Python dependencies
├── README.md # Project documentation
└── insights.md # Key findings from data




---

## 📁 Simulated Datasets

| Dataset        | Description |
|----------------|-------------|
| **influencers.csv** | Influencer metadata including category, platform, and follower count |
| **posts.csv**       | Post-level data including engagement metrics like reach, likes, comments |
| **tracking_data.csv** | Tracking user actions (orders, revenue) mapped to influencers |
| **payouts.csv**     | Influencer payout structure (per post/order), rate, and total payout |

---

## 🚀 How to Run

### 1. Install dependencies
```bash
pip install -r requirements.txt

#2. Run the Streamlit dashboard 
streamlit run dashboard.py

## ⚙️ Key Features

- Visualize campaign performance (reach, revenue, ROAS)
- Post- and influencer-level performance tracking
- Platform, category, and brand filtering
- ROAS and Incremental ROAS calculation
- Export filtered data to CSV (optional)

## 💻 Tech Stack

- Python 3
- Streamlit
- Pandas
- Plotly
- Jupyter Notebook (for EDA)

## 👨‍💻 Author

**Sumati Tripathi**  
*Data Science Intern*

## 📜 License

This project is for educational and demonstration purposes only.



