import streamlit as st
from utils.styles import apply_custom_styles


st.set_page_config(
    page_title="Celo Proof of Ship",
    page_icon="👋",
    layout="wide"
)

def main():
    apply_custom_styles()
    
    st.markdown("""
        <div style="display: flex; align-items: center; height: 100%; margin-bottom: 1rem;">
            <img src="https://images.ctfassets.net/wr0no19kwov9/5yVbTScDuXaZE0JL0w1kL0/f626c00085927069b473e684148c36f3/Union_1_.svg" 
                    style="width: 134px; margin-right: 2rem;">
            <h1 style="font-family: 'Inter', sans-serif;">Proof of Ship</h1>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()