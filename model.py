from dotenv import load_dotenv
import os
import json
from datetime import datetime, timedelta
import gradio as gr
from openai import OpenAI
from exa_py import Exa
# from trulens_eval import Tru
# from trulens_eval.feedback.provider.openai import OpenAI as fOpenAI
# from trulens_eval import Feedback, Select

# tru = Tru()
# tru.reset_database()
# Load environment variables
load_dotenv()

# Initialize Exa and OpenAI clients
exa_api_key = os.getenv('EXA_API_KEY')
openai_api_key = os.getenv('OPENAI_API_KEY')


SYSTEM_MESSAGE = "You are a helpful assistant that generates search queries based on user questions. Only generate one search query."
USER_QUESTION_TEMPLATE = "What's the recent news in {interests} this week?"
SYSTEM_MESSAGE_SUMMARY = """
"Create a weekly news summary based on the following key highlights:

{highlights}

Summarize these points into a cohesive narrative that reflects the week's most newsworthy events and trends."
"""
SYSTEM_MESSAGE_TITLE = "conclude with a single title that encapsulates the main themes of the week's news provided."

def format_docs(docs):
        return "\n".join([f"Title: {doc.title}\nHighlights: {doc.highlights}" for doc in docs])

class NewsAISummary:

    def __init__(self, , days_ago=7) -> None:
title = ""
interests = ""
summary = ""
llm_model="gpt-4-turbo-preview"
days_ago = days_ago
user_question = USER_QUESTION_TEMPLATE.format(interests=self.interests)

if not exa_api_key or not openai_api_key:
    raise ValueError("EXA_API_KEY and/or OPENAI_API_KEY environment variables not set! Go to settings to set the API keys.")
self.exa = Exa(exa_api_key)
self.llm_client = OpenAI()

    def set_api_keys(self, **kwarg):
        if 'openai_api_key' in kwarg and kwarg['openai_api_key'] != "":
            self.openai = OpenAI(kwarg['openai_api_key'])
        if 'exa_api_key' in kwarg and kwarg['exa_api_key'] != "":
            self.exa = Exa(kwarg['exa_api_key'])

    def set_user_question(self, interests):
        if interests == "":
            return
        self.interests = interests
        self.user_question = USER_QUESTION_TEMPLATE.format(interests=self.interests)

def generate_news_summary(self, interests):
    """
    Generate answer from context.
    """
    if interests == "":
        return
    set_user_question(interests)
    time_frame = (datetime.now() - timedelta(days=self.days_ago))
    date_cutoff = time_frame.strftime("%Y-%m-%d")
            
    # Generate the search query using OpenAI
    completion = llm_client.chat.completions.create(
        model=llm_model,
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
        model=llm_model,
        messages=[
            {"role": "system", "content": SYSTEM_MESSAGE_SUMMARY},
            {"role": "user", "content": formatted_results}
        ],
    )
    
    summary = summary_response.choices[0].message.content

    return summary

def get_title(summary):
    title = llm_client.chat.completions.create(
        model=llm_model,
        messages=[
            {"role": "system", "content": SYSTEM_MESSAGE_TITLE},
            {"role": "user", "content": summary}
        ],
    ).choices[0].message.content
    return title

def generate_image(title):
    gen_image = llm_client.images.generate(
        model="dall-e-3",
        prompt=title,
        size="1024x1024",
        quality="standard",
        n=1,
    )
    return gen_image.data[0].url
