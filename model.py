from dotenv import load_dotenv
load_dotenv()
# Imports main tools:
from trulens_eval import TruChain, Feedback, Tru
tru = Tru()
tru.reset_database()

import os
from exa_py import Exa
from openai import OpenAI
from datetime import datetime, timedelta

# Setting and parameters:

if not os.getenv('EXA_API_KEY'):
    raise ValueError("EXA_API_KEY environment variable not set!")
if not os.getenv('OPENAI_API_KEY'):
    raise ValueError("OPENAI_API_KEY environment variable not set!")

exa = Exa(os.getenv('EXA_API_KEY'))

llm_client = OpenAI()

model = "gpt-4-turbo-preview"

SYSTEM_MESSAGE = "You are a helpful assistant that generates search queries based on user questions. Only generate one search query."
USER_QUESTION = "What's the recent news in AI this week?"


# Making the search query:
completion = llm_client.chat.completions.create(
    model=model,
    messages=[
        {"role": "system", "content": SYSTEM_MESSAGE},
        {"role": "user", "content": USER_QUESTION},
    ],
)

search_query = completion.choices[0].message.content

print("Search query:")
print(search_query)

one_week_ago = (datetime.now() - timedelta(days=7))
date_cutoff = one_week_ago.strftime("%Y-%m-%d")

search_response = exa.search_and_contents(
    search_query, use_autoprompt=True, start_published_date=date_cutoff,
    highlights=True, text={'max_characters': 1000},
    num_results=5
)

urls = [result.url for result in search_response.results]
print("URLs:")
for url in urls:
    print(url)

results = search_response.results
# result_item = results[0]

# Write the result into a json file
import json
with open('search_results.json', 'w') as f:
    json.dump([
        {'title': result.title, 'highlights': str(result.highlights),
          'text': result.text, 'url': result.url} for result in results],
            f, indent=4)

