import streamlit as st
import pandas as pd
import plotly.express as px
from style import apply_custom_theme, modern_plotly_layout

st.set_page_config(page_title="Cohort Retention | FlowMetrics", page_icon="🔄", layout="wide")
apply_custom_theme()

st.markdown('<span class="badge">RETENTION & STICKINESS</span>', unsafe_allow_html=True)
st.title("Cohort Retention Matrix")
st.caption("Tracks the percentage of weekly signup cohorts returning to perform core activities.")
st.markdown("<br>", unsafe_allow_html=True)

@st.cache_data
def load_cohort_data():
    users = pd.read_csv("data/raw/users.csv")
    events = pd.read_csv("data/raw/events.csv")

    # Define cohort by signup calendar week
    users["cohort_week"] = pd.to_datetime(users["signup_date"]).dt.to_period("W").astype(str)
    events["event_date"] = pd.to_datetime(events["event_timestamp"])

    merged = pd.merge(
        events[events["event_name"] != "signup_completed"],
        users[["user_id", "cohort_week", "signup_date"]],
        on="user_id"
    )

    merged["signup_date"] = pd.to_datetime(merged["signup_date"])
    merged["days_diff"] = (
        merged["event_date"].dt.normalize() - merged["signup_date"].dt.normalize()
    ).dt.days
    merged["weeks_diff"] = merged["days_diff"] // 7

    cohort_sizes = users.groupby("cohort_week")["user_id"].nunique()
    
    # Calculate active user matrix
    matrix = merged.groupby(["cohort_week", "weeks_diff"])["user_id"].nunique().unstack()

    # Reindex to guarantee all columns from Week 0 to Week 6 exist without KeyErrors
    all_weeks = list(range(7))
    matrix = matrix.reindex(columns=all_weeks, fill_value=0)

    # Compute percentage retention relative to starting cohort size
    matrix_pct = matrix.divide(cohort_sizes, axis=0) * 100
    matrix_pct.columns = [f"Week {col}" for col in all_weeks]

    # Select the earliest mature cohorts that have full historical runways
    matrix_pct = matrix_pct.head(14)
    return matrix_pct

matrix_pct = load_cohort_data()

fig_heat = px.imshow(
    matrix_pct,
    text_auto=".1f",
    color_continuous_scale="Viridis",
    aspect="auto",
    labels=dict(x="Weeks Elapsed", y="Signup Cohort", color="Retention %")
)

modern_plotly_layout(fig_heat, height=520)
st.plotly_chart(fig_heat, use_container_width=True)