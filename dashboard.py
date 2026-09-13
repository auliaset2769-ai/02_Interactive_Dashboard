import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration
st.set_page_config(page_title="Big Mart Sales Dashboard", layout="wide")
st.title("🏬 Big Mart Sales Prediction Explorer")
st.markdown("Interact with the controls on the left to analyze how **Item_MRP** impacts total outlet sales.")

# 2. Mock Data Generation (Replace with: pd.read_csv('Train.csv'))
@st.cache_data
def load_data():
    # Simulated structure of the Big Mart dataset
    data = {
        'Item_Identifier': [f'FDA{i}' for i in range(100)],
        'Item_MRP': [40, 120, 185, 240, 90, 150, 210, 60, 175, 260] * 10,
        'Item_Outlet_Sales': [200, 1500, 3200, 4800, 900, 2200, 3900, 500, 2900, 5500] * 10,
        'Outlet_Location_Type': ['Tier 1', 'Tier 2', 'Tier 3', 'Tier 1', 'Tier 2'] * 20,
        'Item_Type': ['Dairy', 'Soft Drinks', 'Meat', 'Fruits', 'Baking Goods'] * 20
    }
    return pd.DataFrame(data)

df = load_data()

# 3. Sidebar Interactive Controls
st.sidebar.header("🎛️ Dashboard Filters")

# Filter A: Outlet Tier
location_types = df['Outlet_Location_Type'].unique()
selected_tiers = st.sidebar.multiselect(
    "Select Outlet Location Type:",
    options=location_types,
    default=location_types
)

# Filter B: Interactive Item_MRP Slider
min_mrp, max_mrp = int(df['Item_MRP'].min()), int(df['Item_MRP'].max())
mrp_range = st.sidebar.slider(
    "Select Item_MRP Range ($):",
    min_value=min_mrp,
    max_value=max_mrp,
    value=(min_mrp, max_mrp)
)

# 4. Filter the Dataset Based on User Input
filtered_df = df[
    (df['Outlet_Location_Type'].isin(selected_tiers)) & 
    (df['Item_MRP'].between(mrp_range[0], mrp_range[1]))
]

# 5. Key Metrics Displays
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Filtered Sales", f"${filtered_df['Item_Outlet_Sales'].sum():,}")
with col2:
    st.metric("Average Item MRP", f"${filtered_df['Item_MRP'].mean():.2f}")
with col3:
    st.metric("Total Items Displayed", len(filtered_df))

st.markdown("---")

# 6. Interactive Visualizations
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("📈 Item_MRP vs. Outlet Sales")
    fig_scatter = px.scatter(
        filtered_df, 
        x="Item_MRP", 
        y="Item_Outlet_Sales", 
        color="Outlet_Location_Type",
        hover_data=["Item_Type", "Item_Identifier"],
        title="Check for Price Clusters and Sales Trends"
    )
    st.plotly_chart(fig_scatter, width='stretch')

with chart_col2:
    st.subheader("📊 Sales Contribution by Item Type")
    fig_bar = px.bar(
        filtered_df.groupby("Item_Type", as_index=False)["Item_Outlet_Sales"].sum(),
        x="Item_Type",
        y="Item_Outlet_Sales",
        title="Total Revenue per Product Category"
    )
    st.plotly_chart(fig_bar, width='stretch')
