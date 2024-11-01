# Cookiebot IP Address Change Checker

This Python script checks for updates to the IP addresses used by Cookiebot’s scanning service, as documented on Cookiebot’s support page. It scrapes the page for any changes in IP addresses, generates a new regex pattern, and sends a notification email if any updates are detected since the last check. This regex can be used directly in Google Analytics 4 (GA4) to filter out unwanted Cookiebot bot traffic, ensuring that analytics data more accurately reflects real user activity.

## Features

- **Automated IP Address Check**: Periodically checks for updates to Cookiebot IPs.
- **Regex Generation**: Compiles a regex pattern of current IP addresses for easy integration into GA4 filtering.
- **Email Notifications**: Sends a notification email with the updated regex if any changes are detected.
- **Centralized Management**: Optionally uses a Google Sheets document to manage links to GA4 properties, making it easier to locate and update filters for each tracked property.

## Setup

1. **Python Environment**  
   Ensure you have Python installed. You can set up a virtual environment for this script:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # For macOS/Linux
   venv\Scripts\activate     # For Windows

2. **Install Dependencies**
   Install required libraries via pip:
   bash
   pip install selenium beautifulsoup4

3. **Create the Configuration File**
   Create a secrets.json file in the same directory as the script. This file should contain:

   ```json
   {
     "address": "sender.address@gmail.com",
     "password": "16-character password",
     "receivers": "receiver.address.1@example.it, receiver.address.2@example.it",
     "sites_list_link": "https://docs.google.com/spreadsheets/d/xxxxxxxxx"
   }
   ```
   where:  
     **- address:** The sender's email (Gmail).  
     **- password:** A 16-character app-specific password for the Gmail account. To create it, it is necessary to go to the sender's email address settings and enable two-step verification, following this link. A name for
     the app must be entered in the appropriate field (e.g., “Cookiebot IP Checker”), then you must click “Create” and copy the 16-digit password that will appear.  
     **- receivers:** A comma-separated list of recipient email addresses for notifications.  
     **- sites_list_link:** A link to a Google Sheets file listing the GA4 property links for quick access when updating filters.  
   
5. **Google Sheets File**
   Prepare a Google Sheets document where each row represents a GA4 property you are managing. Include links to the GA4 Data Stream settings page, allowing you to quickly access and update IP filters across multiple
   properties. Ensure sharing permissions allow access to the relevant team members.

7. **Schedule Script Execution**
   The script can be scheduled to fire at a according to a desired frequency using tools such as Windows Task Scheduler or macOS Automator. For example, to run the script upon user login on Windows:

8. **Usage**
   Upon execution, the script will:  

   Scrape the Cookiebot support article for IP addresses.  
   Generate a regex string including all detected IP addresses.  
   Compare with the previous regex stored in last_ip_regex.txt.  
   If a change is detected or if it is the first time firing the script, update/create last_ip_regex.txt and send an email with the new regex, including a link to the Google Sheets document for easier access to the GA4
   property links.

