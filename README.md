# AIAssistant

## Plan

## Audio
- Thread #1
while(True):
 - convo = listens for 3 seconds
 - reads the audio for keyword "Pluto"
 - if pluto:
    talking = true (get gv)
  - while convo:
   - tag = process_input_function(input)
   - response = ask gpt3.5 input + tag
   - speak response with eleven labs
   - if convo doesn't include ending keywords:
    - convo = record input for 8 seconds
   - else:
    - convo = ""
    - talking = false (after while loop)

## Graphics
- Thread #2
while(True):
- if(talking):
* test
- else:
* test

## Brain

## Global Variables
animation (boolean)
talking (boolean)
