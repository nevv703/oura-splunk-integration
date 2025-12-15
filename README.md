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
pip install -r requirements.txt
```

## Usage

### Fetch and Send Data to Splunk

```bash
python oura_to_splunk.py
```

### Schedule Regular Updates

Use cron (Linux/Mac) or Task Scheduler (Windows) to run the script periodically:

```bash
# Example cron entry for daily execution at 6 AM
0 6 * * * /path/to/python /path/to/oura_to_splunk.py
```

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
```

## License

MIT License

## Contributing

Feel free to open issues or submit pull requests for improvements.
