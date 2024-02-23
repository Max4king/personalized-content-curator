import os
import json
from datetime import datetime, timedelta
from openai import OpenAI
import openai
from exa_py import Exa
# from trulens_eval import Tru
# from trulens_eval.feedback.provider.openai import OpenAI as fOpenAI
# from trulens_eval import Feedback, Select

# tru = Tru()
# tru.reset_database()
# Load environment variables


SYSTEM_MESSAGE = "You are a helpful assistant that generates search queries based on user questions. Only generate one search query."
USER_QUESTION_TEMPLATE = "What's the recent news/update in {interests} this week?"
SYSTEM_MESSAGE_SUMMARY = """
"Create a weekly news summary based on the following key highlights:

{highlights}

Summarize these points into a cohesive narrative that reflects the week's most newsworthy events and trends. Make sure to be provide a clear and concise summary. It must be no longer than 500 words."
"""
SYSTEM_MESSAGE_TITLE = "conclude with a single title that encapsulates the main themes of the week's news provided."

def format_docs(docs):
        return "\n".join([f"Title: {doc.title}\nHighlights: {doc.highlights}" for doc in docs])

class NewsAISummary:
    # gpt-4-turbo-preview or gpt-3.5-turbo
    def __init__(self, llm_model="gpt-4-turbo-preview", days_ago=7, exa_api_key=None, open_api_key=None) -> None:
        self.title = ""
        self.interests = ""
        self.summary = ""
        self.image_url = ""
        self.llm_model=llm_model
        self.days_ago = days_ago
        self.user_question = USER_QUESTION_TEMPLATE.format(interests=self.interests)
        self.exa = Exa(exa_api_key)
        openai.api_key = open_api_key
        self.llm_client = OpenAI()

    def set_api_keys(self, openai_api_key=None, exa_api_key=None):
        if openai_api_key != "" or openai_api_key is not None:
            openai.api_key = openai_api_key
        if exa_api_key is not None and exa_api_key != "":
            self.exa = Exa(exa_api_key)

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
        self.set_user_question(interests)
        time_frame = (datetime.now() - timedelta(days=self.days_ago))
        date_cutoff = time_frame.strftime("%Y-%m-%d")
                
        # Generate the search query using OpenAI
        completion = self.llm_client.chat.completions.create(
            model=self.llm_model,
            messages=[
                {"role": "system", "content": SYSTEM_MESSAGE},
                {"role": "user", "content": self.user_question},
            ],
        )
        search_query = completion.choices[0].message.content
        
        # Perform the search with Exa
        search_response = self.exa.search_and_contents(
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
        summary_response = self.llm_client.chat.completions.create(
            model=self.llm_model,
            messages=[
                {"role": "system", "content": SYSTEM_MESSAGE_SUMMARY},
                {"role": "user", "content": formatted_results}
            ],
        )
        
        self.summary = summary_response.choices[0].message.content

        return self.summary

    def get_title(self):
        self.title = self.llm_client.chat.completions.create(
            model=self.llm_model,
            messages=[
                {"role": "system", "content": SYSTEM_MESSAGE_TITLE},
                {"role": "user", "content": self.summary}
            ],
        ).choices[0].message.content
        return self.title

    def generate_image(self):
        image_prompt = self.llm_client.chat.completions.create(
            model=self.llm_model,
            messages=[
                {"role": "system", "content": "Generate an prompt for an image based on the summary provided."},
                {"role": "user", "content": self.title},
            ],
            max_tokens=100,
        ).choices[0].message.content

        gen_image = self.llm_client.images.generate(
            model="dall-e-3",
            prompt=image_prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        self.image_url = gen_image.data[0].url
        print("This is the image url: ", self.image_url)
        return gen_image.data[0].url

    # def save_summary(self):
    #     filename = "-".join(x for x in self.title if x.isalnum() or x in "._-")
    #     with open("./archive_summary/" + filename + ".txt", "w") as f:
    #         f.write(self.summary)
    #     import requests
    #     print("This is the url in the save_summary function: ", self.image_url)
    #     response = requests.get(self.image_url)
    #     if response.status_code == 200:
    #         # Define the filename and path where you want to save the image
    #         filename = "".join(x for x in self.title if x.isalnum() or x in "._-") + ".webp"
    #         path = f"./archive_summary/{filename}"
            
    #         # Open a file in binary write mode and save the image data
    #         with open(path, 'wb') as file:
    #             file.write(response.content)
