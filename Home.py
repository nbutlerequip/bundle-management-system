import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Compatible Parts System",
    page_icon="📦",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: #1a1a1a;
        color: white;
        padding: 2rem;
        margin: -1rem -1rem 2rem -1rem;
        border-bottom: 3px solid #0066cc;
        text-align: center;
    }
    .big-button {
        background: #0066cc;
        color: white;
        padding: 2rem;
        text-align: center;
        border-radius: 5px;
        cursor: pointer;
        margin: 2rem 0;
        transition: background 0.3s;
    }
    .big-button:hover {
        background: #0052a3;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1 style="margin: 0;">Compatible Parts System</h1>
    <p style="margin: 0.5rem 0 0 0; color: #ccc;">Identify Compatible Parts</p>
</div>
""", unsafe_allow_html=True)

# Main content
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown("### Welcome")
    st.markdown("""
    This system helps you identify compatible parts based on customer purchase patterns.
    
    **Features:**
    - Search for compatible parts by part number
    - View recommended compatible parts sorted by customer count
    """)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Single button to access system
    if st.button("🔍 Find Compatible Parts", use_container_width=True, type="primary"):
        st.switch_page("pages/Compatible_Part_Search.py")
    
    st.markdown("---")
    
    st.caption("System automatically loads the latest compatible parts data")
