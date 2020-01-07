from gtts import gTTS

from telegram.ext import Updater

import speech_recognition as sr

import string, random
import os
import io
import logging
from os import path
import time

import ffmpeg

TG_TOKEN = '<TELEGRAM TOKEN>'

updater = Updater(token=TG_TOKEN, use_context=True)
dispatcher = updater.dispatcher

def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

#Add Start Context
def start(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="Hey! Send me a text message and I will turn it into an audio clip")
    context.bot.send_message(chat_id=update.message.chat_id, text="Otherwise, send me a voice clip and I will get it in text form")

from telegram.ext import CommandHandler
from telegram import ChatAction
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

#DONE
def text_to_audio_tg(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="Getting Audio Recording For: " + update.message.text)
    context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
    filename = randomString() + '.mp3'
    tts = gTTS(update.message.text)
    tts.save(filename)
    context.bot.send_voice(chat_id=update.message.chat_id, voice=open(filename, 'rb'))
    
    os.remove(filename)

def audio_to_text_tg(update, context):
    AUDIO_FILE_MP3 = path.join(path.dirname(path.realpath(__file__)), randomString() + '.mp3')
    AUDIO_FILE_WAV = path.join(path.dirname(path.realpath(__file__)), randomString() + '.wav')
    file_id = update.message.voice.file_id
    newFile = context.bot.get_file(file_id)
    #Saves the file to the current directory
    newFile.download(AUDIO_FILE_MP3)
    time.sleep(3)
    context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
    stream = ffmpeg.input(AUDIO_FILE_MP3)
    stream = ffmpeg.output(stream, AUDIO_FILE_WAV)
    ffmpeg.run(stream)

    r = sr.Recognizer()
    with sr.AudioFile(AUDIO_FILE_WAV) as source:
        audio = r.record(source)  # read the entire audio file
        said = ""

    try:
        said = r.recognize_google(audio)
        context.bot.send_message(chat_id=update.message.chat_id, text=said)
    except Exception as e:
        err_msg = "An Error Occured - Exception: " + str(e)
        context.bot.send_message(chat_id=update.message.chat_id, text=err_msg)

    os.remove(AUDIO_FILE_WAV)
    os.remove(AUDIO_FILE_MP3)
        

from telegram.ext import MessageHandler, Filters
text_to_audio_tg_handler = MessageHandler(Filters.text, text_to_audio_tg)
audio_to_text_tg_handler = MessageHandler(Filters.voice, audio_to_text_tg)
dispatcher.add_handler(text_to_audio_tg_handler)
dispatcher.add_handler(audio_to_text_tg_handler)


#Polling
updater.start_polling()
