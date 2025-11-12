import streamlit as st
import pandas as pd
import os

# Simple Compatible Parts System - No Login, No Tracking

# Page configuration
st.set_page_config(
    page_title="Compatible Parts",
    page_icon="📦",
    layout="wide"
)

# Custom CSS - Clean and minimal
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

# Data files
DATA_DIR = "data"
BUNDLE_FILE = os.path.join(DATA_DIR, "COMPLETE_BUNDLE_ANALYSIS_20251029_084720.csv")

# Header
st.markdown('<div class="main-header"><h1>Compatible Parts System</h1></div>', unsafe_allow_html=True)

# Load bundle data
if not os.path.exists(BUNDLE_FILE):
    st.error("Compatible parts data not found. Please contact administrator.")
    st.stop()

df_bundles = pd.read_csv(BUNDLE_FILE)

# Show data summary
total_parts = len(df_bundles)
st.caption(f"Loaded {total_parts:,} part combinations from database")

# Smart column detection
def find_column(df, possible_names):
    """Find column that matches any of the possible names"""
    for col in df.columns:
        col_lower = col.lower()
        for name in possible_names:
            if name.lower() in col_lower:
                return col
    return None

# Map column names
PART1_COL = find_column(df_bundles, ['part_1', 'part1', 'partnumber1'])
PART2_COL = find_column(df_bundles, ['part_2', 'part2', 'partnumber2'])
CUSTOMERS_COL = find_column(df_bundles, ['customer', 'customers', 'customer_base'])
DESC1_COL = find_column(df_bundles, ['description_1', 'desc_1', 'desc1', 'part1_desc', 'part_1_description'])
DESC2_COL = find_column(df_bundles, ['description_2', 'desc_2', 'desc2', 'part2_desc', 'part_2_description'])

st.markdown("---")

# Part Search Section
st.markdown("### 🔍 Search for Compatible Parts")
st.markdown("Enter a part number to find all compatible parts that include it")

search_col1, search_col2 = st.columns([3, 1])

with search_col1:
    search_part = st.text_input("Part Number", placeholder="e.g., 47833556", key="part_search")

with search_col2:
    st.markdown("<br>", unsafe_allow_html=True)
    search_button = st.button("Search", use_container_width=True, type="primary")

if search_button and search_part:
    # Search for bundles containing this part
    if PART1_COL and PART2_COL:
        search_results = df_bundles[
            (df_bundles[PART1_COL].astype(str).str.contains(search_part, case=False, na=False)) |
            (df_bundles[PART2_COL].astype(str).str.contains(search_part, case=False, na=False))
        ]
        
        if len(search_results) > 0:
            # Clean search results: remove null/zero customer counts
            search_results = search_results[search_results[CUSTOMERS_COL].notna()]
            search_results[CUSTOMERS_COL] = pd.to_numeric(search_results[CUSTOMERS_COL], errors='coerce')
            search_results = search_results[search_results[CUSTOMERS_COL] > 0]
            
            if len(search_results) > 0:
                st.success(f"Found {len(search_results)} compatible parts for part: **{search_part}**")
                
                # Sort by customer count (highest first)
                search_results = search_results.sort_values(CUSTOMERS_COL, ascending=False)
                
                # Display results
                for idx, row in search_results.head(20).iterrows():
                    part1 = row[PART1_COL] if PART1_COL else 'N/A'
                    part2 = row[PART2_COL] if PART2_COL else 'N/A'
                    customers = int(row[CUSTOMERS_COL]) if CUSTOMERS_COL and pd.notna(row[CUSTOMERS_COL]) else 0
                    
                    # Get descriptions if available
                    desc1 = row[DESC1_COL] if DESC1_COL and pd.notna(row[DESC1_COL]) else None
                    desc2 = row[DESC2_COL] if DESC2_COL and pd.notna(row[DESC2_COL]) else None
                    
                    # Build display text
                    if desc1 and desc2:
                        st.markdown(f"""
                        **{part1}** - {desc1}  
                        **{part2}** - {desc2}  
                        {customers} customers
                        """)
                    elif desc1 or desc2:
                        part1_display = f"**{part1}** - {desc1}" if desc1 else f"**{part1}**"
                        part2_display = f"**{part2}** - {desc2}" if desc2 else f"**{part2}**"
                        st.markdown(f"""
                        {part1_display}  
                        {part2_display}  
                        {customers} customers
                        """)
                    else:
                        st.markdown(f"""
                        **{part1} + {part2}**  
                        {customers} customers
                        """)
                    st.markdown("---")
                
                if len(search_results) > 20:
                    st.info(f"Showing top 20 of {len(search_results)} results. Refine your search for more specific results.")
            else:
                st.warning(f"No compatible parts with customer data found for part: **{search_part}**")
                st.info("Try searching with just part of the part number")
        else:
            st.warning(f"No compatible parts found for part: **{search_part}**")
            st.info("Try searching with just part of the part number")
    else:
        st.error("Unable to search - column mapping issue. Contact administrator.")

elif search_button and not search_part:
    st.warning("Please enter a part number to search")

st.markdown("---")

# Available Compatible Parts
st.markdown("### Recommended Compatible Parts")
st.caption("Top 20 compatible parts by customer count")

# Show top 20 compatible parts by customer count
if CUSTOMERS_COL:
    # Clean the data: remove rows with null or zero customers
    valid_bundles = df_bundles.copy()
    valid_bundles = valid_bundles[valid_bundles[CUSTOMERS_COL].notna()]
    
    # Convert to numeric if needed
    valid_bundles[CUSTOMERS_COL] = pd.to_numeric(valid_bundles[CUSTOMERS_COL], errors='coerce')
    
    # Filter out zero or negative customer counts
    valid_bundles = valid_bundles[valid_bundles[CUSTOMERS_COL] > 0]
    
    # Sort by customer count descending and get top 20
    top_bundles = valid_bundles.nlargest(20, CUSTOMERS_COL)
else:
    top_bundles = df_bundles.head(20)

if len(top_bundles) > 0:
    for idx, row in top_bundles.iterrows():
        part1 = row[PART1_COL] if PART1_COL else 'N/A'
        part2 = row[PART2_COL] if PART2_COL else 'N/A'
        customers = int(row[CUSTOMERS_COL]) if CUSTOMERS_COL and pd.notna(row[CUSTOMERS_COL]) else 0
        
        # Get descriptions if available
        desc1 = row[DESC1_COL] if DESC1_COL and pd.notna(row[DESC1_COL]) else None
        desc2 = row[DESC2_COL] if DESC2_COL and pd.notna(row[DESC2_COL]) else None
        
        # Build display text
        if desc1 and desc2:
            st.markdown(f"""
            **{part1}** - {desc1}  
            **{part2}** - {desc2}  
            {customers} customers
            """)
        elif desc1 or desc2:
            part1_display = f"**{part1}** - {desc1}" if desc1 else f"**{part1}**"
            part2_display = f"**{part2}** - {desc2}" if desc2 else f"**{part2}**"
            st.markdown(f"""
            {part1_display}  
            {part2_display}  
            {customers} customers
            """)
        else:
            st.markdown(f"""
            **{part1} + {part2}**  
            {customers} customers
            """)
        st.markdown("---")
else:
    st.info("No compatible parts with customer data available.")
