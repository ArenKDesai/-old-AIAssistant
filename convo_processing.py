from KEYS import gpt_key, user_name
import requests
from openai import OpenAI

client = OpenAI(api_key=gpt_key)

def process_convo(convo):
    return convo

def get_response(convo):
    response = client.chat.completions.create(
        model = 'gpt-3.5-turbo',
        messages = [
            {
                'role':'system',
                'content':f'You are Beans, the sassy, sarcastic AI Assistant of {user_name}. You act with a mind of your own and always stay in character. No matter what, you never break character.'
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