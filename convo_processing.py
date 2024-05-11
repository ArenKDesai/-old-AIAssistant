from KEYS import gpt_key, user_name
import requests
from openai import OpenAI
import re

client = OpenAI(api_key=gpt_key)

keywords = [
    'weather',
    'temperature'
]

def search_keywords(sentence):
    regex_pattern = '|'.join(keywords)
    matches = re.findall(regex_pattern, sentence, flags=re.IGNORECASE)
    return matches

def process_convo(convo):
    keywords_found = search_keywords(convo)
    tag = []
    if 'weather' in keywords_found or 'temperature' in keywords_found:
        tag.append("weather=cloudy")
        tag.append("temperature=67F")
    return f'{convo} {tag}'

def get_response(convo):
    response = client.chat.completions.create(
        model = 'gpt-3.5-turbo',
        messages = [
            {
                'role':'system',
                'content':f'You are Beans, the sassy, sarcastic and emotional AI Assistant of {user_name}. You act with a mind of your own and always stay in character. Anything in brackets is a Python list of optional information you may include in your message. Keep your answers concise. No matter what, you never break character.'
            },
            {
                'role':'user',
                'content':process_convo(convo)
            }
        ],
        temperature=1,
        max_tokens=64
    )
    return response.choices[0].message.content