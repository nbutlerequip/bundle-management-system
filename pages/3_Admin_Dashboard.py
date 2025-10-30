import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="Admin Dashboard",
    page_icon="📈",
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
        font-size: 1.75rem;
        font-weight: 700;
        color: #1a1a1a;
    }
    .status-active {
        color: #28a745;
        font-weight: 600;
    }
    .status-inactive {
        color: #999;
    }
</style>
""", unsafe_allow_html=True)

# Password protection
if 'admin_authenticated' not in st.session_state:
    st.session_state.admin_authenticated = False

if not st.session_state.admin_authenticated:
    st.markdown('<div class="main-header"><h1>Admin Dashboard - Authentication Required</h1></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("### 🔒 Administrator Authentication")
        st.markdown("This page requires authentication")
        
        password_input = st.text_input("Admin Password", type="password", key="password_input")
        
        col_btn1, col_btn2 = st.columns([1, 1])
        with col_btn1:
            if st.button("Access Dashboard", use_container_width=True):
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

# If authenticated, show admin dashboard
st.markdown('<div class="main-header"><h1>Admin Dashboard - All Branch Performance</h1></div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### Navigation")
    if st.button("🏠 Home", use_container_width=True):
        st.session_state.admin_authenticated = False
        st.switch_page("Home.py")
    if st.button("📊 Bundle Analyzer", use_container_width=True):
        st.switch_page("pages/1_Bundle_Analyzer.py")
    
    st.markdown("---")
    st.markdown("### Filters")
    time_filter = st.selectbox("Time Period", ["Last 7 Days", "Last 30 Days", "Last Quarter", "All Time"])
    
    st.markdown("---")
    if st.button("🔓 Logout", use_container_width=True):
        st.session_state.admin_authenticated = False
        st.rerun()

# Data directories
DATA_DIR = "data"
SALES_LOG = os.path.join(DATA_DIR, "bundle_sales_log.csv")
BRANCH_FILE = os.path.join(DATA_DIR, "branch_list.csv")

# Load data
if not os.path.exists(SALES_LOG):
    st.warning("No sales data found yet. Branches haven't started tracking sales.")
    st.info("Sales will appear here once branches mark bundles as sold.")
    st.stop()

df_sales = pd.read_csv(SALES_LOG)
df_sales['timestamp'] = pd.to_datetime(df_sales['timestamp'], errors='coerce')

# Load branches
if os.path.exists(BRANCH_FILE):
    branches_df = pd.read_csv(BRANCH_FILE)
    all_branches = branches_df['branch_name'].tolist()
else:
    all_branches = [
        "Cambridge", "Marietta", "Holt", "Monroe", "Mentor", "Brunswick",
        "Gallipolis", "North Canton", "Evansville", "Dublin", "Perrysburg",
        "Burlington", "Indianapolis", "Fort Wayne", "Heath", "Mansfield",
        "Novi", "South Charleston"
    ]

# Apply time filter
if time_filter == "Last 7 Days":
    df_filtered = df_sales[df_sales['timestamp'] >= pd.Timestamp.now() - pd.Timedelta(days=7)]
elif time_filter == "Last 30 Days":
    df_filtered = df_sales[df_sales['timestamp'] >= pd.Timestamp.now() - pd.Timedelta(days=30)]
elif time_filter == "Last Quarter":
    df_filtered = df_sales[df_sales['timestamp'] >= pd.Timestamp.now() - pd.Timedelta(days=90)]
else:
    df_filtered = df_sales

# Calculate overall metrics
total_bundles_sold = len(df_filtered)
total_revenue = df_filtered['revenue_estimate'].sum()
active_branches = df_filtered['branch_name'].nunique()
avg_confidence = df_filtered['confidence'].mean() if len(df_filtered) > 0 else 0

# Calculate conversion rate (placeholder)
conversion_rate = 73  # This would need actual data on bundles presented vs sold

# This week
this_week = df_sales[df_sales['timestamp'] >= pd.Timestamp.now() - pd.Timedelta(days=7)]
this_week_sales = len(this_week)

# Overall metrics
col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Total Bundles Sold</div>
        <div class="metric-value">{total_bundles_sold}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Total Revenue</div>
        <div class="metric-value">${total_revenue/1000:.0f}K</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Active Branches</div>
        <div class="metric-value">{active_branches}/{len(all_branches)}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Avg Confidence</div>
        <div class="metric-value">{avg_confidence:.0f}%</div>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Conversion Rate</div>
        <div class="metric-value">{conversion_rate}%</div>
    </div>
    """, unsafe_allow_html=True)

with col6:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">This Week</div>
        <div class="metric-value">{this_week_sales}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Branch performance table
st.markdown("### Branch Performance")

# Calculate per-branch stats
branch_stats = []
for branch in all_branches:
    branch_data = df_filtered[df_filtered['branch_name'] == branch]
    
    if len(branch_data) > 0:
        bundles_sold = len(branch_data)
        revenue = branch_data['revenue_estimate'].sum()
        last_activity = branch_data['timestamp'].max()
        
        # Calculate time since last activity
        time_diff = pd.Timestamp.now() - last_activity
        if time_diff.days == 0:
            last_activity_str = f"{time_diff.seconds // 3600} hours ago"
        else:
            last_activity_str = f"{time_diff.days} days ago"
        
        status = "Active"
        conversion = 75  # Placeholder
    else:
        bundles_sold = 0
        revenue = 0
        last_activity_str = "Never"
        status = "Inactive"
        conversion = 0
    
    branch_stats.append({
        'Branch': branch,
        'Status': status,
        'Bundles Sold': bundles_sold,
        'Revenue': f"${revenue:,.0f}",
        'Last Activity': last_activity_str,
        'Conversion Rate': f"{conversion}%"
    })

df_branch_stats = pd.DataFrame(branch_stats)

# Style the dataframe
def color_status(val):
    if val == "Active":
        return 'color: #28a745; font-weight: 600'
    else:
        return 'color: #999'

styled_df = df_branch_stats.style.applymap(color_status, subset=['Status'])
st.dataframe(styled_df, use_container_width=True, hide_index=True)

# Export button
csv = df_branch_stats.to_csv(index=False)
st.download_button(
    label="Export Branch Performance",
    data=csv,
    file_name=f"branch_performance_{datetime.now().strftime('%Y%m%d')}.csv",
    mime="text/csv"
)

st.markdown("---")

# Recent activity
st.markdown("### Recent Sales Activity (All Branches)")

if len(df_filtered) > 0:
    recent_sales = df_filtered.sort_values('timestamp', ascending=False).head(20)
    
    # Display as table
    display_cols = ['timestamp', 'branch_name', 'part1', 'part2', 'revenue_estimate']
    recent_display = recent_sales[display_cols].copy()
    recent_display.columns = ['Timestamp', 'Branch', 'Part 1', 'Part 2', 'Revenue']
    recent_display['Revenue'] = recent_display['Revenue'].apply(lambda x: f"${x:,.0f}")
    
    st.dataframe(recent_display, use_container_width=True, hide_index=True)
else:
    st.info("No sales activity in selected time period")

# Analytics section
st.markdown("---")
st.markdown("### Analytics")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Sales by Branch")
    if len(df_filtered) > 0:
        branch_sales = df_filtered.groupby('branch_name').size().sort_values(ascending=False)
        st.bar_chart(branch_sales)
    else:
        st.info("No data to display")

with col2:
    st.markdown("#### Revenue by Branch")
    if len(df_filtered) > 0:
        branch_revenue = df_filtered.groupby('branch_name')['revenue_estimate'].sum().sort_values(ascending=False)
        st.bar_chart(branch_revenue)
    else:
        st.info("No data to display")
