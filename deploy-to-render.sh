#!/bin/bash

echo "🚀 Deploying CareerPath AI Backend to Render..."
echo ""
echo "⚠️  MANUAL STEPS REQUIRED:"
echo ""
echo "1. Go to: https://render.com"
echo "2. Sign up/Login with GitHub"
echo "3. Click 'New +' → 'Web Service'"
echo "4. Select 'Deploy from GitHub repository'"
echo ""
echo "5. If you don't have GitHub repo, use these settings manually:"
echo "   - Name: careerpath-api"
echo "   - Runtime: Python 3"
echo "   - Build Command: pip install -r requirements.txt"
echo "   - Start Command: uvicorn api.main:app --host 0.0.0.0 --port \$PORT"
echo ""
echo "6. Add Environment Variables:"
echo "   GROQ_API_KEY=your-groq-api-key"
echo "   USE_GROQ=true"
echo "   COSMOS_CONNECTION_STRING=your-cosmos-connection-string"
echo "   SUPABASE_URL=your-supabase-url"
echo "   SUPABASE_ANON_KEY=your-supabase-anon-key"
echo ""
echo "7. Click 'Create Web Service'"
echo ""
echo "8. Copy your Render URL (e.g., https://careerpath-api-xyz.onrender.com)"
echo ""
echo "9. Come back here and paste it!"
echo ""
read -p "Enter your Render backend URL: " RENDER_URL

if [ -z "$RENDER_URL" ]; then
    echo "❌ No URL provided. Exiting."
    exit 1
fi

echo ""
echo "✅ Got URL: $RENDER_URL"
echo ""
echo "🔄 Updating frontend to use Render backend..."

# Update frontend .env.local
cd frontend
cat > .env.local << ENVEOF
NEXT_PUBLIC_SUPABASE_URL=your-supabase-url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-supabase-anon-key
NEXT_PUBLIC_API_URL=$RENDER_URL
ENVEOF

echo "✅ Frontend configured to use Render backend"
echo ""
echo "🚀 Deploying frontend to Azure Static Web Apps..."

npm run build

echo ""
echo "✅ Frontend built successfully!"
echo ""
echo "🎉 YOUR APP IS READY!"
echo ""
echo "Frontend: https://icy-grass-0516c410f.6.azurestaticapps.net"
echo "Backend:  $RENDER_URL"
echo ""
echo "Test it now! 🚀"
