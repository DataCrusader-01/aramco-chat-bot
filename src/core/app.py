import streamlit as st
import sys
from pathlib import Path

# Add src directory to Python path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from utils.video_downloader import VideoDownloader
from utils.audio_converter import Audio_Prcessor
from services.news_service import NewsService
from utils.handle_youtube import yt_info


def main():
    # Streamlit configuration
    st.set_page_config(page_title="Media Analysis App", page_icon="📊", layout="wide")
    st.title("Media Analysis App")

    # Sidebar input options
    st.sidebar.header("Input Options")
    input_source = st.sidebar.radio("Choose Input Source", ["Video File", "Video URL", "News Article URL"])

    # Initialize session state variables
    if "article_data" not in st.session_state:
        st.session_state["article_data"] = None
    if "user_input" not in st.session_state:
        st.session_state["user_input"] = "No"

    # Handle Video File Input
    if input_source == "Video File":
        uploaded_file = st.file_uploader("Upload Video", type=["mp4", "avi", "mov"])
        if uploaded_file is not None:
            video_service = VideoDownloader()
            video_path = video_service.download(uploaded_file)
            audio_service = Audio_Prcessor()
            audio_output = audio_service.audio_processor(video_path)
            st.json(audio_output)

    # Handle Video URL Input
    elif input_source == "Video URL":
        video_url = st.text_input("Enter Video URL")

        if st.button("Download Video"):
            if video_url:
                if "youtube.com" not in video_url:
                    video_service = VideoDownloader()
                    video_path = video_service.download(video_url)
                    audio_service = Audio_Prcessor()
                    st.session_state["article_data"] = audio_service.audio_processor(video_path=video_path)
                elif "youtube.com" in video_url:
                    yt_dict = yt_info(video_url)
                    st.session_state["article_data"] = yt_dict
                    st.success("YouTube video processed successfully!")
                else:
                    st.error("Please enter a valid Video URL.")
            else:
                st.error("Please enter a valid Video URL.")
        
        # Display results based on session state
        if st.session_state.get("article_data"):
            article_data = st.session_state["article_data"]
            if "Aramco Mention" in article_data and article_data["Aramco Mention"] == False:
                st.warning("There are no Aramco mentions in the video content.")
                st.radio(
                    "There are no Aramco mentions. Do you still wish to have further analysis?",
                    ["No", "Yes"],
                    key="user_input"
                )
                if st.session_state["user_input"] == "Yes":
                    st.json(article_data)
                elif st.session_state["user_input"] == "No":
                    st.json({"Aramco Mention": "We don't have any Aramco mentions in the video content."})
            else:
                st.json(article_data)


    # Handle News Article URL Input
    elif input_source == "News Article URL":
        news_url = st.text_input("Enter News Article URL")

        if st.button("Fetch News"):
            if news_url:
                news_service = NewsService()
                st.session_state["article_data"] = news_service.fetch_article(news_url)
                if st.session_state["article_data"]:
                    article_data = st.session_state["article_data"]
                    if article_data["Aramco Mention"] == False:
                        st.warning("There are no Aramco mentions in the article.")
            else:
                st.error("Please enter a valid News Article URL.")
        # Display results based on session state
        if st.session_state.get("article_data"):
            article_data = st.session_state["article_data"]
            if article_data["Aramco Mention"] == False:
                st.warning("There are no Aramco mentions in the article.")
                st.radio(
                    "There are no Aramco mentions. Do you still wish to have further analysis?",
                    ["No", "Yes"],
                   key="user_input"
                )
                if st.session_state["user_input"] == "Yes":
                    st.json(article_data)
                elif st.session_state["user_input"] == "No":
                    st.json({"Aramco Mention": "We don't have any Aramco mentions in the news article."})
            else:
                st.json(article_data)



if __name__ == "__main__":
    main()
