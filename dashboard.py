import streamlit as st
import pandas as pd
from report_engine import StayPulseReportEngine
import os
import base64

# Page Config
st.set_page_config(page_title="StayPulse Wyndham Intelligence", page_icon="✨", layout="wide")

# Initialize Engine
@st.cache_resource
def get_engine():
    return StayPulseReportEngine()

engine = get_engine()

# Sidebar for Selection
st.sidebar.image("https://tse1.mm.bing.net/th/id/OIP.3lNQjRFhsU8NfdTXY15WFQHaEK?w=512&h=288&rs=1&pid=ImgDetMain&o=7&rm=3", width=200)
st.sidebar.title("Report Generator")

report_type = st.sidebar.radio("Select Report Type", ["Brand", "Chain Scale"])

if report_type == "Brand":
    options = sorted(engine.df['property_brand_name'].unique())
    selected = st.sidebar.selectbox("Choose Brand", options)
    filter_type = 'brand'
else:
    options = sorted(engine.df['chain_scale'].unique())
    selected = st.sidebar.selectbox("Choose Chain Scale", options)
    filter_type = 'scale'

generate_btn = st.sidebar.button("Generate Executive Report")

# Main UI
st.title("✨ StayPulse: AI-Powered Hospitality Insights")
st.markdown(f"Currently analyzing **{len(engine.df):,}** guest records for Wyndham Hotels.")

if generate_btn:
    with st.spinner(f"AI is analyzing {selected} data and generating insights..."):
        # 1. Generate the report file
        engine.generate_report(filter_type=filter_type, filter_value=selected)
        
        # 2. Locate the generated file
        file_name = f"{selected.replace(' ', '_').lower()}_report.html"
        file_path = os.path.join("reports", file_name)
        
        if os.path.exists(file_path):
            st.success(f"✅ Report for {selected} generated successfully!")
            
            # Display metrics in Streamlit for quick view
            data = engine.df[engine.df['property_brand_name'] == selected.upper()] if filter_type == 'brand' else engine.df[engine.df['chain_scale'] == selected]
            
            col1, col2, col3 = st.columns(3)
            col1.metric("NPS Score", round(data['nps_score'].mean(), 1))
            col2.metric("Overall OSAT", round(data['osat_score'].mean(), 1))
            col3.metric("Total Responses", f"{len(data):,}")
            
            # Preview and Download
            with open(file_path, "r", encoding="utf-8") as f:
                html_content = f.read()
                
            st.download_button(
                label="📥 Download HTML Report (Ready for Email)",
                data=html_content,
                file_name=file_name,
                mime="text/html",
                use_container_width=True
            )
            
            # HTML Preview in an iframe
            st.markdown("---")
            st.subheader("Report Preview")
            st.components.v1.html(html_content, height=800, scrolling=True)
        else:
            st.error("Failed to generate report file.")

else:
    # Welcome Screen
    st.info("Select a brand or category from the sidebar and click 'Generate' to begin the AI analysis.")
    
    # Show high-level stats
    st.subheader("Global Portfolio Snapshot")
    scale_avg = engine.df.groupby('chain_scale')['nps_score'].mean().sort_values(ascending=False)
    st.bar_chart(scale_avg)
