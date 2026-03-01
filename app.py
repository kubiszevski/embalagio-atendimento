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

# CSS Limpo e Seguro
st.markdown(f"""
<style>
.stApp {{ background-color: #0f0f0f; }}

.chat-panel {{ 
    background-color: #0b141a; 
    background-image: url("data:image/jpeg;base64,{bg_b64}");
    background-size: cover;
    background-position: center;
    background-blend-mode: overlay;
    border: 1px solid #2a2a2a; 
    border-radius: 12px; 
    padding: 15px; 
    height: 400px; 
    display: flex; 
    flex-direction: column; 
}}

.chat-messages {{ flex: 1; overflow-y: auto; padding-right: 5px; display: flex; flex-direction: column; gap: 12px; }}
.chat-empty {{ flex: 1; display: flex; align-items: center; justify-content: center; color: #8696a0; font-size: 0.9rem; font-family: monospace; text-align: center; }}

.msg-user {{ display: flex; justify-content: flex-end; }}
.msg-ai   {{ display: flex; justify-content: flex-start; }}
.bubble {{ max-width: 85%; padding: 10px 14px; font-size: 0.95rem; line-height: 1.4; word-wrap: break-word; box-shadow: 0 1px 2px rgba(0,0,0,0.3); color: #e9edef; font-family: sans-serif; }}
.bubble-user {{ background: #005c4b; border-radius: 12px 4px 12px 12px; }}
.bubble-ai {{ background: #202c33; border-radius: 4px 12px 12px 12px; }}
.bubble-label {{ font-size: 0.7rem; color: #8696a0; margin-bottom: 4px; font-family: monospace; }}

/* Esconde menu padrao do Streamlit */
#MainMenu, footer, header {{ visibility: hidden; }}
.block-container {{ padding-top: 1rem !important; max-width: 1200px; }}
</style>
""", unsafe_allow_html=True)

# ─── INICIALIZAÇÃO DE ESTADOS ───
if "history" not in st.session_state:
    st.session_state.history = []
if "status" not in st.session_state:
    st.session_state.status = None

# ─── CHECAR SE N8N ESTÁ ONLINE ───
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
    badge_color = "#4ade80"
    badge_bg = "#0d2b1a"
    badge_border = "#1a5c35"
    badge_text  = "● SISTEMA ATIVO"
else:
    badge_color = "#f87171"
    badge_bg = "#2b0d0d"
    badge_border = "#5c1a1a"
    badge_text  = "○ SISTEMA OFFLINE"

# ─── HEADER ───
col_logo, col_title, col_badge = st.columns([1, 2.5, 1], vertical_alignment="center")

with col_logo:
    st.image("logo_embalagio.png", use_container_width=True)

with col_title:
    st.markdown("<h2 style='color: #00a884; font-weight: 800; margin-bottom: 0px;'>PORTAL DE ATENDIMENTO</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #888; font-family: monospace; margin-top: 0px;'>Triagem inteligente de leads · IA WhatsApp</p>", unsafe_allow_html=True)
    
    with st.popover("ℹ️ Sobre este Projeto"):
        st.markdown("""
        ### 📦 Embalagio IA - Atendimento & CRM
        
        **A Ideia do Projeto:**
        O objetivo é simular o atendimento automatizado de uma franquia via WhatsApp. 
        O sistema recebe a mensagem não-estruturada do cliente, a Inteligência Artificial interpreta a intenção (dúvida, orçamento, pedido), extrai os itens desejados e salva tudo de forma automática e organizada no CRM.

        **Como Usar (Passo a Passo):**
        1. Simule ser um cliente: escolha um exemplo no menu suspenso ou digite livremente no campo de texto.
        2. Clique em **ENVIAR MENSAGEM**.
        3. Veja a mágica acontecer: a IA responderá cordialmente no chat e, simultaneamente, os dados serão cadastrados na planilha ao lado.
        
        **Tecnologias:** Streamlit (Frontend), n8n (Orquestração), Llama 3.3 via Groq (IA) e Google Sheets (Banco de Dados).
        """)

with col_badge:
    st.markdown(f'''
    <div style="background-color: {badge_bg}; border: 1px solid {badge_border}; color: {badge_color}; 
    padding: 8px 15px; border-radius: 20px; text-align: center; font-family: monospace; font-size: 0.85rem; font-weight: bold;">
    {badge_text}</div>
    ''', unsafe_allow_html=True)

st.divider()

# ─── LAYOUT PRINCIPAL ───
col1, col2 = st.columns([1, 1.3], gap="large")

with col1:
    chat_head_col1, chat_head_col2 = st.columns([3, 1], vertical_alignment="center")
    chat_head_col1.markdown('<p style="color: #00a884; font-family: monospace; font-weight: bold; text-transform: uppercase;">💬 Chat de Atendimento</p>', unsafe_allow_html=True)
    if chat_head_col2.button("🗑️ Limpar", help="Apagar histórico"):
        st.session_state.history = []
        st.rerun()

    # Histórico de mensagens
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
                    <div class="bubble bubble-user">{m["text"]}</div>
                  </div>
                </div>'''
            else:
                msgs_html += f'''
                <div class="msg-ai">
                  <div>
                    <div class="bubble-label">🤖 Embalagio IA</div>
                    <div class="bubble bubble-ai">{m["text"]}</div>
                  </div>
                </div>'''

    st.markdown(f'<div class="chat-panel"><div class="chat-messages">{msgs_html}</div></div>', unsafe_allow_html=True)

    st.write("")
    # Menu suspenso de exemplos
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

    if st.button("ENVIAR MENSAGEM ➜", use_container_width=True, type="primary"):
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
            st.success(f"✓ {msg}")
        else:
            st.error(f"✗ {msg}")

with col2:
    st.markdown('<p style="color: #00a884; font-family: monospace; font-weight: bold; text-transform: uppercase;">📊 CRM — Leads em Tempo Real</p>', unsafe_allow_html=True)
    st.markdown(
        f'<div style="border: 1px solid #2a2a2a; border-radius: 12px; overflow: hidden;"><iframe src="{SHEET_EMBED}" width="100%" height="600" frameborder="0"></iframe></div>',
        unsafe_allow_html=True
    )
    st.markdown('<p style="font-size: 0.75rem; color: #888; text-align: right; margin-top: 5px;">Desenvolvido por <b style="color:#00a884;">Emmanuel</b> | Atualização em tempo real</p>', unsafe_allow_html=True)

# ─── WORKFLOW SEMPRE ABERTO ───
st.markdown("---")
st.markdown('<h3 style="color: #00a884;">🔍 Arquitetura Técnica (Backend Automatizado)</h3>', unsafe_allow_html=True)
st.image("workflow_n8n.png", use_container_width=True)
st.markdown("""
<div style="color: #bbb; font-size: 0.9rem;">
<b>Como os dados fluem:</b><br>
1. <b>Porta de Entrada:</b> O n8n recebe a requisição via Webhook.<br>
2. <b>Inteligência Artificial (Llama 3.3):</b> Processa a linguagem natural, entende a intenção, resume o pedido e redige a resposta humanizada.<br>
3. <b>CRM:</b> O nó do Google Sheets atua como banco de dados, persistindo o lead automaticamente.<br>
4. <b>Retorno:</b> A resposta formatada é devolvida ao cliente na interface do Streamlit.
</div>
""", unsafe_allow_html=True)