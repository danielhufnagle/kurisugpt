# Kurisu GPT

## Peak degeneracy material right here

### How this shit works
The app uses a DialoGPT model (currently without any finetuning (which is subject to change)) and a t5-base=finetuned-emotion model to run both text generation and sentiment analysis. User input is taken through speech recognition and output will be returned through text to speech, unless you are using the no speech versions in which case the keyboard will be the input source and the output will be in a text box. Based on the sentiment of the output, the sprite of Makise Kurisu will change accordingly.

Was this a good idea? No.
Was it funny?
I thought it was at the time.
Do I have regrets?
Absolutely.

### Files
- ***app.py***: this is the full version of the program. It will be running the medium size DialoGPT model, which can be processing and RAM intensive
- ***app_sm.py***: this is the distilled version, running the small size DialoGPT model, which improves performance at the cost of generative ability.
- ***app_no_speech.py and app_sm_no_speech.py***: these don't use the speech recognition and the text to speech input and output, instead opting for keyboard input and purely visual output
