import streamlit as st
import pandas as pd
import plotly.express as px
from style import apply_custom_theme, modern_plotly_layout

st.set_page_config(page_title="Feature Adoption | FlowMetrics", page_icon="⚡", layout="wide")
apply_custom_theme()

st.markdown('<span class="badge">PRODUCT USAGE & ENGAGEMENT</span>', unsafe_allow_html=True)
st.title("Feature Adoption & Penetration")
st.caption("Evaluate engagement density across core modules and compare feature adoption across subscription tiers.")
st.markdown("<br>", unsafe_allow_html=True)

@st.cache_data
def load_data():
    events = pd.read_csv("data/raw/events.csv")
    users = pd.read_csv("data/raw/users.csv")
    features = pd.read_csv("data/raw/features.csv")
    return events, users, features

events, users, features = load_data()

# Clean feature mapping
feature_event_names = [
    "task_created", 
    "calendar_viewed", 
    "file_shared", 
    "report_exported", 
    "automation_created",
    "teammate_invited"
]

feature_events = events[events["event_name"].isin(feature_event_names)]
merged = pd.merge(feature_events, users[["user_id", "plan_type", "company_size"]], on="user_id")

# Top KPI highlights
col_m1, col_m2, col_m3, col_m4 = st.columns(4)
total_feature_hits = len(feature_events)
unique_engaged_users = feature_events["user_id"].nunique()
most_used_feature = feature_events["event_name"].value_counts().index[0].replace("_", " ").title()
avg_features_per_user = (feature_events.groupby("user_id")["event_name"].nunique()).mean()

col_m1.metric("Feature Interactions", f"{total_feature_hits:,}")
col_m2.metric("Engaged User Pool", f"{unique_engaged_users:,}", delta=f"{unique_engaged_users / len(users) * 100:.1f}% of users")
col_m3.metric("Top Feature by Volume", most_used_feature)
col_m4.metric("Avg Features / User", f"{avg_features_per_user:.2f}")

st.markdown("<br>", unsafe_allow_html=True)

# Main Visuals
c1, c2 = st.columns(2)

with c1:
    st.subheader("Total Interactions by Core Feature")
    freq = feature_events["event_name"].value_counts().reset_index()
    freq.columns = ["Feature Event", "Total Interactions"]
    freq["Clean Feature"] = freq["Feature Event"].str.replace("_", " ").str.title()
    
    fig_bar = px.bar(
        freq, 
        x="Clean Feature", 
        y="Total Interactions", 
        color="Clean Feature",
        color_discrete_sequence=["#6366f1", "#3b82f6", "#06b6d4", "#10b981", "#f59e0b", "#ec4899"],
        text_auto=True
    )
    modern_plotly_layout(fig_bar, height=380)
    fig_bar.update_layout(showlegend=False)
    st.plotly_chart(fig_bar, use_container_width=True)

with c2:
    st.subheader("Feature Adoption by Subscription Plan")
    plan_usage = merged.groupby(["event_name", "plan_type"])["user_id"].nunique().reset_index()
    plan_usage.columns = ["Feature", "Plan", "Unique Users"]
    plan_usage["Feature"] = plan_usage["Feature"].str.replace("_", " ").str.title()
    
    fig_plan = px.bar(
        plan_usage, 
        x="Feature", 
        y="Unique Users", 
        color="Plan", 
        barmode="group",
        color_discrete_sequence=["#94a3b8", "#6366f1", "#10b981"]
    )
    modern_plotly_layout(fig_plan, height=380)
    st.plotly_chart(fig_plan, use_container_width=True)

# Detailed data table
with st.expander("🔍 View Raw Feature Adoption Metric Table"):
    table_df = feature_events.groupby("event_name").agg(
        Total_Events=("event_id", "count"),
        Unique_Users=("user_id", "nunique")
    ).reset_index()
    table_df["Adoption_Rate_%"] = (table_df["Unique_Users"] / len(users) * 100).round(2)
    table_df.columns = ["Event Name", "Total Event Volume", "Unique Adopters", "Total Adoption %"]
    st.dataframe(table_df.sort_values(by="Unique Adopters", ascending=False), use_container_width=True)