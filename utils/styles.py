import streamlit as st

def apply_custom_styles():
    st.markdown("""
        <style>
        .activity-grid {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
        }
        .tooltip {
            background-color: #24292e !important;
            color: #ffffff !important;
        }
        .month-label {
            font-size: 14px;
            font-weight: 600;
            color: #24292e;
            margin-bottom: 8px;
        }
        </style>
    """, unsafe_allow_html=True)
