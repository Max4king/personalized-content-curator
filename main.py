import streamlit as st
from model import NewsAISummary
from trulens_eval import Tru
from trulens_eval import Feedback
from trulens_eval import Feedback, OpenAI as fOpenAI, Tru
from trulens_eval import TruBasicApp
from dotenv import load_dotenv
load_dotenv()
import os
if os.getenv("OPENAI_API_KEY") is not None:
    st.session_state["openai_api_key"] = os.getenv("OPENAI_API_KEY")
if os.getenv("EXA_API_KEY") is not None:
    st.session_state["exa_api_key"] = os.getenv("EXA_API_KEY")

st.session_state['days_ago'] = 7
tru = Tru()
# tru.reset_database()

def init_or_update_news_ai_summary():
    if 'news_ai_summary' not in st.session_state or 'openai_api_key' in st.session_state or 'exa_api_key' in st.session_state:
        # Initialize NewsAISummary with provided API keys or existing ones
        st.session_state.news_ai_summary = NewsAISummary(
            days_ago= st.session_state.get('days_ago'),
            open_api_key= st.session_state.get('openai_api_key'),
            exa_api_key= st.session_state.get('exa_api_key'),
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
    
init_or_update_news_ai_summary()


with tab1:
    st.header("Generate Summary")
    st.write("The structure of the input is 'What's the recent news/update in {interests} this week?'\nYou can enter more than one interest separated by a comma. But it will become less detailed when the interest is not related to each other.")
    if 'news_ai_summary' in st.session_state:

        # Add a warning if the api keys are not set
        if not st.session_state.get('openai_api_key') or not st.session_state.get('exa_api_key'):
            st.warning("Please configure your API keys in the Settings tab.")

        ai_summary = st.session_state.news_ai_summary
        interests_input = st.text_area("Enter your interests", height=20, placeholder="Examples: AI, Machine Learning, LLM from Google....")

        if st.button("Generate Summary"):
            with st.spinner('Processing...'):
                summary = ai_summary.generate_news_summary(interests_input)
                title = ai_summary.get_title()
                image_url = ai_summary.generate_image()
                with tru_llm_recorder as recording:
                        tru_llm_recorder.app(ai_summary.user_question)
                st.markdown(f"# {title}\n")
                st.image(image_url, use_column_width=True)
                st.write(summary)

        # if st.button("Save Summary"):
        #     ai_summary.save_summary()
        #     st.success("Summary saved.")
    else:
        st.warning("Please configure your API keys in the Settings tab.")

with setting:
    st.header("Settings")
    openai_api_key = st.text_input("OpenAI API Key", key="openai_key")
    exa_api_key = st.text_input("Exa API Key", key="exa_key")
    days_ago = st.number_input("Days ago", min_value=1, max_value=30, value=7)
    if st.button("Save API Keys"):
        # Save the API keys in session_state
        st.session_state['openai_api_key'] = openai_api_key
        st.session_state['exa_api_key'] = exa_api_key
        st.session_state['days_ago'] = days_ago
        # Initialize or update the NewsAISummary instance with new API keys
        init_or_update_news_ai_summary()
        st.session_state.news_ai_summary.set_api_keys()
        st.success("API keys updated and saved.")
        st.rerun()

    if 'openai_api_key' in st.session_state and st.session_state['openai_api_key']:
        st.success("OpenAI API Key is set.")
    else:
        st.warning("Please add your OpenAI API keys.")

    if 'exa_api_key' in st.session_state and st.session_state['exa_api_key']:
        st.success("Exa API Key is set.")
    else:
        st.warning("Please add your Exa API keys.")

tru.run_dashboard(port=8502)
