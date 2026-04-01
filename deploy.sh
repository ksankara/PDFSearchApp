#!/bin/bash

# Veritiv Data Dashboard - Heroku Deployment Script
echo "🚀 Deploying Veritiv Data Dashboard to Heroku..."

# Check if Heroku CLI is installed
if ! command -v heroku &> /dev/null; then
    echo "❌ Heroku CLI not found. Please install it first:"
    echo "   https://devcenter.heroku.com/articles/heroku-cli"
    exit 1
fi

# Login to Heroku
echo "🔐 Logging into Heroku..."
heroku login

# Get app name
read -p "📝 Enter your app name (e.g., veritiv-dashboard-yourname): " APP_NAME

if [ -z "$APP_NAME" ]; then
    echo "❌ App name cannot be empty"
    exit 1
fi

# Create Heroku app
echo "🏗️ Creating Heroku app: $APP_NAME"
heroku create $APP_NAME

# Set environment variables
echo "⚙️ Setting environment variables..."
heroku config:set REDSHIFT_HOST=de-prod-redshift.c1ccwpwhe047.us-east-1.redshift.amazonaws.com -a $APP_NAME
heroku config:set REDSHIFT_PORT=5439 -a $APP_NAME
heroku config:set REDSHIFT_DATABASE=veritiv -a $APP_NAME
heroku config:set REDSHIFT_USERNAME=svc_finance_cube -a $APP_NAME
heroku config:set REDSHIFT_PASSWORD=Veritiv001! -a $APP_NAME
heroku config:set FLASK_DEBUG=False -a $APP_NAME

# Ask for OpenAI API key (optional)
read -p "🤖 Enter OpenAI API key (optional, for PDF features): " OPENAI_KEY
if [ ! -z "$OPENAI_KEY" ]; then
    heroku config:set OPENAI_API_KEY=$OPENAI_KEY -a $APP_NAME
fi

# Initialize git if not already done
if [ ! -d ".git" ]; then
    echo "📦 Initializing git repository..."
    git init
    git add .
    git commit -m "Initial commit for Veritiv Data Dashboard"
fi

# Add Heroku remote
heroku git:remote -a $APP_NAME

# Deploy to Heroku
echo "🚀 Deploying to Heroku..."
git add .
git commit -m "Deploy to Heroku" || echo "No changes to commit"
git push heroku main

# Open the app
echo "✅ Deployment complete!"
echo "🌐 Your app URL: https://$APP_NAME.herokuapp.com"
echo "📊 Redshift Dashboard: https://$APP_NAME.herokuapp.com/redshift"
echo "📄 PDF Extractor: https://$APP_NAME.herokuapp.com/"

# Ask if user wants to open the app
read -p "🔗 Open the app in browser? (y/n): " OPEN_APP
if [ "$OPEN_APP" = "y" ] || [ "$OPEN_APP" = "Y" ]; then
    heroku open -a $APP_NAME
fi

echo ""
echo "🎉 Success! Share these URLs with your Veritiv colleagues:"
echo "   Main Dashboard: https://$APP_NAME.herokuapp.com"
echo "   Direct to Data: https://$APP_NAME.herokuapp.com/redshift"