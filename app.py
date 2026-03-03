import streamlit as st
import requests
import base64
import re
import json

WEBHOOK_URL = "https://n8n-production-adc8.up.railway.app/webhook/embalagio-atendimento"
SHEET_EMBED  = "https://docs.google.com/spreadsheets/d/1QcAuW2CIVvVv03asnwpj32AvT6rXKV9FXwLdSHXWhiw/edit?usp=sharing&rm=minimal"

st.set_page_config(page_title="Embalagio CRM", page_icon="📦", layout="wide")

def get_img_as_base64(file_path):
    try:
        with open(file_path, 'rb') as f:
            return base64.b64encode(f.read()).decode()
    except:
        return ""

logo_b64 = get_img_as_base64("logo_embalagio.png")

st.markdown(f"""
<style>
#MainMenu {{ visibility: hidden; }}
footer {{ visibility: hidden; }}
header {{ visibility: hidden; }}
[data-testid="stToolbar"] {{ visibility: hidden; }}

.stApp, .stApp > header {{ background-color: #0A1F2C !important; }}

h1, h2, h3, h4, p, label, li, span {{ color: #f0f0f0; }}

.brand-text {{ color: #FF6A00 !important; }}

.panel-title {{
    color: #FF6A00;
    font-family: monospace;
    font-weight: bold;
    text-transform: uppercase;
    margin: 0;
    font-size: 1.05rem;
}}

button[kind="primary"] {{ 
    background: #FF6A00 !important; 
    color: #ffffff !important; 
    border: none !important; 
    border-radius: 8px !important; 
    font-weight: 800 !important; 
    padding: 12px 0 !important;
    transition: all 0.3s ease;
}}
button[kind="primary"]:hover {{ 
    background: #FF7A1A !important; 
}}

button[kind="secondary"] {{
    background: transparent !important;
    color: #8696a0 !important;
    border: 1px solid #1a3c54 !important;
    box-shadow: none !important;
    font-size: 0.85rem !important;
    padding: 4px 10px !important;
    border-radius: 6px !important;
    min-height: 0 !important;
    transition: all 0.2s ease;
}}
button[kind="secondary"]:hover {{
    color: #f0f0f0 !important;
    border-color: #FF6A00 !important;
    background: rgba(255, 106, 0, 0.1) !important;
}}

div[data-testid="stButton"]:has(button[kind="secondary"]) {{
    display: flex;
    justify-content: flex-end;
}}
@media (max-width: 768px) {{
    div[data-testid="stButton"]:has(button[kind="secondary"]) {{
        justify-content: center;
    }}
}}

div[data-testid="stPopoverBody"] * {{ color: #333333 !important; }}

.stSelectbox div[data-baseweb="select"] {{ border-color: #FF6A00 !important; background-color: #0E2A3A !important; color: #f0f0f0 !important; }}
.stTextArea textarea {{ border-color: #FF6A00 !important; background-color: #0E2A3A !important; color: #f0f0f0 !important; }}

.stSelectbox div[data-baseweb="select"]:focus-within, .stTextArea textarea:focus {{ box-shadow: 0 0 0 2px #FF6A00 !important; outline: none !important; }}

.chat-panel {{ background-color: #0E2A3A; border: 1px solid #FF6A00; border-radius: 12px; padding: 15px; height: 400px; display: flex; flex-direction: column; }}
.chat-messages {{ flex: 1; overflow-y: auto; padding-right: 5px; display: flex; flex-direction: column-reverse; gap: 12px; }}
.msg-user {{ display: flex; justify-content: flex-end; }}
.msg-ai   {{ display: flex; justify-content: flex-start; }}

.bubble {{ 
    width: fit-content; 
    min-width: min-content !important;
    max-width: 85%; 
    padding: 10px 14px; 
    border-radius: 12px;
    font-family: sans-serif; 
}}

.bubble p {{
    margin: 0 !important;
    font-size: 0.95rem; 
    line-height: 1.4; 
    white-space: pre-wrap !important; 
    word-break: normal !important; 
    overflow-wrap: break-word !important; 
    -webkit-hyphens: none !important; 
    hyphens: none !important;
}}

.bubble-user {{ background: #005c4b !important; color: #e9edef !important; border-radius: 12px 4px 12px 12px; }}
.bubble-ai {{ background: #202c33 !important; color: #e9edef !important; border-radius: 4px 12px 12px 12px; }}
.bubble-label {{ color: #8696a0 !important; font-size: 0.7rem; font-family: monospace; margin-bottom: 4px;}}
.chat-empty {{ color: #8696a0 !important; text-align: center; font-family: monospace; font-size: 0.85rem; margin-top: auto; margin-bottom: auto; }}
.block-container {{ padding-top: 1rem !important; max-width: 1400px; }}

.header-container {{
    display: flex; justify-content: space-between; align-items: center; 
    padding-bottom: 15px; border-bottom: 2px solid #FF6A00; margin-bottom: 25px; width: 100%;
}}
.header-left {{ display: flex; align-items: center; gap: 20px; }}
.header-logo {{ width: 140px; border-radius: 8px; }}
.header-title-box h1 {{ color: #FF6A00; font-size: 1.5rem; margin: 0; font-weight: 900; line-height: 1.2; }}
.header-title-box p {{ color: #888; font-size: 0.85rem; margin: 0; font-family: monospace; }}

@media (max-width: 768px) {{
    .header-container {{ flex-direction: column; align-items: center; text-align: center; gap: 15px; }}
    .header-left {{ flex-direction: column; align-items: center; gap: 10px; }}
    .header-logo {{ width: 100px; }}
    .header-title-box h1 {{ font-size: 1.3rem; }}
    .header-title-box p {{ font-size: 0.75rem; }}
}}
</style>
""", unsafe_allow_html=True)

if "history" not in st.session_state:
    st.session_state.history = []
if "status" not in st.session_state:
    st.session_state.status = None
if "context_start_idx" not in st.session_state:
    st.session_state.context_start_idx = 0
if "caixa_texto" not in st.session_state:
    st.session_state.caixa_texto = ""
if "texto_enviado" not in st.session_state:
    st.session_state.texto_enviado = ""

@st.cache_data(ttl=30)
def check_n8n():
    try:
        r = requests.post(WEBHOOK_URL, json={"message": "__ping__", "history": ""}, timeout=4)
        return r.status_code == 200
    except:
        return False

n8n_online = check_n8n()
badge_bg, badge_border, badge_color, badge_text = ("#0d2b1a", "#1a5c35", "#4ade80", "● SISTEMA ATIVO") if n8n_online else ("#2b0d0d", "#5c1a1a", "#f87171", "○ SISTEMA OFFLINE")

st.markdown(f"""
<div class="header-container">
    <div class="header-left">
        <img src="data:image/png;base64,{logo_b64}" class="header-logo">
        <div class="header-title-box">
            <h1>PORTAL DE ATENDIMENTO</h1>
            <p>Triagem de leads · IA WhatsApp · Powered by Groq + Qwen 32B</p>
        </div>
    </div>
    <div style="background-color: {badge_bg}; border: 1px solid {badge_border}; color: {badge_color}; padding: 8px 18px; border-radius: 20px; font-size: 0.85rem; font-family: monospace; font-weight: bold; white-space: nowrap;">
        {badge_text}
    </div>
</div>
""", unsafe_allow_html=True)

with st.popover("ℹ️ Sobre este Projeto"):
    st.markdown("""
    <div style="color: #333333; font-family: sans-serif; font-size: 0.95rem; padding: 5px;">
        <h3 style="color: #FF6A00; margin-top: 0; margin-bottom: 10px;">📦 Embalagio IA - Triagem & CRM</h3>
        <p style="margin-bottom: 10px;">O <b>Embalagio IA</b> é um assistente virtual autônomo focado na qualificação de leads. Utilizando LLMs (Qwen 32B via Groq) integrados ao n8n e hospedado no Railway, ele simula o atendimento via WhatsApp.</p>
        <p style="margin-bottom: 10px;">Ele interpreta mensagens, extrai dados (Nome, Categoria dinâmica e Quantidade) e alimenta um CRM no Google Sheets em tempo real, garantindo leads qualificados para o time comercial.</p>
        <p style="font-size: 0.70rem; border-top: 1px solid #ccc; padding-top: 10px; color: #666;">Desenvolvido com Python, Streamlit, n8n, Railway, Groq API e Google Sheets.</p>
    </div>
    """, unsafe_allow_html=True)

st.write("")

col1, col2 = st.columns([1.2, 2.2], gap="large")

with col1:
    c_title1, c_btn = st.columns([0.7, 0.3], vertical_alignment="center")
    with c_title1:
        st.markdown('<p class="panel-title">💬 Chat de Atendimento</p>', unsafe_allow_html=True)
    with c_btn:
        if st.button("🗑️ Limpar", type="secondary"):
            st.session_state.history = []
            st.session_state.status = None
            st.session_state.context_start_idx = 0
            st.session_state.caixa_texto = ""
            st.rerun()

    chat_container = st.empty()

    def renderizar_chat():
        msgs_html = ''
        if not st.session_state.history:
            msgs_html = '<div class="chat-empty">Nenhuma mensagem ainda.<br/>Selecione um cenário de teste ou digite abaixo ↓</div>'
        else:
            for m in reversed(st.session_state.history):
                if m["role"] == "user":
                    msgs_html += f'<div class="msg-user"><div><div class="bubble-label bubble-label-right" style="text-align: right;">Você</div><div class="bubble bubble-user"><p>{m["text"]}</p></div></div></div>'
                else:
                    msgs_html += f'<div class="msg-ai"><div><div class="bubble-label">🤖 Embalagio IA</div><div class="bubble bubble-ai"><p>{m["text"]}</p></div></div></div>'
        return f'<div class="chat-panel"><div class="chat-messages" id="chat-messages-box">{msgs_html}</div></div>'

    chat_container.markdown(renderizar_chat(), unsafe_allow_html=True)
    
    st.write("")
    
    testes_opcoes = {
        "Digite livremente ou escolha um cenário de teste": {
            "msg": "", 
            "desc": ""
        },
        "Saudação": {
            "msg": "Bom dia! Tudo bem com vocês?", 
            "desc": "Valida se o assistente inicia o atendimento de forma humanizada e solicita as informações necessárias para o pedido."
        },
        "Pedido de Caixas de Pizza": {
            "msg": "Oi, sou o Marcos. Preciso de 500 caixas de pizza G.", 
            "desc": "Testa a extração imediata dos dados fundamentais (Nome, Produto e Quantidade) e a correta categorização do item."
        },
        "Pedido Personalizado": {
            "msg": "Olá, sou a Patrícia da Doce Arte. Preciso de 150 sacolas de papel kraft azul marinho com alça de cetim branca para kits de presente.", 
            "desc": "Avalia a precisão da IA em processar um pedido com detalhes de cor e uso específico em uma única frase."
        },
        "Filtro de Segurança e Escopo": {
            "msg": "Boa tarde, sou o Pedro. Vocês consertam impressoras?", 
            "desc": "Verifica se o sistema identifica e bloqueia solicitações fora do catálogo de produtos, mantendo o banco de dados limpo."
        },
        "Validação de Grande Volume": {
            "msg": "Oi, sou a Renata. Quero 3000 mini embalagens kraft para doces.", 
            "desc": "Demonstra o protocolo de segurança obrigatório: para qualquer pedido acima de 1000 unidades, o sistema pausa para solicitar uma confirmação humana."
        },
        "Confirmação de Segurança Explicita": {
            "msg": "Olá, aqui é a Renata. Queremos 3000 mini embalagens kraft, pode confirmar esse volume pra mim.", 
            "desc": "Valida o rigor do sistema: mesmo que o cliente peça para confirmar na primeira mensagem, a IA cumpre o protocolo e solicita uma resposta afirmativa dedicada."
        }
    }

    def on_select_change():
        escolha = st.session_state.seletor_teste
        if escolha != "Digite livremente ou escolha um cenário de teste":
            st.session_state.caixa_texto = testes_opcoes[escolha]["msg"]

    escolha_atual = st.selectbox(
        "💡 Sugestões de pedidos rápidos:", 
        list(testes_opcoes.keys()), 
        key="seletor_teste", 
        on_change=on_select_change
    )

    if escolha_atual != "Digite livremente ou escolha um cenário de teste":
        st.markdown(f"""
        <div style="background-color: #0d212e; border-left: 4px solid #FF6A00; padding: 12px; margin-bottom: 15px; border-radius: 0 8px 8px 0;">
            <span style="color: #FF6A00; font-size: 0.8rem; font-family: monospace; font-weight: bold; text-transform: uppercase;">Objetivo do Teste</span><br>
            <span style="font-size: 0.85rem; color: #d1d5db;">{testes_opcoes[escolha_atual]['desc']}</span>
        </div>
        """, unsafe_allow_html=True)

    def preparar_envio():
        st.session_state.texto_enviado = st.session_state.caixa_texto
        st.session_state.caixa_texto = ""

    st.text_area("Sua mensagem:", key="caixa_texto", height=80, placeholder="Digite seu pedido aqui...")

    if st.button("ENVIAR MENSAGEM ➜", type="primary", use_container_width=True, on_click=preparar_envio):
        msg = st.session_state.texto_enviado.strip()
        if msg:
            st.session_state.history.append({"role": "user", "text": msg})
            chat_container.markdown(renderizar_chat(), unsafe_allow_html=True)
            
            with st.spinner("Processando Inteligência Artificial..."):
                try:
                    historico_ativo = st.session_state.history[st.session_state.context_start_idx:]
                    conversa_texto = ""
                    for h in historico_ativo:
                        ator = "Cliente" if h["role"] == "user" else "Assistente"
                        conversa_texto += f"{ator}: {h['text']}\n"
                    
                    payload = {"message": msg, "history": conversa_texto}
                    r = requests.post(WEBHOOK_URL, json=payload, timeout=45)
                    
                    if r.status_code == 200:
                        raw_text = r.text
                        try:
                            match = re.search(r'(\{.*\})', raw_text, re.DOTALL)
                            if match:
                                clean_json = match.group(1)
                                data = json.loads(clean_json)
                                
                                reply = data.get("Reply", data.get("reply", "Sem resposta."))
                                status_ia = data.get("Status", data.get("status", "Qualifying"))
                                
                                st.session_state.history.append({"role": "ai", "text": reply})
                                
                                if status_ia == "Complete":
                                    st.session_state.status = ("ok", "Lead qualificado e salvo no CRM!")
                                    st.session_state.context_start_idx = len(st.session_state.history)
                                else:
                                    st.session_state.status = ("info", "🤖 IA coletando dados...")
                            else:
                                texto_debug = raw_text if raw_text.strip() else "[RESPOSTA VAZIA DO N8N]"
                                st.session_state.history.append({"role": "ai", "text": f"⚠️ ERRO DE FORMATO. O modelo respondeu assim: {texto_debug}"})
                                st.session_state.status = ("err", "🤖 IA não gerou o JSON esperado.")
                                
                        except Exception as e:
                            st.session_state.status = ("err", f"Erro crítico no Python: {str(e)}")
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
        elif t == "info":
            st.markdown(f'<div style="color: #60a5fa; font-family: monospace; font-size: 0.85rem; font-weight: bold; margin-top: 10px;">⟳ {msg}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div style="color: #f87171; font-family: monospace; font-size: 0.85rem; font-weight: bold; margin-top: 10px;">✗ {msg}</div>', unsafe_allow_html=True)

with col2:
    c_title2, c_empty = st.columns([0.7, 0.3], vertical_alignment="center")
    with c_title2:
        st.markdown('<p class="panel-title">📊 CRM — Leads em Tempo Real</p>', unsafe_allow_html=True)
    with c_empty:
        st.empty() 

    st.markdown(
        f'<div style="background-color: #0E2A3A; border: 2px solid #FF6A00; border-radius: 12px; overflow: hidden; line-height: 0;"><iframe src="{SHEET_EMBED}" width="100%" height="600" frameborder="0" style="border-radius: 10px;"></iframe></div>',
        unsafe_allow_html=True
    )
    st.markdown('<p style="font-size: 0.75rem; color: #888; text-align: right; margin-top: 5px; font-family: monospace;">Atualização em tempo real · Google Sheets</p>', unsafe_allow_html=True)

st.markdown("---")
st.markdown('<h3 class="brand-text" style="text-align: center; margin-bottom: 20px;">🔍 Arquitetura Técnica (Backend Automatizado)</h3>', unsafe_allow_html=True)
st.image("workflow_n8n.png", use_container_width=True)

st.markdown("""
<div style="text-align: center; margin-top: 60px; padding-top: 20px; border-top: 1px solid #1a3c54;">
    <a href="https://github.com/kubiszevski/embalagio-atendimento/blob/main/README.md" target="_blank" style="color: #d1d5db; text-decoration: none; font-size: 0.9rem; font-family: monospace; display: inline-block; margin-bottom: 12px; border: 1px solid #4ade80; padding: 6px 16px; border-radius: 6px;">📖 Ver Documentação Completa no GitHub</a>
    <p style="color: #888; font-size: 0.85rem; font-family: monospace; margin-bottom: 0;">
        Sistema de Triagem Automatizada | Desenvolvido por <b>Emmanuel</b>
    </p>
</div>
""", unsafe_allow_html=True)