#!/bin/bash
# Keep Azure backend warm by pinging every 5 minutes
# Run this in the background: ./keep-warm.sh &

while true; do
  echo "[$(date)] Keeping backend warm..."
  curl -s https://careerpath-api.thankfulsea-42148813.eastus.azurecontainerapps.io/health > /dev/null
  sleep 300  # 5 minutes
done
