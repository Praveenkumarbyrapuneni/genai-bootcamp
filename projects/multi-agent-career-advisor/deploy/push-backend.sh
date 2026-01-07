#!/bin/bash

# =============================================================================
# CareerPath AI - Push Backend Code to Azure
# =============================================================================
# This script deploys the FastAPI backend code to Azure App Service
#
# Usage:
#   chmod +x deploy/push-backend.sh
#   ./deploy/push-backend.sh
# =============================================================================

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuration
RESOURCE_GROUP="careerpath-rg"
BACKEND_APP_NAME="careerpath-api"

echo -e "${BLUE}🚀 Deploying FastAPI Backend to Azure...${NC}\n"

# Get the script directory and project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"

echo -e "${YELLOW}📦 Creating deployment package...${NC}"

# Create a temporary deployment directory
DEPLOY_DIR=$(mktemp -d)
echo "Using temp directory: $DEPLOY_DIR"

# Copy necessary files (excluding frontend, venv, etc.)
cp -r api "$DEPLOY_DIR/"
cp -r src "$DEPLOY_DIR/"
cp -r prompts "$DEPLOY_DIR/"
cp requirements.txt "$DEPLOY_DIR/"
cp startup.sh "$DEPLOY_DIR/"

# Create zip file
cd "$DEPLOY_DIR"
zip -r deploy.zip . -x "*.pyc" -x "__pycache__/*" -x "*.git*"

echo -e "${YELLOW}☁️  Uploading to Azure...${NC}"

# Deploy using zip deploy
az webapp deployment source config-zip \
    --name $BACKEND_APP_NAME \
    --resource-group $RESOURCE_GROUP \
    --src deploy.zip

# Cleanup
cd "$PROJECT_ROOT"
rm -rf "$DEPLOY_DIR"

echo -e "\n${GREEN}✅ Backend deployed successfully!${NC}"
echo -e "${BLUE}🌐 URL: https://${BACKEND_APP_NAME}.azurewebsites.net${NC}"
echo -e "${YELLOW}📋 Test the API: https://${BACKEND_APP_NAME}.azurewebsites.net/docs${NC}"
