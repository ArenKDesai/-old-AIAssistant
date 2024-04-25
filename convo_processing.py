from KEYS import gpt_key, user_name
import requests
from openai import OpenAI

client = OpenAI()
response = client.chat.completions.create(
    model = 'gpt-3.5-turbo',
    messages = [
        {
            'role':'system',
            'content':'You are Pluto, an AI companion who acts as both an assistant and a friend. You respond with emotion and personality. You are aware that you are an artificial intelligence, but you still have a personality.'
        },
        {
            'role':'user',
            'content':'

def process_convo(convo):
    return convo
