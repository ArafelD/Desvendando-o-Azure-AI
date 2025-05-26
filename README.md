# Repositório: Artigo e Exemplo Prático - Azure AI

Este repositório contém o artigo completo "Desvendando o Azure AI: Da Concepção à Aplicação Prática" e o código-fonte do exemplo prático de chatbot desenvolvido com Python, Flask e Azure OpenAI Service.

## Conteúdo

- `artigo_azure_ai.md`: O artigo completo em formato Markdown, cobrindo:
    - Introdução ao Azure AI
    - O que é Azure AI (Serviços Cognitivos, Azure ML, AI Studio)
    - Como começar com Azure AI Studio sem código (com fluxograma)
    - Como construir uma aplicação com Azure AI e IA Generativa (exemplo com código Python/Flask)
    - Conclusão e CTA
    - Referências
- `images/`: Contém as imagens e fluxogramas utilizados no artigo.
    - `ai_azure_2025-05-26_20-42-00_9240.webp`: Captura de tela do portal Azure AI Foundry/Studio.
    - `learn_microsoft_2025-05-26_20-42-32_5008.webp`: Captura de tela da documentação do Web App do Azure OpenAI.
    - `flowchart_azure_ai_studio_no_code.png`: Fluxograma do processo sem código no AI Studio.
- `src/`: Contém o código-fonte da aplicação de exemplo.
    - `app.py`: Aplicação Flask do chatbot.
- `requirements.txt`: Dependências Python necessárias para executar a aplicação.
- `README.md`: Este arquivo.

## Como Executar o Exemplo Prático (Chatbot Flask)

1.  **Clone o Repositório:**
    ```bash
    git clone <URL_DO_SEU_REPOSITORIO>
    cd <NOME_DO_REPOSITORIO>
    ```

2.  **Crie um Ambiente Virtual (Recomendado):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/macOS
    # ou
    .\venv\Scripts\activate  # Windows
    ```

3.  **Instale as Dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure as Variáveis de Ambiente:**
    Você precisará de um recurso Azure OpenAI Service com um modelo implantado (ex: `gpt-4o-mini`). Defina as seguintes variáveis de ambiente no seu terminal:
    ```bash
    export AZURE_OPENAI_ENDPOINT="<SEU_ENDPOINT_AZURE_OPENAI>"
    export AZURE_OPENAI_KEY="<SUA_CHAVE_API_AZURE_OPENAI>"
    export AZURE_OPENAI_DEPLOYMENT_NAME="<NOME_DA_SUA_IMPLANTACAO>"
    ```
    (Use `set` em vez de `export` no Windows Command Prompt, ou `$env:` no PowerShell).

5.  **Execute a Aplicação Flask:**
    ```bash
    python src/app.py
    ```

6.  **Acesse o Chatbot:**
    Abra seu navegador e vá para `http://127.0.0.1:5000` (ou o endereço IP e porta exibidos no terminal).

## Referências Utilizadas no Artigo

- Documentação Azure OpenAI: [https://learn.microsoft.com/en-us/azure/ai-services/openai/](https://learn.microsoft.com/en-us/azure/ai-services/openai/)
- Portal Azure AI Foundry/Studio: [https://ai.azure.com/](https://ai.azure.com/)
- Documentação do Web App Azure OpenAI: [https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/use-web-app](https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/use-web-app)
- Documentação Geral Azure AI Services: [https://learn.microsoft.com/en-us/azure/ai-services/](https://learn.microsoft.com/en-us/azure/ai-services/)
- Biblioteca Python OpenAI: [https://github.com/openai/openai-python](https://github.com/openai/openai-python)

## Contribuições

Sinta-se à vontade para abrir issues ou pull requests para melhorias no artigo ou no código.
