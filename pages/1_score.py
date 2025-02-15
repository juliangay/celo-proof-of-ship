import streamlit as st
import re
import sys
import os
# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.utils import generate_mock_data, create_activity_grid
from utils.styles import apply_custom_styles

st.set_page_config(
    page_title="Celo Proof of Ship",
    page_icon="👋",
    layout="wide"
)

def validate_celo_address(address):
    return bool(re.match(r'^0x[a-fA-F0-9]{40}$', address))

def validate_github_username(username):
    return bool(re.match(r'^[a-zA-Z0-9-]+$', username))

def validate_farcaster_id(farcaster_id):
    return bool(re.match(r'^[a-zA-Z0-9-_]+$', farcaster_id))

def show_form():
    st.markdown("""
        <div style="display: flex; align-items: center; height: 100%; margin-bottom: 1rem;">
            <img src="https://images.ctfassets.net/wr0no19kwov9/5yVbTScDuXaZE0JL0w1kL0/f626c00085927069b473e684148c36f3/Union_1_.svg" 
                    style="width: 134px; margin-right: 2rem;">
            <h1 style="font-family: 'Inter', sans-serif;">Proof of Ship</h1>
        </div>
    """, unsafe_allow_html=True)

    with st.form("sbt_request_form"):
        github = st.text_input("GitHub Username")
        celo_address = st.text_input("Celo Address", placeholder="0x...")
        farcaster_id = st.text_input("Farcaster ID")
        
        submitted = st.form_submit_button("Submit")
        
        if submitted:
            errors = []
            
            if not validate_github_username(github):
                errors.append("Invalid GitHub username. Use only alphanumeric characters and hyphens.")
            
            if not validate_celo_address(celo_address):
                errors.append("Invalid Celo address. Must start with '0x' followed by 40 hexadecimal characters.")
            
            if not validate_farcaster_id(farcaster_id):
                errors.append("Invalid Farcaster ID. Use only alphanumeric characters, hyphens, and underscores.")
            
            if errors:
                for error in errors:
                    st.error(error)
                return False
            
            # If we get here, all validations passed
            st.session_state.form_submitted = True
            st.session_state.user_data = {
                "github": github,
                "celo_address": celo_address,
                "farcaster_id": farcaster_id
            }
            return True
    
    return False

def main():
    # Apply custom styling
    apply_custom_styles()
    
    # Initialize session state if needed
    if 'form_submitted' not in st.session_state:
        st.session_state.form_submitted = False
    
    if not st.session_state.form_submitted:
        if show_form():
            st.rerun()  # Rerun to show the dashboard
    else:
        # Show success message
        st.success("Form submitted successfully!")
        
        # Add link to dashboard
        st.markdown("[View Full Dashboard](/pages/dashboard)", unsafe_allow_html=True)
        
        # Show the dashboard content
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

        # Activity grid
        fig = create_activity_grid(data)
        
        # Display the visualization
        st.plotly_chart(fig, use_container_width=True)

        # Add a button to reset the form
        if st.button("Submit Another Request"):
            st.session_state.form_submitted = False
            st.rerun()

if __name__ == "__main__":
    main() 