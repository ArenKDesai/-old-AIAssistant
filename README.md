# AIAssistant

## For Users
Prototype build v1.0 is not out yet. 

## For Developers

### audio.py
The file that controls all the audio processing. Functions:
- record_audio: Uses a user-sent model (typically Whisper tiny or medium) to record audio. Default length is 3 seconds, but the "duration" parameter can be set to something else.
- main_audio_loop: the main loop that will run continuously on a separate thread. It will process audio in 3-second intervals and process it. If the name "Pluto" is heard, it starts the AI's proper listening process.
- speak: takes a string input (the GPT response to the user's input) and creates an mp3 file of an ElevenLabs model speaking the string. This will soon be updated to automatically speak the sentence and delete the temporary mp3 file. 

### convo_processing.py
The file that manages the GPT API. Functions:
- process_convo: Not currently implemented, but will search for keywords in the user's input and add the corresponding tags to the string being sent to the GPT model.
- get_response: Takes the output from process_convo and sends it to the GPT model. Returns the GPT model's output. 
