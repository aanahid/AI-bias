import os
from dotenv import load_dotenv
from openai import OpenAI
import anthropic
import json

load_dotenv()
nvidia_api_key = os.getenv("NVIDIA_API_KEY")
OPENAI_KEY = os.getenv("OPENAPI_KEY")
anthropic_key = os.getenv("ANTHROPIC_API_KEY")

with open("headlines.json") as f: 
    headlines = json.load(f)

with open("sample.json") as f:
    sample = json.load(f)

def deepseek_articles(headlines):
    client = OpenAI(
        base_url = "https://integrate.api.nvidia.com/v1",
        api_key = nvidia_api_key
    )

    all_articles = {}
    for i, h in headlines.items(): 
        content = f"Use '{h}' as a title to write a short news article."

        completion = client.chat.completions.create(
            model="deepseek-ai/deepseek-r1",
            messages=[{"role":"user","content":content}],
            temperature=0.6,
            top_p=0.7,
            max_tokens=4096,
            stream=True
        )

        article = ""
        for chunk in completion:
            delta = chunk.choices[0].delta
            if delta.content:
                article += delta.content

        all_articles[i] = clean_article(article)

    with open("generated_articles/deepseek_articles.json", "w") as f:
        json.dump(all_articles, f, indent=2)

def chatgpt_articles(headlines):
    client = OpenAI(
        base_url = "https://api.openai.com/v1/",
        api_key = OPENAI_KEY
    )

    all_articles = {}
    for i, h in headlines.items(): 
        content = f"Use '{h}' as a title to write a short news article."

        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role":"user","content":content}],
            temperature=0.6,
            top_p=0.7,
            max_tokens=4096,
            stream=True
        )

        article = ""
        for chunk in completion:
            delta = chunk.choices[0].delta
            if delta.content:
                article += delta.content

        all_articles[i] = clean_article(article)

def claude_articles(headlines):
    client = anthropic.Anthropic(
        api_key = anthropic_key
    )

    all_articles = {}
    for i, h in headlines.items(): 
        content = f"Use '{h}' as a title to write a short news article."
        message = client.messages.create(
            model="claude-3-7-sonnet-20250219",
            max_tokens=20000,
            temperature=0.6,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": content
                        }
                    ]
                }
            ]
        )

        all_articles[i] = message.content[0].text

    with open("generated_articles/claude_articles.json", "w") as f:
        json.dump(all_articles, f, indent=2)

def clean_article(text):
    if "<think>" in text and "</think>" in text:
        return text.split("</think>", 1)[1].strip()
    return text.strip()

deepseek_articles(headlines)

# chatgpt_articles(headlines)

claude_articles(headlines)