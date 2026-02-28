# app.py
import os
import json
import streamlit as st
import google.generativeai as genai
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="Embalagio IA", layout="wide")
st.title("📦 Estruturador de Pedidos - Embalagio")
st.markdown("Transforme mensagens de WhatsApp em tabelas estruturadas.")

pedido = st.text_area("Cole o pedido do WhatsApp aqui:", height=150)

if st.button("Processar Pedido", type="primary"):
    if not pedido.strip():
        st.warning("Insira o texto do pedido.")
        st.stop()
        
    prompt = f"""
    Você é assistente da Embalagio. Extraia os produtos deste pedido de WhatsApp.
    Retorne OBRIGATORIAMENTE APENAS um array JSON válido. Sem texto extra ou formatação markdown (sem ```json).
    Formato obrigatório: [{{"Produto": "Nome", "Quantidade": Numero, "Tamanho": "Tamanho ou N/A"}}]
    
    Pedido: {pedido}
    """
    
    with st.spinner("Processando com IA..."):
        try:
            response = model.generate_content(prompt)
            texto_limpo = response.text.replace('```json', '').replace('```', '').strip()
            
            dados = json.loads(texto_limpo)
            df = pd.DataFrame(dados)
            
            st.dataframe(df, use_container_width=True)
            st.success("✅ Pedido pronto para inserção no banco de dados!")
            
        except json.JSONDecodeError:
            st.error("Erro na conversão. A IA não retornou um formato válido. Tente novamente.")
        except Exception as e:
            st.error(f"Erro: {str(e)}")