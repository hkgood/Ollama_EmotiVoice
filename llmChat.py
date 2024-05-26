import streamlit as st
from voice import createRequest

# Print Chat conversation with right format
def print_chat_message(message):
    text = message["content"]
    if message["role"] == "user":
        with st.chat_message("user", avatar="😊"):
            print_txt(text)
    else:
        with st.chat_message("assistant", avatar="🤖"):
            print_txt(text)
            createRequest(text)


# Print LLM content 
def print_txt(text):
    #if any("\u0600" <= c <= "\u06FF" for c in text): # check if text contains Arabic characters
    #    text = f"<p style='direction: rtl; text-align: right;'>{text}</p>"
    st.write(text)
    #st.markdown(text, unsafe_allow_html=True)