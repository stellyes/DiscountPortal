import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import random
import string
from datetime import datetime

# Configuration
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

# Get admin password from Streamlit secrets
try:
    ADMIN_PASSWORD = st.secrets["admin_password"]
except:
    st.error("⚠️ Admin password not configured in secrets!")
    ADMIN_PASSWORD = "admin123"  # Fallback for local testing

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'sheet' not in st.session_state:
    st.session_state.sheet = None

# Helper functions
def connect_to_sheet():
    """Connect to Google Sheets"""
    try:
        # Get credentials from Streamlit secrets
        creds_dict = st.secrets["gcp_service_account"]
        creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
        client = gspread.authorize(creds)
        
        # Open the spreadsheet (you can use sheet URL or name)
        spreadsheet_url = st.secrets["spreadsheet_url"]
        sheet = client.open_by_url(spreadsheet_url).sheet1
        
        # Initialize headers if empty or update if needed
        headers = sheet.row_values(1)
        if not headers:
            sheet.append_row(['Code', 'Deal', 'Redeemed', 'Redeemed At'])
        elif 'Deal' not in headers:
            # Migrate existing sheet by inserting Deal column
            sheet.insert_cols([['']] * sheet.row_count, col=2)
            sheet.update_cell(1, 2, 'Deal')
        
        return sheet
    except Exception as e:
        st.error(f"Error connecting to Google Sheets: {str(e)}")
        return None

def load_codes(sheet):
    """Load all codes from Google Sheets"""
    try:
        records = sheet.get_all_records()
        codes = {}
        for record in records:
            # Handle different types for Redeemed field
            redeemed_value = record.get('Redeemed', False)
            if isinstance(redeemed_value, str):
                redeemed = redeemed_value.lower() == 'true'
            elif isinstance(redeemed_value, bool):
                redeemed = redeemed_value
            else:
                redeemed = False
            
            codes[str(record['Code'])] = {
                'code': str(record['Code']),
                'deal': str(record.get('Deal', '')),
                'redeemed': redeemed,
                'redeemed_at': str(record.get('Redeemed At', ''))
            }
        return codes
    except Exception as e:
        st.error(f"Error loading codes: {str(e)}")
        return {}

def save_code(sheet, code, deal='', redeemed=False, redeemed_at=''):
    """Add a new code to Google Sheets"""
    try:
        # Convert boolean to string for consistent storage
        sheet.append_row([str(code), str(deal), str(redeemed), str(redeemed_at)])
        return True
    except Exception as e:
        st.error(f"Error saving code: {str(e)}")
        return False

def save_codes_batch(sheet, codes_list, deal=''):
    """Add multiple codes to Google Sheets in a single batch operation"""
    try:
        # Prepare rows for batch insert
        rows = [[str(code), str(deal), 'False', ''] for code in codes_list]
        # Append all rows at once
        sheet.append_rows(rows)
        return True
    except Exception as e:
        st.error(f"Error saving codes in batch: {str(e)}")
        return False

def update_code_status(sheet, code, redeemed=True):
    """Update code redemption status"""
    try:
        cell = sheet.find(str(code))
        if cell:
            row = cell.row
            sheet.update_cell(row, 3, str(redeemed))  # Update Redeemed column (now column 3)
            if redeemed:
                sheet.update_cell(row, 4, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))  # Update timestamp
            else:
                sheet.update_cell(row, 4, '')  # Clear timestamp when unredeemed
            return True
        return False
    except Exception as e:
        st.error(f"Error updating code: {str(e)}")
        return False

def generate_code():
    """Generate a random 8-character alphanumeric code in format XXXX-XXXX"""
    part1 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    part2 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f"{part1}-{part2}"

def generate_unique_codes(num_codes, existing_codes):
    """Generate unique codes that don't already exist"""
    new_codes = []
    attempts = 0
    max_attempts = num_codes * 100
    
    while len(new_codes) < num_codes and attempts < max_attempts:
        attempts += 1
        code = generate_code()
        if code not in existing_codes and code not in new_codes:
            new_codes.append(code)
    
    return new_codes

def delete_all_codes(sheet):
    """Delete all codes from sheet (except header)"""
    try:
        # Delete all rows except the header
        num_rows = len(sheet.get_all_values())
        if num_rows > 1:
            sheet.delete_rows(2, num_rows)
        return True
    except Exception as e:
        st.error(f"Error deleting codes: {str(e)}")
        return False

# Page config
st.set_page_config(
    page_title="Discount Code Manager",
    page_icon="🎟️",
    layout="centered"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .code-box {
        padding: 1rem;
        border-radius: 8px;
        border: 2px solid #e0e0e0;
        margin: 0.5rem 0;
    }
    .code-redeemed {
        background-color: #f5f5f5;
        border-color: #d0d0d0;
        color: #666;
    }
    .code-available {
        background-color: #e8f5e9;
        border-color: #4caf50;
        color: #2e7d32;
    }
    .deal-info {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 4px;
    }
    </style>
""", unsafe_allow_html=True)

# Connect to Google Sheets
if st.session_state.sheet is None:
    with st.spinner("Connecting to Google Sheets..."):
        st.session_state.sheet = connect_to_sheet()

sheet = st.session_state.sheet

if sheet is None:
    st.error("❌ Unable to connect to Google Sheets. Please check your configuration.")
    st.stop()

# Header
st.markdown("""
    <div class="main-header">
        <h1>🎟️ Discount Code Manager</h1>
        <p>Manage and redeem discount codes with Google Sheets</p>
    </div>
""", unsafe_allow_html=True)

# Tab selection
tab1, tab2 = st.tabs(["🔍 Check Code", "⚙️ Admin"])

# TAB 1: Check Code
with tab1:
    st.subheader("Check or Redeem a Code")
    
    code_input = st.text_input(
        "Enter your discount code:",
        max_chars=9,
        placeholder="XXXX-XXXX",
        key="code_input"
    ).upper()
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔍 Check Code", use_container_width=True):
            if not code_input:
                st.error("Please enter a code")
            else:
                with st.spinner("Checking..."):
                    codes = load_codes(sheet)
                    if code_input not in codes:
                        st.error("❌ Invalid code")
                    elif codes[code_input]["redeemed"]:
                        st.warning("⚠️ This code has already been redeemed")
                        # Still show deal info for redeemed codes
                        if codes[code_input]["deal"]:
                            st.markdown(f"""
                                <div class="deal-info">
                                    <strong>💼 Deal:</strong> {codes[code_input]["deal"]}
                                </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.success("✅ Valid code! Ready to redeem.")
                        # Show deal information
                        if codes[code_input]["deal"]:
                            st.markdown(f"""
                                <div class="deal-info">
                                    <strong>💼 Deal:</strong> {codes[code_input]["deal"]}
                                </div>
                            """, unsafe_allow_html=True)
    
    with col2:
        if st.button("✨ Redeem Code", use_container_width=True, type="primary"):
            if not code_input:
                st.error("Please enter a code")
            else:
                with st.spinner("Redeeming..."):
                    codes = load_codes(sheet)
                    if code_input not in codes:
                        st.error("❌ Invalid code")
                    elif codes[code_input]["redeemed"]:
                        st.warning("⚠️ This code has already been redeemed")
                    else:
                        if update_code_status(sheet, code_input, True):
                            st.success("🎉 Code successfully redeemed!")
                            # Show deal information
                            if codes[code_input]["deal"]:
                                st.markdown(f"""
                                    <div class="deal-info">
                                        <strong>💼 Deal:</strong> {codes[code_input]["deal"]}
                                    </div>
                                """, unsafe_allow_html=True)
                            st.balloons()
                        else:
                            st.error("Error redeeming code. Please try again.")

# TAB 2: Admin
with tab2:
    if not st.session_state.authenticated:
        st.subheader("🔒 Admin Access Required")
        
        password_input = st.text_input(
            "Enter admin password:",
            type="password",
            key="password_input"
        )
        
        if st.button("Login", type="primary"):
            if password_input == ADMIN_PASSWORD:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("❌ Incorrect password")
    
    else:
        st.subheader("🔓 Admin Panel")
        
        if st.button("Logout", key="logout"):
            st.session_state.authenticated = False
            st.rerun()
        
        st.markdown("---")
        
        # Generate codes section
        st.subheader("Generate New Codes")
        
        deal_input = st.text_input(
            "Deal/Promotion Description (optional):",
            placeholder="e.g., 20% off all items, Free shipping",
            key="deal_input"
        )
        
        col1, col2 = st.columns([2, 1])
        with col1:
            num_codes = st.number_input(
                "Number of codes to generate:",
                min_value=1,
                max_value=1000,
                value=10,
                step=1
            )
        
        with col2:
            st.write("")  # Spacing
            st.write("")  # Spacing
            if st.button("➕ Generate", use_container_width=True, type="primary"):
                with st.spinner(f"Generating {num_codes} codes..."):
                    codes = load_codes(sheet)
                    new_codes = generate_unique_codes(num_codes, codes.keys())
                    
                    # Add codes to sheet using batch operation
                    if new_codes:
                        if save_codes_batch(sheet, new_codes, deal_input):
                            st.success(f"✅ Generated {len(new_codes)} new codes!")
                            st.rerun()
                        else:
                            st.error("Failed to generate codes")
                    else:
                        st.warning("Could not generate unique codes. Try a smaller number.")
        
        st.markdown("---")
        
        # View all codes section
        st.subheader("All Codes")
        
        if st.button("🔄 Refresh", key="refresh_codes"):
            st.rerun()
        
        with st.spinner("Loading codes..."):
            codes = load_codes(sheet)
        
        if not codes:
            st.info("No codes generated yet. Create some codes to get started!")
        else:
            # Statistics
            total_codes = len(codes)
            redeemed_codes = sum(1 for c in codes.values() if c["redeemed"])
            available_codes = total_codes - redeemed_codes
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Codes", total_codes)
            col2.metric("Available", available_codes)
            col3.metric("Redeemed", redeemed_codes)
            
            st.markdown("---")
            
            # Filter options
            filter_option = st.radio(
                "Filter:",
                ["All", "Available Only", "Redeemed Only"],
                horizontal=True
            )
            
            # Display codes
            filtered_codes = {
                k: v for k, v in codes.items()
                if filter_option == "All"
                or (filter_option == "Available Only" and not v["redeemed"])
                or (filter_option == "Redeemed Only" and v["redeemed"])
            }
            
            if filtered_codes:
                # Display codes with reinvoke option
                for code, data in sorted(filtered_codes.items()):
                    status = "Redeemed" if data["redeemed"] else "Available"
                    css_class = "code-redeemed" if data["redeemed"] else "code-available"
                    
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        redeemed_info = ""
                        if data["redeemed"] and data.get("redeemed_at"):
                            redeemed_info = f"<div style='font-size: 0.8em; margin-top: 0.3rem; color: #666;'>Redeemed: {data['redeemed_at']}</div>"
                        
                        deal_info = ""
                        if data.get("deal"):
                            deal_info = f"<div style='font-size: 0.85em; margin-top: 0.3rem; color: #1976d2;'>💼 {data['deal']}</div>"
                        
                        st.markdown(f"""
                            <div class="code-box {css_class}">
                                <div style="font-size: 1.2em; font-weight: bold; font-family: monospace;">
                                    {code}
                                </div>
                                <div style="font-size: 0.8em; margin-top: 0.3rem;">
                                    Status: {status}
                                </div>
                                {deal_info}
                                {redeemed_info}
                            </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        # Show reinvoke button only for redeemed codes
                        if data["redeemed"]:
                            if st.button("🔄 Reinvoke", key=f"reinvoke_{code}", use_container_width=True):
                                with st.spinner(f"Reinvoking {code}..."):
                                    if update_code_status(sheet, code, False):
                                        st.success(f"✅ Code {code} has been reinstated!")
                                        st.rerun()
                                    else:
                                        st.error(f"Error reinvoking {code}")
                        else:
                            st.write("")  # Spacing for alignment
            else:
                st.info("No codes match the selected filter.")
            
            # Delete all codes (dangerous action)
            st.markdown("---")
            st.subheader("⚠️ Danger Zone")
            
            if st.button("🗑️ Delete All Codes", type="secondary"):
                if st.session_state.get('confirm_delete'):
                    with st.spinner("Deleting all codes..."):
                        if delete_all_codes(sheet):
                            st.session_state.confirm_delete = False
                            st.success("All codes deleted!")
                            st.rerun()
                        else:
                            st.error("Failed to delete codes")
                else:
                    st.session_state.confirm_delete = True
                    st.warning("⚠️ Click again to confirm deletion of ALL codes!")
            
            if st.session_state.get('confirm_delete') and st.button("Cancel"):
                st.session_state.confirm_delete = False
                st.rerun()

# Footer
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.8em;">
        <p>💡 Codes are stored in Google Sheets for persistence</p>
        <p>🔐 Admin password configured via Streamlit secrets</p>
        <p>💼 Associate deals with code batches for better tracking</p>
    </div>
""", unsafe_allow_html=True)
