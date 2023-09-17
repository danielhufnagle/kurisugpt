import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, AutoModelWithLMHead
import ttkbootstrap as ttk
import random
import speech_recognition as sr
import subprocess

# set up chatting pipeline
language_model_name = 'microsoft/DialoGPT-small'
language_tokenizer = AutoTokenizer.from_pretrained(language_model_name)
language_model = AutoModelForCausalLM.from_pretrained(language_model_name)

# set up sentiment analysis pipeline
sentiment_model_name = 'mrm8488/t5-base-finetuned-emotion'
sentiment_tokenizer = AutoTokenizer.from_pretrained(sentiment_model_name)
sentiment_model = AutoModelWithLMHead.from_pretrained(sentiment_model_name)

def get_emotion(text):
    input_ids = sentiment_tokenizer.encode(text + '</s>', return_tensors='pt')
    output = sentiment_model.generate(input_ids=input_ids, max_length=2) 
    dec = [sentiment_tokenizer.decode(ids) for ids in output]
    label = dec[0]
    return label
# possible emotion labels are sadness, joy, love, anger, fear, and surprise

step = 0

def button_clicked():
    global step
    global image_path
    with mic as source:
        audio = r.listen(source, phrase_time_limit=3, timeout=5)
    prompt = r.recognize_google(audio)
    input_ids = language_tokenizer.encode(prompt + language_tokenizer.eos_token, return_tensors='pt')
    bot_input_ids = torch.cat([chat_history_ids, input_ids], dim=-1) if step>0 else input_ids
    chat_history_ids = language_model.generate(
            bot_input_ids,
            max_length=1000,
            do_sample=True,
            top_p=0.95,
            top_k=0,
            temperature=0.75,
            pad_token_id=language_tokenizer.eos_token_id,
        )
    output = language_tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
    subprocess.call(['say', output])
    input_txt['state'] = 'normal'
    input_txt.delete('1.0', 'end-1c')
    input_txt.insert('1.0', prompt)
    input_txt['state'] = 'disabled'
    output_txt['state'] = 'normal'
    output_txt.delete('1.0', 'end-1c')
    output_txt.insert('1.0', output)
    output_txt['state'] = 'disabled'
    emotion = get_emotion(output)
    emotion = emotion[6:]
    image_choice = random.randint(1, 2)
    image_path = 'images/' + emotion + str(image_choice) + ' (Phone).png'
    new_image = ttk.PhotoImage(file=image_path)
    img_container.configure(image=new_image)
    img_container.photo = new_image

r = sr.Recognizer()
mic = sr.Microphone()

root = ttk.Window(themename='darkly')
root.title('Kurisu-chan')
root.geometry('1500x1500')

title = ttk.Label(root, text='Kurisu GPT', font='Calibri 32 bold')
title.pack(pady=10)

button = ttk.Button(root, text='Chat!', command=button_clicked)
button.pack(pady=40)

image_path = 'images/neutral (Phone).png'
image = ttk.PhotoImage(file=image_path)

img_container = ttk.Label(root)
img_container.configure(image=image)
img_container.pack()

input_txt = ttk.Text(root, height=2, width=50)
input_txt['state'] = 'disabled'
input_txt.pack(pady=5)

output_txt = ttk.Text(root, height=2, width=50)
output_txt['state'] = 'disabled'
output_txt.pack(pady=5)

root.mainloop()