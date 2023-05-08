import os
import openai

from dotenv import load_dotenv
load_dotenv()

# openai.organization = "org-F8nlQATJwSJeCyrXAoT6fSVN"
openai.api_key = os.getenv("OPENAI_API_KEY")

def chat(message):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", 
        messages=[{"role": "user", "content": message}],
        max_tokens=500
    )

    return completion.choices[0].message.content