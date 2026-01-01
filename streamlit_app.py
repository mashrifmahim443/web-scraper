"""
Streamlit Web Scraper with OpenAI Q&A
Web interface for scraping websites and asking questions
"""

import streamlit as st
import os
from scraper import WebScraper
from openai_qa import OpenAIQA

# Page configuration
st.set_page_config(
    page_title="Web Scraper with AI Q&A",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        font-weight: bold;
    }
    .info-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f0f2f6;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'scraped_content' not in st.session_state:
    st.session_state.scraped_content = None
if 'scraped_url' not in st.session_state:
    st.session_state.scraped_url = None
if 'qa_initialized' not in st.session_state:
    st.session_state.qa_initialized = False

def initialize_qa():
    """Initialize OpenAI QA client"""
    api_key = st.session_state.get('api_key') or os.getenv('OPENAI_API_KEY')
    if api_key:
        try:
            return OpenAIQA(api_key=api_key)
        except Exception as e:
            st.error(f"Error initializing OpenAI: {str(e)}")
            return None
    return None

# Header
st.markdown('<h1 class="main-header">🌐 Web Scraper with AI Q&A</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Scrape websites and ask questions using AI</p>', unsafe_allow_html=True)

# Sidebar for configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # API Key input
    api_key_input = st.text_input(
        "OpenAI API Key",
        type="password",
        value=st.session_state.get('api_key', ''),
        help="Enter your OpenAI API key or set OPENAI_API_KEY environment variable"
    )
    st.session_state['api_key'] = api_key_input
    
    if api_key_input or os.getenv('OPENAI_API_KEY'):
        st.success("✅ API Key configured")
        st.session_state.qa_initialized = True
    else:
        st.warning("⚠️ Please enter your OpenAI API key")
        st.session_state.qa_initialized = False
    
    st.divider()
    
    # Model selection
    model = st.selectbox(
        "OpenAI Model",
        ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo-preview"],
        index=0,
        help="Select the OpenAI model to use"
    )
    
    st.divider()
    
    # Instructions
    st.header("📖 How to Use")
    st.markdown("""
    1. Enter a website URL
    2. Click "Scrape Website"
    3. Ask questions about the content
    4. Or generate a summary
    """)
    
    st.divider()
    
    # Clear button
    if st.button("🗑️ Clear All Data"):
        st.session_state.scraped_content = None
        st.session_state.scraped_url = None
        st.rerun()

# Main content area
tab1, tab2, tab3 = st.tabs(["🔍 Scrape & Ask", "📋 Summary", "📊 About"])

with tab1:
    # URL input
    url = st.text_input(
        "Enter Website URL",
        placeholder="https://example.com",
        value=st.session_state.scraped_url or ""
    )
    
    col1, col2 = st.columns([1, 4])
    with col1:
        scrape_button = st.button("🔍 Scrape Website", type="primary", use_container_width=True)
    
    if scrape_button:
        if not url:
            st.error("Please enter a URL")
        else:
            with st.spinner("Scraping website..."):
                try:
                    scraper = WebScraper()
                    content = scraper.scrape(url)
                    st.session_state.scraped_content = content['text']
                    st.session_state.scraped_url = url
                    st.success(f"✅ Successfully scraped {len(content['text'])} characters from {url}")
                except Exception as e:
                    st.error(f"❌ Error scraping website: {str(e)}")
    
    # Display scraped content if available
    if st.session_state.scraped_content:
        st.divider()
        st.subheader(f"📄 Content from: {st.session_state.scraped_url}")
        
        # Content preview
        with st.expander("📖 View Scraped Content", expanded=False):
            content_preview = st.session_state.scraped_content[:2000] + "..." if len(st.session_state.scraped_content) > 2000 else st.session_state.scraped_content
            st.text_area("Content", content_preview, height=200, disabled=True, label_visibility="collapsed")
            st.caption(f"Total characters: {len(st.session_state.scraped_content)}")
        
        st.divider()
        
        # Question input
        st.subheader("❓ Ask a Question")
        
        if not st.session_state.qa_initialized:
            st.warning("⚠️ Please configure your OpenAI API key in the sidebar to ask questions")
        else:
            question = st.text_input(
                "Enter your question",
                placeholder="What is this website about?",
                key="question_input"
            )
            
            col1, col2 = st.columns([1, 1])
            with col1:
                ask_button = st.button("💡 Ask Question", type="primary", use_container_width=True)
            with col2:
                summary_button = st.button("📋 Generate Summary", use_container_width=True)
            
            if ask_button and question:
                with st.spinner("🤔 Thinking..."):
                    try:
                        qa = initialize_qa()
                        if qa:
                            result = qa.answer_question(
                                st.session_state.scraped_content,
                                question,
                                model=model
                            )
                            
                            st.success("✅ Answer Generated")
                            st.markdown("### 💡 Answer:")
                            st.markdown(result['answer'])
                            st.caption(f"📊 Tokens used: {result['tokens_used']}")
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
            
            elif ask_button and not question:
                st.warning("Please enter a question")
            
            if summary_button:
                with st.spinner("📋 Generating summary..."):
                    try:
                        qa = initialize_qa()
                        if qa:
                            summary = qa.summarize_content(st.session_state.scraped_content)
                            st.success("✅ Summary Generated")
                            st.markdown("### 📋 Summary:")
                            st.markdown(summary)
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")

with tab2:
    st.subheader("📋 Content Summary")
    
    if not st.session_state.scraped_content:
        st.info("👆 Please scrape a website first using the 'Scrape & Ask' tab")
    elif not st.session_state.qa_initialized:
        st.warning("⚠️ Please configure your OpenAI API key in the sidebar")
    else:
        if st.button("🔄 Generate New Summary", type="primary"):
            with st.spinner("📋 Generating summary..."):
                try:
                    qa = initialize_qa()
                    if qa:
                        summary = qa.summarize_content(st.session_state.scraped_content)
                        st.markdown("### 📋 Summary:")
                        st.markdown(summary)
                        
                        st.divider()
                        st.markdown(f"**Source URL:** {st.session_state.scraped_url}")
                        st.caption(f"**Content Length:** {len(st.session_state.scraped_content)} characters")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
        else:
            st.info("Click the button above to generate a summary of the scraped content")

with tab3:
    st.header("📊 About This App")
    
    st.markdown("""
    ### 🌐 Web Scraper with AI Q&A
    
    This application allows you to:
    - **Scrape websites** and extract clean text content
    - **Ask questions** about the scraped content using OpenAI
    - **Generate summaries** of website content
    
    ### 🚀 Features
    
    - ✅ Clean text extraction from any website
    - ✅ AI-powered question answering
    - ✅ Content summarization
    - ✅ User-friendly web interface
    - ✅ Multiple OpenAI model support
    
    ### 🔧 Technology Stack
    
    - **Streamlit** - Web interface
    - **BeautifulSoup** - HTML parsing
    - **OpenAI API** - Question answering and summarization
    - **Requests** - HTTP requests
    
    ### 📝 Usage Tips
    
    1. Make sure you have a valid OpenAI API key
    2. Enter a valid website URL
    3. Wait for the content to be scraped
    4. Ask questions or generate summaries
    
    ### ⚠️ Important Notes
    
    - Some websites may block automated scraping
    - OpenAI API usage incurs costs based on token usage
    - Content is truncated to fit within token limits
    - Always respect website terms of service
    
    ### 📚 Source Code
    
    Check out the source code on [GitHub](https://github.com/mashrifmahim443/web-scraper)
    """)
    
    st.divider()
    
    st.subheader("🔑 API Key Setup")
    st.markdown("""
    To use this app, you need an OpenAI API key:
    
    1. Sign up at [OpenAI Platform](https://platform.openai.com)
    2. Get your API key from [API Keys](https://platform.openai.com/api-keys)
    3. Enter it in the sidebar configuration
    
    For Streamlit Cloud deployment, set the `OPENAI_API_KEY` environment variable.
    """)

# Footer
st.divider()
st.markdown(
    "<div style='text-align: center; color: #666; padding: 1rem;'>"
    "Made with ❤️ using Streamlit | "
    "<a href='https://github.com/mashrifmahim443/web-scraper' target='_blank'>GitHub</a>"
    "</div>",
    unsafe_allow_html=True
)

