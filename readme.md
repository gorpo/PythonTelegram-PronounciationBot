# Pronounce It Bot

A python bot that utilizes the Telegram API to allow users to send text to be converted to audio and audio clips turning into text.

## Requirements

* Python 3
* [ffmpeg](https://www.ffmpeg.org/download.html)
* [ffmpeg-python](https://github.com/kkroening/ffmpeg-python)
* [python-telegram-bot](https://python-telegram-bot.readthedocs.io/en/stable/)
* [SpeechRecognition](https://pypi.org/project/SpeechRecognition/)
* [gTTs](https://pypi.org/project/gTTS/)

**The requirements are the same for both the Webhook Version & Non-Webhook Version**

The '*bot_version.py*' is the non-webhook version where you can run it locally.

If you wish to run it on a server, use the '*bot_webhook.py* to and put the URL that you want Telegram to call. 

*Tip:* The 'Procfile' is there if you wish to deploy to Heroku, otherwise, it can be removed