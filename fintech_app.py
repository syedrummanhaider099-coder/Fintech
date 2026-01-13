import streamlit as st
import pandas as pd
import plotly.express as px

# Page ki configuration
st.set_page_config(page_title="Company Performance Dashboard", layout="wide")

st.title("Company Growth Predictor")
st.markdown("Change the inputs and see how they affect Volume, Revenue, and Profit.")

# --- SIDEBAR: INPUTS ---
st.sidebar.header("Company Inputs")

# 4 Inputs
volume = st.sidebar.slider("Volume (Units Sold)", min_value=100, max_value=10000, value=1000)
price = st.sidebar.number_input("Price per Unit ($)", min_value=1.0, value=50.0)
variable_cost = st.sidebar.number_input("Variable Cost per Unit ($)", min_value=1.0, value=20.0)
fixed_cost = st.sidebar.number_input("Monthly Fixed Cost ($)", min_value=0, value=5000)

# --- CALCULATIONS (OUTPUTS) ---
revenue = volume * price
total_variable_cost = volume * variable_cost
total_cost = fixed_cost + total_variable_cost
profit = revenue - total_cost

# --- DISPLAY OUTPUTS ---
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Total Volume", value=f"{volume:,} units")

with col2:
    st.metric(label="Total Revenue", value=f"${revenue:,}")

with col3:
    st.metric(label="Net Profit", value=f"${profit:,}", delta=f"{profit/revenue*100:.1f}% Margin")

st.divider()

# --- GRAPHS & CHARTS ---
st.subheader("Financial Visualization")

# Data for Charts
df_data = pd.DataFrame({
    "Category": ["Revenue", "Total Cost", "Profit"],
    "Amount": [revenue, total_cost, profit]
})

col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    # Bar Chart for Comparison
    fig_bar = px.bar(df_data, x="Category", y="Amount", color="Category", 
                     title="Revenue vs Cost vs Profit",
                     color_discrete_map={"Revenue": "#31333F", "Total Cost": "#EF553B", "Profit": "#00CC96"})
    st.plotly_chart(fig_bar, use_container_width=True)

with col_chart2:
    # Pie Chart for Cost Structure
    pie_data = pd.DataFrame({
        "Type": ["Profit", "Fixed Cost", "Variable Cost"],
        "Value": [max(0, profit), fixed_cost, total_variable_cost]
    })
    fig_pie = px.pie(pie_data, values="Value", names="Type", title="Budget Breakdown", hole=0.4)
    st.plotly_chart(fig_pie, use_container_width=True)

# Profitability Trend (Simulated projection)
st.subheader("Profitability Projection (at different volumes)")
volumes = [v for v in range(100, 10001, 500)]
profits = [(v * price) - (fixed_cost + (v * variable_cost)) for v in volumes]
trend_df = pd.DataFrame({"Volume": volumes, "Predicted Profit": profits})

fig_line = px.line(trend_df, x="Volume", y="Predicted Profit", title="Volume vs Profit Trend")
st.plotly_chart(fig_line, use_container_width=True)