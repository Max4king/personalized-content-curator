import streamlit as st
from model import NewsAISummary
from trulens_eval import Tru
from trulens_eval import Feedback
from trulens_eval import Feedback, OpenAI as fOpenAI, Tru

tru = Tru()
tru.reset_database()

# Define a relevance function from openai
# Setting the page title and layout
st.set_page_config(page_title="Personalized Content Curator", layout="wide")

# Header or title for the app
st.title("Personalized Content Curator")

# Creating a tabbed interface
tab1, setting = st.tabs(["Summary", "Setting"])


from trulens_eval import TruBasicApp

ai_summary = NewsAISummary()
with tab1:
    st.header("Generate Summary")
    interests_input = st.text_area("Enter your interests", height=50)
    
    # Placeholder for the output
    output_placeholder = st.empty()
    if st.button("Generate Summary"):
        with st.spinner('Processing...'):
            # Generate the summarys            
            summary = ai_summary.generate_news_summary(interests_input)
            title = ai_summary.get_title()
            image_url = ai_summary.generate_image()
            # Display the title and summary in the placeholder
            # st.image(image_url,caption ='Generated Image')
            output_placeholder.markdown(f"# Title: {title}\n![Generated Image]({image_url})\n\n# Summary:\n{summary}")

fopenai = fOpenAI()
f_relevance = Feedback(fopenai.relevance).on_input_output()

tru_llm_recorder = TruBasicApp( ai_summary.generate_news_summary,app_id="Personalized Content Curator", Feedbacks=[f_relevance])
# tru.get_leaderboard(app_ids=["Personalized Content Curator"])
with tru_llm_recorder as recording:
            tru_llm_recorder.app(ai_summary.user_question)

with setting:
    st.header("Settings")
    
    # input for openai api key
    openai_api_key = st.text_input("OpenAI API Key")
    exa_api_key = st.text_input("Exa API Key")

    # Save the api keys
    if st.button("Save"):
        ai_summary.set_api_keys(openai_api_key=openai_api_key, exa_api_key=exa_api_key)

# add more functionality or tabs later
# with tab2:
#     st.write("Q&A.")
        

tru.run_dashboard(port=8502)
