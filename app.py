import streamlit as st
import requests
import base64

WEBHOOK_URL = "https://n8n-production-e6639.up.railway.app/webhook/embalagio-ai"
SHEET_EMBED  = "https://docs.google.com/spreadsheets/d/1QcAuW2CIVvVv03asnwpj32AvT6rXKV9FXwLdSHXWhiw/edit?usp=sharing"

st.set_page_config(page_title="Embalagio CRM", page_icon="📦", layout="wide")

# ─── FUNÇÃO PARA A LOGO ───
def get_img_as_base64(file_path):
    try:
        with open(file_path, 'rb') as f:
            return base64.b64encode(f.read()).decode()
    except:
        return ""

logo_b64 = get_img_as_base64("logo_embalagio.png")

# ─── CSS GLOBAL ───
st.markdown(f"""
<style>
/* Fundo Geral */
.stApp, .stApp > header {{ background-color: #0A1F2C !important; }}

h1, h2, h3, h4, p, label, li, span {{ color: #f0f0f0; }}

/* Destaques na Cor da Marca */
.brand-text {{ color: #FF6A00 !important; }}

/* Botão de Enviar Principal */
.stButton > button {{ 
    background: #FF6A00 !important; 
    color: #ffffff !important; 
    border: none !important; 
    border-radius: 8px !important; 
    font-weight: 800 !important; 
    padding: 12px 0 !important;
    transition: all 0.3s ease;
}}
.stButton > button:hover {{ 
    background: #FF7A1A !important; 
    box-shadow: 0 0 10px #FF6A00 !important;
}}

/* Correção do Botão "Sobre este Projeto" e "Limpar" */
button[kind="secondary"] {{
    background-color: transparent !important;
    color: #f0f0f0 !important;
    border: 1px solid #FF6A00 !important;
    box-shadow: none !important;
}}
button[kind="secondary"]:hover {{
    background-color: #0E2A3A !important;
    color: #FF6A00 !important;
    border: 1px solid #FF6A00 !important;
    box-shadow: 0 0 8px rgba(255, 106, 0, 0.4) !important;
}}

/* Inputs e Selectbox */
.stSelectbox div[data-baseweb="select"] {{ 
    border-color: #FF6A00 !important; 
    background-color: #0E2A3A !important; 
    color: #f0f0f0 !important; 
}}
.stTextArea textarea {{ 
    border-color: #FF6A00 !important; 
    background-color: #0E2A3A !important; 
    color: #f0f0f0 !important; 
}}

/* Bordas Ativas / Glow nos campos de texto */
.stSelectbox div[data-baseweb="select"]:focus-within, 
.stTextArea textarea:focus {{
    box-shadow: 0 0 10px #FF6A00 !important;
    outline: none !important;
}}

/* Painel do Chat */
.chat-panel {{ 
    background-color: #0E2A3A; 
    border: 1px solid #FF6A00; 
    border-radius: 12px; 
    padding: 15px; 
    height: 400px; 
    display: flex; 
    flex-direction: column; 
    box-shadow: 0 0 5px rgba(255, 106, 0, 0.2);
}}

.chat-messages {{ flex: 1; overflow-y: auto; padding-right: 5px; display: flex; flex-direction: column; gap: 12px; }}
.msg-user {{ display: flex; justify-content: flex-end; }}
.msg-ai   {{ display: flex; justify-content: flex-start; }}
.bubble {{ max-width: 85%; padding: 10px 14px; font-size: 0.95rem; line-height: 1.4; word-wrap: break-word; box-shadow: 0 1px 2px rgba(0,0,0,0.3); font-family: sans-serif; }}
.bubble-user {{ background: #005c4b !important; color: #e9edef !important; border-radius: 12px 4px 12px 12px; }}
.bubble-ai {{ background: #202c33 !important; color: #e9edef !important; border-radius: 4px 12px 12px 12px; }}
.bubble-label {{ color: #8696a0 !important; font-size: 0.7rem; font-family: monospace; margin-bottom: 4px;}}
.chat-empty {{ color: #8696a0 !important; text-align: center; font-family: monospace; font-size: 0.85rem; margin-top: auto; margin-bottom: auto; }}

#MainMenu, footer, header {{ visibility: hidden; }}
.block-container {{ padding-top: 1rem !important; max-width: 1200px; }}
</style>
""", unsafe_allow_html=True)

if "history" not in st.session_state:
    st.session_state.history = []
if "status" not in st.session_state:
    st.session_state.status = None

def check_n8n():
    try:
        r = requests.post(WEBHOOK_URL, json={"message": "__ping__"}, timeout=4)
        if r.status_code == 200:
            r.json() 
            return True
        return False
    except:
        return False

n8n_online = check_n8n()

if n8n_online:
    badge_bg = "#0d2b1a"
    badge_border = "#1a5c35"
    badge_color = "#4ade80"
    badge_text  = "● SISTEMA ATIVO"
else:
    badge_bg = "#2b0d0d"
    badge_border = "#5c1a1a"
    badge_color = "#f87171"
    badge_text  = "○ SISTEMA OFFLINE"

# ─── CABEÇALHO (Largura Total e Efeito Glow) ───
st.markdown(f"""
<div style="display: flex; justify-content: space-between; align-items: center; padding-bottom: 15px; border-bottom: 2px solid #FF6A00; margin-bottom: 25px; box-shadow: 0 4px 15px -5px #FF6A00; width: 100%;">
    <div style="display: flex; align-items: center; gap: 15px;">
        <img src="data:image/png;base64,{logo_b64}" style="width: 80px; border-radius: 8px;">
        <div>
            <h1 style="color: #FF6A00; font-size: 1.4rem; margin: 0; font-weight: 900; line-height: 1.2; text-shadow: 0 0 5px rgba(255, 106, 0, 0.4);">PORTAL DE ATENDIMENTO</h1>
            <p style="color: #888; font-size: 0.8rem; margin: 0; font-family: monospace;">Triagem de leads · IA WhatsApp · Powered by Groq + Llama 3.3</p>
        </div>
    </div>
    <div style="background-color: {badge_bg}; border: 1px solid {badge_border}; color: {badge_color}; padding: 6px 12px; border-radius: 20px; font-size: 0.7rem; font-family: monospace; font-weight: bold; white-space: nowrap;">
        {badge_text}
    </div>
</div>
""", unsafe_allow_html=True)

with st.popover("ℹ️ Sobre este Projeto"):
    st.markdown("""
    ### 📦 Embalagio IA - Atendimento & CRM
    Sistema inteligente que simula o atendimento automatizado de uma franquia via WhatsApp. 
    A IA interpreta a mensagem, extrai os itens do pedido e salva automaticamente no CRM, confirmando a solicitação com o cliente.

    **Como Testar:**
    1. Escolha um exemplo no menu suspenso ou digite seu pedido.
    2. Clique em **ENVIAR MENSAGEM**.
    3. A IA registrará os dados e responderá instantaneamente.
    """)

st.write("")

# ─── LAYOUT PRINCIPAL ───
col1, col2 = st.columns([1, 1.3], gap="large")

with col1:
    chat_head_col1, chat_head_col2 = st.columns([3, 1.2], vertical_alignment="center")
    chat_head_col1.markdown('<p class="brand-text" style="font-family: monospace; font-weight: bold; text-transform: uppercase; margin: 0;">💬 Chat de Atendimento</p>', unsafe_allow_html=True)
    if chat_head_col2.button("🗑️ Limpar", use_container_width=True):
        st.session_state.history = []
        st.rerun()

    msgs_html = ''
    if not st.session_state.history:
        msgs_html = '<div class="chat-empty">Nenhuma mensagem ainda.<br/>Selecione um pedido ou digite abaixo ↓</div>'
    else:
        for m in st.session_state.history:
            if m["role"] == "user":
                msgs_html += f'''
                <div class="msg-user">
                  <div>
                    <div class="bubble-label bubble-label-right">Você</div>
                    <div class="bubble bubble-user"><p style="margin:0;">{m["text"]}</p></div>
                  </div>
                </div>'''
            else:
                msgs_html += f'''
                <div class="msg-ai">
                  <div>
                    <div class="bubble-label">🤖 Embalagio IA</div>
                    <div class="bubble bubble-ai"><p style="margin:0;">{m["text"]}</p></div>
                  </div>
                </div>'''

    st.markdown(f'<div class="chat-panel"><div class="chat-messages">{msgs_html}</div></div>', unsafe_allow_html=True)

    st.write("")
    opcoes_exemplos = [
        "-- Digite livremente ou escolha um pedido --",
        "Oi, quero orçar 1000 caixas de hambúrguer tamanho G.",
        "Me chamo Ana. Preciso de 500 sacolas kraft P para minha loja.",
        "Olá! Quero pedir 300 caixas de pizza personalizadas, sou o Marcos.",
        "Bom dia. Queremos 2000 sacos de papel para pão. Aqui é a padaria Doce Pão."
    ]
    escolha = st.selectbox("💡 Sugestões de pedidos rápidos:", opcoes_exemplos)
    texto_padrao = escolha if escolha != opcoes_exemplos[0] else ""

    user_input = st.text_area("Sua mensagem:", value=texto_padrao, height=80, placeholder="Digite seu pedido aqui...")

    if st.button("ENVIAR MENSAGEM ➜", use_container_width=True):
        if user_input.strip():
            st.session_state.history.append({"role": "user", "text": user_input.strip()})
            with st.spinner("Processando Inteligência Artificial..."):
                try:
                    r = requests.post(WEBHOOK_URL, json={"message": user_input.strip()}, timeout=45)
                    if r.status_code == 200:
                        try:
                            data = r.json()
                            reply = data.get("Reply", data.get("reply", "Pedido recebido com sucesso!"))
                            st.session_state.history.append({"role": "ai", "text": reply})
                            st.session_state.status = ("ok", "Lead extraído e salvo no CRM")
                        except ValueError:
                            st.session_state.status = ("err", "Erro: n8n não retornou JSON válido.")
                    else:
                        st.session_state.status = ("err", f"Erro de comunicação: {r.status_code}")
                except Exception as e:
                    st.session_state.status = ("err", "Sistema Offline ou Falha na Conexão.")
            st.rerun()
        else:
            st.warning("A mensagem não pode estar vazia.")

    if st.session_state.status:
        t, msg = st.session_state.status
        if t == "ok":
            st.markdown(f'<div style="color: #4ade80; font-family: monospace; font-size: 0.85rem; font-weight: bold; margin-top: 10px;">✓ {msg}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div style="color: #f87171; font-family: monospace; font-size: 0.85rem; font-weight: bold; margin-top: 10px;">✗ {msg}</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<p class="brand-text" style="font-family: monospace; font-weight: bold; text-transform: uppercase; margin: 0 0 10px 0;">📊 CRM — Leads em Tempo Real</p>', unsafe_allow_html=True)
    st.markdown(
        f'<div style="background-color: #0E2A3A; border: 2px solid #FF6A00; border-radius: 12px; overflow: hidden; line-height: 0; box-shadow: 0 0 8px rgba(255, 106, 0, 0.3);"><iframe src="{SHEET_EMBED}" width="100%" height="600" frameborder="0" style="border-radius: 10px;"></iframe></div>',
        unsafe_allow_html=True
    )
    st.markdown('<p style="font-size: 0.75rem; color: #888; text-align: right; margin-top: 5px; font-family: monospace;">Atualização em tempo real · Google Sheets</p>', unsafe_allow_html=True)

st.markdown("---")
st.markdown('<h3 class="brand-text" style="text-align: center; margin-bottom: 20px;">🔍 Arquitetura Técnica (Backend Automatizado)</h3>', unsafe_allow_html=True)
st.image("workflow_n8n.png", use_container_width=True)
st.markdown('<p style="text-align: center; font-size: 0.8rem; color: #888;">*(Clique na imagem para ampliar e arrastar)*</p>', unsafe_allow_html=True)

# ─── RODAPÉ PROFISSIONAL ───
st.markdown("""
<div style="text-align: center; margin-top: 60px; padding-top: 20px; border-top: 1px solid #1a3c54;">
    <p style="color: #888; font-size: 0.85rem; font-family: monospace;">
        &lt;/&gt; Sistema de Triagem Automatizada | Desenvolvido por <b style="color: #FF6A00; text-shadow: 0 0 5px rgba(255,106,0,0.4);">Emmanuel</b>
    </p>
</div>
""", unsafe_allow_html=True)