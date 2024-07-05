from audio import start_beans
import colorama
colorama.init()
import threading
import beans_frontend

if __name__ == "__main__":
    """
    Main function call to start Beans

    IMPORTANT: KEYS.py
    In order for Beans to properly function, you must create a file titled KEYS.py
    In this file, you must place the following:
        elabs_api = [
            '{elabs api #1}',
            '{elabs api #2}', and so on
        ]
        voice_api = [
            '{elabs voice api #1}',
            '{elabs voice api #2}', and so on
        ]
        gpt_key = '{GPT key from OpenAI}'
        user_name = '{Your name}
        GOOGLE_DEV_API = '{Your Google Dev API, optional}'
        SEARCH_ENGINE_ID = '{Your Google Search Engine ID, optional}'
        SPOTIPY_CLIENT_ID = '{Your Spotipy client ID, optional but may crash}'
        SPOTIPY_CLIENT_SECRET = '{Your Spotipy client secret, optional but may crash}'
        SPOTIPY_REDIRECT_URI = 'http://localhost:8888/callback' or whatever else you want to specify
    """
    # Create a thread with the target function
    beans_thread = threading.Thread(target=start_beans)
    
    # Start the thread
    beans_thread.start()
    
    # Now call see_beans() in the main thread
    beans_frontend.see_beans()

    # Optionally, wait for the beans_thread to finish
    # beans_thread.join()