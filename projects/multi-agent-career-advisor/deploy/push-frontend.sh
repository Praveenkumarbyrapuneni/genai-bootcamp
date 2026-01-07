#!/bin/bash

# =============================================================================
# CareerPath AI - Push Frontend Code to Azure Static Web Apps
# =============================================================================
# This script builds and deploys the Next.js frontend
#
# Prerequisites:
#   - Azure Static Web Apps CLI: npm install -g @azure/static-web-apps-cli
#   - Or use Azure Portal deployment token
#
# Usage:
#   chmod +x deploy/push-frontend.sh
#   ./deploy/push-frontend.sh
# =============================================================================

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

# Configuration
FRONTEND_APP_NAME="careerpath-frontend"
BACKEND_URL="https://careerpath-api.azurewebsites.net"

# Get the script directory and project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
FRONTEND_DIR="$PROJECT_ROOT/frontend"

echo -e "${BLUE}🚀 Deploying Next.js Frontend to Azure...${NC}\n"

# Check if SWA CLI is installed
if ! command -v swa &> /dev/null; then
    echo -e "${YELLOW}Installing Azure Static Web Apps CLI...${NC}"
    npm install -g @azure/static-web-apps-cli
fi

# Navigate to frontend directory
cd "$FRONTEND_DIR"

# Check if .env.local exists, if not create from example
if [ ! -f .env.local ]; then
    echo -e "${YELLOW}Creating .env.local from .env.example...${NC}"
    if [ -f .env.example ]; then
        cp .env.example .env.local
        echo -e "${RED}⚠️  Please update .env.local with your actual values!${NC}"
    fi
fi

# Install dependencies
echo -e "${YELLOW}📦 Installing dependencies...${NC}"
npm install

# Build the Next.js app
echo -e "${YELLOW}🔨 Building Next.js app...${NC}"
npm run build

# Deploy using SWA CLI
echo -e "${YELLOW}☁️  Deploying to Azure Static Web Apps...${NC}"

# Check if deployment token exists
if [ -z "$SWA_DEPLOYMENT_TOKEN" ]; then
    echo -e "${YELLOW}No deployment token found.${NC}"
    echo -e "${BLUE}Please choose a deployment method:${NC}\n"
    echo "Option 1: Set deployment token and run again"
    echo "  export SWA_DEPLOYMENT_TOKEN='your-token-from-azure-portal'"
    echo "  ./deploy/push-frontend.sh"
    echo ""
    echo "Option 2: Use interactive login"
    echo "  swa login"
    echo "  swa deploy .next --app-name $FRONTEND_APP_NAME"
    echo ""
    echo "Option 3: Deploy via Azure Portal"
    echo "  1. Go to Azure Portal → Static Web Apps → $FRONTEND_APP_NAME"
    echo "  2. Click 'Manage deployment token'"
    echo "  3. Copy the token"
    echo "  4. Set it as environment variable and run this script again"
    echo ""
    
    # Try interactive deployment
    echo -e "${YELLOW}Attempting interactive deployment...${NC}"
    swa deploy .next --env production --app-name $FRONTEND_APP_NAME
else
    swa deploy .next \
        --deployment-token $SWA_DEPLOYMENT_TOKEN \
        --env production
fi

echo -e "\n${GREEN}✅ Frontend deployed successfully!${NC}"
echo -e "${BLUE}🌐 URL: https://${FRONTEND_APP_NAME}.azurestaticapps.net${NC}"
