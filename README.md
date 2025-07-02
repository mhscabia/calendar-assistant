# Calendar Assistant

Um assistente automatizado que lê seus eventos do Google Calendar e envia um resumo diário via WhatsApp usando a API do Twilio.

## Funcionalidades

- Autentica com o Google Calendar (OAuth2)
- Filtra calendários indesejados
- Busca eventos do dia atual
- Envia resumo dos eventos via WhatsApp usando Twilio

## Pré-requisitos

- Python 3.8+
- Conta no Google Cloud com API do Google Calendar habilitada
- Conta Twilio com acesso ao WhatsApp Sandbox

## Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/calendar-assistant.git
   cd calendar-assistant
   ```
2. Crie e ative um ambiente virtual (opcional, mas recomendado):
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate    # Windows
   ```
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

## Configuração

1. **Google Calendar**

   - Crie um projeto no [Google Cloud Console](https://console.cloud.google.com/)
   - Ative a API do Google Calendar
   - Gere um arquivo `credentials.json` e coloque em `credentials/credentials.json`

2. **Twilio**

   - Crie uma conta em [twilio.com](https://www.twilio.com/)
   - Ative o Sandbox do WhatsApp
   - Defina as variáveis de ambiente:
     - `TWILIO_ACOUNT_ID` (SID da conta Twilio)
     - `TWILIO_AUTH_TOKEN` (Auth Token da conta Twilio)
     - `TWILIO_NUMBER_FROM` (número do WhatsApp do Sandbox, formato: 'whatsapp:+14155238886')
     - `TWILIO_NUMBER_TO` (seu número do WhatsApp, formato: 'whatsapp:+55XXXXXXXXX')

   Exemplo (Linux/macOS):

   ```bash
   export TWILIO_ACOUNT_ID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   export TWILIO_AUTH_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   export TWILIO_NUMBER_FROM='whatsapp:+14155238886'
   export TWILIO_NUMBER_TO='whatsapp:+55XXXXXXXXX'
   ```

## Uso

Execute o assistente:

```bash
python src/main.py
```

Na primeira execução, será solicitado autenticar com sua conta Google.

## Estrutura do Projeto

```
calendar-assistant/
├── credentials/           # Coloque aqui o credentials.json do Google
├── src/
│   ├── main.py            # Script principal
│   └── services/
│       └── twilio.py      # Serviço de envio via Twilio
├── requirements.txt
└── README.md
```

## Licença

Este projeto está sob a licença MIT. Sinta-se livre para usar, modificar e contribuir!
