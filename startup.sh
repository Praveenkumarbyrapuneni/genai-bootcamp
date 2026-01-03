#!/bin/bash
cd /home/site/wwwroot
export PYTHONPATH=/home/site/wwwroot
uvicorn api.main:app --host 0.0.0.0 --port 8000