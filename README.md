# Discount Code Manager Documentation

A Streamlit web application for generating, managing, and redeeming four-character alphanumeric discount codes with Google Sheets integration for persistent storage.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Deployment](#deployment)
- [Usage Guide](#usage-guide)
- [Troubleshooting](#troubleshooting)
- [Security Considerations](#security-considerations)

---

## Overview

This application provides a secure way to manage discount codes for your business. It features:
- A public interface for customers to check and redeem codes
- A password-protected admin panel for generating and monitoring codes
- Google Sheets backend for reliable, persistent storage
- Real-time updates and tracking of redemption status

---

## Features

### Public Interface
- **Code Validation**: Check if a discount code is valid and available
- **Code Redemption**: Redeem codes with instant feedback
- **User-Friendly**: Simple, clean interface with clear error messages

### Admin Panel
- **Bulk Code Generation**: Generate up to 1,000 unique codes at once
- **Code Monitoring**: View all codes with their redemption status
- **Statistics Dashboard**: Track total, available, and redeemed codes
- **Filtering**: Filter codes by availability status
- **Timestamping**: Automatic tracking of redemption date/time
- **Data Export**: Download all codes as JSON
- **Batch Operations**: Delete all codes with confirmation prompt

---

## Prerequisites

### Required Accounts & Services
1. **Google Account** - For Google Cloud Console and Google Sheets
2. **Google Cloud Project** - With billing enabled (free tier is sufficient)
3. **Streamlit Account** (optional) - For cloud deployment at share.streamlit.io

### Required APIs
- Google Sheets API
- Google Drive API

---

## Installation

### 1. Clone or Download the Application

Save the application code as `app.py`.

### 2. Install Dependencies

Create a `requirements.txt` file:
```txt
streamlit
gspread
google-auth
```

Install dependencies:
```bash
pip install -r requirements.txt
```

---

## Configuration

### Step 1: Set Up Google Cloud Project

#### Create a Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Select a project" → "New Project"
3. Enter a project name (e.g., "discount-codes")
4. Click "Create"

#### Enable Required APIs
1. In your project, go to "APIs & Services" → "Library"
2. Search for and enable:
   - **Google Sheets API**
   - **Google Drive API**

### Step 2: Create Service Account

#### Create the Account
1. Go to "IAM & Admin" → "Service Accounts"
2. Click "Create Service Account"
3. Enter a name (e.g., "discount-code-manager")
4. Click "Create and Continue"
5. Skip optional steps and click "Done"

#### Generate Credentials
1. Click on your new service account
2. Go to the "Keys" tab
3. Click "Add Key" → "Create new key"
4. Select "JSON" format
5. Click "Create"
6. **Save the downloaded JSON file securely** (you'll need it for configuration)

### Step 3: Set Up Google Sheet

#### Create the Spreadsheet
1. Create a new Google Sheet
2. Copy the spreadsheet URL from your browser
   - Example: `https://docs.google.com/spreadsheets/d/1f7jO6y9KxhXMdMEGV3s_VZNrks8Y1yTIVHFGknTJmDs/edit`

#### Share with Service Account
1. Click the "Share" button in your Google Sheet
2. Paste your service account email (found in the JSON file)
   - Format: `your-service-account@your-project.iam.gserviceaccount.com`
3. Give it **Editor** permissions
4. **Uncheck** "Notify people" (it's a bot account)
5. Click "Share"

### Step 4: Configure Streamlit Secrets

#### For Local Development

Create `.streamlit/secrets.toml` in your project directory:

```toml
admin_password = "your_secure_password_here"
spreadsheet_url = "https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID"

[gcp_service_account]
type = "service_account"
project_id = "your-project-id"
private_key_id = "your-private-key-id"
private_key = "-----BEGIN PRIVATE KEY-----\nYour private key here\n-----END PRIVATE KEY-----\n"
client_email = "your-service-account@your-project.iam.gserviceaccount.com"
client_id = "your-client-id"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "your-cert-url"
```

**Important Notes:**
- Copy values from your downloaded JSON service account file
- Remove `/edit` from the end of your spreadsheet URL
- Choose a strong admin password
- **Never commit this file to version control!**

#### Configuration Values

| Key | Description | Example |
|-----|-------------|---------|
| `admin_password` | Password for admin panel access | `"MySecurePass123!"` |
| `spreadsheet_url` | Your Google Sheet URL (without `/edit`) | `"https://docs.google.com/spreadsheets/d/ABC123..."` |
| `gcp_service_account` | All fields from your service account JSON file | See JSON file |

---

## Deployment

### Local Deployment

Run the application locally:
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

### Streamlit Cloud Deployment

#### Step 1: Prepare Repository
1. Create a new GitHub repository
2. Add these files:
   - `app.py` (your application code)
   - `requirements.txt`
   - `.gitignore` (add `.streamlit/` to ignore secrets)
3. **DO NOT** commit your `secrets.toml` file
4. Push to GitHub

#### Step 2: Deploy on Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click "New app"
4. Select your repository and branch
5. Set main file path to `app.py`

#### Step 3: Configure Secrets
1. Click "Advanced settings"
2. In the "Secrets" section, paste your entire `secrets.toml` content
3. Click "Deploy"

Your app will be live at: `https://your-app-name.streamlit.app`

---

## Usage Guide

### For Customers (Public Interface)

#### Checking a Code
1. Go to the "Check Code" tab
2. Enter the 4-character code
3. Click "Check Code"
4. You'll see if the code is valid, invalid, or already redeemed

#### Redeeming a Code
1. Enter the 4-character code
2. Click "Redeem Code"
3. If valid, you'll see a success message with balloons 🎉
4. The code will be marked as redeemed and cannot be used again

### For Administrators

#### Logging In
1. Go to the "Admin" tab
2. Enter your admin password
3. Click "Login"

#### Generating Codes
1. In the admin panel, find "Generate New Codes"
2. Enter the number of codes you want (1-1000)
3. Click "Generate"
4. Codes are generated instantly and added to Google Sheets

#### Viewing All Codes
- **Statistics**: See total, available, and redeemed code counts
- **Filter Options**: View all codes, only available, or only redeemed
- **Code Display**: Grid view showing each code and its status
- **Timestamps**: Redeemed codes show when they were used

#### Refreshing Code List
Click the "Refresh" button to reload codes from Google Sheets

#### Downloading Codes
Click "Download Codes as JSON" to export all codes and their status

#### Deleting All Codes
1. Scroll to "Danger Zone"
2. Click "Delete All Codes"
3. Click again to confirm
4. All codes will be permanently deleted

---

## Troubleshooting

### Connection Issues

**Error: "Unable to connect to Google Sheets"**

Possible causes and solutions:

1. **APIs not enabled**
   - Go to Google Cloud Console
   - Enable Google Sheets API and Google Drive API

2. **Sheet not shared with service account**
   - Open your Google Sheet
   - Share it with the service account email
   - Give Editor permissions

3. **Wrong spreadsheet URL**
   - Remove `/edit` from the end of the URL
   - Ensure the URL is complete and correct

4. **Invalid credentials**
   - Verify all values in `secrets.toml` match your JSON file
   - Check that private key includes newlines (`\n`)

### Rate Limit Errors

**Error: "Quota exceeded for quota metric 'Write requests'"**

- The app uses batch operations to avoid this
- If you still encounter it, wait 60 seconds and try again
- Google Sheets allows 60 write requests per minute

### Authentication Issues

**Error: "Incorrect password"**

- Verify the password in your `secrets.toml` file
- Passwords are case-sensitive
- Clear browser cache if issues persist

### Code Generation Issues

**Warning: "Could not generate unique codes"**

- You may be trying to generate too many codes
- The system uses 4-character alphanumeric codes (1,296 possible combinations)
- If you need more than ~1,000 codes, consider upgrading to 5-character codes

---

## Security Considerations

### Password Security
- Use a strong admin password (mix of letters, numbers, symbols)
- Change the default password immediately
- Never share the admin password
- Consider using a password manager

### Credential Management
- **Never** commit `secrets.toml` to version control
- Add `.streamlit/` to your `.gitignore` file
- Keep your service account JSON file secure
- Rotate credentials periodically

### Access Control
- The service account only has access to the specific sheet you shared
- You can revoke access anytime by removing the service account from sheet sharing
- Monitor Google Cloud Console for unusual API activity

### Data Privacy
- Codes are stored in your own Google Sheet
- Only you and authorized service accounts can access the data
- Consider the sensitivity of your discount codes when choosing deployment

### Production Recommendations
1. Use environment-specific passwords (dev vs production)
2. Enable 2-factor authentication on your Google account
3. Regularly audit who has access to your Google Sheet
4. Monitor redemption patterns for suspicious activity
5. Consider implementing rate limiting for code checks
6. Set up alerting for unusual API usage

---

## Google Sheets Structure

The application automatically creates and maintains this structure:

| Column | Data Type | Description |
|--------|-----------|-------------|
| Code | String | 4-character alphanumeric code |
| Redeemed | String | "True" or "False" |
| Redeemed At | String | Timestamp (YYYY-MM-DD HH:MM:SS) |

### Manual Sheet Management

You can manually edit the sheet:
- Add codes directly (ensure unique 4-character codes)
- Mark codes as redeemed by changing "False" to "True"
- View redemption timestamps
- Export data using Google Sheets' built-in export

**Warning**: Editing the header row may break the application.

---

## API Rate Limits

### Google Sheets API Quotas (Free Tier)
- **Read requests**: 300 per minute per project
- **Write requests**: 60 per minute per user
- **Read requests per day**: 50,000 per project

### How the App Handles Limits
- Uses batch operations for code generation (1 write for multiple codes)
- Efficient data loading with minimal API calls
- Caches data in session state where appropriate

### If You Hit Limits
- Wait 60 seconds for write quota to reset
- Consider upgrading your Google Cloud project for higher quotas
- Reduce frequency of refresh operations

---

## Support and Maintenance

### Regular Maintenance Tasks
1. **Weekly**: Review redeemed codes and statistics
2. **Monthly**: Backup your Google Sheet
3. **Quarterly**: Audit access permissions
4. **As Needed**: Generate new batches of codes

### Backup Procedures
1. Use the "Download Codes as JSON" feature
2. Or use Google Sheets' File → Download feature
3. Store backups securely
4. Test restoration procedures periodically

### Updating the Application
1. Pull latest code changes
2. Check for new dependencies in `requirements.txt`
3. Test in local environment first
4. Deploy updates to Streamlit Cloud
5. Verify functionality after deployment

---

## Technical Details

### Technology Stack
- **Frontend**: Streamlit (Python web framework)
- **Backend Storage**: Google Sheets API
- **Authentication**: Google Service Account
- **Deployment**: Streamlit Cloud (or self-hosted)

### Code Generation Algorithm
- Uses uppercase letters (A-Z) and digits (0-9)
- Generates 4-character combinations
- Validates uniqueness against existing codes
- Maximum attempts: requested codes × 100

### Data Flow
1. User interacts with Streamlit interface
2. App authenticates with Google Sheets via service account
3. Operations performed through gspread library
4. Changes immediately reflected in Google Sheet
5. Interface updates on successful operations

---

## Frequently Asked Questions

**Q: Can I customize the code length?**  
A: Yes, modify the `generate_code()` function and change the `k=4` parameter.

**Q: Can multiple admins access the panel?**  
A: Yes, share the admin password securely. All admins use the same password.

**Q: What happens if two people redeem the same code simultaneously?**  
A: The first redemption wins. The second will see "already redeemed."

**Q: Can I use this for thousands of codes?**  
A: Yes, but consider increasing code length beyond 4 characters for better scalability.

**Q: Is this suitable for high-traffic usage?**  
A: For moderate traffic, yes. For very high traffic, consider upgrading to a dedicated database.

**Q: Can I track who redeemed each code?**  
A: Not currently, but you can extend the app to collect user information during redemption.

**Q: How do I change the admin password?**  
A: Update the `admin_password` value in your `secrets.toml` file and redeploy.

---

## License and Credits

This application is provided as-is for business use. Ensure compliance with your local regulations regarding discount codes and promotions.

**Built with:**
- Streamlit
- Google Sheets API
- gspread library
- google-auth library

---

## Changelog

### Version 1.0
- Initial release
- Basic code generation and redemption
- Google Sheets integration
- Admin panel with authentication
- Batch operations for rate limit handling
- Timestamp tracking for redemptions

---

*For additional support or feature requests, please refer to your development team or the application maintainer.*
