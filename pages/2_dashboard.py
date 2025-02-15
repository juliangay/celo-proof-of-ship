import streamlit as st
import datetime
import sys
import os
# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.utils import generate_mock_data, create_activity_grid
from utils.styles import apply_custom_styles


# Page configuration must be first
st.set_page_config(
    page_title="Celo Proof of Ship",
    page_icon="📊",
    layout="wide"
)

def main():
    # Apply custom styling
    apply_custom_styles()

    # Header
    st.markdown("""
        <div style="display: flex; align-items: center; height: 100%; margin-bottom: 1rem;">
            <img src="https://images.ctfassets.net/wr0no19kwov9/5yVbTScDuXaZE0JL0w1kL0/f626c00085927069b473e684148c36f3/Union_1_.svg" 
                    style="width: 134px; margin-right: 2rem;">
            <h1 style="font-family: 'Inter', sans-serif;">Proof of Ship</h1>
        </div>
    """, unsafe_allow_html=True)
    
    try:
        data = generate_mock_data(2025)        
    except Exception as e:
        st.error(f"Error occurred: {str(e)}")

    # Activity summary
    total_activities = data['activity'].sum()
    active_days = len(data[data['activity'] > 0])

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Activities", total_activities)
    with col2:
        st.metric("Active Days", active_days)

    # Generate and display activity data
    current_year = datetime.datetime.now().year
    selected_year = st.selectbox(
        "Select Year",
        range(current_year - 2, current_year + 1),
        index=2
    )

    # Activity grid
    fig = create_activity_grid(data)
    
    # Display the visualization
    st.plotly_chart(fig, use_container_width=True)

    # Legend
    st.markdown("### Activity Levels")
    legend_col1, legend_col2, legend_col3, legend_col4, legend_col5 = st.columns(5)

    with legend_col1:
        st.markdown('<div style="background-color: #ebedf0; width: 20px; height: 20px; display: inline-block;"></div> No activity', unsafe_allow_html=True)
    with legend_col2:
        st.markdown('<div style="background-color: #9be9a8; width: 20px; height: 20px; display: inline-block;"></div> 1-3 activities', unsafe_allow_html=True)
    with legend_col3:
        st.markdown('<div style="background-color: #40c463; width: 20px; height: 20px; display: inline-block;"></div> 4-7 activities', unsafe_allow_html=True)
    with legend_col4:
        st.markdown('<div style="background-color: #30a14e; width: 20px; height: 20px; display: inline-block;"></div> 8-11 activities', unsafe_allow_html=True)
    with legend_col5:
        st.markdown('<div style="background-color: #216e39; width: 20px; height: 20px; display: inline-block;"></div> 12+ activities', unsafe_allow_html=True)

if __name__ == "__main__":
    main()