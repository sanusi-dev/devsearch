#!/bin/bash
# =============================================================================
# DevSearch Mailer Worker
#
# This script runs the django-mailer background worker locally.
# It polls the email queue every 30 seconds and dispatches any pending emails
# via the configured SMTP backend.
#
# Usage (development):
#   ./run_mailer.sh
#
# Production:
#   On a PaaS (Render, Heroku, Railway), configure a dedicated "Worker" service
#   to run:  python manage.py runmailer
#
#   On a VPS, set up a cron job to run every minute instead:
#   * * * * * cd /path/to/devsearch && .venv/bin/python manage.py send_mail >> mailer.log 2>&1
# =============================================================================

echo "Starting DevSearch Mailer Worker... (Press Ctrl+C to stop)"

while true; do
    .venv/bin/python manage.py send_mail
    sleep 30
done
