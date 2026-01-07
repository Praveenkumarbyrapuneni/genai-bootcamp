#!/bin/bash

# Fast deployment to Azure App Service (not Container Apps)
set -e

echo "🚀 Fast Deployment to Azure App Service"
echo "========================================"

# Variables
RG="careerpath-rg"
APP_NAME="careerpath-api-fast"
LOCATION="eastus"

# Create App Service Plan (Free tier)
echo "📦 Creating App Service Plan..."
az appservice plan create \
  --name ${APP_NAME}-plan \
  --resource-group $RG \
  --location $LOCATION \
  --sku F1 \
  --is-linux \
  || echo "Plan already exists"

# Create Web App
echo "🌐 Creating Web App..."
az webapp create \
  --name $APP_NAME \
  --resource-group $RG \
  --plan ${APP_NAME}-plan \
  --runtime "PYTHON:3.11" \
  || echo "App already exists"

# Configure environment variables
echo "⚙️ Setting environment variables..."
az webapp config appsettings set \
  --name $APP_NAME \
  --resource-group $RG \
  --settings \
    AZURE_OPENAI_ENDPOINT="your-azure-openai-endpoint" \
    AZURE_OPENAI_API_KEY="your-azure-openai-key" \
    AZURE_OPENAI_DEPLOYMENT_NAME="gpt-4o-mini" \
    AZURE_OPENAI_API_VERSION="2024-10-21" \
    COSMOS_CONNECTION_STRING="your-cosmos-connection-string" \
    SUPABASE_URL="your-supabase-url" \
    SUPABASE_ANON_KEY="your-supabase-anon-key" \
    SCM_DO_BUILD_DURING_DEPLOYMENT="true"

# Deploy code using ZIP deploy (FAST!)
echo "📦 Deploying code..."
cd /Users/praveen/Desktop/careerpath\ with\ auth
zip -r deploy.zip . -x "*.git*" "node_modules/*" "frontend/*" "__pycache__/*" "*.pyc" "deploy.log" "*.zip"

az webapp deployment source config-zip \
  --name $APP_NAME \
  --resource-group $RG \
  --src deploy.zip

rm deploy.zip

echo ""
echo "✅ DEPLOYMENT COMPLETE!"
echo "🌐 Backend URL: https://${APP_NAME}.azurewebsites.net"
echo ""
echo "Testing in 30 seconds..."
sleep 30

echo "🧪 Testing validation..."
curl -X POST https://${APP_NAME}.azurewebsites.net/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"user_id":"test","target_role":"hello","current_skills":[],"timeframe_months":6}' \
  -w "\n⏱️ Response Time: %{time_total}s\n"

echo ""
echo "✅ Done! Now update your frontend to use: https://${APP_NAME}.azurewebsites.net"
