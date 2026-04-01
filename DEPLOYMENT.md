# Deployment Guide: Veritiv Data Dashboard

## 🚀 Quick Deploy to Heroku

### Option 1: One-Click Deploy (Recommended for sharing)

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

Click the button above to deploy directly from this repository.

### Option 2: Manual Deployment

#### Prerequisites
- Git installed on your machine
- Heroku account (free tier available)
- Heroku CLI installed

#### Steps

1. **Install Heroku CLI**
   ```bash
   # Download from: https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Login to Heroku**
   ```bash
   heroku login
   ```

3. **Create Heroku App**
   ```bash
   heroku create veritiv-data-dashboard-[your-initials]
   # Example: heroku create veritiv-data-dashboard-js
   ```

4. **Set Environment Variables**
   ```bash
   heroku config:set REDSHIFT_HOST=de-prod-redshift.c1ccwpwhe047.us-east-1.redshift.amazonaws.com
   heroku config:set REDSHIFT_PORT=5439
   heroku config:set REDSHIFT_DATABASE=veritiv
   heroku config:set REDSHIFT_USERNAME=svc_finance_cube
   heroku config:set REDSHIFT_PASSWORD=Veritiv001!
   heroku config:set FLASK_DEBUG=False
   
   # Optional: For PDF functionality
   heroku config:set OPENAI_API_KEY=your_openai_key_here
   ```

5. **Deploy the Application**
   ```bash
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   ```

6. **Open Your Deployed App**
   ```bash
   heroku open
   ```

---

## 🌐 Deployment Options for Corporate Use

### 1. **Heroku (Recommended for Quick Sharing)**
- **Pros**: Fast deployment, easy sharing, good for prototypes
- **URL Format**: `https://your-app-name.herokuapp.com`
- **Cost**: Free tier available, paid plans for production

### 2. **AWS (Best for Production)**
- **Elastic Beanstalk**: Easy AWS deployment
- **ECS/Fargate**: Container-based deployment
- **Lambda**: Serverless option (requires code changes)

### 3. **Internal Corporate Server**
- Deploy on Veritiv's internal infrastructure
- Requires IT department coordination
- Best security for sensitive data

---

## 🔐 Security Considerations for Corporate Deployment

### Environment Variables (Critical)
Never commit these to Git:
- `REDSHIFT_PASSWORD`
- `OPENAI_API_KEY`
- Any database credentials

### Recommendations for Production:
1. **Use environment variables** for all sensitive data
2. **Enable HTTPS** (Heroku provides this automatically)
3. **Consider authentication** for corporate access
4. **Review IP restrictions** on Redshift cluster
5. **Monitor access logs**

---

## 👥 Sharing with Colleagues

### After Deployment:

1. **Share the URL**
   ```
   Your dashboard: https://veritiv-data-dashboard-[initials].herokuapp.com
   ```

2. **Access Instructions**
   - **Redshift Dashboard**: `[your-url]/redshift`
   - **PDF Extractor**: `[your-url]/`

3. **User Guide for Colleagues**:
   ```
   📊 Redshift Dashboard Features:
   - Browse 1,796+ tables across 66 schemas
   - View table data with customizable limits
   - Execute custom SQL queries
   - Export data in JSON format

   📄 PDF Extractor Features:
   - Upload PDF files
   - Ask questions about PDF content
   - Get AI-powered answers
   ```

---

## 🔧 Production Optimizations

### For High-Traffic Use:
1. **Upgrade Heroku dyno** from eco to standard/performance
2. **Connection pooling** for Redshift (already implemented)
3. **Caching** for frequently accessed tables
4. **Rate limiting** for API endpoints

### Monitoring & Logging:
```bash
# View app logs
heroku logs --tail

# Monitor performance
heroku ps:scale web=1
```

---

## 🆘 Troubleshooting

### Common Issues:

1. **"Application Error" on Heroku**
   ```bash
   heroku logs --tail
   # Check for missing environment variables
   ```

2. **Redshift Connection Issues**
   ```bash
   heroku config
   # Verify all REDSHIFT_* variables are set
   ```

3. **Build Failures**
   - Check `requirements.txt` dependencies
   - Python version compatibility (3.12.0)

### Support:
- **Internal**: Contact your deployment administrator
- **Heroku**: Check Heroku status page
- **Redshift**: Verify cluster accessibility

---

## 📋 Deployment Checklist

- [ ] Environment variables configured
- [ ] Redshift cluster accessible from deployment platform
- [ ] Application tested locally
- [ ] Security review completed
- [ ] Colleagues notified with access instructions
- [ ] Monitoring setup (logs, performance)

---

## 🎯 Next Steps for Team Collaboration

1. **Create shared documentation** for query patterns
2. **Set up user accounts** if authentication is needed
3. **Regular backups** of important queries/bookmarks
4. **Performance monitoring** for optimization
5. **User feedback collection** for improvements

Your Veritiv Data Dashboard is ready for team collaboration! 🚀