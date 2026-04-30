# Daily LinkedIn Job Link Generator

Generates LinkedIn search links for jobs posted in the **last 24 hours** with up to **50 jobs per query**.

## Run now

```bash
python3 linkedin_daily_jobs.py --roles all --locations all --max-jobs 50
```

Output is saved to `job_links_last24h.json`.

## Daily morning schedule (cron)

Example: run every day at 7:00 AM UTC:

```bash
0 7 * * * cd /workspace/job && /usr/bin/python3 linkedin_daily_jobs.py --roles all --locations all --max-jobs 50 >> /workspace/job/daily_jobs.log 2>&1
```

## Customize

- `--roles "Data Engineer,Backend SDE"`
- `--locations "Remote,United States,New York, India"`
- `--max-jobs 50`
- `--output my_links.json`
