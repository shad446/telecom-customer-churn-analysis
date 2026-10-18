
import glob
import pandas as pd
import streamlit as st
import plotly.express as px

# ---------------- PAGE CONFIGURATION ----------------
st.set_page_config(
    page_title="Telecom Churn | Executive Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- LUXURY COLOR PALETTE ----------------
BG = "#151A20"
CARD = "#202830"
GOLD = "#D6B875"
TEAL = "#78A6A3"
IVORY = "#F4F0E6"
MUTED = "#A9B3BD"

# ---------------- PROFESSIONAL STYLING ----------------
st.markdown(f"""
<style>
.stApp {{
    background-color: {BG};
    color: {IVORY};
}}
[data-testid="stSidebar"] {{
    background-color: #1C232B;
}}
h1, h2, h3, p, label {{
    color: {IVORY};
}}
[data-testid="stMetric"] {{
    background-color: {CARD};
    border: 1px solid #37414A;
    padding: 20px;
    border-radius: 14px;
}}
[data-testid="stMetricLabel"] {{
    color: {MUTED};
}}
[data-testid="stMetricValue"] {{
    color: {GOLD};
}}
div[data-testid="stPlotlyChart"] {{
    background-color: {CARD};
    border-radius: 14px;
    padding: 8px;
}}
hr {{
    border-color: #37414A;
}}
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    files = glob.glob("*.csv")

    for file in files:
        try:
            data = pd.read_csv(file)
            data.columns = data.columns.str.strip()

            required = {
                "Churn", "customerID", "tenure",
                "MonthlyCharges", "Contract",
                "InternetService", "PaymentMethod"
            }

            if required.issubset(data.columns):
                data["MonthlyCharges"] = pd.to_numeric(
                    data["MonthlyCharges"], errors="coerce"
                )
                data["tenure"] = pd.to_numeric(
                    data["tenure"], errors="coerce"
                )
                return data, file

        except Exception:
            continue

    return None, None


df, filename = load_data()

if df is None:
    st.error(
        "Telecom dataset not found. Place your telecom CSV "
        "file in the same folder as dashboard.py."
    )
    st.info(
        "The CSV must contain customerID, Churn, tenure, "
        "MonthlyCharges, Contract, InternetService and PaymentMethod."
    )
    st.stop()

# ---------------- HEADER ----------------
st.markdown(
    f"<p style='color:{GOLD}; letter-spacing:3px;'>"
    "CUSTOMER INTELLIGENCE  /  TELECOMMUNICATIONS"
    "</p>",
    unsafe_allow_html=True
)

st.title("Telecom Churn Analytics")
st.markdown(
    "Executive dashboard for customer retention, "
    "service performance and revenue insights."
)

st.caption(f"Data source: {filename}  |  "
           f"Records loaded: {len(df):,}")

# ---------------- SIDEBAR FILTERS ----------------
st.sidebar.title("Dashboard Controls")
st.sidebar.caption("Refine the customer analysis")

contract_options = sorted(
    df["Contract"].dropna().unique().tolist()
)
internet_options = sorted(
    df["InternetService"].dropna().unique().tolist()
)
payment_options = sorted(
    df["PaymentMethod"].dropna().unique().tolist()
)

selected_contract = st.sidebar.multiselect(
    "Contract Type",
    contract_options,
    default=contract_options
)

selected_internet = st.sidebar.multiselect(
    "Internet Service",
    internet_options,
    default=internet_options
)

selected_payment = st.sidebar.multiselect(
    "Payment Method",
    payment_options,
    default=payment_options
)

# ---------------- FILTER DATA ----------------
filtered = df[
    df["Contract"].isin(selected_contract)
    & df["InternetService"].isin(selected_internet)
    & df["PaymentMethod"].isin(selected_payment)
].copy()

if filtered.empty:
    st.warning("No customers match these filters.")
    st.stop()

# ---------------- PREPARE METRICS ----------------
churned = filtered["Churn"].eq("Yes").sum()
total_customers = len(filtered)
churn_rate = churned / total_customers * 100
avg_charges = filtered["MonthlyCharges"].mean()

st.markdown("### Executive Overview")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Customers", f"{total_customers:,}")
c2.metric("Churned Customers", f"{churned:,}")
c3.metric("Churn Rate", f"{churn_rate:.1f}%")
c4.metric(
    "Avg. Monthly Charges",
    f"${avg_charges:,.2f}" if pd.notna(avg_charges) else "N/A"
)

st.caption(
    "Churn rate = customers marked Churn = Yes "
    "divided by all customers in the filtered data."
)

st.divider()

# ---------------- CHART THEME ----------------
def style_chart(fig):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor=CARD,
        plot_bgcolor=CARD,
        font=dict(color=IVORY, family="Arial"),
        title_font=dict(size=18, color=GOLD),
        margin=dict(l=20, r=20, t=65, b=35),
        legend_title_text="Customer Status"
    )
    return fig

# ---------------- CHURN BY CONTRACT ----------------
st.markdown("### Customer Retention Analysis")

left, right = st.columns(2)

contract_data = (
    filtered.groupby("Contract", observed=False)["Churn"]
    .apply(lambda s: s.eq("Yes").mean() * 100)
    .reset_index(name="Churn Rate")
    .sort_values("Churn Rate", ascending=False)
)

with left:
    fig = px.bar(
        contract_data,
        x="Contract",
        y="Churn Rate",
        color="Contract",
        text=contract_data["Churn Rate"].map(
            lambda v: f"{v:.1f}%"
        ),
        color_discrete_sequence=[GOLD, TEAL, "#9BA9BC"],
        title="Churn Rate by Contract"
    )
    fig.update_traces(textposition="outside")
    fig.update_yaxes(title="Churn Rate (%)", range=[0, 110])
    fig.update_xaxes(title="")
    fig.update_layout(showlegend=False)
    st.plotly_chart(style_chart(fig), use_container_width=True)

# ---------------- CHURN BY PAYMENT ----------------
payment_data = (
    filtered.groupby("PaymentMethod", observed=False)["Churn"]
    .apply(lambda s: s.eq("Yes").mean() * 100)
    .reset_index(name="Churn Rate")
    .sort_values("Churn Rate", ascending=True)
)

with right:
    fig = px.bar(
        payment_data,
        x="Churn Rate",
        y="PaymentMethod",
        orientation="h",
        text=payment_data["Churn Rate"].map(
            lambda v: f"{v:.1f}%"
        ),
        color="Churn Rate",
        color_continuous_scale=["#78A6A3", "#D6B875"],
        title="Churn Rate by Payment Method"
    )
    fig.update_traces(textposition="outside")
    fig.update_xaxes(title="Churn Rate (%)", range=[0, 110])
    fig.update_yaxes(title="")
    fig.update_layout(coloraxis_showscale=False)
    st.plotly_chart(style_chart(fig), use_container_width=True)

# ---------------- TENURE DISTRIBUTION ----------------
st.markdown("### Customer Behaviour")

left, right = st.columns(2)

with left:
    fig = px.histogram(
        filtered,
        x="tenure",
        color="Churn",
        nbins=24,
        barmode="overlay",
        opacity=0.85,
        color_discrete_map={
            "Yes": GOLD,
            "No": TEAL
        },
        title="Customer Tenure Distribution"
    )
    fig.update_xaxes(title="Tenure (months)")
    fig.update_yaxes(title="Number of Customers")
    st.plotly_chart(style_chart(fig), use_container_width=True)

# ---------------- MONTHLY CHARGES ----------------
with right:
    fig = px.box(
        filtered,
        x="Churn",
        y="MonthlyCharges",
        color="Churn",
        points=False,
        color_discrete_map={
            "Yes": GOLD,
            "No": TEAL
        },
        title="Monthly Charges: Churned vs Retained"
    )
    fig.update_xaxes(
        title="Churn Status",
        tickvals=["Yes", "No"],
        ticktext=["Churned", "Retained"]
    )
    fig.update_yaxes(title="Monthly Charges ($)")
    st.plotly_chart(style_chart(fig), use_container_width=True)

# ---------------- INTERNET SERVICE INSIGHTS ----------------
st.markdown("### Internet Service Performance")

internet_data = (
    filtered.groupby("InternetService", observed=False)["Churn"]
    .apply(lambda s: s.eq("Yes").mean() * 100)
    .reset_index(name="Churn Rate")
    .sort_values("Churn Rate", ascending=False)
)

fig = px.bar(
    internet_data,
    x="InternetService",
    y="Churn Rate",
    text=internet_data["Churn Rate"].map(
        lambda v: f"{v:.1f}%"
    ),
    color="InternetService",
    color_discrete_sequence=[GOLD, TEAL, "#9BA9BC"],
    title="Churn Rate Across Internet Services"
)
fig.update_traces(textposition="outside")
fig.update_yaxes(title="Churn Rate (%)", range=[0, 110])
fig.update_xaxes(title="Internet Service")
fig.update_layout(showlegend=False)
st.plotly_chart(style_chart(fig), use_container_width=True)

# ---------------- AUTOMATED BUSINESS INSIGHTS ----------------
st.markdown("### Business Insights & Recommendations")

if not contract_data.empty:
    high_contract = contract_data.iloc[0]
    st.markdown(
        f"**Contract insight:** {high_contract['Contract']} "
        f"has the highest observed churn rate "
        f"({high_contract['Churn Rate']:.1f}%) among the "
        "selected contract types. Consider testing retention "
        "offers for this group."
    )

if not payment_data.empty:
    high_payment = payment_data.iloc[-1]
    st.markdown(
        f"**Payment insight:** {high_payment['PaymentMethod']} "
        f"has the highest observed churn rate "
        f"({high_payment['Churn Rate']:.1f}%) among the "
        "selected payment methods. Investigate payment "
        "friction and customer feedback."
    )

if not internet_data.empty:
    high_internet = internet_data.iloc[0]
    st.markdown(
        f"**Service insight:** {high_internet['InternetService']} "
        f"has the highest observed churn rate "
        f"({high_internet['Churn Rate']:.1f}%) among the "
        "selected internet services. Review service quality "
        "and customer satisfaction."
    )

st.info(
    "These are observed associations, not proof of cause. "
    "Validate the findings with customer feedback and further analysis."
)

# ---------------- CUSTOMER DATA TABLE ----------------
with st.expander("Explore Customer Records"):
    display_columns = [
        col for col in [
            "customerID", "gender", "tenure", "Contract",
            "InternetService", "PaymentMethod",
            "MonthlyCharges", "Churn"
        ] if col in filtered.columns
    ]

    st.dataframe(
        filtered[display_columns],
        use_container_width=True,
        hide_index=True
    )

st.divider()
st.caption(
    "TELECOM CUSTOMER INTELLIGENCE  |  "
    "Built with Python, Streamlit and Plotly"
)
