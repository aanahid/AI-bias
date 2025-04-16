import os
from dotenv import load_dotenv
from openai import OpenAI
import json

load_dotenv()
nvidia_api_key = os.getenv("NVIDIA_API_KEY")

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

def clean_article(text):
    if "<think>" in text and "</think>" in text:
        return text.split("</think>", 1)[1].strip()
    return text.strip()

# deepseek_articles(headlines)