import spotipy
from spotipy.oauth2 import SpotifyOAuth
from KEYS import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI

# Spotipy - Spotify handler
sp = None

# Begin spotify control
def initialize_spotify():
    global sp
    # Define your credentials and the scope
    SCOPE = 'user-read-playback-state user-modify-playback-state user-read-currently-playing'

    # Create a SpotifyOAuth object
    sp_oauth = SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                            client_secret=SPOTIPY_CLIENT_SECRET,
                            redirect_uri=SPOTIPY_REDIRECT_URI,
                            scope=SCOPE)

    # Get the authorization URL
    auth_url = sp_oauth.get_authorize_url()

    print(f'Please navigate to the following URL to authorize the application: {auth_url}')

    # After the user authorizes the application, they will be redirected to the redirect URI with a code in the URL
    response = input('Enter the URL you were redirected to: ')

    # Extract the authorization code from the URL
    code = sp_oauth.parse_response_code(response)
    token_info = sp_oauth.get_access_token(code)

    # Create a Spotify object with the access token
    sp = spotipy.Spotify(auth=token_info['access_token'])

def get_current_song():
    # Get the current playback information
    current_playback = sp.current_playback()
    # Print the current playback information
    if current_playback is not None:
        item = current_playback['item']
        return f'{item["name"]} by {", ".join(artist["name"] for artist in item["artists"])}'
    else:
        return 'No current playback found.' 