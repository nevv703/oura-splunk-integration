# Splunk Alert Configurations for Oura Ring Data

## Alert 1: Low Readiness Score

**Purpose:** Alert when readiness score drops below 60

**Configuration:**
1. In Splunk: Settings → Searches, Reports, and Alerts → New Alert
2. **Title:** Low Readiness Score Alert
3. **Search:**
```
index=oura_data sourcetype="oura:readiness" score<60
| stats latest(score) as latest_score by day
```
4. **Alert Type:** Real-time
5. **Trigger Conditions:** Number of Results is greater than 0
6. **Trigger Actions:** Send email (configure your email settings)

---

## Alert 2: Low Sleep Score

**Purpose:** Alert when sleep score is below 70 for 3 consecutive days

**Configuration:**
1. **Title:** Poor Sleep Alert
2. **Search:**
```
index=oura_data sourcetype="oura:sleep"
| stats avg(score) as avg_score by day
| where avg_score<70
```
3. **Schedule:** Run daily at 8:00 AM
4. **Trigger Conditions:** Number of Results is greater than 2
5. **Trigger Actions:** Send email notification

---

## Alert 3: Missed Daily Sync

**Purpose:** Alert if no data has been synced in the last 25 hours

**Configuration:**
1. **Title:** Oura Data Sync Failure
2. **Search:**
```
index=oura_data
| stats latest(_time) as last_sync
| eval hours_since_sync=round((now()-last_sync)/3600, 1)
| where hours_since_sync>25
```
3. **Schedule:** Run every 6 hours
4. **Trigger Conditions:** Number of Results is greater than 0
5. **Trigger Actions:** Send email notification

---

## Alert 4: High Activity Achievement

**Purpose:** Celebrate when you exceed 10,000 steps

**Configuration:**
1. **Title:** Daily Step Goal Achieved
2. **Search:**
```
index=oura_data sourcetype="oura:activity" steps>10000
| stats latest(steps) as steps by day
```
3. **Schedule:** Run daily at 9:00 PM
4. **Trigger Conditions:** Number of Results is greater than 0
5. **Trigger Actions:** Send email celebration

---

## How to Create These Alerts in Splunk

1. Go to **Settings** → **Searches, Reports, and Alerts**
2. Click **New Alert** button
3. Fill in the Title and Description
4. Enter the Search query
5. Configure the Schedule (Real-time or Scheduled)
6. Set Trigger Conditions
7. Configure Trigger Actions (Email, Webhook, etc.)
8. Click **Save**

## Email Configuration

To enable email alerts:
1. Go to **Settings** → **Server Settings** → **Email Settings**
2. Configure your SMTP server details
3. Test the email configuration
4. Apply email actions to your alerts
