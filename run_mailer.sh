#!/bin/bash
echo "Starting DevSearch Mailer Worker... (Press Ctrl+C to stop)"
while true; do
  # Run the Django-mailer send_mail command
  .venv/bin/python manage.py send_mail
  
  # Wait for 10 seconds before checking for new emails again
  sleep 20
done
