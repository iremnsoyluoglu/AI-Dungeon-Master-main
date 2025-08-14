# 🚀 Heroku Deployment Guide for AI Dungeon Master

This guide will help you deploy your AI Dungeon Master application to Heroku using the Heroku Button deployment method.

## 📋 Prerequisites

Before deploying, make sure you have:

1. **GitHub Account**: Your code must be hosted on GitHub
2. **Heroku Account**: Sign up at [heroku.com](https://heroku.com)
3. **API Keys** (Optional): OpenAI and/or Anthropic API keys for AI features

## 🎯 Method 1: Heroku Button Deployment (Recommended)

### Step 1: Prepare Your Repository

1. **Push your code to GitHub**:
   ```bash
   git add .
   git commit -m "Add Heroku deployment configuration"
   git push origin main
   ```

2. **Update the deployment button** in your README.md:
   Replace `yourusername` with your actual GitHub username in the button URL:
   ```markdown
   [![Deploy to Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/YOUR_ACTUAL_USERNAME/AI-Dungeon-Master)
   ```

### Step 2: Deploy with Heroku Button

1. **Click the Deploy Button**: Click the "Deploy to Heroku" button in your README
2. **Log in to Heroku**: If not already logged in, you'll be prompted to sign in
3. **Configure Your App**:
   - **App name**: Choose a unique name for your app (e.g., `my-ai-dungeon-master`)
   - **Region**: Select the region closest to your users
   - **Environment Variables** (Optional):
     - `OPENAI_API_KEY`: Your OpenAI API key for AI storytelling
     - `ANTHROPIC_API_KEY`: Your Anthropic API key for alternative AI features
4. **Deploy**: Click "Deploy app"

### Step 3: Access Your App

Once deployment is complete:
- Your app will be available at: `https://your-app-name.herokuapp.com`
- You'll be automatically redirected to your app

## 🔧 Method 2: Manual Heroku Deployment

If you prefer to deploy manually using the Heroku CLI:

### Step 1: Install Heroku CLI

```bash
# Windows (using Chocolatey)
choco install heroku

# macOS
brew install heroku

# Linux
curl https://cli-assets.heroku.com/install.sh | sh
```

### Step 2: Login and Create App

```bash
# Login to Heroku
heroku login

# Create a new Heroku app
heroku create your-app-name

# Add your GitHub repository as remote
heroku git:remote -a your-app-name
```

### Step 3: Configure Environment Variables

```bash
# Set environment variables
heroku config:set FLASK_ENV=production
heroku config:set FLASK_DEBUG=0

# Optional: Set API keys
heroku config:set OPENAI_API_KEY=your_openai_api_key
heroku config:set ANTHROPIC_API_KEY=your_anthropic_api_key
```

### Step 4: Deploy

```bash
# Push to Heroku
git push heroku main

# Open your app
heroku open
```

## 📁 Configuration Files

The following files are required for Heroku deployment:

### `app.json`
- **Purpose**: Heroku Button configuration
- **Contains**: App metadata, environment variables, buildpacks, add-ons
- **Status**: ✅ Created

### `Procfile`
- **Purpose**: Tells Heroku how to run your app
- **Content**: `web: python app.py`
- **Status**: ✅ Already exists

### `requirements.txt`
- **Purpose**: Python dependencies
- **Status**: ✅ Already exists

## 🔍 Troubleshooting

### Common Issues

1. **Build Fails**:
   - Check that all dependencies are in `requirements.txt`
   - Ensure `app.py` exists and is the main entry point
   - Verify Python version compatibility

2. **App Crashes on Startup**:
   - Check Heroku logs: `heroku logs --tail`
   - Verify environment variables are set correctly
   - Ensure the app listens on the correct port

3. **Static Files Not Loading**:
   - Make sure static files are in the correct directory
   - Check Flask static folder configuration

### Useful Commands

```bash
# View logs
heroku logs --tail

# Check app status
heroku ps

# Restart app
heroku restart

# Open app
heroku open

# Run commands on Heroku
heroku run python app.py
```

## 🌟 Features After Deployment

Once deployed, your AI Dungeon Master will have:

- ✅ **Web Interface**: Accessible from anywhere via HTTPS
- ✅ **Multiplayer Support**: Real-time multiplayer sessions
- ✅ **AI Storytelling**: If API keys are configured
- ✅ **Character Management**: Persistent character data
- ✅ **Campaign System**: Save and load game states
- ✅ **Responsive Design**: Works on desktop and mobile

## 🔐 Security Considerations

1. **API Keys**: Never commit API keys to your repository
2. **Environment Variables**: Use Heroku config vars for sensitive data
3. **HTTPS**: Heroku automatically provides SSL certificates
4. **Rate Limiting**: Consider implementing rate limiting for API endpoints

## 📈 Scaling

To scale your app on Heroku:

```bash
# Scale to multiple dynos
heroku ps:scale web=2

# Upgrade to a larger dyno type
heroku ps:type standard-1x
```

## 🆘 Support

If you encounter issues:

1. **Check Heroku Status**: [status.heroku.com](https://status.heroku.com)
2. **Heroku Documentation**: [devcenter.heroku.com](https://devcenter.heroku.com)
3. **GitHub Issues**: Create an issue in your repository

## 🎉 Success!

Your AI Dungeon Master is now live on Heroku! Share your app URL with friends and start your epic adventures together.

---

**Note**: Remember to replace `yourusername` in the deployment button URL with your actual GitHub username before sharing your repository.
