#!/bin/bash

# =============================================================================
# CareerPath AI - Azure Container Apps Deployment (ONE COMMAND DEPLOYMENT)
# =============================================================================
# This script deploys the complete CareerPath AI application to Azure
# using Azure Container Apps (better free tier than App Service)
#
# Usage:
#   chmod +x deploy/deploy-container-apps.sh
#   ./deploy/deploy-container-apps.sh
# =============================================================================

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# =============================================================================
# CONFIGURATION
# =============================================================================
RESOURCE_GROUP="careerpath-rg"
LOCATION="eastus"
CONTAINER_ENV="careerpath-env"
BACKEND_APP="careerpath-api"
ACR_NAME="careerpathacr$(date +%s | tail -c 6)"  # Unique name for Azure Container Registry
IMAGE_NAME="careerpath-api"
IMAGE_TAG="latest"

# Environment Variables (loaded from .env file)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
ENV_FILE="$PROJECT_ROOT/.env"

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================
print_header() {
    echo -e "\n${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${CYAN}  $1${NC}"
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"
}

print_step() {
    echo -e "${BLUE}▶ $1${NC}"
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

load_env() {
    if [ -f "$ENV_FILE" ]; then
        print_step "Loading environment variables from .env file..."
        export $(grep -v '^#' "$ENV_FILE" | xargs)
        print_success "Environment variables loaded"
    else
        print_error ".env file not found at $ENV_FILE"
        exit 1
    fi
}

# =============================================================================
# MAIN DEPLOYMENT
# =============================================================================

print_header "🚀 CareerPath AI - Azure Container Apps Deployment"

# Check prerequisites
print_step "Checking prerequisites..."

if ! command -v az &> /dev/null; then
    print_error "Azure CLI not installed. Please install it first."
    exit 1
fi

if ! command -v docker &> /dev/null; then
    print_error "Docker not installed. Please install Docker Desktop first."
    exit 1
fi

# Check Azure login
if ! az account show &> /dev/null; then
    print_warning "Not logged into Azure. Running 'az login'..."
    az login
fi

SUBSCRIPTION=$(az account show --query name -o tsv)
print_success "Logged into Azure: $SUBSCRIPTION"

# Load environment variables
load_env

# Navigate to project root
cd "$PROJECT_ROOT"

# =============================================================================
# STEP 1: Create Resource Group (if not exists)
# =============================================================================
print_header "📦 Step 1: Creating Resource Group"

if az group show --name $RESOURCE_GROUP &> /dev/null; then
    print_warning "Resource group '$RESOURCE_GROUP' already exists"
else
    az group create --name $RESOURCE_GROUP --location $LOCATION --output none
    print_success "Created resource group: $RESOURCE_GROUP"
fi

# =============================================================================
# STEP 2: Create Azure Container Registry
# =============================================================================
print_header "🏗️  Step 2: Creating Azure Container Registry"

# Check if any ACR exists in the resource group
EXISTING_ACR=$(az acr list --resource-group $RESOURCE_GROUP --query "[0].name" -o tsv 2>/dev/null)

if [ -n "$EXISTING_ACR" ] && [ "$EXISTING_ACR" != "null" ]; then
    ACR_NAME=$EXISTING_ACR
    print_warning "Using existing ACR: $ACR_NAME"
else
    print_step "Creating new ACR: $ACR_NAME"
    az acr create \
        --resource-group $RESOURCE_GROUP \
        --name $ACR_NAME \
        --sku Basic \
        --admin-enabled true \
        --output none
    print_success "Created ACR: $ACR_NAME"
fi

# Get ACR credentials
ACR_LOGIN_SERVER=$(az acr show --name $ACR_NAME --query loginServer -o tsv)
ACR_USERNAME=$(az acr credential show --name $ACR_NAME --query username -o tsv)
ACR_PASSWORD=$(az acr credential show --name $ACR_NAME --query "passwords[0].value" -o tsv)

print_success "ACR Login Server: $ACR_LOGIN_SERVER"

# =============================================================================
# STEP 3: Build and Push Docker Image
# =============================================================================
print_header "🐳 Step 3: Building and Pushing Docker Image"

FULL_IMAGE_NAME="$ACR_LOGIN_SERVER/$IMAGE_NAME:$IMAGE_TAG"

print_step "Building Docker image..."
docker build -t $FULL_IMAGE_NAME .

print_step "Logging into ACR..."
docker login $ACR_LOGIN_SERVER -u $ACR_USERNAME -p $ACR_PASSWORD

print_step "Pushing image to ACR..."
docker push $FULL_IMAGE_NAME

print_success "Image pushed: $FULL_IMAGE_NAME"

# =============================================================================
# STEP 4: Create Container Apps Environment
# =============================================================================
print_header "🌐 Step 4: Creating Container Apps Environment"

# Install/upgrade containerapp extension
az extension add --name containerapp --upgrade --yes 2>/dev/null || true

# Register required providers
print_step "Registering Azure providers..."
az provider register --namespace Microsoft.App --wait 2>/dev/null || true
az provider register --namespace Microsoft.OperationalInsights --wait 2>/dev/null || true

# Check if environment exists
if az containerapp env show --name $CONTAINER_ENV --resource-group $RESOURCE_GROUP &> /dev/null; then
    print_warning "Container Apps Environment '$CONTAINER_ENV' already exists"
else
    print_step "Creating Container Apps Environment (this may take 2-3 minutes)..."
    az containerapp env create \
        --name $CONTAINER_ENV \
        --resource-group $RESOURCE_GROUP \
        --location $LOCATION \
        --output none
    print_success "Created Container Apps Environment: $CONTAINER_ENV"
fi

# =============================================================================
# STEP 5: Deploy Backend Container App
# =============================================================================
print_header "🐍 Step 5: Deploying FastAPI Backend"

# Check if app exists
if az containerapp show --name $BACKEND_APP --resource-group $RESOURCE_GROUP &> /dev/null; then
    print_step "Updating existing Container App..."
    az containerapp update \
        --name $BACKEND_APP \
        --resource-group $RESOURCE_GROUP \
        --image $FULL_IMAGE_NAME \
        --output none
else
    print_step "Creating new Container App..."
    az containerapp create \
        --name $BACKEND_APP \
        --resource-group $RESOURCE_GROUP \
        --environment $CONTAINER_ENV \
        --image $FULL_IMAGE_NAME \
        --registry-server $ACR_LOGIN_SERVER \
        --registry-username $ACR_USERNAME \
        --registry-password $ACR_PASSWORD \
        --target-port 8000 \
        --ingress external \
        --cpu 0.5 \
        --memory 1.0Gi \
        --min-replicas 0 \
        --max-replicas 1 \
        --env-vars \
            AZURE_OPENAI_ENDPOINT="$AZURE_OPENAI_ENDPOINT" \
            AZURE_OPENAI_API_KEY="$AZURE_OPENAI_API_KEY" \
            AZURE_OPENAI_DEPLOYMENT_NAME="$AZURE_OPENAI_DEPLOYMENT_NAME" \
            AZURE_OPENAI_API_VERSION="$AZURE_OPENAI_API_VERSION" \
            AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME="$AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME" \
            COSMOS_CONNECTION_STRING="$COSMOS_CONNECTION_STRING" \
            SUPABASE_URL="$SUPABASE_URL" \
            SUPABASE_ANON_KEY="$SUPABASE_ANON_KEY" \
            PYTHONPATH="/app" \
        --output none
fi

print_success "Backend deployed successfully!"

# Get the backend URL
BACKEND_URL=$(az containerapp show --name $BACKEND_APP --resource-group $RESOURCE_GROUP --query "properties.configuration.ingress.fqdn" -o tsv)
BACKEND_URL="https://$BACKEND_URL"

print_success "Backend URL: $BACKEND_URL"

# =============================================================================
# STEP 6: Update Frontend Environment
# =============================================================================
print_header "⚛️  Step 6: Configuring Frontend"

FRONTEND_ENV_FILE="$PROJECT_ROOT/frontend/.env.local"

# Create/update frontend .env.local
cat > "$FRONTEND_ENV_FILE" << EOF
# Auto-generated by deploy script
# Generated on: $(date)

# Supabase Configuration
NEXT_PUBLIC_SUPABASE_URL=$SUPABASE_URL
NEXT_PUBLIC_SUPABASE_ANON_KEY=$SUPABASE_ANON_KEY

# Backend API URL (Azure Container Apps)
NEXT_PUBLIC_API_URL=$BACKEND_URL
EOF

print_success "Updated frontend/.env.local with backend URL"

# =============================================================================
# STEP 7: Deploy Frontend to Azure Static Web Apps
# =============================================================================
print_header "🌐 Step 7: Deploying Frontend"

# Check if SWA CLI is installed
if ! command -v swa &> /dev/null; then
    print_step "Installing Azure Static Web Apps CLI..."
    npm install -g @azure/static-web-apps-cli
fi

cd "$PROJECT_ROOT/frontend"

print_step "Installing frontend dependencies..."
npm install

print_step "Building Next.js app..."
npm run build

# Check for existing Static Web App
EXISTING_SWA=$(az staticwebapp list --resource-group $RESOURCE_GROUP --query "[0].name" -o tsv 2>/dev/null)

if [ -n "$EXISTING_SWA" ] && [ "$EXISTING_SWA" != "null" ]; then
    FRONTEND_APP=$EXISTING_SWA
    print_warning "Using existing Static Web App: $FRONTEND_APP"
else
    FRONTEND_APP="careerpath-frontend"
    print_step "Creating Static Web App..."
    az staticwebapp create \
        --name $FRONTEND_APP \
        --resource-group $RESOURCE_GROUP \
        --location "eastus2" \
        --sku Free \
        --output none 2>/dev/null || print_warning "Static Web App may need manual creation"
fi

# Get deployment token
DEPLOYMENT_TOKEN=$(az staticwebapp secrets list --name $FRONTEND_APP --resource-group $RESOURCE_GROUP --query "properties.apiKey" -o tsv 2>/dev/null)

if [ -n "$DEPLOYMENT_TOKEN" ] && [ "$DEPLOYMENT_TOKEN" != "null" ]; then
    print_step "Deploying frontend..."
    swa deploy .next \
        --deployment-token $DEPLOYMENT_TOKEN \
        --env production \
        2>/dev/null || print_warning "SWA deployment may need manual setup"
    
    FRONTEND_URL=$(az staticwebapp show --name $FRONTEND_APP --resource-group $RESOURCE_GROUP --query "defaultHostname" -o tsv 2>/dev/null)
    FRONTEND_URL="https://$FRONTEND_URL"
else
    print_warning "Could not get deployment token. Frontend may need manual deployment."
    FRONTEND_URL="https://$FRONTEND_APP.azurestaticapps.net"
fi

cd "$PROJECT_ROOT"

# =============================================================================
# DEPLOYMENT COMPLETE
# =============================================================================
print_header "🎉 Deployment Complete!"

echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}  Your CareerPath AI is now live!${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${BLUE}🔗 URLs:${NC}"
echo -e "   ${CYAN}Backend API:${NC}  $BACKEND_URL"
echo -e "   ${CYAN}API Docs:${NC}     $BACKEND_URL/docs"
echo -e "   ${CYAN}Frontend:${NC}     $FRONTEND_URL"
echo ""
echo -e "${BLUE}📋 Next Steps:${NC}"
echo -e "   1. Test the API: ${CYAN}curl $BACKEND_URL/health${NC}"
echo -e "   2. Update Supabase redirect URLs to include:"
echo -e "      ${CYAN}$FRONTEND_URL${NC}"
echo -e "   3. Visit your frontend and login!"
echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

# Save deployment info
cat > "$PROJECT_ROOT/deploy/deployment-info.txt" << EOF
CareerPath AI Deployment Info
=============================
Deployed on: $(date)

Backend (Azure Container Apps):
  URL: $BACKEND_URL
  API Docs: $BACKEND_URL/docs
  Resource: $BACKEND_APP
  
Frontend (Azure Static Web Apps):
  URL: $FRONTEND_URL
  Resource: $FRONTEND_APP

Azure Resources:
  Resource Group: $RESOURCE_GROUP
  Container Registry: $ACR_NAME
  Container Environment: $CONTAINER_ENV
  
Don't forget to add this URL to Supabase redirect URLs:
  $FRONTEND_URL
EOF

print_success "Deployment info saved to deploy/deployment-info.txt"
