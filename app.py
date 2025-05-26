import streamlit as st
import pandas as pd
import plotly.express as px
from data_simulator import generate_tracking_data
from io import BytesIO

st.set_page_config(page_title="Courier Tracking Dashboard", layout="wide")

st.title("📦 Courier Tracking Dashboard - Pakistan")
st.markdown("Track courier statuses and locations across **Pakistan** in real-time.")

# Simulated data
df = generate_tracking_data(200)

# Filter to simulate Pakistan coordinates
df["Latitude"] = df["Latitude"].apply(lambda x: 24 + (x % 6))     # ~24 to 30 (South to North)
df["Longitude"] = df["Longitude"].apply(lambda x: 66 + (x % 7))   # ~66 to 73 (West to East)

# Sidebar filters
st.sidebar.header("Filters")
status_filter = st.sidebar.multiselect("Select Status", options=df["Status"].unique(), default=df["Status"].unique())

# Filtered data
filtered_df = df[df["Status"].isin(status_filter)]

# Metrics
col1, col2, col3 = st.columns(3)
col1.metric("Total Packages", len(df))
col2.metric("In Transit", (df["Status"] == "In Transit").sum())
col3.metric("Delivered", (df["Status"] == "Delivered").sum())

# Pie chart
fig_status = px.pie(filtered_df, names='Status', title="📊 Package Status Distribution", hole=0.4)
st.plotly_chart(fig_status, use_container_width=True)

# Pakistan Map
st.subheader("📍 Package Locations in Pakistan")
fig_map = px.scatter_mapbox(
    filtered_df,
    lat="Latitude",
    lon="Longitude",
    hover_name="Package ID",
    color="Status",
    zoom=5,
    height=500
)
fig_map.update_layout(mapbox_style="open-street-map", mapbox_center={"lat": 30.3753, "lon": 69.3451})
st.plotly_chart(fig_map, use_container_width=True)

# Table
st.subheader("📋 Package Data")
st.dataframe(filtered_df.sort_values(by="Updated At", ascending=False), use_container_width=True)

# --- Export buttons ---
st.subheader("📁 Download Data")

# CSV
csv = filtered_df.to_csv(index=False)
st.download_button("Download as CSV", csv, "courier_data.csv", "text/csv")

# Excel
def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='CourierData')
    return output.getvalue()

excel_data = to_excel(filtered_df)
st.download_button("Download as Excel", excel_data, "courier_data.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
