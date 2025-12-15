#!/bin/bash
cd /Users/nefarooq/oura-splunk-integration
source venv/bin/activate
python oura_to_splunk.py >> sync.log 2>&1
