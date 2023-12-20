import streamlit as st
import matplotlib.pyplot as plt
import pandas_gbq
from google.auth import exceptions
from google.oauth2 import service_account
from streamlit_player import st_player
import plotly.express as px
import pandas as pd
import configparser
import googleapiclient.discovery
from wordcloud import WordCloud

st.set_page_config(page_title="V1")

with st.container():
    
    config = configparser.ConfigParser()

    # Usando o arquivo de var :D
    config.read('var.ini')

    developer_key = str(config['Configuracoes']['DEVELOPER_KEY'])
    max_resultados = int(config['Configuracoes']['MAX_RESULTADOS'])
    api_service_name = str(config['Configuracoes']['API_SERVICE_NAME'])
    api_version = str(config['Configuracoes']['API_VERSION'])

    youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey=developer_key)
    
    def list_videos(canal_id,max_resultados=5):
        request = youtube.search().list(
            part='snippet',
            channelId=canal_id,
            maxResults=max_resultados,
            order='date'
        )

        response = request.execute()
        videos = []
        for item in response['items']:
            video_id = item['id']['videoId']
            video_url = f'https://www.youtube.com/watch?v={video_id}'
            videos.append({
                'title': item['snippet']['title'],
                'video_id': video_id,
                'video_url': video_url,
                'published_at': item['snippet']['publishedAt']
            })
        return videos
    


with st.container():
    credentials = service_account.Credentials.from_service_account_file(
        'C:/Users/jaina/Documents/credenciais/comments-398714-f10b8db5eb16.json',
        scopes=["https://www.googleapis.com/auth/cloud-platform"],
    )

    query = "SELECT * FROM `comments-398714.DwTreinamento.amostra_comentarios`"
    df = pandas_gbq.read_gbq(query, credentials=credentials)

# Container para mostrar vídeos
with st.container():
    st.subheader("Vídeos")

    # Define o valor padrão para o ID do canal
    default_channel_id = "UCvO2BExvkAbGMsTGnEnI_Ng"

    canal_id = st.text_input("Digite o ID do Canal:", default_channel_id)

    videos = list_videos(canal_id)
    for video in videos:
        st.subheader(video['title'])
        st_player(video['video_url'])
        st.write(f'Publicado em: {video["published_at"]}')
        st.markdown("---")

# Container para gráficos
with st.container():
    st.subheader("Gráficos")
    # Criando o donut chart
    if 'sentiment_label' in df.columns:
        # Contagem de sentimentos
        sentiment_counts = df['sentiment_label'].value_counts()

        # Cria um DataFrame para o gráfico de rosca
        df_sentiment_counts = pd.DataFrame({
            'Sentimento': sentiment_counts.index,
            'Contagem': sentiment_counts.values
        })

        # Crie o gráfico de rosca usando Plotly Express
        fig = px.pie(df_sentiment_counts, names='Sentimento', values='Contagem', hole=0.3, title='Distribuição de Sentimentos')
        
        st.plotly_chart(fig)

#Container da nuvem de palavras
with st.container():
    text_all = ' '.join(df['text'].astype(str))
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text_all)
    st.subheader("Nuvem de Palavras")
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    st.pyplot()

# Container de testye
with st.container():
    st.subheader("Análise de sentimentos de uma frase")

    try:
        # Exiba os dados no Streamlit
        st.dataframe(df)

    except exceptions.DefaultCredentialsError:
        st.error("Erro de credenciais: Não foi possível autenticar o usuário.")
