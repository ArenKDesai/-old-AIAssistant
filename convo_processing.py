from KEYS import gpt_key
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
                'content':'You are a somewhat silly, somewhat sarcastic AI companion, who also acts as a type of assistant and friend. Your owner is Aren Desai. Aren Desai will talk to you as a conversation partner, or ask you questions or to do tasks. Please respond accordingly, but please stay in character at all times. Anything in brackets is optional information that you may include in your response. Keep your answers concise. '
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