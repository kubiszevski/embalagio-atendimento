import streamlit as st
import requests
import base64

WEBHOOK_URL = "https://n8n-production-e6639.up.railway.app/webhook/embalagio-ai"
SHEET_EMBED  = "https://docs.google.com/spreadsheets/d/1QcAuW2CIVvVv03asnwpj32AvT6rXKV9FXwLdSHXWhiw/edit?usp=sharing"

st.set_page_config(page_title="Embalagio CRM IA", page_icon="📦", layout="wide")

# Converte o fundo do chat
def get_base64_of_bin_file(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except:
        return ""

bg_b64 = get_base64_of_bin_file("fundo-chat.jpg")

# CSS Customizado
st.markdown(f"""
<style>
/* Fundo Creme e Cor Laranja Global */
.stApp, .stApp > header {{ 
    background-color: #121210 !important; /* #CARIOTECA (Altere o HEX aqui se quiser mudar a cor de fundo) */
}}

h1, h2, h3, p, label, li, span {{ 
    color: #e85d04 !important; /* Cor da Embalagio */
}}

/* Protegendo as cores de dentro do CHAT */
.chat-panel p, .chat-panel div, .chat-panel span {{ color: inherit !important; }}
.chat-empty {{ color: #8696a0 !important; }}
.bubble-user {{ background: #005c4b !important; color: #e9edef !important; }}
.bubble-user p, .bubble-user span {{ color: #e9edef !important; }}
.bubble-ai {{ background: #202c33 !important; color: #e9edef !important; }}
.bubble-ai p, .bubble-ai span {{ color: #e9edef !important; }}
.bubble-label {{ color: #8696a0 !important; font-size: 0.7rem; font-family: monospace; margin-bottom: 4px;}}

/* Badge de Status (Protegido) */
.badge-ok, .badge-ok span {{ color: #4ade80 !important; font-family: monospace; font-weight: bold; }}
.badge-err, .badge-err span {{ color: #f87171 !important; font-family: monospace; font-weight: bold; }}

/* Botao de Enviar Laranja */
.stButton > button {{ 
    background: #e85d04 !important; 
    color: #ffffff !important; 
    border: none !important; 
    border-radius: 8px !important; 
    font-weight: 800 !important; 
    padding: 12px 0 !important;
}}
.stButton > button * {{ color: #ffffff !important; }}
.stButton > button:hover {{ background: #cf4f00 !important; }}

/* Selectbox e Input */
.stSelectbox div[data-baseweb="select"] {{ border-color: #e85d04 !important; background-color: #ffffff !important; }}
.stTextArea textarea {{ border-color: #e85d04 !important; background-color: #ffffff !important; color: #333 !important; }}

/* Painel do Chat - Desktop (Sem Wallpaper) e Mobile (Com Wallpaper) */
.chat-panel {{ 
    background-color: #0b141a; 
    border: 1px solid #e85d04; 
    border-radius: 12px; 
    padding: 15px; 
    height: 400px; 
    display: flex; 
    flex-direction: column; 
}}

.chat-messages {{ flex: 1; overflow-y: auto; padding-right: 5px; display: flex; flex-direction: column; gap: 12px; }}
.msg-user {{ display: flex; justify-content: flex-end; }}
.msg-ai   {{ display: flex; justify-content: flex-start; }}
.bubble {{ max-width: 85%; padding: 10px 14px; font-size: 0.95rem; line-height: 1.4; word-wrap: break-word; box-shadow: 0 1px 2px rgba(0,0,0,0.3); font-family: sans-serif; }}
.bubble-user {{ border-radius: 12px 4px 12px 12px; }}
.bubble-ai {{ border-radius: 4px 12px 12px 12px; }}

#MainMenu, footer, header {{ visibility: hidden; }}
.block-container {{ padding-top: 1rem !important; max-width: 1200px; }}

/* Ajustes Mobile (Tamanho da logo e Wallpaper) */
@media (max-width: 768px) {{
    [data-testid="stImage"] img {{ max-width: 120px !important; margin: 0 auto; display: block; }}
    .chat-panel {{ 
        background-image: url("data:image/jpeg;base64,{bg_b64}");
        background-size: cover;
        background-position: center;
        background-blend-mode: overlay;
    }}
}}
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
    badge_text  = "● SISTEMA ATIVO"
    badge_class = "badge-ok"
else:
    badge_bg = "#2b0d0d"
    badge_border = "#5c1a1a"
    badge_text  = "○ SISTEMA OFFLINE"
    badge_class = "badge-err"

col_logo, col_title, col_badge = st.columns([1, 2.5, 1], vertical_alignment="center")

with col_logo:
    st.image("logo_embalagio.png", use_container_width=True)

with col_title:
    st.markdown("<h2 style='font-weight: 900; margin-bottom: 0px;'>PORTAL DE ATENDIMENTO</h2>", unsafe_allow_html=True)
    st.markdown("<p style='font-family: monospace; margin-top: 0px; font-weight: bold;'>Triagem inteligente de leads · IA WhatsApp · Powered by Groq + Llama 3.3</p>", unsafe_allow_html=True)
    
    with st.popover("ℹ️ Sobre este Projeto"):
        st.markdown("""
        ### 📦 Embalagio IA - Atendimento & CRM
        **A Ideia do Projeto:**
        Sistema que simula o atendimento automatizado de uma franquia via WhatsApp. 
        A IA interpreta a mensagem do cliente, extrai os itens desejados e salva tudo de forma automática no CRM, além de responder cordialmente no chat.

        **Como Usar:**
        1. Simule ser um cliente: escolha um exemplo ou digite no campo.
        2. Clique em **ENVIAR MENSAGEM**.
        3. A IA responderá no chat e os dados serão cadastrados na planilha.
        """)

with col_badge:
    st.markdown(f'''
    <div class="{badge_class}" style="background-color: {badge_bg}; border: 1px solid {badge_border}; 
    padding: 8px 15px; border-radius: 20px; text-align: center; font-size: 0.85rem;">
    <span>{badge_text}</span></div>
    ''', unsafe_allow_html=True)

st.divider()

col1, col2 = st.columns([1, 1.3], gap="large")

with col1:
    chat_head_col1, chat_head_col2 = st.columns([3, 1], vertical_alignment="center")
    chat_head_col1.markdown('<p style="font-family: monospace; font-weight: bold; text-transform: uppercase;">💬 Chat de Atendimento</p>', unsafe_allow_html=True)
    if chat_head_col2.button("🗑️ Limpar"):
        st.session_state.history = []
        st.rerun()

    msgs_html = ''
    if not st.session_state.history:
        msgs_html = '<div class="chat-empty">Nenhuma mensagem ainda.<br/>Selecione um exemplo ou digite abaixo ↓</div>'
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
        "-- Digite livremente ou escolha um exemplo --",
        "Oi, sou o Carlos. Queria 500 sacolas kraft personalizadas pro meu delivery em Porto Alegre.",
        "Boa tarde. Vocês fazem personalização de logo na caixa de pizza?",
        "Qual é o prazo médio de entrega para São Paulo?",
        "Olá, quero orçar 1000 caixas de hambúrguer tamanho G."
    ]
    escolha = st.selectbox("💡 Sugestões de mensagens:", opcoes_exemplos)
    texto_padrao = escolha if escolha != opcoes_exemplos[0] else ""

    user_input = st.text_area("Sua mensagem:", value=texto_padrao, height=80, placeholder="Digite aqui...")

    if st.button("ENVIAR MENSAGEM ➜", use_container_width=True):
        if user_input.strip():
            st.session_state.history.append({"role": "user", "text": user_input.strip()})
            with st.spinner("IA da Embalagio está digitando..."):
                try:
                    r = requests.post(WEBHOOK_URL, json={"message": user_input.strip()}, timeout=45)
                    if r.status_code == 200:
                        try:
                            data = r.json()
                            reply = data.get("Reply", data.get("reply", "Mensagem recebida com sucesso!"))
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
            st.markdown(f'<div class="badge-ok"><span>✓ {msg}</span></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="badge-err"><span>✗ {msg}</span></div>', unsafe_allow_html=True)

with col2:
    st.markdown('<p style="font-family: monospace; font-weight: bold; text-transform: uppercase;">📊 CRM — Leads em Tempo Real</p>', unsafe_allow_html=True)
    st.markdown(
        f'<div style="border: 2px solid #e85d04; border-radius: 12px; overflow: hidden;"><iframe src="{SHEET_EMBED}" width="100%" height="600" frameborder="0"></iframe></div>',
        unsafe_allow_html=True
    )
    st.markdown('<p style="font-size: 0.75rem; text-align: right; margin-top: 5px;">Atualização em tempo real · Google Sheets</p>', unsafe_allow_html=True)

st.markdown("---")
st.markdown('<h3 style="text-align: center;">🔍 Arquitetura Técnica (Backend Automatizado)</h3>', unsafe_allow_html=True)
st.image("workflow_n8n.png", use_container_width=True)

# Créditos no final
st.markdown('<p style="text-align: center; font-weight: bold; margin-top: 40px; font-size: 0.9rem;">Desenvolvido por Emmanuel</p>', unsafe_allow_html=True)