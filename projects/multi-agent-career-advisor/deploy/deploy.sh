#!/bin/bash

# =============================================================================
# CareerPath AI - Azure Deployment Script
# =============================================================================
# This script deploys both the FastAPI backend and Next.js frontend to Azure
# 
# Prerequisites:
#   1. Azure CLI installed and logged in (az login)
#   2. Node.js and npm installed
#   3. Python 3.11+ installed
#
# Usage:
#   chmod +x deploy/deploy.sh
#   ./deploy/deploy.sh
# =============================================================================

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# =============================================================================
# CONFIGURATION - UPDATE THESE VALUES
# =============================================================================
RESOURCE_GROUP="careerpath-rg"
LOCATION="eastus"
BACKEND_APP_NAME="careerpath-api"
FRONTEND_APP_NAME="careerpath-frontend"
APP_SERVICE_PLAN="careerpath-plan"
SKU="F1"  # Free tier - no quota required

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================
print_header() {
    echo -e "\n${BLUE}=============================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}=============================================${NC}\n"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

check_command() {
    if ! command -v $1 &> /dev/null; then
        print_error "$1 is not installed. Please install it first."
        exit 1
    fi
}

# =============================================================================
# PRE-FLIGHT CHECKS
# =============================================================================
print_header "🔍 Pre-flight Checks"

check_command "az"
check_command "node"
check_command "npm"
check_command "python3"

# Check Azure login
if ! az account show &> /dev/null; then
    print_warning "Not logged into Azure. Running 'az login'..."
    az login
fi

SUBSCRIPTION=$(az account show --query name -o tsv)
print_success "Logged into Azure subscription: $SUBSCRIPTION"

# =============================================================================
# CREATE RESOURCE GROUP
# =============================================================================
print_header "📦 Creating Resource Group"

if az group show --name $RESOURCE_GROUP &> /dev/null; then
    print_warning "Resource group '$RESOURCE_GROUP' already exists"
else
    az group create --name $RESOURCE_GROUP --location $LOCATION
    print_success "Created resource group: $RESOURCE_GROUP"
fi

# =============================================================================
# CREATE APP SERVICE PLAN
# =============================================================================
print_header "📋 Creating App Service Plan"

if az appservice plan show --name $APP_SERVICE_PLAN --resource-group $RESOURCE_GROUP &> /dev/null; then
    print_warning "App Service Plan '$APP_SERVICE_PLAN' already exists"
else
    az appservice plan create \
        --name $APP_SERVICE_PLAN \
        --resource-group $RESOURCE_GROUP \
        --sku $SKU \
        --is-linux
    print_success "Created App Service Plan: $APP_SERVICE_PLAN"
fi

# =============================================================================
# DEPLOY BACKEND (FastAPI)
# =============================================================================
print_header "🐍 Deploying FastAPI Backend"

# Create backend web app
if az webapp show --name $BACKEND_APP_NAME --resource-group $RESOURCE_GROUP &> /dev/null; then
    print_warning "Backend app '$BACKEND_APP_NAME' already exists"
else
    az webapp create \
        --name $BACKEND_APP_NAME \
        --resource-group $RESOURCE_GROUP \
        --plan $APP_SERVICE_PLAN \
        --runtime "PYTHON:3.11"
    print_success "Created backend web app: $BACKEND_APP_NAME"
fi

# Configure startup command
az webapp config set \
    --name $BACKEND_APP_NAME \
    --resource-group $RESOURCE_GROUP \
    --startup-file "uvicorn api.main:app --host 0.0.0.0 --port 8000"

print_success "Configured startup command"

# Set PYTHONPATH
az webapp config appsettings set \
    --name $BACKEND_APP_NAME \
    --resource-group $RESOURCE_GROUP \
    --settings PYTHONPATH="/home/site/wwwroot"

print_success "Set PYTHONPATH environment variable"

# Get the backend URL
BACKEND_URL="https://${BACKEND_APP_NAME}.azurewebsites.net"
print_success "Backend URL: $BACKEND_URL"

# =============================================================================
# DEPLOY FRONTEND (Next.js Static Web App)
# =============================================================================
print_header "⚛️  Deploying Next.js Frontend"

# Check if Static Web App exists
if az staticwebapp show --name $FRONTEND_APP_NAME --resource-group $RESOURCE_GROUP &> /dev/null 2>&1; then
    print_warning "Static Web App '$FRONTEND_APP_NAME' already exists"
else
    # Create Static Web App (requires GitHub or manual deployment)
    print_warning "Static Web Apps require GitHub connection or manual deployment"
    print_warning "Please create it manually in Azure Portal or use the Azure Static Web Apps CLI"
    
    echo -e "\n${YELLOW}To create via Azure Portal:${NC}"
    echo "1. Go to Azure Portal → Create a resource → Static Web App"
    echo "2. Name: $FRONTEND_APP_NAME"
    echo "3. Region: $LOCATION"
    echo "4. Deployment source: GitHub or Other"
    echo "5. Build Details:"
    echo "   - App location: /frontend"
    echo "   - Output location: .next"
fi

FRONTEND_URL="https://${FRONTEND_APP_NAME}.azurestaticapps.net"

# =============================================================================
# PRINT SUMMARY
# =============================================================================
print_header "📋 Deployment Summary"

echo -e "${GREEN}Backend API:${NC}"
echo "  URL: $BACKEND_URL"
echo "  Resource: $BACKEND_APP_NAME"
echo ""
echo -e "${GREEN}Frontend:${NC}"
echo "  URL: $FRONTEND_URL"
echo "  Resource: $FRONTEND_APP_NAME"
echo ""

print_header "🔧 Next Steps"

echo "1. Set backend environment variables:"
echo "   Run: ./deploy/set-env-backend.sh"
echo ""
echo "2. Deploy backend code:"
echo "   Run: ./deploy/push-backend.sh"
echo ""
echo "3. Deploy frontend code:"
echo "   Run: ./deploy/push-frontend.sh"
echo ""
echo "4. Update Supabase redirect URLs to include:"
echo "   $FRONTEND_URL"
echo ""

print_success "Infrastructure setup complete!"
