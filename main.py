"""
Main Web Scraper with Q&A Functionality
Combines web scraping and OpenAI question answering
"""

import argparse
import sys
from scraper import WebScraper
from openai_qa import OpenAIQA


def main():
    parser = argparse.ArgumentParser(
        description='Web Scraper with OpenAI Q&A - Scrape websites and answer questions'
    )
    parser.add_argument('url', help='URL of the website to scrape')
    parser.add_argument(
        '-q', '--question',
        help='Question to answer based on the scraped content'
    )
    parser.add_argument(
        '-s', '--summarize',
        action='store_true',
        help='Generate a summary of the website content'
    )
    parser.add_argument(
        '--structured',
        action='store_true',
        help='Extract structured content (title, headings, paragraphs)'
    )
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
    
    # Initialize scraper
    print(f"🔍 Scraping website: {args.url}")
    scraper = WebScraper()
    
    try:
        # Scrape the website
        content = scraper.scrape(args.url, structured=args.structured)
        
        if args.structured:
            text_content = content['full_text']
            print(f"\n📄 Title: {content['structured']['title']}")
            print(f"📊 Found {len(content['structured']['headings'])} headings")
            print(f"📝 Found {len(content['structured']['paragraphs'])} paragraphs")
        else:
            text_content = content['text']
            print(f"\n✅ Successfully scraped {len(text_content)} characters")
        
        # Initialize OpenAI QA
        if args.question or args.summarize:
            print("\n🤖 Initializing OpenAI...")
            qa = OpenAIQA(api_key=args.api_key)
        
        # Answer question if provided
        if args.question:
            print(f"\n❓ Question: {args.question}")
            print("💭 Thinking...")
            result = qa.answer_question(text_content, args.question, model=args.model)
            print(f"\n💡 Answer:\n{result['answer']}")
            print(f"\n📊 Tokens used: {result['tokens_used']}")
        
        # Generate summary if requested
        if args.summarize:
            print("\n📋 Generating summary...")
            summary = qa.summarize_content(text_content)
            print(f"\n📄 Summary:\n{summary}")
        
        # If no question or summary, just show content preview
        if not args.question and not args.summarize:
            preview = text_content[:500] + "..." if len(text_content) > 500 else text_content
            print(f"\n📄 Content Preview:\n{preview}")
            print(f"\n💡 Tip: Use -q 'your question' to ask questions about this content")
            print(f"💡 Tip: Use -s to generate a summary")
    
    except Exception as e:
        print(f"\n❌ Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

