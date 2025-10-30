import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Bundle Management System",
    page_icon="📊",
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
    }
    .card {
        background: white;
        padding: 2rem;
        border: 1px solid #ddd;
        border-radius: 0px;
        margin: 1rem 0;
        cursor: pointer;
        transition: all 0.2s;
    }
    .card:hover {
        border-color: #0066cc;
        box-shadow: 0 4px 12px rgba(0,102,204,0.1);
    }
    .card-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    .card-title {
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        color: #1a1a1a;
    }
    .card-description {
        color: #666;
        line-height: 1.6;
        margin-bottom: 1rem;
    }
    .badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        background: #e6f2ff;
        color: #0066cc;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-top: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header"><h1>Bundle Management System</h1></div>', unsafe_allow_html=True)

st.title("Welcome")
st.markdown("Select your workspace")

# Create three columns for cards
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="card">
        <div class="card-icon">📊</div>
        <div class="card-title">Bundle Analyzer</div>
        <div class="card-description">
            Comprehensive analysis tool for identifying bundling opportunities. 
            Analyze purchase patterns, supersession data, and generate revenue predictions.
        </div>
        <div class="badge">Admin Only</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Open Bundle Analyzer", use_container_width=True):
        st.switch_page("pages/1_Bundle_Analyzer.py")

with col2:
    st.markdown("""
    <div class="card">
        <div class="card-icon">🏢</div>
        <div class="card-title">Branch Tracking</div>
        <div class="card-description">
            Branch portal for viewing recommended bundles and recording sales. 
            Track your branch performance and mark bundles as sold.
        </div>
        <div class="badge">Branch Access</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Open Branch Tracking", use_container_width=True):
        st.switch_page("pages/2_Branch_Tracking.py")

with col3:
    st.markdown("""
    <div class="card">
        <div class="card-icon">📈</div>
        <div class="card-title">Admin Dashboard</div>
        <div class="card-description">
            Monitor all branch activity, validate bundle predictions, and track 
            conversion rates across all locations. View comprehensive sales analytics.
        </div>
        <div class="badge">Admin Only</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Open Admin Dashboard", use_container_width=True):
        st.switch_page("pages/3_Admin_Dashboard.py")

# Footer info
st.markdown("---")
st.markdown("""
**System Information:**
- 18 Active Branches
- Real-time Bundle Tracking
- Comprehensive Analytics
""")
