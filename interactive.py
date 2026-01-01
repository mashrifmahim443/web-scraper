"""
Interactive Web Scraper with Q&A
Allows interactive question answering on scraped content
"""

import sys
from scraper import WebScraper
from openai_qa import OpenAIQA


def interactive_mode(url, api_key=None, model="gpt-3.5-turbo"):
    """
    Run interactive Q&A mode
    
    Args:
        url: URL to scrape
        api_key: OpenAI API key
        model: OpenAI model to use
    """
    print(f"🔍 Scraping website: {url}")
    scraper = WebScraper()
    
    try:
        # Scrape the website
        content = scraper.scrape(url)
        text_content = content['text']
        print(f"✅ Successfully scraped {len(text_content)} characters\n")
        
        # Initialize OpenAI QA
        print("🤖 Initializing OpenAI...")
        qa = OpenAIQA(api_key=api_key)
        print("✅ Ready!\n")
        
        print("=" * 60)
        print("Interactive Q&A Mode")
        print("Type 'exit' or 'quit' to stop")
        print("Type 'summary' to get a summary of the content")
        print("=" * 60)
        print()
        
        while True:
            try:
                question = input("❓ Your question: ").strip()
                
                if not question:
                    continue
                
                if question.lower() in ['exit', 'quit', 'q']:
                    print("\n👋 Goodbye!")
                    break
                
                if question.lower() == 'summary':
                    print("\n📋 Generating summary...")
                    summary = qa.summarize_content(text_content)
                    print(f"\n📄 Summary:\n{summary}\n")
                    continue
                
                print("💭 Thinking...")
                result = qa.answer_question(text_content, question, model=model)
                print(f"\n💡 Answer:\n{result['answer']}")
                print(f"📊 Tokens used: {result['tokens_used']}\n")
            
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {str(e)}\n")
    
    except Exception as e:
        print(f"\n❌ Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Interactive Web Scraper with Q&A'
    )
    parser.add_argument('url', help='URL of the website to scrape')
    parser.add_argument(
        '--api-key',
        help='OpenAI API key (or set OPENAI_API_KEY environment variable)'
    )
    parser.add_argument(
        '--model',
        default='gpt-3.5-turbo',
        help='OpenAI model to use (default: gpt-3.5-turbo)'
    )
    
    args = parser.parse_args()
    interactive_mode(args.url, args.api_key, args.model)

