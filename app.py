import streamlit as st
import requests
import base64

WEBHOOK_URL = "https://n8n-production-e6639.up.railway.app/webhook/embalagio-ai"
SHEET_EMBED  = "https://docs.google.com/spreadsheets/d/1QcAuW2CIVvVv03asnwpj32AvT6rXKV9FXwLdSHXWhiw/edit?usp=sharing"

st.set_page_config(page_title="Embalagio CRM IA", page_icon="📦", layout="wide")

def get_base64_of_bin_file(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except:
        return ""

bg_b64 = get_base64_of_bin_file("fundo-chat.jpg")

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&family=Space+Mono:wght@400;700&display=swap');

*, html, body, [class*="css"] {{ font-family: 'Nunito', sans-serif !important; box-sizing: border-box; }}
.stApp {{ background: #0f0f0f; color: #f0f0f0; }}

.emb-header {{ display: flex; align-items: center; gap: 18px; padding: 28px 0 8px 0; border-bottom: 2px solid #00a884; margin-bottom: 28px; flex-wrap: wrap; }}
.emb-logo {{ width: 130px; border-radius: 12px; }}
.emb-title-block h1 {{ font-size: 1.05rem; font-weight: 900; color: #00a884; letter-spacing: 0.12em; text-transform: uppercase; margin: 0 0 2px 0; }}
.emb-title-block p {{ font-size: 0.82rem; color: #888; margin: 0; font-family: 'Space Mono', monospace !important; }}
.emb-badge {{ margin-left: auto; background: #1a1a1a; border: 1px solid #00a884; color: #00a884; font-size: 0.72rem; font-family: 'Space Mono', monospace !important; padding: 5px 12px; border-radius: 20px; letter-spacing: 0.08em; display:flex; align-items:center; gap:8px; white-space: nowrap;}}

.section-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }}
.section-label {{ font-size: 0.7rem; font-family: 'Space Mono', monospace !important; letter-spacing: 0.15em; text-transform: uppercase; color: #00a884; display: flex; align-items: center; gap: 8px; width: 100%;}}
.section-label::after {{ content: ''; flex: 1; height: 1px; background: #2a2a2a; }}

.chat-panel {{ 
    background-color: #0b141a; 
    background-image: url("data:image/jpeg;base64,{bg_b64}");
    background-size: cover;
    background-position: center;
    background-blend-mode: overlay;
    border: 1px solid #2a2a2a; 
    border-radius: 16px; 
    padding: 20px; 
    min-height: 460px; 
    display: flex; 
    flex-direction: column; 
}}

.chat-messages {{ flex: 1; overflow-y: auto; max-height: 340px; padding-right: 4px; display: flex; flex-direction: column; gap: 14px; }}
.chat-empty {{ flex: 1; display: flex; align-items: center; justify-content: center; color: #8696a0; font-size: 0.85rem; font-family: 'Space Mono', monospace; text-align: center; line-height: 2; }}

.msg-user {{ display: flex; justify-content: flex-end; }}
.msg-ai   {{ display: flex; justify-content: flex-start; }}
.bubble {{ max-width: 85%; padding: 11px 16px; font-size: 0.9rem; line-height: 1.5; word-wrap: break-word; box-shadow: 0 1px 2px rgba(0,0,0,0.3); }}
.bubble-user {{ background: #005c4b; color: #e9edef; border-radius: 16px 4px 16px 16px; font-weight: 500; }}
.bubble-ai {{ background: #202c33; color: #e9edef; border-radius: 4px 16px 16px 16px; }}
.bubble-label {{ font-size: 0.65rem; font-family: 'Space Mono', monospace; color: #8696a0; margin-bottom: 4px; }}
.bubble-label-right {{ text-align: right; }}
.chat-divider {{ height: 1px; background: rgba(255,255,255,0.1); margin: 16px 0; }}

.stTextArea > div > div > textarea {{ background: #2a3942 !important; color: #d1d7db !important; border: none !important; border-radius: 10px !important; font-family: 'Nunito', sans-serif !important; font-size: 0.95rem !important; transition: background 0.2s; }}
.stTextArea > div > div > textarea:focus {{ background: #202c33 !important; box-shadow: 0 0 0 1px #00a884 !important; }}
.stButton > button {{ background: #00a884 !important; color: #111b21 !important; border: none !important; border-radius: 10px !important; font-family: 'Nunito', sans-serif !important; font-weight: 800 !important; font-size: 0.9rem !important; letter-spacing: 0.05em !important; padding: 10px 0 !important; width: 100% !important; transition: background 0.2s, transform 0.1s !important; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}
.stButton > button:hover {{ background: #00c298 !important; transform: translateY(-1px) !important; }}
.stButton > button:active {{ transform: translateY(0) !important; }}

.btn-quick {{ background: #202c33 !important; color: #00a884 !important; border: 1px solid #00a884 !important; font-size: 0.75rem !important; padding: 4px 10px !important; width: auto !important; margin-right: 5px !important; margin-bottom: 5px !important; font-weight: 600 !important; }}

.btn-clear {{ background: transparent !important; color: #8696a0 !important; border: none !important; width: auto !important; padding: 0 !important; font-size: 1.2rem !important; margin-left: auto; box-shadow: none !important; }}
.btn-clear:hover {{ background: transparent !important; color: #f87171 !important; transform: none !important; }}

.badge-ok {{ display: inline-flex; align-items: center; gap: 6px; background: #0d2b1a; border: 1px solid #1a5c35; color: #4ade80; padding: 5px 12px; border-radius: 20px; font-size: 0.75rem; font-family: 'Space Mono', monospace; }}
.badge-err {{ display: inline-flex; align-items: center; gap: 6px; background: #2b0d0d; border: 1px solid #5c1a1a; color: #f87171; padding: 5px 12px; border-radius: 20px; font-size: 0.75rem; font-family: 'Space Mono', monospace; }}

.sheet-panel {{ background: #111b21; border: 1px solid #2a2a2a; border-radius: 16px; overflow: hidden; }}
.sheet-footer {{ font-size: 0.72rem; font-family: 'Space Mono', monospace; color: #8696a0; margin-top: 8px; display:flex; justify-content: space-between; flex-wrap: wrap; gap: 5px; }}
.credits {{ color: #8696a0; }}
.credits b {{ color: #00a884; }}

#MainMenu, footer, header {{ visibility: hidden; }}
.block-container {{ padding-top: 0 !important; max-width: 1300px; }}

@media (max-width: 768px) {{
    .emb-header {{ flex-direction: column; align-items: flex-start; gap: 10px; padding: 15px 0; }}
    .emb-logo {{ width: 100px; }}
    .emb-badge {{ margin-left: 0; align-self: flex-start; }}
    .stButton > button {{ font-size: 0.8rem !important; padding: 12px 0 !important; }}
}}
</style>
""", unsafe_allow_html=True)

if "history" not in st.session_state:
    st.session_state.history = []
if "status" not in st.session_state:
    st.session_state.status = None
if "n8n_online" not in st.session_state:
    st.session_state.n8n_online = False
if "pre_msg" not in st.session_state:
    st.session_state.pre_msg = ""

def check_n8n():
    try:
        r = requests.post(WEBHOOK_URL, json={"message": "__ping__"}, timeout=5)
        if r.status_code == 200:
            r.json() 
            return True
        return False
    except:
        return False

st.session_state.n8n_online = check_n8n()

if st.session_state.n8n_online:
    badge_style = "border-color:#1a5c35;color:#4ade80;"
    badge_text  = "● ATIVO"
else:
    badge_style = "border-color:#5c1a1a;color:#f87171;"
    badge_text  = "○ OFFLINE"

with st.container():
    head_col1, head_col2, head_col3 = st.columns([1, 2, 1], vertical_alignment="center")
    
    with head_col1:
        st.image("logo_embalagio.png", width=130)
    
    with head_col2:
        st.markdown(f"""
        <div class="emb-title-block">
            <h1>Portal de Atendimento</h1>
            <p>Triagem inteligente de leads</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.popover("ℹ️ Sobre este Projeto"):
            st.markdown("""
            ### 📦 Embalagio IA - Atendimento & CRM
            Sistema de automação para Franchising.
            - **Frontend:** Streamlit
            - **Backend:** n8n (Railway)
            - **IA:** Llama 3.3 (Groq)
            - **Database:** Google Sheets
            """)

    with head_col3:
        st.markdown(f'<span class="emb-badge" style="{badge_style}">{badge_text}</span>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 1.35], gap="large")

with col1:
    col_lbl, col_clr = st.columns([4, 1])
    with col_lbl:
        st.markdown('<div class="section-label">💬 Chat de Atendimento</div>', unsafe_allow_html=True)
    with col_clr:
        if st.button("🗑️", key="btn_clear", help="Limpar conversa"):
            st.session_state.history = []
            st.rerun()

    msgs_html = ''
    if not st.session_state.history:
        msgs_html = '<div class="chat-empty">Nenhuma mensagem ainda.<br/>Simule um atendimento abaixo ↓</div>'
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

    st.markdown(f'''
    <div class="chat-panel">
      <div class="chat-messages">{msgs_html}</div>
      <div class="chat-divider"></div>
    </div>
    ''', unsafe_allow_html=True)

    quick_msgs = [
        "Quero 500 sacolas P",
        "Fazem personalização?",
        "Qual o prazo de entrega?",
        "Quero orçar caixas de pizza G"
    ]
    
    st.write("")
    q_cols = st.columns(4)
    for i, q_msg in enumerate(quick_msgs):
        with q_cols[i]:
            if st.button(q_msg.split()[0] + "...", key=f"q_{i}", help=q_msg):
                st.session_state.pre_msg = q_msg
                st.rerun()

    user_input = st.text_area(
        "msg",
        value=st.session_state.pre_msg,
        height=90,
        key="input_text",
        label_visibility="collapsed",
        placeholder="Digite sua mensagem aqui..."
    )

    if st.button("ENVIAR ➜"):
        if user_input.strip():
            st.session_state.history.append({"role": "user", "text": user_input.strip()})
            st.session_state.pre_msg = "" 
            with st.spinner("IA da Embalagio está digitando..."):
                try:
                    r = requests.post(WEBHOOK_URL, json={"message": user_input.strip()}, timeout=45)
                    if r.status_code == 200:
                        try:
                            data = r.json()
                            reply = data.get("Reply", data.get("reply", "Mensagem recebida e registrada!"))
                            st.session_state.history.append({"role": "ai", "text": reply})
                            st.session_state.status = ("ok", "Lead salvo no CRM")
                        except ValueError:
                            st.session_state.status = ("err", "Erro: n8n não retornou JSON (Ative o workflow)")
                    else:
                        st.session_state.status = ("err", f"Erro {r.status_code}")
                except requests.exceptions.ConnectionError:
                    st.session_state.status = ("err", "n8n offline — verifique o servidor")
                except Exception as e:
                    st.session_state.status = ("err", str(e)[:60])
            st.rerun()
        else:
            st.warning("Digite uma mensagem antes de enviar.")

    if st.session_state.status:
        t, msg = st.session_state.status
        if t == "ok":
            st.markdown(f'<div class="badge-ok">✓ {msg}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="badge-err">✗ {msg}</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="section-label">📊 CRM — Leads em Tempo Real</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="sheet-panel"><iframe src="{SHEET_EMBED}" width="100%" height="560" frameborder="0"></iframe></div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '''<div class="sheet-footer">
             <span class="credits">Desenvolvido por <b>Emmanuel</b></span>
             <span>Atualiza a cada envio · Google Sheets</span>
           </div>''',
        unsafe_allow_html=True
    )

st.markdown("---")
with st.expander("🔍 Ver Arquitetura Técnica (Backend Automatizado)"):
    st.image("workflow_n8n.png", use_container_width=True, caption="Fluxo de automação: do recebimento da mensagem ao registro no CRM")
    st.markdown("""
    **Legenda do Workflow:**
    - **Porta de Entrada:** Webhook que recebe os dados do Portal.
    - **Filtro de Ping:** Verifica a saúde da conexão.
    - **Cérebro (IA):** Processamento de linguagem natural e extração de dados.
    - **CRM:** Persistência dos dados no Google Sheets.
    """)