import os
from dotenv import load_dotenv
from trulens_eval import Tru
from exa_py import Exa
load_dotenv()
exa_api_key = os.getenv('EXA_API_KEY')
tru = Tru()
tru.reset_database()
from model import NewsAISummary
# Create openai client
from openai import OpenAI
client = OpenAI()

# Imports main tools:
from trulens_eval import Feedback, OpenAI as fOpenAI, Tru
tru = Tru()
tru.reset_database()

class AI_TEST:
    def llm_standalone(self, prompt):
        return client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
                {"role": "system", "content": "You are a question and answer bot, and you answer super upbeat."},
                {"role": "user", "content": prompt}
            ]
        ).choices[0].message.content

prompt_input="language AI"
ai_model = NewsAISummary()
prompt_output = ai_model.generate_news_summary(prompt_input)

# Initialize OpenAI-based feedback function collection class:
fopenai = fOpenAI()

# Define a relevance function from openai
f_relevance = Feedback(fopenai.relevance).on_input_output()

from trulens_eval import TruBasicApp
tru_llm_standalone_recorder = TruBasicApp(ai_model.generate_news_summary, app_id="Happy Bot", feedbacks=[f_relevance])

with tru_llm_standalone_recorder as recording:
    tru_llm_standalone_recorder.app(prompt_input)

tru.run_dashboard(port=8502)