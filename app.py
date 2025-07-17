import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Set up Streamlit page config
st.set_page_config(page_title="Telecom Churn Dashboard", layout="wide")

# Load data
@st.cache_data
def load_data():
    df = pd.read_excel("telecom_churn_mock_data.xlsx")
    df.columns = df.columns.str.strip().str.replace(" ", "").str.title()  # Normalize columns
    return df

df = load_data()

# Title
st.title("📊 Telecom Churn Dashboard")

# Show data preview
with st.expander("Preview Dataset"):
    st.dataframe(df)

# Filters
st.sidebar.header("Filter Data")
selected_gender = st.sidebar.multiselect("Select Gender", options=df["Gender"].unique(), default=df["Gender"].unique())
selected_contract = st.sidebar.multiselect("Select Contract Type", options=df["Contract"].unique(), default=df["Contract"].unique())
selected_churn = st.sidebar.multiselect("Churned?", options=df["Churn"].unique(), default=df["Churn"].unique())

# Apply filters
filtered_df = df[
    (df["Gender"].isin(selected_gender)) &
    (df["Contract"].isin(selected_contract)) &
    (df["Churn"].isin(selected_churn))
]

# Column layout
col1, col2 = st.columns(2)

# Bar chart - Contract distribution
with col1:
    st.subheader("📦 Contract Type Distribution")
    contract_counts = filtered_df["Contract"].value_counts()
    st.bar_chart(contract_counts)

# Pie chart - Churn Distribution
with col2:
    st.subheader("⚠️ Churn Rate")
    churn_counts = filtered_df["Churn"].value_counts()
    fig1, ax1 = plt.subplots()
    ax1.pie(churn_counts, labels=churn_counts.index, autopct='%1.1f%%', startangle=90)
    ax1.axis("equal")
    st.pyplot(fig1)

# Scatter plot
st.subheader("📈 Monthly Charges vs Tenure")
fig2, ax2 = plt.subplots()
sns.scatterplot(data=filtered_df, x="Tenure", y="Monthlycharges", hue="Churn", ax=ax2)
st.pyplot(fig2)

# Metrics
st.subheader("📌 Key Metrics")
col3, col4, col5 = st.columns(3)
col3.metric("Total Customers", len(filtered_df))
col4.metric("Churned", filtered_df["Churn"].value_counts().get("Yes", 0))
col5.metric("Average Charges", f"${filtered_df['Monthlycharges'].mean():.2f}")
