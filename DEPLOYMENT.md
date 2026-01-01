# 🚀 Streamlit Cloud Deployment Guide

## Quick Deployment Steps

### 1. Prerequisites
- ✅ Code pushed to GitHub (already done)
- ✅ OpenAI API key ready

### 2. Deploy to Streamlit Cloud

1. **Visit [Streamlit Cloud](https://streamlit.io/cloud)**
   - Sign in with your GitHub account

2. **Create New App**
   - Click "New app" button
   - Select repository: `mashrifmahim443/web-scraper`
   - Branch: `main`
   - Main file path: `streamlit_app.py`

3. **Configure Secrets**
   - Click "Advanced settings"
   - Click "Secrets" tab
   - Add secret:
     ```
     OPENAI_API_KEY = "your_actual_api_key_here"
     ```

4. **Deploy**
   - Click "Deploy" button
   - Wait for deployment (usually 1-2 minutes)

5. **Access Your App**
   - Your app will be live at: `https://web-scraper.streamlit.app` (or similar)
   - Share the URL with others!

## Local Testing

Before deploying, test locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run streamlit_app.py
```

## Environment Variables

For local development, create `.env` file:
```
OPENAI_API_KEY=your_api_key_here
```

For Streamlit Cloud, use the Secrets section in the dashboard.

## Troubleshooting

**App won't deploy:**
- Check that `streamlit_app.py` exists in the root directory
- Verify `requirements.txt` has all dependencies
- Check Streamlit Cloud logs for errors

**API key not working:**
- Verify the secret is named exactly `OPENAI_API_KEY`
- Check that your OpenAI API key is valid and has credits
- Try regenerating the API key

**Import errors:**
- Make sure all dependencies are in `requirements.txt`
- Check Python version (Streamlit Cloud uses Python 3.9+)

## App Features

Once deployed, your app will have:
- ✅ Web scraping interface
- ✅ AI-powered Q&A
- ✅ Content summarization
- ✅ Multiple OpenAI model support
- ✅ Beautiful, responsive UI

Enjoy your deployed app! 🎉

