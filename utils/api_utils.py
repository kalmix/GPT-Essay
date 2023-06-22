import requests

API_URL = 
OPENAI_API_KEY =

HEADERS = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {OPENAI_API_KEY}'
}


def generate_essay(prompt, model):
    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": f"Write an essay about {prompt}, but do not include things such as introduction:, body:, title:, or in conclusion. Use the fist line for the title of the essay. Write at least 5 paragraphs. Don't count Paragraphs in the text, just write the content."
            }
        ],
        "temperature": 1.0
    }

    response = requests.post(API_URL, headers=HEADERS, json=payload)
    response.raise_for_status()

    essay = response.json()['choices'][0]['message']['content']
    return essay
