# Quick Start Guide

## What's Been Set Up

Your Oura Ring to Splunk integration is fully configured and ready to use!

## Files Created

1. **run_sync.sh** - Automated sync script (runs daily)
2. **splunk_dashboard.xml** - Pre-built dashboard with visualizations
3. **splunk_alerts.md** - Alert configuration guide
4. **sync.log** - Log file for sync operations

## Next Steps (5 minutes)

### 1. Import the Dashboard (2 min)

1. Open Splunk: http://127.0.0.1:8000
2. Go to **Dashboards** → **Create New Dashboard**
3. Click **Dashboard** → **Edit** → **Source**
4. Open `splunk_dashboard.xml` and copy all contents
5. Paste into Splunk and click **Save**
6. Name it "Oura Ring Health Dashboard"

### 2. Set Up Daily Automation (30 seconds)

Run this one command to set up automatic daily syncing at 6 AM:

```bash
(crontab -l 2>/dev/null; echo "0 6 * * * /Users/nefarooq/oura-splunk-integration/run_sync.sh") | crontab -
```

Verify it's set up:
```bash
crontab -l
```

Your data will now sync automatically every day at 6 AM!

**Note:** If cron doesn't run, you may need to give Terminal Full Disk Access in System Settings → Privacy & Security.

### 3. Create Alerts (2 min)

Choose any alerts from `splunk_alerts.md`:
1. In Splunk: Settings → Searches, Reports, and Alerts → New Alert
2. Copy a search query from `splunk_alerts.md`
3. Configure trigger conditions
4. Set up email notifications (optional)
5. Save

## Manual Sync

To manually sync data anytime:
```bash
cd /Users/nefarooq/oura-splunk-integration
./run_sync.sh
```

## View Your Data

**Splunk Web Interface:** http://127.0.0.1:8000

**Quick Searches:**
```
index=oura_data
index=oura_data | stats count by sourcetype
index=oura_data sourcetype="oura:sleep" | timechart avg(score)
```

## Troubleshooting

**No data showing up?**
- Check `sync.log` for errors
- Verify your tokens in `.env` are correct
- Make sure Splunk is running: `/Applications/Splunk/bin/splunk status`

**Dashboard not working?**
- Wait 5-10 minutes after importing for Splunk to index data
- Run a manual sync: `./run_sync.sh`
- Refresh the dashboard

## Support

- GitHub Repo: https://github.com/nevv703/oura-splunk-integration
- Check logs: `tail -f sync.log`
- Splunk Web: http://127.0.0.1:8000

Enjoy your health analytics!
