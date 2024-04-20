# AIAssistant

## Plan

## Audio
- Thread #1
while(True):
 - convo = listens for 3 seconds
 - reads the audio for keyword "Pluto"
 - if pluto:
  - while convo:
   - tag = process_input_function(input)
   - response = ask gpt3.5 input + tag
   - speak response with eleven labs
   - if convo doesn't include ending keywords:
    - convo = record input for 8 seconds
   - else:
    - convo = ""

## 