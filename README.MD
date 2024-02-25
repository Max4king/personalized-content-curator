# Personalized Content Curator

This project is made for the hackathon. Trulens is used here to analyse for the best prompt template.

This project is designed as a handy tool for users to stay informed about the latest developments in specific topics of interest. It's not intended to substitute for in-depth news articles or comprehensive research. Instead, it's perfect for anyone who feels overwhelmed by the rapid pace of updates and wants a concise way to stay in the know.

[DEMO](./demo-screenshot.png)

## How to use? 
Simply type in your interest like "AI" for example. Then this click generate and wait for the output to be generated. The application will display the title, complementary image and summary of the past week.

## How it works?
These are the steps which the AI takes when processing the input

### Step 0
Take in user input. Turns it into a search query

### Step 1

It will retrieve the information from the internet with Eva.

### Step 2

It will categorize the information into category.

### Step 3

It will upsert to a vector database with its category as a metadata and date.

### Step 4

The LLM uses RAG to get revelant information from the vector database.
Then put into the context above.

### Step 5

Use GPT-4 to generate a summary of the content or make an article(This is to be make after the competition).

### Step 6

Generate an image with dalle 3 of the content.
