# 📦 Embalagio IA - Atendimento & CRM Automatizado

<div align="center">
  <img src="logo_embalagio.png" alt="Embalagio Logo" width="200"/>
  <br/><br/>
  <a href="https://embalagio-atendimento.streamlit.app/" target="_blank">
    <img src="https://img.shields.io/badge/🟢_Live_Demo-Acessar_Aplicação-FF6A00?style=for-the-badge&logo=streamlit&logoColor=white" alt="Live Demo">
  </a>
</div>

<br/>

Este projeto é um **Portal de Atendimento Inteligente** desenvolvido para automatizar a triagem de leads da franquia Embalagio. Utilizando Inteligência Artificial Generativa, o sistema interpreta mensagens não-estruturadas de clientes (simulando WhatsApp), extrai dados críticos de vendas e os cadastra automaticamente em um CRM na nuvem, fornecendo respostas humanizadas em tempo real.

![Diagrama de Arquitetura Técnica n8n](workflow_n8n.png)

## 🎯 O Problema que este projeto resolve
Em operações de franquias ou delivery, a equipe comercial perde muito tempo interpretando áudios ou mensagens longas para extrair manualmente quantidades, tamanhos e intenções de compra para o sistema. Esta automação elimina essa fricção, garantindo:
- **Zero perda de leads:** Todo pedido válido é registrado instantaneamente.
- **Triagem Inteligente (Anti-Trash):** Solicitações fora do catálogo (ex: consertos, produtos não relacionados) são bloqueadas antes de poluírem o banco de dados.
- **Dados Estruturados:** O time de vendas recebe uma planilha limpa apenas com os leads quentes (Nome, Categoria centralizada e Resumo detalhado do Pedido).

---

## 🚀 Funcionalidades Principais

- **💬 Interface Chatbot:** Painel Streamlit responsivo com simulação de ambiente de chat.
- **🤖 Motor Cognitivo (Qwen 32B):** Compreensão avançada de linguagem natural e extração em formato JSON, rodando na infraestrutura de ultra-baixa latência da Groq.
- **📊 CRM Sincronizado:** Embed nativo do Google Sheets no painel para acompanhamento em tempo real.
- **🛡️ Trava de Segurança Operacional:** Protocolo automatizado que pausa o fluxo e exige confirmação explícita humana para pedidos com volume superior a 1000 unidades.
- **🟢 Health Check Integrado:** Monitoramento contínuo do status do backend n8n (Online/Offline) direto no frontend.

---

## 🛠️ Arquitetura e Stack Tecnológico

A solução foi construída utilizando uma arquitetura baseada em microsserviços, separando a interface do motor de automação:

### 1. Frontend (Interface de Atendimento)
- **Framework:** [Streamlit](https://streamlit.io/) (Python).
- **Hospedagem:** Streamlit Community Cloud.
- **Características:** UI/UX moderna (Dark Theme customizado) e envio assíncrono de payloads via REST API.

### 2. Backend & Orquestração (n8n + PostgreSQL)
- **Plataforma:** [n8n](https://n8n.io/) executado em container Docker.
- **Infraestrutura/Hospedagem:** [Railway](https://railway.app/).
- **Alta Disponibilidade:** Diferente de configurações locais (`sqlite`), o n8n está rodando acoplado a um banco de dados **PostgreSQL** provisionado no Railway, garantindo persistência robusta, escalabilidade e prontidão para ambiente de produção.

### 3. Inteligência Artificial (LLM)
- **Modelo:** `Qwen 32B` (Qwen3-32B). Escolhido por sua excelência em seguir instruções rígidas e gerar saídas estritamente em JSON sem alucinações de formatação.
- **Provedor:** API da [Groq](https://groq.com/) para inferência em tempo real.

### 4. Banco de Dados / CRM
- Integração nativa com a **Google Sheets API** para o registro e armazenamento dos leads qualificados.

---

## ⚙️ Como executar localmente

Para rodar a interface Streamlit na sua máquina e conectá-la a um backend n8n ativo:

### Pré-requisitos
- Python 3.9+
- Servidor n8n rodando com o workflow configurado (importe o arquivo `workflow_embalagio-ai.json` incluído neste repositório).

### Passos

1. **Clone o repositório:**
   ```
   git clone [https://github.com/kubiszevski/embalagio-atendimento.git](https://github.com/kubiszevski/embalagio-atendimento.git)
   cd embalagio-atendimento
   ```

2. **Configure as Variáveis de Ambiente:**
Crie um arquivo .env na raiz do projeto com as seguintes chaves:
```
GROQ_API_KEY=sua_chave_api_da_groq_aqui
WEBHOOK_URL=url_de_producao_do_seu_webhook_n8n
```

3. **Instale as dependências:**
pip install -r requirements.txt

4. **Inicie a aplicação:**
streamlit run app.py

👨‍💻 Autor
Desenvolvido por Emmanuel.
Engenharia de Prompts e Automação de Processos focado em otimização de fluxos comerciais.

## 👨‍💻 Autor
Desenvolvido por Emmanuel.
Engenharia de Prompts e Automação de Processos focado em otimização de fluxos comerciais.