@echo off
echo 🚀 Deploying Veritiv Data Dashboard to Heroku...

REM Check if Heroku CLI is installed
heroku --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Heroku CLI not found. Please install it first:
    echo    https://devcenter.heroku.com/articles/heroku-cli
    pause
    exit /b 1
)

REM Login to Heroku
echo 🔐 Logging into Heroku...
heroku login

REM Get app name
set /p APP_NAME=📝 Enter your app name (e.g., veritiv-dashboard-yourname): 

if "%APP_NAME%"=="" (
    echo ❌ App name cannot be empty
    pause
    exit /b 1
)

REM Create Heroku app
echo 🏗️ Creating Heroku app: %APP_NAME%
heroku create %APP_NAME%

REM Set environment variables
echo ⚙️ Setting environment variables...
heroku config:set REDSHIFT_HOST=de-prod-redshift.c1ccwpwhe047.us-east-1.redshift.amazonaws.com -a %APP_NAME%
heroku config:set REDSHIFT_PORT=5439 -a %APP_NAME%
heroku config:set REDSHIFT_DATABASE=veritiv -a %APP_NAME%
heroku config:set REDSHIFT_USERNAME=svc_finance_cube -a %APP_NAME%
heroku config:set REDSHIFT_PASSWORD=Veritiv001! -a %APP_NAME%
heroku config:set FLASK_DEBUG=False -a %APP_NAME%

REM Ask for OpenAI API key (optional)
set /p OPENAI_KEY=🤖 Enter OpenAI API key (optional, for PDF features): 
if not "%OPENAI_KEY%"=="" (
    heroku config:set OPENAI_API_KEY=%OPENAI_KEY% -a %APP_NAME%
)

REM Initialize git if not already done
if not exist ".git" (
    echo 📦 Initializing git repository...
    git init
    git add .
    git commit -m "Initial commit for Veritiv Data Dashboard"
)

REM Add Heroku remote
heroku git:remote -a %APP_NAME%

REM Deploy to Heroku
echo 🚀 Deploying to Heroku...
git add .
git commit -m "Deploy to Heroku"
git push heroku main

REM Show results
echo ✅ Deployment complete!
echo 🌐 Your app URL: https://%APP_NAME%.herokuapp.com
echo 📊 Redshift Dashboard: https://%APP_NAME%.herokuapp.com/redshift
echo 📄 PDF Extractor: https://%APP_NAME%.herokuapp.com/

REM Ask if user wants to open the app
set /p OPEN_APP=🔗 Open the app in browser? (y/n): 
if /i "%OPEN_APP%"=="y" (
    heroku open -a %APP_NAME%
)

echo.
echo 🎉 Success! Share these URLs with your Veritiv colleagues:
echo    Main Dashboard: https://%APP_NAME%.herokuapp.com
echo    Direct to Data: https://%APP_NAME%.herokuapp.com/redshift

pause