# 📦 Embalagio IA - Atendimento & CRM Automatizado

Este projeto é um **Portal de Atendimento Inteligente** desenvolvido para simular a automação do WhatsApp de uma franquia (Embalagio). Ele utiliza Inteligência Artificial para interpretar mensagens não-estruturadas de clientes, extrair dados relevantes de pedidos e cadastrá-los automaticamente em um CRM, além de fornecer uma resposta humanizada em tempo real.



## 🎯 O Problema que este projeto resolve
Em operações de franquias ou delivery, atendentes perdem muito tempo lendo mensagens longas, extraindo manualmente quantidades, tamanhos e intenções para planilhas. Este sistema elimina essa fricção, garantindo:
- **Zero perda de leads:** Todo pedido é registrado instantaneamente.
- **Atendimento 24/7:** O cliente recebe confirmação imediata.
- **Dados estruturados:** O time de vendas recebe uma planilha limpa apenas com o que importa (Nome, Intenção, Resumo do Pedido).

---

## 🚀 Funcionalidades

- **💬 Chat Integrado:** Interface responsiva simulando um ambiente de mensagens.
- **🤖 Triagem com IA (Llama 3.3):** Compreensão de linguagem natural ultrarrápida (powered by Groq).
- **📊 CRM em Tempo Real:** Visualização do Google Sheets incorporada diretamente no painel.
- **⚡ Respostas Rápidas:** Menu de testes com "quick replies" para facilitar demonstrações.
- **🟢 Monitoramento de Status:** Verificação de saúde (Health Check) do servidor n8n em tempo real (Online/Offline).
- **🎨 UI/UX Moderna:** Tema Dark corporativo com design responsivo (Mobile & Desktop).

---

## 🛠️ Arquitetura e Tecnologias

A solução foi construída utilizando uma arquitetura baseada em microsserviços e integração em nuvem:

1. **Frontend:** [Streamlit](https://streamlit.io/) (Python) hospedado no Streamlit Cloud.
2. **Orquestração (Backend):** [n8n](https://n8n.io/) rodando em container Docker na plataforma Railway.
3. **Cérebro (IA):** Modelo **Llama 3.3** via API da [Groq](https://groq.com/) (Inference engine de baixíssima latência).
4. **Banco de Dados (CRM):** Integração nativa com [Google Sheets API](https://developers.google.com/sheets/api).

### 🔄 Fluxo de Dados (Workflow)
1. O usuário envia a mensagem pelo Streamlit.
2. O Streamlit dispara uma requisição POST para o Webhook do n8n.
3. O n8n recebe o payload e aciona a IA (Groq).
4. A IA processa o texto e retorna um objeto JSON estruturado.
5. O n8n salva os dados extraídos no Google Sheets e devolve a resposta gerada para o frontend.

---

## ⚙️ Como executar localmente

### Pré-requisitos
- Python 3.9+
- Servidor n8n ativo com o workflow configurado.

### Passos

1. Clone o repositório.
2. Instale as dependências: `pip install -r requirements.txt`.
3. Execute a aplicação: `streamlit run app.py`.

---

## 👨‍💻 Autor

Desenvolvido por **Emmanuel**.
Projeto focado em automação de processos e integração de IA para otimização de fluxos comerciais.