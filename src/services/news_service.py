import sys
from pathlib import Path
import json
import streamlit as st

# Add src directory to Python path
sys.path.append(str(Path(__file__).resolve().parent.parent))


from services.news_scrapers import site_selector
from services.translation_service import translate_article_data
from utils.aramco_alert import process_rag


class NewsService:

    aramco_keywords = ["aramco", "#aramco", "#saudiaramco", "#saudi#aramco","#aramcosaudi", "#aramco#saudi"]
    def fetch_article(self, url):
        # Logic to fetch the article content
        content = site_selector(url)
        translated = translate_article_data(content)
        title = translated['title']
        content = translated['content']
        aramco_status: bool = False
        
        if  not any(keyword.lower() in title.lower() for keyword in self.aramco_keywords) and not any(keyword.lower() in content.lower() for keyword in self.aramco_keywords):
                aramco_status = False
        else: aramco_status = True

        rag_result = process_rag(translated_text=content)
        result = {
                                        "Title": title,
                                        "Content": content,
                                        "Date": translated['date'],
                                        "Analysis": json.loads(rag_result),
                                        "Aramco Mention": aramco_status
                                    }
        return result