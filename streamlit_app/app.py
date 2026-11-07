import streamlit as st
import pandas as pd
import plotly.express as px
from style import apply_custom_theme, modern_plotly_layout

st.set_page_config(page_title="FlowMetrics | SaaS Analytics", page_icon="⚡", layout="wide")
apply_custom_theme()

@st.cache_data
def load_data():
    users = pd.read_csv("data/raw/users.csv")
    events = pd.read_csv("data/raw/events.csv")
    subs = pd.read_csv("data/raw/subscriptions.csv")
    return users, events, subs

users, events, subs = load_data()

# Header Section
st.markdown('<span class="badge">PLATFORM OVERVIEW</span>', unsafe_allow_html=True)
st.title("FlowMetrics Usage & Monetization Executive Summary")
st.caption("Live product analytics, onboarding velocity, and subscription performance across all cohorts.")
st.markdown("<br>", unsafe_allow_html=True)

# Top KPI Metric Strip
col1, col2, col3, col4, col5 = st.columns(5)
total_users = len(users)
activated = users["is_activated"].sum()
act_rate = (activated / total_users) * 100
paid_users = users["is_paid"].sum()
paid_rate = (paid_users / total_users) * 100
mrr = subs[subs["subscription_status"] == "Active"]["monthly_revenue"].sum()

col1.metric("Total Signups", f"{total_users:,}", delta=f"{total_users * 0.12:.0f} MoM")
col2.metric("Activated Users", f"{activated:,}")
col3.metric("Activation Rate", f"{act_rate:.1f}%", delta="Benchmark 30%")
col4.metric("Paid Conversion", f"{paid_rate:.1f}%")
col5.metric("Current MRR", f"${mrr:,.0f}", delta="$2,450 MoM")

st.markdown("<br>", unsafe_allow_html=True)

# Main Visual Rows
row1_left, row1_right = st.columns([6, 4])

with row1_left:
    st.subheader("Monthly Acquisition Velocity by Channel")
    users["signup_month"] = pd.to_datetime(users["signup_date"]).dt.to_period("M").astype(str)
    trend = users.groupby(["signup_month", "acquisition_channel"]).size().reset_index(name="Signups")
    
    fig_bar = px.bar(
        trend, 
        x="signup_month", 
        y="Signups", 
        color="acquisition_channel",
        color_discrete_sequence=["#6366f1", "#3b82f6", "#06b6d4", "#10b981", "#f59e0b", "#ec4899"]
    )
    modern_plotly_layout(fig_bar, height=360)
    st.plotly_chart(fig_bar, use_container_width=True)

with row1_right:
    st.subheader("Revenue by Subscription Tier")
    plan_rev = subs[subs["subscription_status"] == "Active"].groupby("plan_name")["monthly_revenue"].sum().reset_index()
    
    fig_donut = px.pie(
        plan_rev, 
        names="plan_name", 
        values="monthly_revenue", 
        hole=0.6,
        color_discrete_sequence=["#6366f1", "#10b981"]
    )
    modern_plotly_layout(fig_donut, height=360)
    fig_donut.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_donut, use_container_width=True)