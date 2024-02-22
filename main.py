import streamlit as st
from model import NewsAISummary
from trulens_eval import Tru
from trulens_eval import Feedback
from trulens_eval import Feedback, OpenAI as fOpenAI, Tru
from trulens_eval import TruBasicApp

tru = Tru()
# tru.reset_database()

# Define a relevance function from openai
# Setting the page title and layout
st.set_page_config(page_title="Personalized Content Curator", layout="wide")

# Header or title for the app
st.title("Personalized Content Curator")

# Creating a tabbed interface
tab1, setting = st.tabs(["Summary", "Setting"])



ai_summary = NewsAISummary()

fopenai = fOpenAI()
f_relevance = Feedback(fopenai.relevance).on_input_output()

tru_llm_recorder = TruBasicApp(ai_summary.generate_news_summary, app_id="Content Curator", feedbacks=[f_relevance])


with tab1:
    st.header("Generate Summary")
    st.write("The structure of the input is 'What's the recent news/update in {interests} this week?' You can enter more than one interest separated by a comma. But it will become less detailed when the interest is not related.")
    interests_input = st.text_area("Enter your interests", height=20, placeholder="Examples: AI, Machine Learning , LLM from google....")
    
    if st.button("Generate Summary"):
        with st.spinner('Processing...'):
            # Generate the summarys            
            summary = ai_summary.generate_news_summary(interests_input)
            title = ai_summary.get_title()
            image_url = ai_summary.generate_image()
            with tru_llm_recorder as recording:
                tru_llm_recorder.app(ai_summary.user_question)
            # Display the title and summary in the placeholder
            # st.image(image_url,caption ='Generated Image')
    # Placeholder for the output
    output_placeholder = st.empty()
                
if 'summary' in locals():
    output_placeholder.markdown(f"# {title}\n![Generated Image]({image_url})\n\n{summary}")




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
