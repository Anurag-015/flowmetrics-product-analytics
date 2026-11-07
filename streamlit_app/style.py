import streamlit as st


# ============================================================
# FLOWMETRICS — PREMIUM SAAS DASHBOARD THEME
# ============================================================

def apply_custom_theme():
    """
    Applies a polished, modern SaaS analytics theme to Streamlit.
    Includes smooth transitions, refined metric cards, sidebar styling,
    typography, buttons, expanders, and responsive layout adjustments.
    """

    st.markdown(
        """
        <style>
        /* =====================================================
           1. DESIGN SYSTEM
        ===================================================== */

        @import url(
            'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap'
        );

        :root {
            --fm-primary: var(--st-primary-color);
            --fm-primary-dark: var(--st-primary-color);

            --fm-success: #10B981;
            --fm-warning: #F59E0B;
            --fm-danger: #EF4444;
            --fm-cyan: #06B6D4;

            --fm-text: var(--st-text-color);
            --fm-muted: var(--st-gray-color);
            --fm-border: var(--st-border-color);
            --fm-surface: var(--st-secondary-background-color);
            --fm-background: var(--st-background-color);

            --fm-radius: 16px;
            --fm-radius-small: 10px;

            --fm-transition:
                all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
        }

        /* =====================================================
           2. GLOBAL TYPOGRAPHY & BACKGROUND
        ===================================================== */

        html,
        body,
        [class*="css"],
        [data-testid="stApp"] {
            font-family: 'Inter', sans-serif !important;
        }

        .stApp {
            background: var(--fm-background);
        }

        h1 {
            font-size: 2.15rem !important;
            font-weight: 800 !important;
            letter-spacing: -0.045em !important;
            color: var(--fm-text) !important;
        }

        h2 {
            font-size: 1.55rem !important;
            font-weight: 700 !important;
            letter-spacing: -0.025em !important;
            color: var(--fm-text) !important;
        }

        h3 {
            font-size: 1.15rem !important;
            font-weight: 700 !important;
            color: var(--fm-text) !important;
        }

        p,
        label {
            color: var(--fm-muted);
        }

        /* =====================================================
           3. MAIN CONTENT
        ===================================================== */

        section[data-testid="stMain"] > div {
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        [data-testid="stVerticalBlock"] {
            gap: 1rem;
        }

        /* =====================================================
           4. KPI METRIC CARDS
        ===================================================== */

        div[data-testid="stMetric"] {
            position: relative;
            overflow: hidden;

            background: var(--fm-surface);
            border: 1px solid var(--fm-border);
            border-radius: var(--fm-radius);

            padding: 22px 24px;

            box-shadow:
                0 2px 8px rgba(15, 23, 42, 0.025),
                0 1px 2px rgba(15, 23, 42, 0.02);

            transition: var(--fm-transition);
        }

        div[data-testid="stMetric"]:hover {
            transform: translateY(-4px);

            border-color: rgba(99, 102, 241, 0.35);

            box-shadow:
                0 12px 28px rgba(99, 102, 241, 0.08),
                0 4px 10px rgba(15, 23, 42, 0.04);
        }

        div[data-testid="stMetric"]::before {
            content: "";
            position: absolute;

            top: 0;
            left: 0;

            width: 100%;
            height: 3px;

            background: linear-gradient(
                90deg,
                var(--fm-primary),
                var(--fm-cyan)
            );

            opacity: 0;
            transition: opacity 0.25s ease;
        }

        div[data-testid="stMetric"]:hover::before {
            opacity: 1;
        }

        div[data-testid="stMetricLabel"] p {
            color: var(--fm-muted) !important;

            font-size: 0.78rem !important;
            font-weight: 600 !important;

            letter-spacing: 0.045em !important;
            text-transform: uppercase !important;

            margin-bottom: 8px !important;
        }

        div[data-testid="stMetricValue"] {
            color: var(--fm-text) !important;
        }

        div[data-testid="stMetricValue"] div {
            font-size: 1.85rem !important;
            font-weight: 800 !important;

            letter-spacing: -0.045em !important;
            line-height: 1.2 !important;
        }

        div[data-testid="stMetricDelta"] {
            font-size: 0.8rem !important;
            font-weight: 600 !important;
        }

        /* =====================================================
           5. CUSTOM METRIC / CONTENT CARDS
        ===================================================== */

        .metric-card {
            background: var(--fm-surface);

            border: 1px solid var(--fm-border);
            border-radius: var(--fm-radius);

            padding: 24px;
            margin-bottom: 18px;

            box-shadow:
                0 2px 8px rgba(15, 23, 42, 0.025);

            transition: var(--fm-transition);
        }

        .metric-card:hover {
            transform: translateY(-3px);

            border-color: rgba(99, 102, 241, 0.25);

            box-shadow:
                0 10px 24px rgba(15, 23, 42, 0.05);
        }

        /* =====================================================
           6. HEADER BADGES
        ===================================================== */

        .badge {
            display: inline-flex;
            align-items: center;

            padding: 6px 12px;

            font-size: 0.70rem;
            font-weight: 700;

            letter-spacing: 0.08em;
            text-transform: uppercase;

            border-radius: 999px;

            background: var(--fm-surface);
            color: var(--fm-primary-dark);

            border: 1px solid rgba(99, 102, 241, 0.12);

            margin-bottom: 10px;
        }

        /* =====================================================
           7. SIDEBAR
        ===================================================== */

        section[data-testid="stSidebar"] {
            background: var(--fm-background);

            border-right: 1px solid var(--fm-border);
        }

        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3 {
            color: var(--fm-text) !important;
        }

        section[data-testid="stSidebar"] label {
            font-weight: 500;
            color: var(--fm-muted) !important;
        }

        section[data-testid="stSidebar"] [data-testid="stMarkdown"] {
            transition: var(--fm-transition);
        }

        /* =====================================================
           8. BUTTONS
        ===================================================== */

        div.stButton > button {
            border-radius: var(--fm-radius-small);

            border: 1px solid var(--fm-border);

            font-weight: 600;

            transition: var(--fm-transition);
        }

        div.stButton > button:hover {
            transform: translateY(-2px);

            border-color: var(--fm-primary);

            box-shadow:
                0 5px 14px rgba(99, 102, 241, 0.10);
        }

        div.stButton > button:active {
            transform: scale(0.98);
        }

        /* =====================================================
           9. INPUTS & FILTERS
        ===================================================== */

        div[data-baseweb="select"] > div,
        div[data-baseweb="input"] > div,
        div[data-baseweb="textarea"] > div {
            border-radius: var(--fm-radius-small);

            border-color: var(--fm-border);

            transition: var(--fm-transition);
        }

        div[data-baseweb="select"] > div:focus-within,
        div[data-baseweb="input"] > div:focus-within,
        div[data-baseweb="textarea"] > div:focus-within {
            border-color: var(--fm-primary);

            box-shadow:
                0 0 0 2px rgba(99, 102, 241, 0.10);
        }

        /* =====================================================
           10. EXPANDERS
        ===================================================== */

        [data-testid="stExpander"] {
            background: var(--fm-surface);

            border: 1px solid var(--fm-border);
            border-radius: var(--fm-radius-small);

            transition: var(--fm-transition);
        }

        [data-testid="stExpander"]:hover {
            border-color: rgba(99, 102, 241, 0.25);
        }

        [data-testid="stExpander"] summary {
            font-weight: 600;
        }

        /* =====================================================
           11. DATAFRAMES
        ===================================================== */

        [data-testid="stDataFrame"] {
            border: 1px solid var(--fm-border);
            border-radius: var(--fm-radius-small);

            overflow: hidden;
        }

        /* =====================================================
           12. PROGRESS BARS
        ===================================================== */

        div[data-testid="stProgress"] > div > div {
            background-color: var(--fm-primary);
            border-radius: 999px;
        }

        div[data-testid="stProgress"] {
            border-radius: 999px;
        }

        /* =====================================================
           13. DIVIDERS
        ===================================================== */

        hr {
            border-color: var(--fm-border) !important;
            margin-top: 1.5rem !important;
            margin-bottom: 1.5rem !important;
        }

        /* =====================================================
           14. RESPONSIVE DESIGN
        ===================================================== */

        @media (max-width: 768px) {
            h1 {
                font-size: 1.65rem !important;
            }

            div[data-testid="stMetric"] {
                padding: 16px;
            }

            div[data-testid="stMetricValue"] div {
                font-size: 1.45rem !important;
            }
        }

        /* =====================================================
           15. ACCESSIBILITY — REDUCED MOTION
        ===================================================== */

        @media (prefers-reduced-motion: reduce) {
            *,
            *::before,
            *::after {
                transition-duration: 0.01ms !important;
                animation-duration: 0.01ms !important;
                animation-iteration-count: 1 !important;
                scroll-behavior: auto !important;
            }
        }

        </style>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# PLOTLY — FLOWMETRICS CHART THEME
# ============================================================

def modern_plotly_layout(fig, height=380):
    """
    Applies a consistent premium analytics theme to Plotly figures.

    Compatible with:
    - Bar charts
    - Line charts
    - Funnel charts
    - Pie and donut charts
    - Heatmaps
    - Scatter plots
    """

    is_dark = st.context.theme.type == "dark"
    text_color = "#CBD5E1" if is_dark else "#64748B"
    title_color = "#F1F5F9" if is_dark else "#0F172A"
    secondary_text_color = "#94A3B8" if is_dark else "#475569"
    hover_background = "#151E30" if is_dark else "#FFFFFF"
    hover_border = "#334155" if is_dark else "#E2E8F0"
    grid_color = "rgba(148, 163, 184, 0.22)" if is_dark else "rgba(148, 163, 184, 0.16)"

    fig.update_layout(
        height=height,

        margin=dict(
            l=20,
            r=20,
            t=45,
            b=20
        ),

        font=dict(
            family="Inter, sans-serif",
            size=12,
            color=text_color
        ),

        title=dict(
            font=dict(
                family="Inter, sans-serif",
                size=16,
                color=title_color
            ),
            x=0.02,
            xanchor="left"
        ),

        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",

        hoverlabel=dict(
            bgcolor=hover_background,
            bordercolor=hover_border,
            font=dict(
                family="Inter, sans-serif",
                size=12,
                color=title_color
            ),
            namelength=-1
        ),

        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            title=None,
            font=dict(
                size=11,
                color=text_color
            )
        ),

        xaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=False,
            tickfont=dict(
                size=11,
                color=text_color
            ),
            title_font=dict(
                size=12,
                color=secondary_text_color
            )
        ),

        yaxis=dict(
            showgrid=True,
            gridcolor=grid_color,
            zeroline=False,
            showline=False,
            tickfont=dict(
                size=11,
                color=text_color
            ),
            title_font=dict(
                size=12,
                color=secondary_text_color
            )
        ),

        hovermode="closest",

        transition=dict(
            duration=350,
            easing="cubic-in-out"
        )
    )

    return fig