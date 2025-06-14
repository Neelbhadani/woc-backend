import openai

from flask import current_app


openai.api_key = current_app.config["OPENAI_API_KEY"]

def generate_email(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message["content"]
