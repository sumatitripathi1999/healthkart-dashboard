import streamlit as st
import pandas as pd
import plotly.express as px

# ---------- Load Data ----------
@st.cache_data
def load_data():
    posts = pd.read_csv("data/posts.csv")
    tracking = pd.read_csv("data/tracking_data.csv")
    payouts = pd.read_csv("data/payouts.csv")
    influencers = pd.read_csv("data/influencers.csv")

    for df in [posts, tracking, payouts, influencers]:
        df.columns = df.columns.str.strip().str.lower()


    df = pd.merge(posts, tracking, on='influencer_id',how='left')
    df = pd.merge(df, payouts, on='influencer_id', how='left')
    df = pd.merge(df, influencers, on='influencer_id',how='left')
    df.rename(columns={'total_payout': 'payout'}, inplace=True)
    df['ROAS'] = df['revenue'] / df['payout']
    df.rename(columns={'influencer_id': 'influencer'}, inplace=True)
    df.rename(columns={'platform_y': 'platform'}, inplace=True)
    df.rename(columns={'orders_y': 'orders'}, inplace=True)

    return df

df = load_data()


# ---------- Sidebar Filters ----------
st.sidebar.header("Filters")
selected_platform = st.sidebar.multiselect("Platform", df['platform'].unique(), default=df['platform'].unique())
selected_brand = st.sidebar.multiselect("Brand", df['brand'].unique(), default=df['brand'].unique())
selected_category = st.sidebar.multiselect("Category", df['category'].unique(), default=df['category'].unique())
selected_gender = st.sidebar.multiselect("Gender", df['gender'].unique(), default=df['gender'].unique())

df_filtered = df[
    (df['platform'].isin(selected_platform)) &
    (df['brand'].isin(selected_brand)) &
    (df['category'].isin(selected_category)) &
    (df['gender'].isin(selected_gender))
]

# ---------- Dashboard Header ----------
st.title("📊 HealthKart Influencer Campaign Dashboard")
st.markdown("Analyze influencer campaign performance by platform, brand, and persona.")

# ---------- KPI Metrics ----------
total_revenue = df_filtered['revenue'].sum()
total_cost = df_filtered['payout'].sum()
overall_roas = total_revenue / total_cost if total_cost != 0 else 0

col1, col2, col3 = st.columns(3)
col1.metric("Total Revenue", f"₹{total_revenue:,.0f}")
col2.metric("Total Payout", f"₹{total_cost:,.0f}")
col3.metric("Overall ROAS", f"{overall_roas:.2f}")

# ---------- Optional: Incremental ROAS ----------
if 'source' in df.columns:
    influencer_data = df_filtered[df_filtered['source'] == 'influencer']
    baseline_data = df_filtered[df_filtered['source'] == 'organic']
    
    influencer_roas = influencer_data['revenue'].sum() / influencer_data['payout'].sum() if influencer_data['payout'].sum() else 0
    baseline_roas = baseline_data['revenue'].sum() / baseline_data['payout'].sum() if baseline_data['payout'].sum() else 0
    incremental_roas = influencer_roas - baseline_roas
    
    st.metric("📈 Incremental ROAS", f"{incremental_roas:.2f}")

# ---------- ROAS by Platform ----------
platform_roas = df_filtered.groupby('platform').apply(lambda x: x['revenue'].sum() / x['payout'].sum()).reset_index(name='ROAS')
fig1 = px.bar(platform_roas, x='platform', y='ROAS', title='ROAS by Platform', color='ROAS', text_auto='.2f')
st.plotly_chart(fig1, use_container_width=True)

# ---------- ROAS by Brand ----------
brand_roas = df_filtered.groupby('brand').apply(lambda x: x['revenue'].sum() / x['payout'].sum()).reset_index(name='ROAS')
fig2 = px.bar(brand_roas, x='brand', y='ROAS', title='ROAS by Brand', color='ROAS', text_auto='.2f')
st.plotly_chart(fig2, use_container_width=True)

# ---------- ROAS by Influencer ----------
influencer_roas = df_filtered.groupby('influencer').apply(lambda x: x['revenue'].sum() / x['payout'].sum()).reset_index(name='ROAS')
top_influencers = influencer_roas.sort_values(by='ROAS', ascending=False).head(10)
fig3 = px.bar(top_influencers, x='influencer', y='ROAS', title='Top 10 Influencers by ROAS', color='ROAS', text_auto='.2f')
st.plotly_chart(fig3, use_container_width=True)

# ---------- Scatter Plot: Revenue vs Reach ----------
fig4 = px.scatter(df_filtered, x='reach', y='revenue', title="Revenue vs Reach", trendline="ols", opacity=0.6)
st.plotly_chart(fig4, use_container_width=True)

# ---------- Bottom Influencers Table ----------
st.subheader("❌ Bottom 5 Influencers by ROAS")
bottom_influencers = influencer_roas.sort_values(by='ROAS').head(5)
st.dataframe(bottom_influencers)

# ---------- Payout Tracker ----------
st.subheader("💰 Influencer Payout Tracker")
payout_table = df_filtered[['influencer', 'platform', 'basis', 'rate', 'orders', 'payout']].drop_duplicates()
st.dataframe(payout_table)

# ---------- Export Data ----------
st.download_button(
    label="📥 Download Filtered Data (CSV)",
    data=df_filtered.to_csv(index=False),
    file_name="filtered_campaign_data.csv",
    mime="text/csv"
)

# ---------- Footer ----------
st.markdown("---")
st.markdown("🔧 Built by HealthKart Data Team | Powered by Streamlit & Plotly")
