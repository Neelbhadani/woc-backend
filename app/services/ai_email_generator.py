import openai

openai.api_key = "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"

def generate_email(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message["content"]
