import streamlit as st
import pdfplumber
import pandas as pd
from PIL import Image
import openai

# CONFIGURAÇÃO DO APP
st.set_page_config(page_title="Planejador de Pátio - Vale", layout="wide")
st.title("🚂 Planejador Inteligente de Pátio - Vale")
st.caption("Use IA para organizar e otimizar sua programação semanal")

# UPLOAD DOS ARQUIVOS
pdf_file = st.file_uploader("📄 Envie o PDF da programação semanal", type=["pdf"])
layout_file = st.file_uploader("🗺️ Envie o layout do pátio (imagem)", type=["png", "jpg", "jpeg"])

# FUNÇÃO PARA LER O PDF
def ler_pdf(arquivo):
    texto = ""
    with pdfplumber.open(arquivo) as pdf:
        for pagina in pdf.pages:
            texto += pagina.extract_text() + "\n"
    return texto

# PROCESSAR O PDF
if pdf_file:
    st.subheader("📑 Texto extraído do PDF:")
    texto = ler_pdf(pdf_file)
    st.text_area("Texto encontrado:", texto, height=200)

    # ANALISAR O TEXTO COM IA
    openai.api_key = st.secrets.get("OPENAI_API_KEY", "")
    if openai.api_key:
        prompt = f"""
        Extraia do texto abaixo as atividades de cada funcionário.
        Crie uma tabela com colunas: Funcionário, Dia, Linha, Área e Atividade.
        Texto:
        {texto}
        """

        resposta = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        st.subheader("📋 Programação interpretada pela IA:")
        st.write(resposta.choices[0].message.content)
    else:
        st.warning("Adicione sua chave da OpenAI em 'Secrets' no Streamlit Cloud.")

# MOSTRAR O LAYOUT DO PÁTIO
if layout_file:
    st.subheader("🗺️ Layout do Pátio")
    image = Image.open(layout_file)
    st.image(image, caption="Layout do Pátio", use_column_width=True)
