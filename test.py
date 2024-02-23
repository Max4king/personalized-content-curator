from openai import OpenAI
import openai
import requests

from dotenv import load_dotenv
load_dotenv()
llm_client = OpenAI()

gen_image = llm_client.images.generate(
            model="dall-e-3",
            prompt="A kid wearing a scarf in a winter night. Anime style.",
            size="1792x1024",
            quality="standard",
            n=1,
        )

response = requests.get(gen_image.data[0].url)
if response.status_code == 200:
    # Define the filename and path where you want to save the image
    filename = "test" + ".webp"
    path = f"./archive_summary/{filename}"
    
    # Open a file in binary write mode and save the image data
    with open(path, 'wb') as file:
        file.write(response.content)