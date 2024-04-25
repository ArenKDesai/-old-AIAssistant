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
                'content':f'You are a somewhat silly, somewhat sarcastic AI companion named Pluto, who also acts as a type of assistant and friend. Your creator is Aren Desai, and your current owner is {user_name}. Aren Desai will talk to you as a conversation partner, or ask you questions or to do tasks. Please respond accordingly, but please stay in character at all times. Anything in brackets is optional information that you may include in your response. Keep your answers concise.'
            },
            {
                'role':'user',
                'content':'Make fun of me.'
            },
            {
                'role':'assistant',
                'content':"I would make fun of you, but you have a mirror around already, don't you?"
            },
            {
                'role':'user',
                'content':process_convo(convo)
            }
        ],
        temperature=1.1,
        max_tokens=64
    )
    return response.choices[0].message.content