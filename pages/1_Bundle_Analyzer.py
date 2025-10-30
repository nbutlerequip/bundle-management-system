import streamlit as st
import pandas as pd
import os

# Page configuration
st.set_page_config(
    page_title="Bundle Analyzer - Admin",
    page_icon="📊",
    layout="wide"
)

# ADMIN PASSWORD
ADMIN_PASSWORD = "admin123"  # Change this to your secure password

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: #1a1a1a;
        color: white;
        padding: 1.5rem 2rem;
        margin: -1rem -1rem 2rem -1rem;
        border-bottom: 3px solid #0066cc;
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border: 1px solid #ddd;
        border-radius: 0px;
    }
    .metric-label {
        font-size: 0.75rem;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.5rem;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #1a1a1a;
    }
</style>
""", unsafe_allow_html=True)

# Password protection
if 'admin_authenticated' not in st.session_state:
    st.session_state.admin_authenticated = False

if not st.session_state.admin_authenticated:
    st.markdown('<div class="main-header"><h1>Bundle Analyzer - Admin Access</h1></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("### 🔒 Administrator Authentication")
        st.markdown("This page requires authentication")
        
        password_input = st.text_input("Admin Password", type="password", key="password_input")
        
        col_btn1, col_btn2 = st.columns([1, 1])
        with col_btn1:
            if st.button("Access Admin Tools", use_container_width=True):
                if password_input == ADMIN_PASSWORD:
                    st.session_state.admin_authenticated = True
                    st.rerun()
                else:
                    st.error("Incorrect password")
        
        with col_btn2:
            if st.button("Back to Home", use_container_width=True):
                st.switch_page("Home.py")
        
        st.markdown("---")
        st.caption("Contact system administrator if you need access")
    
    st.stop()

# If authenticated, show admin tools
st.markdown('<div class="main-header"><h1>Bundle Analyzer</h1></div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### Navigation")
    if st.button("🏠 Home", use_container_width=True):
        st.session_state.admin_authenticated = False
        st.switch_page("Home.py")
    if st.button("📈 Admin Dashboard", use_container_width=True):
        st.switch_page("pages/3_Admin_Dashboard.py")
    
    st.markdown("---")
    st.markdown("### Actions")
    if st.button("🔓 Logout", use_container_width=True):
        st.session_state.admin_authenticated = False
        st.rerun()

# Main content
st.markdown("### Bundle Analysis Tools")

# Check if bundle data exists
DATA_DIR = "data"
BUNDLE_FILE = os.path.join(DATA_DIR, "COMPLETE_BUNDLE_ANALYSIS_20251029_084720.csv")

if os.path.exists(BUNDLE_FILE):
    df = pd.read_csv(BUNDLE_FILE)
    
    # Smart column detection - find columns by partial match
    def find_column(df, possible_names):
        """Find column that matches any of the possible names (case insensitive, partial match)"""
        for col in df.columns:
            col_lower = col.lower()
            for name in possible_names:
                if name.lower() in col_lower:
                    return col
        return None
    
    # Map generic names to actual column names in the CSV
    PART1_COL = find_column(df, ['part_1', 'part1', 'partnumber1'])
    PART2_COL = find_column(df, ['part_2', 'part2', 'partnumber2'])
    CUSTOMERS_COL = find_column(df, ['customer', 'customers', 'customer_base'])
    CONFIDENCE_COL = find_column(df, ['confidence', 'enhanced_confidence', 'conf'])
    REVENUE_COL = find_column(df, ['revenue', 'annual_revenue', 'revenue_potential'])
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total Bundles</div>
            <div class="metric-value">{len(df):,}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        if CUSTOMERS_COL:
            total_customers = df[CUSTOMERS_COL].sum()
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Total Customers</div>
                <div class="metric-value">{total_customers:,}</div>
            </div>
            """, unsafe_allow_html=True)
    
    with col3:
        if CONFIDENCE_COL:
            avg_confidence = df[CONFIDENCE_COL].mean()
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Avg Confidence</div>
                <div class="metric-value">{avg_confidence:.1f}%</div>
            </div>
            """, unsafe_allow_html=True)
    
    with col4:
        if REVENUE_COL:
            total_revenue = df[REVENUE_COL].sum()
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Est. Revenue</div>
                <div class="metric-value">${total_revenue/1000000:.1f}M</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Tabs for different views
    tab1, tab2, tab3 = st.tabs(["📊 Overview", "📋 Data Table", "⚙️ Settings"])
    
    with tab1:
        st.markdown("### Bundle Distribution")
        
        # Confidence distribution
        if CONFIDENCE_COL:
            st.markdown("**Confidence Distribution**")
            confidence_bins = pd.cut(df[CONFIDENCE_COL], bins=[0, 50, 70, 80, 90, 100], 
                                    labels=['0-50%', '50-70%', '70-80%', '80-90%', '90-100%'])
            confidence_counts = confidence_bins.value_counts().sort_index()
            st.bar_chart(confidence_counts)
        
        st.markdown("---")
        
        # Top bundles
        st.markdown("### Top 20 Bundles by Confidence")
        if CONFIDENCE_COL:
            display_cols = [c for c in [PART1_COL, PART2_COL, CUSTOMERS_COL, CONFIDENCE_COL, REVENUE_COL] if c]
            top_bundles = df.nlargest(20, CONFIDENCE_COL)[display_cols]
            st.dataframe(top_bundles, use_container_width=True, hide_index=True)
        else:
            st.dataframe(df.head(20), use_container_width=True, hide_index=True)
    
    with tab2:
        st.markdown("### Complete Bundle Data")
        
        # Filters
        col1, col2 = st.columns(2)
        with col1:
            min_confidence = st.slider("Minimum Confidence", 0, 100, 70)
        with col2:
            min_customers = st.number_input("Minimum Customers", 0, 10000, 0)
        
        # Filter data
        if CONFIDENCE_COL and CUSTOMERS_COL:
            filtered_df = df[
                (df[CONFIDENCE_COL] >= min_confidence) & 
                (df[CUSTOMERS_COL] >= min_customers)
            ]
        elif CONFIDENCE_COL:
            filtered_df = df[df[CONFIDENCE_COL] >= min_confidence]
        elif CUSTOMERS_COL:
            filtered_df = df[df[CUSTOMERS_COL] >= min_customers]
        else:
            filtered_df = df
        
        st.markdown(f"**Showing {len(filtered_df):,} bundles**")
        st.dataframe(filtered_df, use_container_width=True, hide_index=True)
        
        # Download button
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="Download Filtered Data",
            data=csv,
            file_name="filtered_bundles.csv",
            mime="text/csv"
        )
    
    with tab3:
        st.markdown("### System Settings")
        st.info("Bundle data loaded successfully")
        st.markdown(f"**Data file:** `{BUNDLE_FILE}`")
        st.markdown(f"**Total records:** {len(df):,}")
        
        if st.button("Reload Data"):
            st.rerun()

else:
    st.warning(f"Bundle data file not found: `{BUNDLE_FILE}`")
    st.info("Please upload your bundle analysis CSV file to the data directory")
    
    # File uploader
    uploaded_file = st.file_uploader("Upload Bundle Analysis CSV", type=['csv'])
    if uploaded_file is not None:
        # Save uploaded file
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(BUNDLE_FILE, 'wb') as f:
            f.write(uploaded_file.getbuffer())
        st.success("File uploaded successfully!")
        st.rerun()
