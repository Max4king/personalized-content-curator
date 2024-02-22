import streamlit as st
from model import NewsAISummary
from trulens_eval import Tru
from trulens_eval import Feedback
from trulens_eval import Feedback, OpenAI as fOpenAI, Tru
from trulens_eval import TruBasicApp

tru = Tru()
# tru.reset_database()

def init_or_update_news_ai_summary(openai_api_key=None, exa_api_key=None):
    if 'news_ai_summary' not in st.session_state or openai_api_key or exa_api_key:
        # Initialize NewsAISummary with provided API keys or existing ones
        st.session_state.news_ai_summary = NewsAISummary(
            open_api_key=openai_api_key or st.session_state.get('openai_api_key'),
            exa_api_key=exa_api_key or st.session_state.get('exa_api_key')
        )

# Define a relevance function from openai
# Setting the page title and layout
st.set_page_config(page_title="Personalized Content Curator", layout="wide")
st.title("Personalized Content Curator")

# Creating a tabbed interface
tab1, setting = st.tabs(["Summary", "Setting"])


try:
    ai_summary = NewsAISummary()
except ValueError as e:
    ai_summary = None
    st.error(f"Failed to initialize NewsAISummary: {e}")

fopenai = fOpenAI()
f_relevance = Feedback(fopenai.relevance).on_input_output()

tru_llm_recorder = TruBasicApp(ai_summary.generate_news_summary, app_id="Content Curator", feedbacks=[f_relevance])

def update_api_keys(openai_api_key=None, exa_api_key=None):
    if openai_api_key:
        ai_summary.set_api_keys(openai_api_key=openai_api_key)
    if exa_api_key:
        ai_summary.set_api_keys(exa_api_key=exa_api_key)

    # Update the instance in session_state
    st.session_state['news_ai_summary'] = ai_summary

        
init_or_update_news_ai_summary()


with tab1:
    st.header("Generate Summary")
    st.write("The structure of the input is 'What's the recent news/update in {interests} this week?'\nYou can enter more than one interest separated by a comma. But it will become less detailed when the interest is not related.")
    if 'news_ai_summary' in st.session_state:
        ai_summary = st.session_state.news_ai_summary
        interests_input = st.text_area("Enter your interests", height=20, placeholder="Examples: AI, Machine Learning, LLM from Google....")

        if st.button("Generate Summary"):
            with st.spinner('Processing...'):
                summary = ai_summary.generate_news_summary(interests_input)
                title = ai_summary.get_title()
                image_url = ai_summary.generate_image()
                with tru_llm_recorder as recording:
                        tru_llm_recorder.app(ai_summary.user_question)
                st.markdown(f"# {title}\n![Generated Image]({image_url})\n\n{summary}")

        if st.button("Save Summary"):
            ai_summary.save_summary()
            st.success("Summary saved.")
    else:
        st.warning("Please configure your API keys in the Settings tab.")

with setting:
    st.header("Settings")
    openai_api_key = st.text_input("OpenAI API Key", key="openai_key")
    exa_api_key = st.text_input("Exa API Key", key="exa_key")

    if st.button("Save API Keys"):
        # Save the API keys in session_state
        st.session_state['openai_api_key'] = openai_api_key
        st.session_state['exa_api_key'] = exa_api_key
        # Initialize or update the NewsAISummary instance with new API keys
        init_or_update_news_ai_summary(openai_api_key, exa_api_key)
        st.success("API keys updated and saved.")

tru.run_dashboard(port=8502)
