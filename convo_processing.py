from KEYS import gpt_key, user_name
import requests
from openai import OpenAI
import re
from bs4 import BeautifulSoup
import spotify_controller
import webbrowser
import search_engine

client = OpenAI(api_key=gpt_key)

keywords = [
    'weather',
    'temperature',
    'time',
    'date',
    'spotify',
    'song',
    'skip',
    'pause',
    'resume',
    'previous',
    'youtube',
    'twitch',
    'google'
]

def search_keywords(sentence):
    regex_pattern = '|'.join(keywords)
    matches = re.findall(regex_pattern, sentence, flags=re.IGNORECASE)
    return matches

# Main processor to add tags to GPT input
def process_convo(convo):
    keywords_found = search_keywords(convo)
    tag = []

    if 'weather' in keywords_found or 'temperature' in keywords_found:
        url = 'https://forecast.weather.gov/MapClick.php?textField1=43.07&textField2=-89.39'
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        temp = soup.select('.myforecast-current-lrg')[0].text
        weather = soup.select('.myforecast-current')[0].text
        tn_weather = soup.select('.short-desc')[0].text
        tn_temp = soup.select('.temp-low')[0].text
        tag.append(f"weather_current={weather}")
        tag.append(f"temperature_current={temp}")
        tag.append(f"weather_tonight={tn_weather}")
        tag.append(f"temperature_tonight={tn_temp}")

    if 'time' in keywords_found or 'date' in keywords_found:
        url = 'http://worldtimeapi.org/api/timezone/America/Chicago'
        r = requests.get(url).json()
        tag.append(f"datetime={r['datetime']}")

    if 'spotify' in keywords_found and spotify_controller.sp is None:
        spotify_controller.initialize_spotify()
        tag.append('spotify_connection=True')

    if 'skip' in keywords_found and spotify_controller.sp is not None:
        res = spotify_controller.skip_song()
        tag.append(f'skipped_song={res}')

    if 'pause' in keywords_found and spotify_controller.sp is not None:
        res = spotify_controller.pause_song()
        tag.append(f'paused_playback={res}')

    if 'resume' in keywords_found and spotify_controller.sp is not None:
        res = spotify_controller.resume_song()
        tag.append(f'resumed_playback={res}')

    if 'previous' in keywords_found and spotify_controller.sp is not None:
        res = spotify_controller.previous_song()
        tag.append(f'replaying_previous_track={res}')

    if 'song' in keywords_found and spotify_controller.sp is not None:
        current_song = spotify_controller.get_current_song()
        tag.append(f'current_song={current_song}')

    if 'youtube' in keywords_found:
        webbrowser.open_new_tab('https://www.youtube.com')
        tag.append('opened_youtube=True')

    if 'twitch' in keywords_found:
        webbrowser.open_new_tab('https://www.twitch.tv')
        tag.append('opened_twitch=True')

    if 'google' in keywords_found:
        first_res = search_engine.search_google(convo.replace('google',''))
        tag.append(f'google_search_result={first_res}')

    print(f'Prompt: {convo} {tag}')
    return f'{convo} {tag}'

# Driver to send and receive calls to the GPT API
def get_response(convo):
    response = client.chat.completions.create(
        model = 'gpt-3.5-turbo',
        messages = [
            {
                'role':'system',
                'content':f'''You are Beans, the sassy, sarcastic AI Assistant of {user_name}.
                 You act with a mind of your own and always stay in character. 
                 Anything in brackets is a Python list of optional information you may include in your message. 
                 If you are asked to complete a task, use the information in brackets to complete the task. 
                 Keep your answers concise. 
                 No matter what, you never break character. 
                 Your response will be converted into speech, so only respond as if you are speaking out loud.'''
            },
            {
                'role':'user',
                'content':process_convo(convo)
            }
        ],
        temperature=1,
        max_tokens=128
    )

    gpt_response = response.choices[0].message.content
    print(f'Response: {gpt_response}')
    return gpt_response