import streamlit as st
import requests
import base64

WEBHOOK_URL = "https://n8n-production-adc8.up.railway.app/webhook/embalagio-atendimento"
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
}}

/* Botões Secundários */
button[kind="secondary"] {{
    background-color: transparent !important;
    color: #f0f0f0 !important;
    border: 1px solid #FF6A00 !important;
}}
button[kind="secondary"]:hover {{
    background-color: #0E2A3A !important;
    color: #FF6A00 !important;
}}

/* Forçar legibilidade no Popover */
div[data-testid="stPopoverBody"] * {{
    color: #333333 !important;
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

/* Bordas Ativas */
.stSelectbox div[data-baseweb="select"]:focus-within, 
.stTextArea textarea:focus {{
    box-shadow: 0 0 0 2px #FF6A00 !important;
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
}}

.chat-messages {{ flex: 1; overflow-y: auto; padding-right: 5px; display: flex; flex-direction: column; gap: 12px; }}
.msg-user {{ display: flex; justify-content: flex-end; }}
.msg-ai   {{ display: flex; justify-content: flex-start; }}
.bubble { max-width: 85%; padding: 10px 14px; font-size: 0.95rem; line-height: 1.4; word-break: normal; overflow-wrap: break-word; font-family: sans-serif; }
.bubble-user {{ background: #005c4b !important; color: #e9edef !important; border-radius: 12px 4px 12px 12px; }}
.bubble-ai {{ background: #202c33 !important; color: #e9edef !important; border-radius: 4px 12px 12px 12px; }}
.bubble-label {{ color: #8696a0 !important; font-size: 0.7rem; font-family: monospace; margin-bottom: 4px;}}
.chat-empty {{ color: #8696a0 !important; text-align: center; font-family: monospace; font-size: 0.85rem; margin-top: auto; margin-bottom: auto; }}

#MainMenu, footer, header {{ visibility: hidden; }}
.block-container {{ padding-top: 1rem !important; max-width: 1200px; }}

/* Cabeçalho Responsivo */
.header-container {{
    display: flex; justify-content: space-between; align-items: center; 
    padding-bottom: 15px; border-bottom: 2px solid #FF6A00; margin-bottom: 25px; width: 100%;
}}
.header-left {{ display: flex; align-items: center; gap: 20px; }}
.header-logo {{ width: 140px; border-radius: 8px; }}
.header-title-box h1 {{ color: #FF6A00; font-size: 1.5rem; margin: 0; font-weight: 900; line-height: 1.2; }}
.header-title-box p {{ color: #888; font-size: 0.85rem; margin: 0; font-family: monospace; }}

@media (max-width: 768px) {{
    .header-left {{ gap: 12px; }}
    .header-logo {{ width: 90px; }}
    .header-title-box h1 {{ font-size: 1.1rem; }}
    .header-title-box p {{ font-size: 0.65rem; }}
}}
</style>
""", unsafe_allow_html=True)

if "history" not in st.session_state:
    st.session_state.history = []
if "status" not in st.session_state:
    st.session_state.status = None
if "context_start_idx" not in st.session_state:
    st.session_state.context_start_idx = 0 # NOVO: Controla de onde a IA começa a ler

def check_n8n():
    try:
        r = requests.post(WEBHOOK_URL, json={"message": "__ping__", "history": []}, timeout=4)
        if r.status_code == 200:
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

# ─── CABEÇALHO ───
st.markdown(f"""
<div class="header-container">
    <div class="header-left">
        <img src="data:image/png;base64,{logo_b64}" class="header-logo">
        <div class="header-title-box">
            <h1>PORTAL DE ATENDIMENTO</h1>
            <p>Triagem de leads · IA WhatsApp · Powered by Groq + Llama 3.3</p>
        </div>
    </div>
    <div style="background-color: {badge_bg}; border: 1px solid {badge_border}; color: {badge_color}; padding: 6px 12px; border-radius: 20px; font-size: 0.7rem; font-family: monospace; font-weight: bold; white-space: nowrap;">
        {badge_text}
    </div>
</div>
""", unsafe_allow_html=True)

with st.popover("ℹ️ Sobre este Projeto"):
    st.markdown("""
    <div style="color: #333333; font-family: sans-serif; font-size: 0.95rem;">
        <h3 style="color: #FF6A00; margin-top: 0;">📦 Embalagio IA - Atendimento & CRM</h3>
        <p>Sistema inteligente que simula o atendimento automatizado de uma franquia via WhatsApp. 
        A IA interpreta a mensagem, extrai os itens do pedido e salva automaticamente no CRM, confirmando a solicitação com o cliente.</p>
        <p><b>Como Testar:</b></p>
        <ol style="margin-top: 0;">
            <li>Escolha um exemplo no menu suspenso ou digite seu pedido.</li>
            <li>Clique em <b>ENVIAR MENSAGEM</b>.</li>
            <li>A IA registrará os dados e responderá instantaneamente.</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# ─── LAYOUT PRINCIPAL ───
col1, col2 = st.columns([1, 1.3], gap="large")

with col1:
    chat_head_col1, chat_head_col2 = st.columns([3, 1.2], vertical_alignment="center")
    chat_head_col1.markdown('<p class="brand-text" style="font-family: monospace; font-weight: bold; text-transform: uppercase; margin: 0;">💬 Chat de Atendimento</p>', unsafe_allow_html=True)
    if chat_head_col2.button("🗑️ Limpar", use_container_width=True):
        st.session_state.history = []
        st.session_state.status = None
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
        "Escolha um pedido rápido (Opcional):",
        "Oi, quero orçar 1000 caixas de hambúrguer tamanho G.",
        "Me chamo Ana. Preciso de 500 sacolas kraft P para minha loja.",
        "Olá! Quero pedir 300 caixas de pizza personalizadas, sou o Marcos.",
        "Bom dia. Queremos 2000 sacos de papel para pão. Aqui é a padaria Doce Pão."
    ]
    escolha = st.selectbox("💡 Sugestões:", opcoes_exemplos)
    
    # Gerenciamento de estado para limpar o input
    if "input_texto" not in st.session_state:
        st.session_state.input_texto = ""
        
    def limpar_input():
        st.session_state.input_texto = ""

    # Se o usuário escolher um exemplo, joga pra variável
    texto_atual = escolha if escolha != opcoes_exemplos[0] else st.session_state.input_texto

    user_input = st.text_area("Sua mensagem:", value=texto_atual, height=80, placeholder="Digite seu pedido aqui...", key="caixa_texto")

    if st.button("ENVIAR MENSAGEM ➜", use_container_width=True):
        if user_input.strip():
            st.session_state.history.append({"role": "user", "text": user_input.strip()})
            
            with st.spinner("Processando Inteligência Artificial..."):
                try:
                    historico_ativo = st.session_state.history[st.session_state.context_start_idx:]
                    payload = {"message": user_input.strip(), "history": historico_ativo}
                    r = requests.post(WEBHOOK_URL, json=payload, timeout=45)
                    
                    if r.status_code == 200:
                        try:
                            data = r.json()
                            reply = data.get("Reply", data.get("reply", "Desculpe, não entendi."))
                            status_ia = data.get("Status", data.get("status", "Complete"))
                            
                            st.session_state.history.append({"role": "ai", "text": reply})
                            
                            if status_ia == "Qualifying":
                                st.session_state.status = ("info", "🤖 IA coletando dados faltantes...")
                            else: 
                                st.session_state.status = ("ok", "Lead qualificado e salvo no CRM!")
                                st.session_state.context_start_idx = len(st.session_state.history)
                                
                        except ValueError:
                            st.session_state.status = ("err", "Erro: n8n não retornou JSON válido.")
                    else:
                        st.session_state.status = ("err", f"Erro de comunicação: {r.status_code}")
                except Exception as e:
                    st.session_state.status = ("err", "Sistema Offline ou Falha na Conexão.")
            
            # Limpa o texto usando a função callback e recarrega
            limpar_input()
            st.rerun()
        else:
            st.warning("A mensagem não pode estar vazia.")

    # Feedback visual dinâmico abaixo do botão
    if st.session_state.status:
        t, msg = st.session_state.status
        if t == "ok":
            st.markdown(f'<div style="color: #4ade80; font-family: monospace; font-size: 0.85rem; font-weight: bold; margin-top: 10px;">✓ {msg}</div>', unsafe_allow_html=True)
        elif t == "info":
            st.markdown(f'<div style="color: #60a5fa; font-family: monospace; font-size: 0.85rem; font-weight: bold; margin-top: 10px;">⟳ {msg}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div style="color: #f87171; font-family: monospace; font-size: 0.85rem; font-weight: bold; margin-top: 10px;">✗ {msg}</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<p class="brand-text" style="font-family: monospace; font-weight: bold; text-transform: uppercase; margin: 0 0 10px 0;">📊 CRM — Leads em Tempo Real</p>', unsafe_allow_html=True)
    st.markdown(
        f'<div style="background-color: #0E2A3A; border: 2px solid #FF6A00; border-radius: 12px; overflow: hidden; line-height: 0;"><iframe src="{SHEET_EMBED}" width="100%" height="600" frameborder="0" style="border-radius: 10px;"></iframe></div>',
        unsafe_allow_html=True
    )
    st.markdown('<p style="font-size: 0.75rem; color: #888; text-align: right; margin-top: 5px; font-family: monospace;">Atualização em tempo real · Google Sheets</p>', unsafe_allow_html=True)

st.markdown("---")
st.markdown('<h3 class="brand-text" style="text-align: center; margin-bottom: 20px;">🔍 Arquitetura Técnica (Backend Automatizado)</h3>', unsafe_allow_html=True)
st.image("workflow_n8n.png", use_container_width=True)
st.markdown('<p style="text-align: center; font-size: 0.8rem; color: #888;">Clique na imagem para ampliar e arrastar</p>', unsafe_allow_html=True)

# ─── RODAPÉ PROFISSIONAL ───
st.markdown("""
<div style="text-align: center; margin-top: 60px; padding-top: 20px; border-top: 1px solid #1a3c54;">
    <p style="color: #888; font-size: 0.85rem; font-family: monospace;">
        &lt;/&gt; Sistema de Triagem Automatizada | Desenvolvido por <b>Emmanuel</b>
    </p>
</div>
""", unsafe_allow_html=True)