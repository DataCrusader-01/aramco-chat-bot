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

    def fetch_article(self, url):
        # Logic to fetch the article content
        content = site_selector(url)
        translated = translate_article_data(content)
        title = translated['title']
        content = translated['content']
        # if "aramco" not in title.lower() and "aramco" not in content.lower():
        #     return {"Mention":"No Aramco Mention"}
        # rag_result = process_rag(translated_text=content)
        if  not any(keyword.lower() in title.lower() for keyword in self.aramco_keywords) and not any(keyword.lower() in content.lower() for keyword in self.aramco_keywords):
                user_response = st.radio("Do you want to process further?", ("Yes", "No"))
                submit_button = st.button("Submit")
                if submit_button:
                    if user_response == "Yes":
                        rag_result = process_rag(translated_text=content)
                        result = {
                                        "Title": title,
                                        "Content": content,
                                        "Date": translated['date'],
                                        "Analysis": json.loads(rag_result)
                                    }
                        return result
                    elif user_response == "No":
                        return {"Mention":"No Aramco Mention"}
        else:
            rag_result = process_rag(translated_text=content)
            result = {
            "Title": title,
            "Content": content,
            "Date": translated['date'],
            "Analysis": json.loads(rag_result)
        }
            return result
        # print(content)
    # result = {
    #         "Title": title,
    #         "Content": content,
    #         "Date": translated['date'],
    #         "Analysis": json.loads(rag_result)
    #     }
        
    # return result