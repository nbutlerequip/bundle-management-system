# Unified Bundle Management System - Deployment Guide

## COMPLETE MULTI-PAGE APPLICATION

This guide will help you deploy the unified bundle management system with:
- Admin bundle analyzer with password protection
- Branch tracking portal
- Admin dashboard with all-branch monitoring

---

## FILE STRUCTURE

Your complete application structure:

```
bundle-management-system/
├── Home.py                              (Main landing page)
├── pages/
│   ├── 1_Bundle_Analyzer.py            (Admin analysis tool - password protected)
│   ├── 2_Branch_Tracking.py            (Branch login and tracking)
│   └── 3_Admin_Dashboard.py            (Admin monitoring - password protected)
├── data/
│   ├── branch_list.csv                 (18 branches)
│   ├── COMPLETE_BUNDLE_ANALYSIS_20251029_084720.csv  (Your bundle data)
│   └── bundle_sales_log.csv            (Created automatically when branches mark sales)
└── requirements.txt                     (Dependencies)
```

---

## QUICK START - LOCAL TESTING

### Step 1: Set Up Files

1. Create a new folder: `bundle-management-system`
2. Copy all files from outputs:
   - `Home.py` → main folder
   - `pages/` folder with all 3 page files → main folder
   - `requirements.txt` → main folder
3. Create `data/` folder
4. Add your data files to `data/`:
   - `branch_list.csv`
   - `COMPLETE_BUNDLE_ANALYSIS_20251029_084720.csv`

### Step 2: Install Dependencies

```bash
pip install streamlit pandas
```

### Step 3: Run the App

```bash
cd bundle-management-system
streamlit run Home.py
```

### Step 4: Test

The app will open in your browser at `http://localhost:8501`

Test each section:
- Home page navigation
- Admin pages (password: `admin123`)
- Branch login and tracking

---

## DEPLOYMENT TO STREAMLIT CLOUD

### Step 1: Prepare GitHub Repository

1. Go to GitHub and create a new repository: `bundle-management-system`
2. Clone it to your computer:
   ```bash
   git clone https://github.com/YOUR-USERNAME/bundle-management-system.git
   cd bundle-management-system
   ```

### Step 2: Add Files

1. Copy all files to the repository:
   - `Home.py`
   - `pages/` folder with all 3 pages
   - `data/` folder with your CSV files
   - `requirements.txt`

2. Commit and push:
   ```bash
   git add .
   git commit -m "Initial commit - unified bundle management system"
   git push
   ```

### Step 3: Deploy on Streamlit Cloud

1. Go to https://share.streamlit.io/
2. Click "New app"
3. Select your repository: `bundle-management-system`
4. Main file path: `Home.py`
5. Click "Deploy"

### Step 4: Wait for Deployment

- Usually takes 2-5 minutes
- You'll get a URL like: `https://bundle-management-system.streamlit.app/`

### Step 5: Share URLs

**For Branches:**
- `https://your-app.streamlit.app/Branch_Tracking`

**For Admin:**
- `https://your-app.streamlit.app/Bundle_Analyzer`
- `https://your-app.streamlit.app/Admin_Dashboard`

---

## CHANGING THE ADMIN PASSWORD

### Option 1: In Code (Simple)

1. Open `pages/1_Bundle_Analyzer.py`
2. Find line: `ADMIN_PASSWORD = "admin123"`
3. Change to your password: `ADMIN_PASSWORD = "YourSecurePassword"`
4. Open `pages/3_Admin_Dashboard.py`
5. Find line: `ADMIN_PASSWORD = "admin123"`
6. Change to same password: `ADMIN_PASSWORD = "YourSecurePassword"`
7. Commit and push to GitHub
8. Streamlit auto-redeploys

### Option 2: Using Streamlit Secrets (Recommended for Production)

1. In your repository, create `.streamlit/secrets.toml`:
   ```toml
   admin_password = "YourSecurePassword123"
   ```

2. Update both admin pages to use:
   ```python
   ADMIN_PASSWORD = st.secrets["admin_password"]
   ```

3. In Streamlit Cloud dashboard:
   - Go to app settings
   - Add secret: `admin_password = "YourSecurePassword123"`

---

## HOW THE SYSTEM WORKS

### For Admin Users

1. **Navigate to home** → Choose "Bundle Analyzer" or "Admin Dashboard"
2. **Enter password** → Access granted
3. **Bundle Analyzer:**
   - Upload data
   - View bundle analysis
   - Export reports
4. **Admin Dashboard:**
   - Monitor all 18 branches
   - View sales activity
   - Track performance
   - Export reports

### For Branch Users

1. **Navigate to home** → Choose "Branch Tracking"
2. **Select branch** from dropdown → No password needed
3. **View bundles** → Top 20 recommendations
4. **Mark as sold** → Click button when customer buys
5. **Check performance** → View branch statistics

### Data Flow

```
ADMIN:
Upload bundle data → Bundle Analyzer → CSV generated
                                          ↓
                          Automatically available to branches

BRANCHES:
Login → View bundles → Customer buys → Mark as Sold
                                          ↓
                        Saved to bundle_sales_log.csv

ADMIN:
Admin Dashboard → View all branch sales → Validate predictions
```

---

## SECURITY NOTES

### What's Protected
✅ Bundle Analyzer - requires admin password
✅ Admin Dashboard - requires admin password
✅ Branch data isolation - each branch sees only their data

### What's Not Protected
⚠️ Branch tracking portal - intentionally easy access
⚠️ Home page - public navigation

### For Production Use
- Use Streamlit Secrets for password
- Use HTTPS (automatically provided by Streamlit Cloud)
- Don't commit passwords to public GitHub repos
- Change default password (`admin123`) immediately

---

## UPDATING DATA

### To Update Bundle Analysis Data

1. Run your bundle analysis
2. Generate new CSV file
3. Replace `data/COMPLETE_BUNDLE_ANALYSIS_20251029_084720.csv`
4. Commit and push to GitHub
5. Streamlit auto-redeploys
6. New bundles immediately available to branches

### Sales Data

- Automatically created and updated
- Stored in `data/bundle_sales_log.csv`
- Updated in real-time when branches mark sales
- Download from Admin Dashboard to analyze

---

## TROUBLESHOOTING

### App Won't Start
- Check all files are in correct locations
- Verify `requirements.txt` exists
- Check for Python syntax errors in pages

### Password Not Working
- Verify password matches in both admin pages
- Check for typos
- Try clearing browser cache

### No Bundle Data
- Verify CSV file exists in `data/` folder
- Check file name matches exactly
- Try re-uploading through Bundle Analyzer

### Branches Can't Log In
- Verify `branch_list.csv` exists
- Check branch names match exactly
- Look for console errors

---

## MAINTENANCE

### Weekly
- Download sales data from Admin Dashboard
- Review branch performance
- Identify top bundles

### Monthly
- Update bundle analysis with new data
- Review and adjust password if needed
- Check system performance

### As Needed
- Add new branches to `branch_list.csv`
- Update bundle recommendations
- Export reports for stakeholders

---

## SUPPORT

### For Branch Users
Contact your branch manager or system administrator

### For Admins
- Check Streamlit Cloud logs for errors
- Review CSV file formats
- Verify all files are properly uploaded

---

## NEXT STEPS

1. ✅ Deploy the system
2. ✅ Change admin password
3. ✅ Test all three sections
4. ✅ Share branch URL with all 18 branches
5. ✅ Train branch staff on marking sales
6. ✅ Monitor Admin Dashboard weekly
7. ✅ Validate bundle predictions after 30-60 days

---

## SUCCESS METRICS

After 30 days, you'll be able to answer:

- Which bundles actually convert to sales?
- Which branches are top performers?
- What's the real conversion rate vs predictions?
- Which bundle types work best?
- What's the actual revenue impact?

This data validates your $50M bundle analysis and proves ROI!
