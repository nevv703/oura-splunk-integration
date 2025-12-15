#!/usr/bin/env python3
"""
Oura Ring to Splunk Integration Script

Fetches data from the Oura API and sends it to Splunk via HTTP Event Collector (HEC).
"""

import os
import requests
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class OuraClient:
    """Client for interacting with the Oura API."""

    BASE_URL = "https://api.ouraring.com/v2/usercollection"

    def __init__(self, api_token: str):
        self.api_token = api_token
        self.headers = {
            "Authorization": f"Bearer {api_token}"
        }

    def get_sleep_data(self, start_date: str, end_date: str) -> List[Dict]:
        """Fetch sleep data for the specified date range."""
        url = f"{self.BASE_URL}/sleep"
        params = {
            "start_date": start_date,
            "end_date": end_date
        }
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json().get("data", [])

    def get_daily_activity(self, start_date: str, end_date: str) -> List[Dict]:
        """Fetch daily activity data for the specified date range."""
        url = f"{self.BASE_URL}/daily_activity"
        params = {
            "start_date": start_date,
            "end_date": end_date
        }
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json().get("data", [])

    def get_daily_readiness(self, start_date: str, end_date: str) -> List[Dict]:
        """Fetch daily readiness data for the specified date range."""
        url = f"{self.BASE_URL}/daily_readiness"
        params = {
            "start_date": start_date,
            "end_date": end_date
        }
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json().get("data", [])

    def get_heart_rate(self, start_datetime: str, end_datetime: str) -> List[Dict]:
        """Fetch heart rate data for the specified datetime range."""
        url = f"{self.BASE_URL}/heartrate"
        params = {
            "start_datetime": start_datetime,
            "end_datetime": end_datetime
        }
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json().get("data", [])

    def get_workouts(self, start_date: str, end_date: str) -> List[Dict]:
        """Fetch workout data for the specified date range."""
        url = f"{self.BASE_URL}/workout"
        params = {
            "start_date": start_date,
            "end_date": end_date
        }
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json().get("data", [])


class SplunkHEC:
    """Client for sending data to Splunk via HTTP Event Collector."""

    def __init__(self, hec_url: str, hec_token: str, index: str = "main"):
        self.hec_url = hec_url
        self.hec_token = hec_token
        self.index = index
        self.headers = {
            "Authorization": f"Splunk {hec_token}",
            "Content-Type": "application/json"
        }

    def send_event(self, event_data: Dict, sourcetype: str, source: str = "oura_api") -> bool:
        """Send a single event to Splunk HEC."""
        event = {
            "time": datetime.now().timestamp(),
            "host": "oura-integration",
            "source": source,
            "sourcetype": sourcetype,
            "index": self.index,
            "event": event_data
        }

        response = requests.post(
            self.hec_url,
            headers=self.headers,
            json=event,
            verify=True
        )

        if response.status_code == 200:
            return True
        else:
            print(f"Error sending event to Splunk: {response.status_code} - {response.text}")
            return False

    def send_events_batch(self, events: List[Dict], sourcetype: str, source: str = "oura_api") -> bool:
        """Send multiple events to Splunk HEC in a batch."""
        success_count = 0
        for event_data in events:
            if self.send_event(event_data, sourcetype, source):
                success_count += 1

        print(f"Sent {success_count}/{len(events)} events to Splunk")
        return success_count == len(events)


def main():
    """Main execution function."""

    # Load configuration
    oura_token = os.getenv("OURA_API_TOKEN")
    splunk_hec_url = os.getenv("SPLUNK_HEC_URL")
    splunk_hec_token = os.getenv("SPLUNK_HEC_TOKEN")
    splunk_index = os.getenv("SPLUNK_INDEX", "oura_data")

    if not all([oura_token, splunk_hec_url, splunk_hec_token]):
        print("Error: Missing required environment variables")
        print("Please ensure OURA_API_TOKEN, SPLUNK_HEC_URL, and SPLUNK_HEC_TOKEN are set")
        return

    # Initialize clients
    oura = OuraClient(oura_token)
    splunk = SplunkHEC(splunk_hec_url, splunk_hec_token, splunk_index)

    # Define date range (last 7 days)
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=7)

    start_date_str = start_date.isoformat()
    end_date_str = end_date.isoformat()

    print(f"Fetching Oura data from {start_date_str} to {end_date_str}")

    try:
        # Fetch and send sleep data
        print("Fetching sleep data...")
        sleep_data = oura.get_sleep_data(start_date_str, end_date_str)
        if sleep_data:
            print(f"Sending {len(sleep_data)} sleep records to Splunk...")
            splunk.send_events_batch(sleep_data, "oura:sleep")

        # Fetch and send daily activity data
        print("Fetching daily activity data...")
        activity_data = oura.get_daily_activity(start_date_str, end_date_str)
        if activity_data:
            print(f"Sending {len(activity_data)} activity records to Splunk...")
            splunk.send_events_batch(activity_data, "oura:activity")

        # Fetch and send daily readiness data
        print("Fetching daily readiness data...")
        readiness_data = oura.get_daily_readiness(start_date_str, end_date_str)
        if readiness_data:
            print(f"Sending {len(readiness_data)} readiness records to Splunk...")
            splunk.send_events_batch(readiness_data, "oura:readiness")

        # Fetch and send workout data
        print("Fetching workout data...")
        workout_data = oura.get_workouts(start_date_str, end_date_str)
        if workout_data:
            print(f"Sending {len(workout_data)} workout records to Splunk...")
            splunk.send_events_batch(workout_data, "oura:workout")

        print("Data sync completed successfully!")

    except requests.exceptions.RequestException as e:
        print(f"Error during data sync: {e}")
        return
    except Exception as e:
        print(f"Unexpected error: {e}")
        return


if __name__ == "__main__":
    main()
