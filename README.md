# Oura Ring to Splunk Integration

This project integrates Oura Ring health and activity data into Splunk for analysis and visualization.

## Overview

This integration fetches data from the Oura API and sends it to Splunk for indexing and analysis. It supports various Oura data types including:
- Sleep data
- Activity data
- Readiness scores
- Heart rate
- Workouts

## Prerequisites

- Python 3.8+
- Oura Ring and API access token
- Splunk instance with HTTP Event Collector (HEC) enabled
- Personal Access Token from Oura Cloud API

## Setup

### 1. Oura API Access

1. Go to [Oura Cloud](https://cloud.ouraring.com/personal-access-tokens)
2. Generate a Personal Access Token
3. Copy the token for use in configuration

### 2. Splunk HEC Configuration

1. In Splunk, go to Settings > Data Inputs > HTTP Event Collector
2. Create a new token or use an existing one
3. Note the token value and HEC endpoint URL

### 3. Environment Configuration

Create a `.env` file in the project root:

```env
OURA_API_TOKEN=your_oura_api_token_here
SPLUNK_HEC_TOKEN=your_splunk_hec_token_here
SPLUNK_HEC_URL=https://your-splunk-instance:8088/services/collector
SPLUNK_INDEX=oura_data
```

### 4. Install Dependencies

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

### Fetch and Send Data to Splunk

```bash
cd /Users/nefarooq/oura-splunk-integration
source venv/bin/activate
python oura_to_splunk.py
```

### Schedule Regular Updates (Automated Daily Sync)

**Option 1: Automated Setup (Recommended)**

The cron job can be added with one command:

```bash
(crontab -l 2>/dev/null; echo "0 6 * * * /Users/nefarooq/oura-splunk-integration/run_sync.sh") | crontab -
```

Verify it was added:
```bash
crontab -l
```

**Option 2: Manual Setup**

1. Open crontab editor:
```bash
crontab -e
```

2. Add this line (press `i` to insert, then `ESC` and `:wq` to save):
```
0 6 * * * /Users/nefarooq/oura-splunk-integration/run_sync.sh
```

**Manual Sync Anytime:**

```bash
cd /Users/nefarooq/oura-splunk-integration
./run_sync.sh
```

**View Logs:**

```bash
tail -f sync.log
```

The script runs daily at 6 AM, fetching the last 7 days of data. Logs are saved to `sync.log` in the project directory.

## Data Structure

Data is sent to Splunk in JSON format with the following structure:

```json
{
  "sourcetype": "oura:sleep",
  "data_type": "sleep",
  "timestamp": "2025-12-15T06:00:00Z",
  "score": 85,
  "...": "additional fields"
}
```

## Splunk Queries

Example queries for analyzing Oura data:

```spl
# View all sleep data
index=oura_data sourcetype="oura:sleep"

# Calculate average sleep score over time
index=oura_data sourcetype="oura:sleep"
| timechart avg(score) as "Average Sleep Score"

# View readiness trends
index=oura_data sourcetype="oura:readiness"
| timechart avg(score) as "Readiness Score"

# Activity summary
index=oura_data sourcetype="oura:activity"
| timechart avg(steps) as Steps, avg(active_calories) as Calories
```

## Dashboards and Alerts

### Import Dashboard

A pre-built dashboard is included in `splunk_dashboard.xml`. To import:

1. In Splunk, go to **Dashboards** → **Create New Dashboard**
2. Choose **Source** as the creation method
3. Copy the contents of `splunk_dashboard.xml`
4. Paste and save

The dashboard includes:
- Sleep score trends
- Readiness score trends
- Activity summaries
- Workout tracking
- Average score statistics

### Set Up Alerts

See `splunk_alerts.md` for pre-configured alert examples:
- Low readiness score alerts
- Poor sleep quality alerts
- Missed sync notifications
- Activity achievement celebrations

## Files

- `oura_to_splunk.py` - Main integration script
- `config.py` - Configuration management
- `run_sync.sh` - Automated sync script
- `splunk_dashboard.xml` - Pre-built Splunk dashboard
- `splunk_alerts.md` - Alert configuration guide
- `splunk_props.conf` - Splunk data parsing configuration
- `QUICK_START.md` - 5-minute setup guide

## Troubleshooting

### No Data Showing in Splunk

1. **Check if Splunk is running:**
```bash
/Applications/Splunk/bin/splunk status
```

2. **Start Splunk if stopped:**
```bash
/Applications/Splunk/bin/splunk start
```

3. **Verify the sync ran successfully:**
```bash
tail -20 sync.log
```

4. **Run manual sync to test:**
```bash
cd /Users/nefarooq/oura-splunk-integration
./run_sync.sh
```

### SSL Certificate Errors

The integration is configured to work with local Splunk's self-signed certificate (`verify=False` in the code). For production use, consider:
- Using HTTP instead of HTTPS for local Splunk
- Or properly configuring SSL certificates

### Oura Data Not Available

- Oura Ring must be synced with the Oura mobile app first
- Data can take 1-24 hours to appear in Oura Cloud API
- Check your Oura app to ensure data is there

### Cron Job Not Running

1. **Verify cron job exists:**
```bash
crontab -l
```

2. **Check Terminal has Full Disk Access:**
- System Settings → Privacy & Security → Full Disk Access
- Add Terminal to the list

3. **Test the script manually:**
```bash
/Users/nefarooq/oura-splunk-integration/run_sync.sh
```

## Accessing Your Dashboard

- **Splunk Web Interface:** http://127.0.0.1:8000
- **GitHub Repository:** https://github.com/nevv703/oura-splunk-integration

## License

MIT License

## Contributing

Feel free to open issues or submit pull requests for improvements.
