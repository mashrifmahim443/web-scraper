"""
OpenAI Question Answering Module
Handles question answering using OpenAI API
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class OpenAIQA:
    def __init__(self, api_key=None):
        """
        Initialize OpenAI client
        
        Args:
            api_key: OpenAI API key. If None, will try to get from environment variable OPENAI_API_KEY
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError(
                "OpenAI API key not found. Please set OPENAI_API_KEY environment variable "
                "or pass it as a parameter."
            )
        self.client = OpenAI(api_key=self.api_key)
    
    def answer_question(self, context, question, model="gpt-3.5-turbo", max_tokens=500):
        """
        Answer a question based on the provided context
        
        Args:
            context: The text content to answer questions from
            question: The question to answer
            model: OpenAI model to use (default: gpt-3.5-turbo)
            max_tokens: Maximum tokens in response (default: 500)
        
        Returns:
            Dictionary with answer and metadata
        """
        # Truncate context if too long (to avoid token limits)
        max_context_length = 12000  # Leave room for question and response
        if len(context) > max_context_length:
            context = context[:max_context_length] + "... [content truncated]"
        
        prompt = f"""Based on the following website content, please answer the question. 
If the answer cannot be found in the content, please say so.

Website Content:
{context}

Question: {question}

Answer:"""
        
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that answers questions based on provided website content."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=0.7
            )
            
            answer = response.choices[0].message.content.strip()
            
            return {
                'question': question,
                'answer': answer,
                'model': model,
                'tokens_used': response.usage.total_tokens
            }
        except Exception as e:
            raise Exception(f"Error calling OpenAI API: {str(e)}")
    
    def summarize_content(self, content, max_length=200):
        """
        Summarize website content
        
        Args:
            content: The text content to summarize
            max_length: Maximum length of summary in words
        
        Returns:
            Summary string
        """
        max_content_length = 8000
        if len(content) > max_content_length:
            content = content[:max_content_length] + "..."
        
        prompt = f"""Please provide a concise summary of the following website content in approximately {max_length} words:

{content}

Summary:"""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that creates concise summaries."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.5
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise Exception(f"Error summarizing content: {str(e)}")

