from dotenv import load_dotenv
import os
import json
from datetime import datetime, timedelta
import gradio as gr
from openai import OpenAI
from exa_py import Exa
from trulens_eval import Tru
from trulens_eval.feedback.provider.openai import OpenAI as fOpenAI
from trulens_eval import Feedback, Select
import numpy as np

tru = Tru()
tru.reset_database()
# Load environment variables
load_dotenv()

# Initialize Exa and OpenAI clients
exa_api_key = os.getenv('EXA_API_KEY')
openai_api_key = os.getenv('OPENAI_API_KEY')
if not exa_api_key or not openai_api_key:
    raise ValueError("EXA_API_KEY and/or OPENAI_API_KEY environment variables not set!")

exa = Exa(exa_api_key)
llm_client = OpenAI()

DAYS_AGO = 7
MODEL = "gpt-4-turbo-preview"
SYSTEM_MESSAGE = "You are a helpful assistant that generates search queries based on user questions. Only generate one search query."
USER_QUESTION_TEMPLATE = "What's the recent news in {interests} this week?"
SYSTEM_MESSAGE_SUMMARY = """
"Create a weekly news summary based on the following key highlights, and conclude with a single title that encapsulates the main themes of the week:

{highlights}

Summarize these points into a cohesive narrative that reflects the week's most newsworthy events and trends."
"""

user_question = ""

def format_docs(docs):
        return "\n".join([f"Title: {doc.title}\nHighlights: {doc.highlights}" for doc in docs])

# Define the Gradio function
def generate_news_summary(interests):

    if interests == "":
         raise ValueError("Please enter your interests to generate a summary.")
    model = MODEL
    days_ago = DAYS_AGO
    time_frame = (datetime.now() - timedelta(days=days_ago))
    date_cutoff = time_frame.strftime("%Y-%m-%d")
    
    # Construct user question
    global user_question
    user_question = f"What's the recent news in {interests} this week?"
    
    # Generate the search query using OpenAI
    completion = llm_client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_MESSAGE},
            {"role": "user", "content": user_question},
        ],
    )
    search_query = completion.choices[0].message.content
    
    # Perform the search with Exa
    search_response = exa.search_and_contents(
        search_query, 
        use_autoprompt=True, 
        start_published_date=date_cutoff,
        highlights=True, 
        text={'max_characters': 1000},
        num_results=5
    )
    
    # Format the search results into highlights
    highlights = format_docs(search_response.results)
    
    # Generate the summary using OpenAI
    formatted_results = SYSTEM_MESSAGE_SUMMARY.format(highlights=highlights) 
    summary_response = llm_client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_MESSAGE_SUMMARY},
            {"role": "user", "content": formatted_results}
        ],
    )
    
    summary = summary_response.choices[0].message.content

    return summary

def news_summary(interests):
    summary = generate_news_summary(interests)
    # Extract the title from the summary
    title = summary.split("\n")[-1].join("")
    only_summary = summary.split("\n")[:-1].join("")
    print("Title:", title)
    print("Summary:", only_summary)
    return title, only_summary

def feedback_function():
    pass


generate_news_summary("AI")

feedback_function()
