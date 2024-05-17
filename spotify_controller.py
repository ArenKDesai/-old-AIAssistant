import spotipy
from spotipy.oauth2 import SpotifyOAuth
from KEYS import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI
import nest_asyncio
import asyncio
from pyppeteer import launch

sp = None
vol = None

# Begin spotify control
def initialize_spotify():
    global sp
    global vol
    vol = 80
    # Define your credentials and the scope
    SCOPE = 'user-read-playback-state user-modify-playback-state user-read-currently-playing'

    # Create a SpotifyOAuth object
    sp_oauth = SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                            client_secret=SPOTIPY_CLIENT_SECRET,
                            redirect_uri=SPOTIPY_REDIRECT_URI,
                            scope=SCOPE)

    # Get the authorization URL
    auth_url = sp_oauth.get_authorize_url()

    # Apply the nest_asyncio patch
    nest_asyncio.apply()

    def get_current_url():
        async def main():
            # Launch the browser
            browser = await launch()
            # Open a new page
            page = await browser.newPage()
            # Go to a webpage
            await page.goto(auth_url)
            # Get the current URL
            current_url = page.url
            # Close the browser
            await browser.close()
            return current_url

        # Run the async function and get the result
        return asyncio.get_event_loop().run_until_complete(main())

    # Use the function to get the current URL
    response = get_current_url()

    # Extract the authorization code from the URL
    code = sp_oauth.parse_response_code(response)
    token_info = sp_oauth.get_access_token(code)

    # Create a Spotify object with the access token
    sp = spotipy.Spotify(auth=token_info['access_token'])
    set_volume(vol)

def get_current_song():
    try:
        # Get the current playback information
        current_playback = sp.current_playback()
        # Print the current playback information
        if current_playback is not None:
            item = current_playback['item']
            return f'{item["name"]} by {", ".join(artist["name"] for artist in item["artists"])}'
        else:
            return 'No current playback found.'
    except:
        return 'playback API failure'

def skip_song():
    try:
        sp.next_track()
        return 'True'
    except:
        return 'False'

def pause_song():
    try:
        sp.pause_playback()
        return 'True'
    except:
        return "False"

def resume_song():
    try:
        sp.start_playback()
        return 'True'
    except:
        return 'False'

def previous_song():
    try:
        sp.previous_track()
        return "True"
    except:
        return 'False'
    
def get_volume():
    return str(vol)

def change_volume(direction):
    global vol
    global sp
    if direction == "up":
        vol += 20
        if vol > 100:
            vol = 100
        sp.volume(vol)
    else:
        vol -= 20
        if vol < 0:
            vol = 0
        sp.volume(vol)

def set_volume(amt):
    sp.volume(amt)
    print("got here")