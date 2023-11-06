import streamlit as st
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

st.set_page_config(page_title="V1")

nltk.download('vader_lexicon')

sia = SentimentIntensityAnalyzer()

with st.container():
    st.subheader("Análise de sentimentos de uma frase")

    st.write("Documentação: [NLTK](https://www.nltk.org/)")

    text = st.text_input('Escreva uma frase (Em inglês)', "This video is a waste of everyone's time")
    
    sentimento = sia.polarity_scores(text)

    maior_valor = max(sentimento.values())

    if maior_valor == sentimento["neg"]:
        resultado = "negativa"
    elif maior_valor == sentimento["pos"]:
        resultado = "positiva"
    else:
        resultado = "neutra"

    st.write("A frase: '", text, "' é ", resultado )
    
    st.write("Análise sem tratamento: ")

    st.write(sentimento)