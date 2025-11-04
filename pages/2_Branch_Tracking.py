import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Version 1.4 - Fixed revenue display (per-bundle instead of total)

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
PART1_COL = find_column(df_bundles, ['part_1', 'part1', 'partnumber1'])
PART2_COL = find_column(df_bundles, ['part_2', 'part2', 'partnumber2'])
CUSTOMERS_COL = find_column(df_bundles, ['customer', 'customers', 'customer_base'])
CONFIDENCE_COL = find_column(df_bundles, ['confidence', 'enhanced_confidence', 'conf'])
REVENUE_COL = find_column(df_bundles, ['revenue', 'annual_revenue', 'revenue_potential'])

# Load or create sales log
if os.path.exists(SALES_LOG):
    try:
        df_sales = pd.read_csv(SALES_LOG)
        if len(df_sales) > 0 and 'timestamp' in df_sales.columns:
            df_sales['timestamp'] = pd.to_datetime(df_sales['timestamp'], errors='coerce')
    except Exception as e:
        df_sales = pd.DataFrame(columns=[
            'timestamp', 'branch_name', 'bundle_id', 'part1', 'part2',
            'customers', 'confidence', 'revenue_estimate', 'status'
        ])
else:
    df_sales = pd.DataFrame(columns=[
        'timestamp', 'branch_name', 'bundle_id', 'part1', 'part2',
        'customers', 'confidence', 'revenue_estimate', 'status'
    ])

# Calculate branch metrics - bulletproof version
try:
    if len(df_sales) > 0:
        branch_sales = df_sales[df_sales['branch_name'] == branch_name].copy()
    else:
        branch_sales = pd.DataFrame(columns=df_sales.columns)
    
    total_bundles_sold = len(branch_sales)
    total_revenue = float(branch_sales['revenue_estimate'].sum()) if len(branch_sales) > 0 else 0.0
    
    # This week's sales
    week_bundles = 0
    week_revenue = 0.0
    
    if len(branch_sales) > 0 and 'timestamp' in branch_sales.columns:
        try:
            cutoff_date = pd.Timestamp.now() - pd.Timedelta(days=7)
            this_week_sales = branch_sales[branch_sales['timestamp'] >= cutoff_date]
            week_bundles = len(this_week_sales)
            week_revenue = float(this_week_sales['revenue_estimate'].sum()) if len(this_week_sales) > 0 else 0.0
        except:
            week_bundles = 0
            week_revenue = 0.0
            
except Exception as e:
    st.error(f"Error loading sales data: {e}")
    branch_sales = pd.DataFrame()
    total_bundles_sold = 0
    total_revenue = 0.0
    week_bundles = 0
    week_revenue = 0.0

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

# Part Search Section
st.markdown("### 🔍 Search for Bundle Opportunities")
st.markdown("Enter a part number to find all potential bundles that include it")

search_col1, search_col2 = st.columns([3, 1])

with search_col1:
    search_part = st.text_input("Part Number", placeholder="e.g., 47833556", key="part_search")

with search_col2:
    st.markdown("<br>", unsafe_allow_html=True)  # Spacing
    search_button = st.button("Search", use_container_width=True, type="primary")

if search_button and search_part:
    # Search for bundles containing this part
    if PART1_COL and PART2_COL:
        search_results = df_bundles[
            (df_bundles[PART1_COL].astype(str).str.contains(search_part, case=False, na=False)) |
            (df_bundles[PART2_COL].astype(str).str.contains(search_part, case=False, na=False))
        ]
        
        if len(search_results) > 0:
            st.success(f"Found {len(search_results)} bundle opportunities for part: **{search_part}**")
            
            # Sort by confidence
            if CONFIDENCE_COL:
                search_results = search_results.sort_values(CONFIDENCE_COL, ascending=False)
            
            # Display results
            for idx, row in search_results.head(20).iterrows():
                part1 = row[PART1_COL] if PART1_COL else 'N/A'
                part2 = row[PART2_COL] if PART2_COL else 'N/A'
                customers = int(row[CUSTOMERS_COL]) if CUSTOMERS_COL else 0
                confidence = row[CONFIDENCE_COL] if CONFIDENCE_COL else 0
                total_revenue = int(row[REVENUE_COL]) if REVENUE_COL else 0
                
                # Calculate per-bundle revenue (total / customers)
                per_bundle_revenue = int(total_revenue / customers) if customers > 0 else total_revenue
                
                col1, col2 = st.columns([4, 1])
                
                with col1:
                    # Highlight the searched part
                    bundle_text = f"**{part1}** + **{part2}**" if search_part in str(part1) or search_part in str(part2) else f"{part1} + {part2}"
                    st.markdown(f"""
                    {bundle_text}  
                    {customers} customers bought this • {confidence:.1f}% confidence • **${per_bundle_revenue:,} per sale** (${total_revenue:,} total potential)
                    """)
                
                with col2:
                    if st.button("Mark as Sold", key=f"search_sell_{idx}", use_container_width=True):
                        try:
                            new_sale = {
                                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                'branch_name': branch_name,
                                'bundle_id': f"BDL-{idx:05d}",
                                'part1': row[PART1_COL] if PART1_COL else '',
                                'part2': row[PART2_COL] if PART2_COL else '',
                                'customers': float(row[CUSTOMERS_COL]) if CUSTOMERS_COL else 0,
                                'confidence': float(row[CONFIDENCE_COL]) if CONFIDENCE_COL else 0,
                                'revenue_estimate': float(row[REVENUE_COL]) if REVENUE_COL else 0,
                                'status': 'Sold'
                            }
                            
                            new_row_df = pd.DataFrame([new_sale])
                            df_sales = pd.concat([df_sales, new_row_df], ignore_index=True)
                            os.makedirs(DATA_DIR, exist_ok=True)
                            df_sales.to_csv(SALES_LOG, index=False)
                            
                            st.success(f"✅ Bundle marked as sold!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error saving sale: {e}")
                
                st.markdown("---")
            
            if len(search_results) > 20:
                st.info(f"Showing top 20 of {len(search_results)} results. Refine your search for more specific results.")
        else:
            st.warning(f"No bundles found for part: **{search_part}**")
            st.info("Try searching with just part of the part number (e.g., '4783' instead of '47833556')")
    else:
        st.error("Unable to search - column mapping issue. Contact administrator.")

elif search_button and not search_part:
    st.warning("Please enter a part number to search")

st.markdown("---")

# Tabs
tab1, tab2 = st.tabs(["📦 Available Bundles", "📊 My Performance"])

with tab1:
    st.markdown("### Recommended Bundles")
    st.caption("Top 20 bundles by confidence")
    
    # Show top 20 bundles
    if CONFIDENCE_COL:
        top_bundles = df_bundles.nlargest(20, CONFIDENCE_COL)
    else:
        top_bundles = df_bundles.head(20)
    
    for idx, row in top_bundles.iterrows():
        col1, col2 = st.columns([4, 1])
        
        with col1:
            part1 = row[PART1_COL] if PART1_COL else 'N/A'
            part2 = row[PART2_COL] if PART2_COL else 'N/A'
            customers = int(row[CUSTOMERS_COL]) if CUSTOMERS_COL else 0
            confidence = row[CONFIDENCE_COL] if CONFIDENCE_COL else 0
            total_revenue = int(row[REVENUE_COL]) if REVENUE_COL else 0
            
            # Calculate per-bundle revenue
            per_bundle_revenue = int(total_revenue / customers) if customers > 0 else total_revenue
            
            st.markdown(f"""
            **{part1} + {part2}**  
            {customers} customers bought this • {confidence:.1f}% confidence • **${per_bundle_revenue:,} per sale**
            """)
        
        with col2:
            button_key = f"sell_{idx}"
            if st.button("Mark as Sold", key=button_key, use_container_width=True):
                try:
                    # Add to sales log
                    new_sale = {
                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'branch_name': branch_name,
                        'bundle_id': f"BDL-{idx:05d}",
                        'part1': row[PART1_COL] if PART1_COL else '',
                        'part2': row[PART2_COL] if PART2_COL else '',
                        'customers': float(row[CUSTOMERS_COL]) if CUSTOMERS_COL else 0,
                        'confidence': float(row[CONFIDENCE_COL]) if CONFIDENCE_COL else 0,
                        'revenue_estimate': float(row[REVENUE_COL]) if REVENUE_COL else 0,
                        'status': 'Sold'
                    }
                    
                    # Create new row as DataFrame
                    new_row_df = pd.DataFrame([new_sale])
                    
                    # Append to existing sales
                    df_sales = pd.concat([df_sales, new_row_df], ignore_index=True)
                    
                    # Save to CSV - ensure directory exists
                    os.makedirs(DATA_DIR, exist_ok=True)
                    df_sales.to_csv(SALES_LOG, index=False)
                    
                    st.success(f"✅ Bundle marked as sold!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error saving sale: {e}")
                    st.info("Please try again or contact support.")
        
        st.markdown("---")

with tab2:
    st.markdown("### Branch Performance")
    
    if len(branch_sales) > 0:
        st.markdown("#### Recent Sales")
        
        # Show recent sales - make sure timestamp column exists and is datetime
        if 'timestamp' in branch_sales.columns:
            recent_sales = branch_sales.sort_values('timestamp', ascending=False).head(10)
            
            for idx, row in recent_sales.iterrows():
                timestamp_str = row['timestamp'].strftime('%Y-%m-%d %H:%M:%S') if pd.notna(row['timestamp']) else 'Unknown'
                st.markdown(f"""
                **{timestamp_str}**  
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
