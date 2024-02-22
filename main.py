import streamlit as st
from model import generate_news_summary, format_title
from trulens_eval import Tru
from trulens_eval.feedback.provider.openai import OpenAI as fOpenAI
from trulens_eval import Feedback, Select

tru = Tru()
tru.reset_database()
# Setting the page title and layout
st.set_page_config(page_title="News Summary Generator", layout="wide")

# Header or title for the app
st.title("News Summary Generator")

# Creating a tabbed interface
tab1, tab2 = st.tabs(["Summary", "Q&A"]) #  = 

with tab1:
    st.header("Generate Summary")
    # Input text box for user interests
    interests_input = st.text_area("Enter your interests", height=150)

    # Button to generate summary
    if st.button("Generate Summary"):
        # Assuming your news_summary function returns a tuple (title, summary)
        title, summary = format_title(generate_news_summary(interests_input))

        # Displaying the generated title and summary
        st.text_input("Title", value=title, max_chars=None, key=None, type="default", help=None, autocomplete=None, on_change=None, args=None, kwargs=None, placeholder=None, disabled=False)
        st.text_area("Summary", value=summary, height=250)

# add more functionality or tabs later
# with tab2:
#     st.write("Q&A.")

fopenai = fOpenAI()

# Define a relevance function from openai
f_relevance = Feedback(fopenai.relevance).on_input_output()
from trulens_eval import TruBasicApp

tru_llm_recorder = TruBasicApp(generate_news_summary, app_id="Personalized Content Curator", feedbacks=[f_relevance])
with tru_llm_recorder as recording:
    tru_llm_recorder.app(interests_input)

tru.get_leaderboard(app_ids=["Personalized Content Curator"])


tru.run_dashboard()
