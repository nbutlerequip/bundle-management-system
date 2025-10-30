import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Branch Tracking",
    page_icon="🏢",
    layout="wide"
)

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
    .bundle-item {
        background: white;
        padding: 1.5rem;
        border: 1px solid #eee;
        margin: 0.5rem 0;
        border-radius: 0px;
    }
</style>
""", unsafe_allow_html=True)

# Data directories
DATA_DIR = "data"
BRANCH_FILE = os.path.join(DATA_DIR, "branch_list.csv")
BUNDLE_FILE = os.path.join(DATA_DIR, "COMPLETE_BUNDLE_ANALYSIS_20251029_084720.csv")
SALES_LOG = os.path.join(DATA_DIR, "bundle_sales_log.csv")

# Initialize session state
if 'branch_logged_in' not in st.session_state:
    st.session_state.branch_logged_in = False
if 'selected_branch' not in st.session_state:
    st.session_state.selected_branch = None

# Branch login
if not st.session_state.branch_logged_in:
    st.markdown('<div class="main-header"><h1>Branch Tracking System</h1></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("### Branch Portal Access")
        st.markdown("Select your branch to continue")
        
        # Load branches
        if os.path.exists(BRANCH_FILE):
            branches_df = pd.read_csv(BRANCH_FILE)
            branches = branches_df['branch_name'].tolist()
        else:
            branches = [
                "Cambridge", "Marietta", "Holt", "Monroe", "Mentor", "Brunswick",
                "Gallipolis", "North Canton", "Evansville", "Dublin", "Perrysburg",
                "Burlington", "Indianapolis", "Fort Wayne", "Heath", "Mansfield",
                "Novi", "South Charleston"
            ]
        
        selected_branch = st.selectbox("Select Your Branch", [""] + branches)
        
        col_btn1, col_btn2 = st.columns([1, 1])
        with col_btn1:
            if st.button("Access System", use_container_width=True, disabled=(selected_branch == "")):
                st.session_state.branch_logged_in = True
                st.session_state.selected_branch = selected_branch
                st.rerun()
        
        with col_btn2:
            if st.button("Back to Home", use_container_width=True):
                st.switch_page("Home.py")
        
        st.markdown("---")
        st.markdown("**Active Locations**")
        st.caption(f"{len(branches)} branches")
    
    st.stop()

# If logged in, show branch dashboard
branch_name = st.session_state.selected_branch

st.markdown(f'<div class="main-header"><h1>Bundle Tracking System</h1><p style="margin:0; color:#ccc; font-size:0.875rem;">{branch_name} Branch</p></div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown(f"### {branch_name}")
    st.markdown(f"**Logged in as:** {branch_name} Branch")
    
    st.markdown("---")
    st.markdown("### Navigation")
    if st.button("🏠 Home", use_container_width=True):
        st.session_state.branch_logged_in = False
        st.session_state.selected_branch = None
        st.switch_page("Home.py")
    
    st.markdown("---")
    if st.button("🔓 Logout", use_container_width=True):
        st.session_state.branch_logged_in = False
        st.session_state.selected_branch = None
        st.rerun()

# Load bundle data
if not os.path.exists(BUNDLE_FILE):
    st.error("Bundle data not found. Please contact administrator.")
    st.stop()

df_bundles = pd.read_csv(BUNDLE_FILE)

# Load or create sales log
if os.path.exists(SALES_LOG):
    df_sales = pd.read_csv(SALES_LOG)
else:
    df_sales = pd.DataFrame(columns=[
        'timestamp', 'branch_name', 'bundle_id', 'part1', 'part2',
        'customers', 'confidence', 'revenue_estimate', 'status'
    ])

# Calculate branch metrics
branch_sales = df_sales[df_sales['branch_name'] == branch_name]
total_bundles_sold = len(branch_sales)
total_revenue = branch_sales['revenue_estimate'].sum() if len(branch_sales) > 0 else 0

# This week's sales
df_sales['timestamp'] = pd.to_datetime(df_sales['timestamp'], errors='coerce')
this_week_sales = branch_sales[branch_sales['timestamp'] >= pd.Timestamp.now() - pd.Timedelta(days=7)]
week_bundles = len(this_week_sales)
week_revenue = this_week_sales['revenue_estimate'].sum() if len(this_week_sales) > 0 else 0

# Metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Bundles Sold (This Week)</div>
        <div class="metric-value">{week_bundles}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Revenue (This Week)</div>
        <div class="metric-value">${week_revenue/1000:.0f}K</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Total Bundles Sold</div>
        <div class="metric-value">{total_bundles_sold}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Total Revenue</div>
        <div class="metric-value">${total_revenue/1000:.0f}K</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Tabs
tab1, tab2 = st.tabs(["📦 Available Bundles", "📊 My Performance"])

with tab1:
    st.markdown("### Recommended Bundles")
    st.caption("Top 20 bundles by confidence")
    
    # Show top 20 bundles
    top_bundles = df_bundles.nlargest(20, 'Enhanced_Confidenci')
    
    for idx, row in top_bundles.iterrows():
        col1, col2 = st.columns([4, 1])
        
        with col1:
            st.markdown(f"""
            **{row['Part_1']} + {row['Part_2']}**  
            {int(row['Customer_Base_Conf'])} customers • {row['Enhanced_Confidenci']:.1f}% confidence • ${int(row['Annual_Revenue_Pote']):,} revenue
            """)
        
        with col2:
            button_key = f"sell_{idx}"
            if st.button("Mark as Sold", key=button_key, use_container_width=True):
                # Add to sales log
                new_sale = {
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'branch_name': branch_name,
                    'bundle_id': f"BDL-{idx:05d}",
                    'part1': row['Part_1'],
                    'part2': row['Part_2'],
                    'customers': row['Customer_Base_Conf'],
                    'confidence': row['Enhanced_Confidenci'],
                    'revenue_estimate': row['Annual_Revenue_Pote'],
                    'status': 'Sold'
                }
                
                df_sales = pd.concat([df_sales, pd.DataFrame([new_sale])], ignore_index=True)
                
                # Save to CSV
                os.makedirs(DATA_DIR, exist_ok=True)
                df_sales.to_csv(SALES_LOG, index=False)
                
                st.success(f"✅ Bundle marked as sold!")
                st.rerun()
        
        st.markdown("---")

with tab2:
    st.markdown("### Branch Performance")
    
    if len(branch_sales) > 0:
        st.markdown("#### Recent Sales")
        
        # Show recent sales
        recent_sales = branch_sales.sort_values('timestamp', ascending=False).head(10)
        
        for idx, row in recent_sales.iterrows():
            st.markdown(f"""
            **{row['timestamp']}**  
            Bundle: {row['part1']} + {row['part2']}  
            Revenue: ${int(row['revenue_estimate']):,}
            """)
            st.markdown("---")
        
        # Summary stats
        st.markdown("#### Statistics")
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Total Sales", f"{total_bundles_sold}")
            st.metric("This Week", f"{week_bundles}")
        
        with col2:
            st.metric("Total Revenue", f"${total_revenue:,.0f}")
            st.metric("This Week Revenue", f"${week_revenue:,.0f}")
    
    else:
        st.info("No sales recorded yet. Start marking bundles as sold!")
