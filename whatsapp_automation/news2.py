import requests
from twilio.rest import Client
from datetime import datetime, timedelta
import time
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# News API Configuration
NEWS_API_KEY = os.getenv('NEWS_API_KEY')
NEWS_KEYWORDS = 'Trump, Biden, USA, Election'
NEWS_LANGUAGE = 'en'
NEWS_COUNT = 5

# Twilio Configuration
TWILIO_SID = os.getenv('TWILIO_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE = os.getenv('TWILIO_PHONE')
GROUP_ID = os.getenv('GROUP_ID')  # Must be a WhatsApp-enabled individual number

MESSAGE_DELAY = 5  # Seconds between messages

def get_news():
    """Fetch news articles from News API for the past day"""
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    url = f'https://newsapi.org/v2/everything?q={NEWS_KEYWORDS}&from={yesterday}&sortBy=popularity&apiKey={NEWS_API_KEY}'
    response = requests.get(url)
    data = response.json()
    return data.get('articles', [])[:NEWS_COUNT]

def send_whatsapp_alert(message):
    """Send message via Twilio's WhatsApp API"""
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=message,
        from_=f'whatsapp:{TWILIO_PHONE}',
        to=f'whatsapp:{GROUP_ID}'
    )
    return message.sid

def format_article(article, index):
    """Format a single news article"""
    title = article.get('title', 'No title')
    url = article.get('url', '')
    source = article.get('source', {}).get('name', 'Unknown source')
    published_at = article.get('publishedAt', '').split('T')[0]
    
    return (
        f"📰 *News Update {index}/{NEWS_COUNT}*\n\n"
        f"*Source:* {source}\n"
        f"*Date:* {published_at}\n\n"
        f"{title}\n\n"
        f"🔗 Read more: {url}"
    )

if __name__ == '__main__':
    articles = get_news()
    print(f"Found {len(articles)} articles")
    
    if not articles:
        print("No articles found!")
        exit()

    for index, article in enumerate(articles, 1):
        message = format_article(article, index)
        print(f"\nSending article {index}/{len(articles)}:")
        print("-" * 50)
        print(message)
        print("-" * 50)
        
        try:
            message_sid = send_whatsapp_alert(message)
            print(f"✅ Successfully sent! (SID: {message_sid})")
            
            if index < len(articles):
                print(f"Waiting {MESSAGE_DELAY} seconds...")
                time.sleep(MESSAGE_DELAY)
                
        except Exception as e:
            print(f"❌ Failed to send: {str(e)}")

    print("\n✨ News distribution completed!")