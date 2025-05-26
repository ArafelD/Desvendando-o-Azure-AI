from flask import Flask, request, jsonify, render_template_string
from openai import AzureOpenAI
import os

# --- Configuração do Cliente Azure OpenAI ---
# Certifique-se de definir as variáveis de ambiente:
# AZURE_OPENAI_KEY: Sua chave de API do Azure OpenAI
# AZURE_OPENAI_ENDPOINT: Seu endpoint do Azure OpenAI
# AZURE_OPENAI_DEPLOYMENT_NAME: O nome da sua implantação de modelo (ex: gpt-4o-mini)
api_key = os.getenv("AZURE_OPENAI_KEY")
azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")

# Validação inicial das variáveis de ambiente
if not all([api_key, azure_endpoint, deployment_name]):
    print("ERRO CRÍTICO: Variáveis de ambiente AZURE_OPENAI_KEY, AZURE_OPENAI_ENDPOINT e AZURE_OPENAI_DEPLOYMENT_NAME devem ser definidas para iniciar a aplicação.")
    exit()

client = AzureOpenAI(
    api_key=api_key,
    api_version="2024-05-01-preview", # Verifique a versão mais recente suportada
    azure_endpoint=azure_endpoint
)

# --- Lógica do Chatbot ---
# Histórico de chat simplificado (em memória, reinicia com o servidor)
# Para produção, use um banco de dados ou gerenciamento de sessão
chat_history = {"default": [{"role": "system", "content": "Você é um assistente de IA prestativo e direto ao ponto."}]}

app = Flask(__name__)

@app.route('/')
def home():
    # Interface HTML básica para o chat
    return render_template_string('''
        <!doctype html>
        <html lang="pt-BR">
            <head>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <title>Azure AI Chatbot</title>
                <style>
                    body { font-family: sans-serif; margin: 20px; background-color: #f4f4f9; }
                    h1 { color: #0078D4; }
                    #chatbox { height: 400px; overflow-y: scroll; border: 1px solid #ccc; margin-bottom: 10px; padding: 10px; background-color: #fff; border-radius: 5px; }
                    #chatbox p { margin: 5px 0; }
                    #chatbox p b { color: #0078D4; }
                    #inputContainer { display: flex; }
                    #userInput { flex-grow: 1; padding: 10px; border: 1px solid #ccc; border-radius: 5px 0 0 5px; }
                    button { padding: 10px 15px; background-color: #0078D4; color: white; border: none; cursor: pointer; border-radius: 0 5px 5px 0; }
                    button:hover { background-color: #005a9e; }
                </style>
            </head>
            <body>
                <h1>Chatbot com Azure AI</h1>
                <div id="chatbox"><p><b>Chatbot:</b> Olá! Como posso ajudar?</p></div>
                <div id="inputContainer">
                    <input type="text" id="userInput" placeholder="Digite sua mensagem aqui..." autofocus>
                    <button onclick="sendMessage()">Enviar</button>
                </div>
                <script>
                    const chatbox = document.getElementById('chatbox');
                    const userInput = document.getElementById('userInput');

                    async function sendMessage() {
                        const userText = userInput.value.trim();
                        if (!userText) return;

                        appendMessage('Você', userText);
                        userInput.value = '';
                        userInput.disabled = true; // Desabilita input durante o processamento

                        try {
                            const response = await fetch('/chat', {
                                method: 'POST',
                                headers: {'Content-Type': 'application/json'},
                                body: JSON.stringify({ message: userText })
                            });
                            const data = await response.json();
                            appendMessage('Chatbot', data.reply);
                        } catch (error) {
                            console.error('Erro ao enviar mensagem:', error);
                            appendMessage('Chatbot', 'Desculpe, não consegui processar sua mensagem. Tente novamente.');
                        } finally {
                            userInput.disabled = false; // Reabilita input
                            userInput.focus();
                        }
                    }

                    function appendMessage(sender, text) {
                        const messageElement = document.createElement('p');
                        // Sanitiza o texto para evitar injeção de HTML (básico)
                        const sanitizedText = text.replace(/</g, "&lt;").replace(/>/g, "&gt;");
                        messageElement.innerHTML = `<b>${sender}:</b> ${sanitizedText}`;
                        chatbox.appendChild(messageElement);
                        chatbox.scrollTop = chatbox.scrollHeight; // Auto-scroll
                    }

                    userInput.addEventListener('keypress', function(e) {
                        if (e.key === 'Enter') {
                            sendMessage();
                        }
                    });
                </script>
            </body>
        </html>
    ''')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    if not user_input:
        return jsonify({'reply': 'Nenhuma mensagem recebida.'}), 400

    session_id = "default" # ID de sessão fixo para este exemplo simplificado

    # Garante que a sessão exista no histórico
    if session_id not in chat_history:
         chat_history[session_id] = [{"role": "system", "content": "Você é um assistente de IA prestativo e direto ao ponto."}]

    current_messages = chat_history[session_id]
    current_messages.append({"role": "user", "content": user_input})

    try:
        response = client.chat.completions.create(
            model=deployment_name,
            messages=current_messages,
            max_tokens=250, # Aumentado um pouco para respostas mais completas
            temperature=0.7
        )
        assistant_response = response.choices[0].message.content

        # Adiciona resposta ao histórico
        current_messages.append({"role": "assistant", "content": assistant_response})

        # Limita o tamanho do histórico para evitar exceder limites de token (estratégia simples)
        # Mantém a mensagem do sistema e as últimas N interações
        max_history_length = 10 # (System + 5 pares User/Assistant)
        if len(current_messages) > max_history_length:
             chat_history[session_id] = [current_messages[0]] + current_messages[-(max_history_length-1):]

        return jsonify({'reply': assistant_response})

    except Exception as e:
        print(f"Erro ao chamar a API do Azure OpenAI: {e}")
        # Remove a última mensagem do usuário do histórico em caso de erro na API
        if current_messages and current_messages[-1]["role"] == "user":
            current_messages.pop()
        return jsonify({'reply': 'Desculpe, ocorreu um erro interno ao processar sua solicitação.'}), 500

if __name__ == '__main__':
    print("Iniciando servidor Flask...")
    # Escuta em todas as interfaces de rede disponíveis na porta 5000
    app.run(debug=False, host='0.0.0.0', port=5000)

