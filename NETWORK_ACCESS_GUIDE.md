# Quick Deployment Guide

## Option 1: ngrok (Recommended)
1. Download: https://ngrok.com/download
2. Extract ngrok.exe to this folder
3. Run: `ngrok http 5000`
4. Share the public URL with colleagues

## Option 2: Heroku Deployment
1. Install Heroku CLI
2. Run these commands:
   ```
   heroku login
   git init
   git add .
   git commit -m "Initial commit"
   heroku create your-app-name
   git push heroku main
   ```

## Option 3: Ask IT Admin
Ask your network admin to:
- Check if routing exists between 192.168.x.x and 10.x.x.x networks
- Provide the correct IP/hostname colleagues should use

## Current Status
- App running on: http://192.168.1.200:5000
- Colleagues need: Different network access method