"""
Configuration module for Oura to Splunk integration.
"""

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class OuraConfig:
    """Configuration for Oura API."""
    api_token: str
    base_url: str = "https://api.ouraring.com/v2/usercollection"


@dataclass
class SplunkConfig:
    """Configuration for Splunk HEC."""
    hec_url: str
    hec_token: str
    index: str = "oura_data"
    verify_ssl: bool = True


@dataclass
class AppConfig:
    """Main application configuration."""
    oura: OuraConfig
    splunk: SplunkConfig
    days_to_fetch: int = 7


def load_config() -> AppConfig:
    """Load configuration from environment variables."""
    oura_config = OuraConfig(
        api_token=os.getenv("OURA_API_TOKEN", "")
    )

    splunk_config = SplunkConfig(
        hec_url=os.getenv("SPLUNK_HEC_URL", ""),
        hec_token=os.getenv("SPLUNK_HEC_TOKEN", ""),
        index=os.getenv("SPLUNK_INDEX", "oura_data"),
        verify_ssl=os.getenv("SPLUNK_VERIFY_SSL", "true").lower() == "true"
    )

    return AppConfig(
        oura=oura_config,
        splunk=splunk_config,
        days_to_fetch=int(os.getenv("DAYS_TO_FETCH", "7"))
    )
