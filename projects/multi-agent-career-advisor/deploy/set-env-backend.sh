#!/bin/bash

# =============================================================================
# CareerPath AI - Set Backend Environment Variables
# =============================================================================
# This script sets all required environment variables for the FastAPI backend
#
# Usage:
#   1. Update the values below with your actual credentials
#   2. Run: chmod +x deploy/set-env-backend.sh
#   3. Run: ./deploy/set-env-backend.sh
# =============================================================================

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# =============================================================================
# CONFIGURATION - UPDATE THESE WITH YOUR ACTUAL VALUES
# =============================================================================
RESOURCE_GROUP="careerpath-rg"
BACKEND_APP_NAME="careerpath-api"

# Azure OpenAI Settings (GET THESE FROM AZURE PORTAL)
AZURE_OPENAI_ENDPOINT="https://your-resource-name.openai.azure.com/"
AZURE_OPENAI_API_KEY="your-azure-openai-api-key"
AZURE_OPENAI_DEPLOYMENT_NAME="gpt-4o-mini"
AZURE_OPENAI_API_VERSION="2024-10-21"
AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME="text-embedding-ada-002"

# Azure Cosmos DB Settings (GET FROM AZURE PORTAL → COSMOS DB → KEYS)
COSMOS_CONNECTION_STRING="AccountEndpoint=https://your-cosmos.documents.azure.com:443/;AccountKey=your-key"

# Supabase Settings (GET FROM SUPABASE DASHBOARD → PROJECT SETTINGS → API)
SUPABASE_URL="https://your-project.supabase.co"
SUPABASE_ANON_KEY="your-supabase-anon-key"

# =============================================================================
# SET ENVIRONMENT VARIABLES
# =============================================================================
echo -e "${BLUE}Setting environment variables for $BACKEND_APP_NAME...${NC}\n"

az webapp config appsettings set \
    --name $BACKEND_APP_NAME \
    --resource-group $RESOURCE_GROUP \
    --settings \
        PYTHONPATH="/home/site/wwwroot" \
        AZURE_OPENAI_ENDPOINT="$AZURE_OPENAI_ENDPOINT" \
        AZURE_OPENAI_API_KEY="$AZURE_OPENAI_API_KEY" \
        AZURE_OPENAI_DEPLOYMENT_NAME="$AZURE_OPENAI_DEPLOYMENT_NAME" \
        AZURE_OPENAI_API_VERSION="$AZURE_OPENAI_API_VERSION" \
        AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME="$AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME" \
        COSMOS_CONNECTION_STRING="$COSMOS_CONNECTION_STRING" \
        SUPABASE_URL="$SUPABASE_URL" \
        SUPABASE_ANON_KEY="$SUPABASE_ANON_KEY" \
        SCM_DO_BUILD_DURING_DEPLOYMENT="true" \
        WEBSITE_RUN_FROM_PACKAGE="0"

echo -e "\n${GREEN}✅ Environment variables set successfully!${NC}"
echo -e "${YELLOW}⚠️  Make sure you updated the placeholder values with your actual credentials!${NC}"
