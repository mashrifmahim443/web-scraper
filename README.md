# Web Scraper with OpenAI Q&A

A powerful web scraper that can extract content from websites and answer questions about the scraped content using OpenAI's API.

## Features

- 🌐 **Web Scraping**: Extract clean text content from any website
- 🤖 **AI-Powered Q&A**: Ask questions about scraped content using OpenAI
- 📋 **Content Summarization**: Generate summaries of website content
- 🎯 **Structured Extraction**: Extract titles, headings, and paragraphs
- 💬 **Interactive Mode**: Chat with the scraper in real-time
- 🚀 **Streamlit Web App**: Beautiful web interface ready for hosting

## Installation

1. **Clone or download this repository**

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your OpenAI API key**:
   
   Create a `.env` file in the project root:
   ```bash
   cp .env.example .env
   ```
   
   Then edit `.env` and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_actual_api_key_here
   ```
   
   You can get your API key from [OpenAI Platform](https://platform.openai.com/api-keys)

## 🚀 Streamlit Web App (Recommended)

### Run Locally

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up OpenAI API key** (create `.env` file or use sidebar in app):
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

3. **Run Streamlit app**:
   ```bash
   streamlit run streamlit_app.py
   ```

4. **Open your browser** to `http://localhost:8501`

### Deploy to Streamlit Cloud

1. **Push your code to GitHub** (already done ✅)

2. **Go to [Streamlit Cloud](https://streamlit.io/cloud)**

3. **Sign in with GitHub** and click "New app"

4. **Select your repository**: `mashrifmahim443/web-scraper`

5. **Set main file path**: `streamlit_app.py`

6. **Add secrets** (click "Advanced settings"):
   - Add secret: `OPENAI_API_KEY` with your API key value

7. **Click "Deploy"** 🎉

Your app will be live at: `https://your-app-name.streamlit.app`

## Usage

### Basic Scraping

Scrape a website and see the content:
```bash
python main.py https://example.com
```

### Ask a Question

Scrape a website and ask a question:
```bash
python main.py https://example.com -q "What is this website about?"
```

### Generate Summary

Get a summary of the website content:
```bash
python main.py https://example.com -s
```

### Structured Content Extraction

Extract structured content (title, headings, paragraphs):
```bash
python main.py https://example.com --structured
```

### Interactive Mode

Run in interactive mode to ask multiple questions:
```bash
python interactive.py https://example.com
```

In interactive mode, you can:
- Ask multiple questions about the scraped content
- Type `summary` to get a summary
- Type `exit` or `quit` to stop

### Advanced Options

Use a different OpenAI model:
```bash
python main.py https://example.com -q "Your question" --model gpt-4
```

Pass API key directly (if not using .env file):
```bash
python main.py https://example.com -q "Your question" --api-key your_key_here
```

## Examples

### Example 1: Basic Question Answering
```bash
python main.py https://en.wikipedia.org/wiki/Python_(programming_language) -q "What is Python programming language?"
```

### Example 2: Get Summary
```bash
python main.py https://news.ycombinator.com -s
```

### Example 3: Interactive Session
```bash
python interactive.py https://docs.python.org/3/
```

Then ask questions like:
- "What is Python?"
- "How do I install Python?"
- "What are the main features?"

## Project Structure

```
web-scrapper/
├── scraper.py          # Web scraping module
├── openai_qa.py        # OpenAI Q&A integration
├── main.py             # Main CLI script
├── interactive.py      # Interactive Q&A mode
├── streamlit_app.py    # Streamlit web application
├── requirements.txt    # Python dependencies
├── packages.txt        # System packages for Streamlit Cloud
├── .streamlit/
│   └── config.toml    # Streamlit configuration
├── .env.example        # Environment variables template
└── README.md          # This file
```

## Requirements

- Python 3.7+
- OpenAI API key
- Internet connection

## Dependencies

- `requests`: HTTP library for fetching web pages
- `beautifulsoup4`: HTML parsing library
- `openai`: OpenAI API client
- `python-dotenv`: Environment variable management
- `lxml`: Fast XML/HTML parser
- `streamlit`: Web framework for the interactive app

## Notes

- The scraper respects robots.txt and uses a standard User-Agent
- Content is truncated to ~12,000 characters to fit within OpenAI token limits
- Some websites may block automated scraping - use responsibly
- OpenAI API usage incurs costs based on token usage

## Troubleshooting

**Error: "OpenAI API key not found"**
- Make sure you've created a `.env` file with your API key
- Or pass the API key using `--api-key` parameter

**Error: "Error fetching URL"**
- Check if the URL is valid and accessible
- Some websites may block automated requests
- Try a different URL

**Error: "Error calling OpenAI API"**
- Verify your API key is correct
- Check your OpenAI account has available credits
- Ensure you have internet connectivity

## License

This project is open source and available for personal and educational use.

