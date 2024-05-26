import streamlit as st
import re
import requests
from streamlit_mic_recorder import speech_to_text
from utils.AuthV3Util import addAuthParams

# EmotionVoice App Key, App secret key, TTSer ID, Server
APP_KEY = ''
APP_SECRET = ''
# TTS_ID List: https://ai.youdao.com/DOCSIRMA/html/tts/api/yyhc/index.html
TTS_ID = '' 
YouDaoServer = 'https://openapi.youdao.com/ttsapi'

# EmotionVoice voice file path：PATH = "media.mp3"
PATH = 'media.mp3'

# Clear Text content
def delete_boring_characters(sentence):
    return re.sub('[0-9’!"#$%&\'()*+,-./:;<=>?@，。?★、…【】《》？“”‘’！[\\]^_`{|}~\s]+', "  ", sentence)

# Record voice base on you lang
def record_voice(language="zh"):
    # https://github.com/B4PT0R/streamlit-mic-recorder?tab=readme-ov-file#example

    state = st.session_state

    if "text_received" not in state:
        state.text_received = []

    text = speech_to_text(
        start_prompt="Click to speak",
        stop_prompt="Stop recording",
        language=language,
        use_container_width=True,
        just_once=True,
    )

    if text:
        state.text_received.append(text)

    result = ""
    for text in state.text_received:
        result += text

    state.text_received = []

    return result if result else None

# Save Audio to Mp3
def saveFile(res):
    contentType = res.headers['Content-Type']
    if 'audio' in contentType:
        fo = open(PATH, 'wb')
        fo.write(res.content)
        fo.close()
        print('save file path: ' + PATH)
    else:
        print(str(res.content, 'utf-8'))


# Convert text to audio
def createRequest(text):
    q = delete_boring_characters(text)
    voiceName = TTS_ID
    format = 'mp3'

    data = {'q': q, 'voiceName': voiceName, 'format': format}

    addAuthParams(APP_KEY, APP_SECRET, data)

    header = {'Content-Type': 'application/x-www-form-urlencoded'}
    res = doCall(YouDaoServer, header, data, 'post')
    saveFile(res)
    st.audio("media.mp3", format="audio/mpeg", autoplay=True,loop=False)

def doCall(url, header, params, method):
    if 'get' == method:
        return requests.get(url, params)
    elif 'post' == method:
        return requests.post(url, params, header)

