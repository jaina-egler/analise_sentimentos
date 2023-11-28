import streamlit as st
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt

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

    st.write("A frase: '", text, "' é classificada como ", resultado )

    dados = {
    "Negativo": sentimento["neg"],
    "Neutro": sentimento["neu"],
    "Positivo": sentimento["pos"]
    }

    cores = ["#942222", "#0b2e59", "#295317"]

    plt.gcf().set_facecolor("#0E1117")

    plt.rcParams['text.color'] = '#FFFFFF'

    plt.gcf().set_size_inches(10, 5)

    plt.pie(dados.values(), labels=dados.keys(), autopct="%.1f%%", colors=cores)
    plt.title("Disposição do sentimento")

    st.pyplot(plt.gcf())
    
    st.write("Análise sem tratamento: ")

    st.write(sentimento)