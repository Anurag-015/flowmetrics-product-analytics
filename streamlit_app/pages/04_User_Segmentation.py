import streamlit as st
import pandas as pd
import plotly.express as px
from style import apply_custom_theme, modern_plotly_layout

st.set_page_config(page_title="User Segmentation | FlowMetrics", page_icon="👥", layout="wide")
apply_custom_theme()

st.markdown('<span class="badge">AUDIENCE ANALYSIS</span>', unsafe_allow_html=True)
st.title("Behavioral Engagement Segmentation")
st.caption("Classify users based on longitudinal activity thresholds to identify dormant risks and monetization candidates.")
st.markdown("<br>", unsafe_allow_html=True)

@st.cache_data
def load_segments():
    users = pd.read_csv("data/raw/users.csv")
    events = pd.read_csv("data/raw/events.csv")
    sessions = pd.read_csv("data/raw/sessions.csv")
    
    sess_count = sessions.groupby("user_id")["session_id"].nunique().rename("sessions_count")
    event_count = events[events["event_name"] != "signup_completed"].groupby("user_id")["event_id"].count().rename("events_count")
    
    df = users.merge(sess_count, on="user_id", how="left").merge(event_count, on="user_id", how="left").fillna(0)
    
    def classify(row):
        if row["events_count"] >= 30 and row["sessions_count"] >= 10:
            return "Highly Engaged"
        elif 10 <= row["events_count"] < 30:
            return "Moderately Engaged"
        elif 1 <= row["events_count"] < 10:
            return "Low Engagement"
        else:
            return "Dormant"
            
    df["segment"] = df.apply(classify, axis=1)
    return df

df_seg = load_segments()

# Metric summary cards
seg_summary = df_seg["segment"].value_counts()
k1, k2, k3, k4 = st.columns(4)
k1.metric("Highly Engaged", f"{seg_summary.get('Highly Engaged', 0):,}", delta="Power Users")
k2.metric("Moderately Engaged", f"{seg_summary.get('Moderately Engaged', 0):,}")
k3.metric("Low Engagement", f"{seg_summary.get('Low Engagement', 0):,}")
k4.metric("Dormant / Inactive", f"{seg_summary.get('Dormant', 0):,}", delta="-High Churn Risk", delta_color="inverse")

st.markdown("<br>", unsafe_allow_html=True)

c1, c2 = st.columns([5, 5])

with c1:
    st.subheader("User Distribution by Segment")
    seg_counts = df_seg["segment"].value_counts().reset_index()
    seg_counts.columns = ["Segment", "User Count"]
    
    fig_donut = px.pie(
        seg_counts, 
        names="Segment", 
        values="User Count", 
        hole=0.6,
        color="Segment",
        color_discrete_map={
            "Highly Engaged": "#10b981",
            "Moderately Engaged": "#6366f1",
            "Low Engagement": "#f59e0b",
            "Dormant": "#ef4444"
        }
    )
    modern_plotly_layout(fig_donut, height=380)
    fig_donut.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_donut, use_container_width=True)

with c2:
    st.subheader("Paid Conversion Rate by Segment")
    conv_by_seg = df_seg.groupby("segment")["is_paid"].mean().reset_index()
    conv_by_seg["Conversion Rate %"] = (conv_by_seg["is_paid"] * 100).round(2)
    
    fig_conv = px.bar(
        conv_by_seg, 
        x="segment", 
        y="Conversion Rate %", 
        color="segment",
        text="Conversion Rate %",
        color_discrete_map={
            "Highly Engaged": "#10b981",
            "Moderately Engaged": "#6366f1",
            "Low Engagement": "#f59e0b",
            "Dormant": "#ef4444"
        }
    )
    modern_plotly_layout(fig_conv, height=380)
    fig_conv.update_layout(showlegend=False)
    fig_conv.update_traces(texttemplate='%{text}%', textposition='outside')
    st.plotly_chart(fig_conv, use_container_width=True)

# Scatter plot correlation
st.markdown("<br>", unsafe_allow_html=True)
st.subheader("Session Volume vs. Event Intensity Correlation")
scatter_data = df_seg.assign(
    paid_status=df_seg["is_paid"].map({True: "Paid", False: "Free"})
)
fig_scatter = px.scatter(
    scatter_data,
    x="sessions_count",
    y="events_count",
    color="segment",
    symbol="paid_status",
    hover_data=["acquisition_channel", "company_size", "plan_type"],
    color_discrete_map={
        "Highly Engaged": "#10b981",
        "Moderately Engaged": "#6366f1",
        "Low Engagement": "#f59e0b",
        "Dormant": "#ef4444"
    },
    labels={"sessions_count": "Total Sessions", "events_count": "Total Events Triggered"}
)
modern_plotly_layout(fig_scatter, height=420)
st.plotly_chart(fig_scatter, use_container_width=True)