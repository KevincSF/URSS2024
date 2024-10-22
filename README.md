# URSS2024

This is a replication package for an URSS 2024 research project, detailed of the information would be provided in:(TO BE UPDATED)

## YouTube API Scraper and Comment Analyzer

This Python script provides a `youtubeAPI` class to interact with the YouTube Data API (v3), allowing you to:
- Retrieve videos from a playlist
- Scrape comments from videos
- Collect video metadata such as views, duration, etc.

### Prerequisites

Before using the script, you'll need to set up the following:

#### 1. **API Key** (for Public Data Access)
To interact with the YouTube Data API, you need a **YouTube Data API v3 key**.

#### 2. **OAuth 2.0 Client Credentials** (for User-Specific Data)
For more advanced requests (like accessing YouTube comments), you need OAuth credentials (a `client_secret.json` file) from Google.

### Setup

#### Step 1: Get Your YouTube Data API Key

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project or select an existing project.
3. Enable the **YouTube Data API v3** for your project:
   - Go to **APIs & Services** > **Library**.
   - Search for **YouTube Data API v3** and click **Enable**.
4. Go to **APIs & Services** > **Credentials** and create a new API key.
5. Copy your API key and store it somewhere safe. You will use this API key in the script.

#### Step 2: Set Up OAuth 2.0 Credentials

1. In the **Credentials** page of your project, click **Create Credentials** and select **OAuth 2.0 Client IDs**.
2. Set the application type to **Desktop App**.
3. Download the resulting `client_secret.json` file and save it in the same directory as your Python script.

#### Step 3: Install the Required Python Libraries

Make sure you have the following Python libraries installed:

```bash
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client isodate requests
