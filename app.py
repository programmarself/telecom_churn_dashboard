import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Page config
st.set_page_config(page_title="Telecom Churn Dashboard", layout="wide")

# Title
st.title("📊 Telecom Customer Churn Dashboard")

# Load data
@st.cache_data
def load_data():
    df = pd.read_excel("telecom_churn_mock_data.xlsx")
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors='coerce')
    df.dropna(inplace=True)
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("Filters")
contract_type = st.sidebar.multiselect("Contract Type", options=df['Contract'].unique(), default=df['Contract'].unique())
internet_service = st.sidebar.multiselect("Internet Service", options=df['InternetService'].unique(), default=df['InternetService'].unique())

# Filtered data
filtered_df = df[df['Contract'].isin(contract_type) & df['InternetService'].isin(internet_service)]

# Metrics
st.markdown("### 📌 Key Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Total Customers", len(filtered_df))
col2.metric("Churned Customers", filtered_df['Churn'].value_counts().get('Yes', 0))
churn_rate = round(filtered_df['Churn'].value_counts(normalize=True).get('Yes', 0)*100, 2)
col3.metric("Churn Rate (%)", f"{churn_rate}%")

# Charts Section
st.markdown("### 📈 Visual Insights")

tab1, tab2, tab3 = st.tabs(["Churn by Contract", "Tenure vs Charges", "Heatmap"])

with tab1:
    fig, ax = plt.subplots()
    sns.countplot(data=filtered_df, x='Contract', hue='Churn', ax=ax)
    ax.set_title("Churn by Contract Type")
    st.pyplot(fig)

with tab2:
    fig, ax = plt.subplots()
    sns.scatterplot(data=filtered_df, x='tenure', y='MonthlyCharges', hue='Churn', ax=ax)
    ax.set_title("Monthly Charges vs Tenure")
    st.pyplot(fig)

with tab3:
    fig, ax = plt.subplots()
    corr = filtered_df[['tenure', 'MonthlyCharges', 'TotalCharges']].corr()
    sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
    ax.set_title("Correlation Heatmap")
    st.pyplot(fig)

# Footer
st.markdown("---")
st.markdown("Developed by **Irfan Ullah Khan** | [GitHub](https://github.com/)")
