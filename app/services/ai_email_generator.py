import openai
from flask import current_app

def generate_email(prompt):
    client = openai.OpenAI(api_key=current_app.config["OPENAI_API_KEY"])

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    return response.choices[0].message.content

