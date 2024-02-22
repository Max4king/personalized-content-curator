import streamlit as st
from model import generate_news_summary, get_title, generate_image
from trulens_eval import Tru
from trulens_eval.feedback.provider.openai import OpenAI as fOpenAI
from trulens_eval import Feedback, Select

tru = Tru()
# tru.reset_database()

fopenai = fOpenAI()

# Define a relevance function from openai
f_relevance = Feedback(fopenai.relevance).on_input_output()
# Setting the page title and layout
st.set_page_config(page_title="News Summary Generator", layout="wide")

# Header or title for the app
st.title("News Summary Generator")

# Creating a tabbed interface
tab1, tab2 = st.tabs(["Summary", "Q&A"]) #  = 


from trulens_eval import TruBasicApp
tru_llm_recorder = TruBasicApp( generate_news_summary,app_id="Personalized Content Curator", Feedbacks=[f_relevance])

with tab1:
    st.header("Generate Summary")
    interests_input = st.text_area("Enter your interests", height=50)
    
    # Placeholder for the output
    output_placeholder = st.empty()

    if st.button("Generate Summary"):
        with st.spinner('Processing...'):
            # Generate the summary
            summary = generate_news_summary(interests_input)
            title = get_title(summary)
            image_url = generate_image(title)
            # Display the title and summary in the placeholder
            # st.image(image_url, caption='Generated Image')
            output_placeholder.markdown(f"# Title:{title}\n![Generated Image]({image_url})\n\n### Summary:\n{summary}")


# add more functionality or tabs later
# with tab2:
#     st.write("Q&A.")
# tru.get_leaderboard(app_ids=["Personalized Content Curator"])
with tru_llm_recorder as recording:
            tru_llm_recorder.app(interests_input)
tru.run_dashboard(port=8502)
