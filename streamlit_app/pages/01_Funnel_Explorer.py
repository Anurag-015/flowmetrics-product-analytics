import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from style import apply_custom_theme, modern_plotly_layout

st.set_page_config(page_title="Funnel Explorer | FlowMetrics", page_icon="🔻", layout="wide")
apply_custom_theme()

st.markdown('<span class="badge">CONVERSION ENGINE</span>', unsafe_allow_html=True)
st.title("Sequential Onboarding Funnel Explorer")
st.caption("Identify user drop-off points from initial signup down to paying customer.")
st.markdown("<br>", unsafe_allow_html=True)

users = pd.read_csv("data/raw/users.csv")
events = pd.read_csv("data/raw/events.csv")

# Clean horizontal filter bar
with st.sidebar:
    st.header("Funnel Slicers")
    selected_channels = st.multiselect(
        "Acquisition Channels", 
        options=users["acquisition_channel"].unique(), 
        default=users["acquisition_channel"].unique()
    )
    selected_sizes = st.multiselect(
        "Company Size", 
        options=users["company_size"].unique(), 
        default=users["company_size"].unique()
    )

filtered_users = users[
    (users["acquisition_channel"].isin(selected_channels)) & 
    (users["company_size"].isin(selected_sizes))
]
filtered_uids = set(filtered_users["user_id"])
filtered_events = events[events["user_id"].isin(filtered_uids)]

stages = [
    ("1. Signup Completed", len(filtered_users)),
    ("2. Workspace Created", filtered_events[filtered_events["event_name"] == "workspace_created"]["user_id"].nunique()),
    ("3. Project Created", filtered_events[filtered_events["event_name"] == "project_created"]["user_id"].nunique()),
    ("4. Task Created", filtered_events[filtered_events["event_name"] == "task_created"]["user_id"].nunique()),
    ("5. Teammate Invited", filtered_events[filtered_events["event_name"] == "teammate_invited"]["user_id"].nunique()),
    ("6. Paid Subscription", filtered_users["is_paid"].sum())
]

df_funnel = pd.DataFrame(stages, columns=["Stage", "Users"])

col1, col2 = st.columns([7, 3])

with col1:
    fig_funnel = go.Figure(go.Funnel(
        y=df_funnel["Stage"],
        x=df_funnel["Users"],
        textinfo="value+percent previous+percent initial",
        marker=dict(color=["#4f46e5", "#6366f1", "#818cf8", "#a5b4fc", "#c7d2fe", "#10b981"])
    ))
    modern_plotly_layout(fig_funnel, height=450)
    st.plotly_chart(fig_funnel, use_container_width=True)

with col2:
    st.subheader("Stage Breakdown")
    for i in range(1, len(stages)):
        prev_cnt = stages[i-1][1]
        curr_cnt = stages[i][1]
        pct = (curr_cnt / prev_cnt * 100) if prev_cnt > 0 else 0
        drop_pct = 100 - pct
        
        st.markdown(f"""
        **{stages[i][0]}**  
        Conversion: `{pct:.1f}%` &nbsp;|&nbsp; Drop-off: <span style="color:#ef4444; font-weight:600;">-{drop_pct:.1f}%</span>
        """, unsafe_allow_html=True)
        st.progress(pct / 100)