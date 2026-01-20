# 🤖 Bot VIP Telegram - Gerenciador de Assinaturas

Bot completo para gerenciamento de grupos VIP no Telegram com sistema de pagamentos recorrentes via Mercado Pago.

## 🚀 Funcionalidades

### Para Usuários
- ✅ Dois planos de assinatura (Fotos e Completo)
- 💳 Pagamento integrado com Mercado Pago
- 🔔 Notificações automáticas 3 dias antes do vencimento
- 📊 Consulta de status da assinatura
- 🔄 Renovação facilitada

### Para Administradores
- 📈 Estatísticas completas do bot
- 👤 Aprovação manual de pagamentos
- 🛡️ Remoção automática de usuários vencidos
- 📋 Logs detalhados

### Automações
- ⏰ Verificação de vencimentos a cada 6 horas
- 📧 Avisos de vencimento diários às 10h
- 💰 Verificação de pagamentos a cada 30 minutos
- 🚫 Remoção automática de membros vencidos

## 📋 Pré-requisitos

- Python 3.8+
- Conta no Telegram Bot (via @BotFather)
- Conta no Mercado Pago (com Access Token)
- Grupo VIP criado no Telegram

## 🔧 Instalação

### 1. Clone ou baixe o projeto

```bash
cd bot-telegram
```

### 2. Crie um ambiente virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

Copie o arquivo `.env.example` para `.env`:

```bash
copy .env.example .env  # Windows
cp .env.example .env    # Linux/Mac
```

Edite o arquivo `.env` com suas credenciais:

```env
# Token do bot (@BotFather)
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz

# Seu ID do Telegram (use @userinfobot para descobrir)
ADMIN_USER_ID=123456789

# ID do Grupo VIP (adicione o bot como admin e use um comando para pegar o ID)
GROUP_ID=-1001234567890

# Access Token do Mercado Pago
MERCADO_PAGO_ACCESS_TOKEN=APP_USR-xxxx

# Valores dos planos
PLANO_FOTOS_VALOR=29.90
PLANO_COMPLETO_VALOR=49.90
```

## 🎯 Como Configurar

### 1. Criar o Bot no Telegram

1. Abra o Telegram e busque por `@BotFather`
2. Envie `/newbot` e siga as instruções
3. Copie o token fornecido
4. Configure o bot:
   - `/setdescription` - Descrição do bot
   - `/setabouttext` - Texto sobre o bot
   - `/setuserpic` - Foto do bot

### 2. Criar o Grupo VIP

1. Crie um grupo no Telegram
2. Adicione o bot como administrador
3. Dê permissões para:
   - Banir usuários
   - Convidar usuários via link
4. Para pegar o ID do grupo:
   - Encaminhe uma mensagem do grupo para `@userinfobot`
   - Copie o ID (será algo como `-1001234567890`)

### 3. Configurar Mercado Pago

1. Acesse [developers.mercadopago.com](https://developers.mercadopago.com)
2. Crie uma aplicação
3. Copie o **Access Token** de produção
4. Cole no arquivo `.env`

### 4. Configurar Webhook (Opcional)

Para receber notificações automáticas de pagamento, você precisa de um servidor com HTTPS:

1. Use serviços como:
   - Heroku
   - Railway
   - DigitalOcean
   - Ngrok (para testes)

2. Configure a URL do webhook no arquivo `pagamentos.py`:
   ```python
   "notification_url": "https://seu-dominio.com/webhook"
   ```

## 🚀 Executando o Bot

```bash
python bot.py
```

O bot estará rodando e pronto para uso!

## 📱 Comandos Disponíveis

### Para Usuários
- `/start` - Inicia o bot e mostra os planos
- Botões interativos para:
  - Ver planos
  - Verificar assinatura
  - Renovar assinatura

### Para Administradores
- `/stats` - Estatísticas do bot
- `/aprovar <telegram_id> <plano>` - Aprovar pagamento manualmente
  - Exemplo: `/aprovar 123456789 fotos`

## 🗂️ Estrutura do Projeto

```
bot-telegram/
│
├── bot.py              # Bot principal
├── config.py           # Configurações
├── database.py         # Gerenciamento do banco de dados
├── pagamentos.py       # Integração com Mercado Pago
├── scheduler.py        # Tarefas automáticas
├── requirements.txt    # Dependências
├── .env               # Variáveis de ambiente (não versionar!)
├── .env.example       # Exemplo de variáveis
└── README.md          # Este arquivo
```

## 💾 Banco de Dados

O bot usa SQLite por padrão. Os dados são armazenados em `bot_vip.db`.

### Tabelas:
- `usuarios` - Informações dos assinantes
- `pagamentos` - Histórico de pagamentos

## 🔐 Segurança

⚠️ **IMPORTANTE:**
- Nunca compartilhe o arquivo `.env`
- Mantenha os tokens seguros
- Use `.gitignore` para não versionar informações sensíveis
- Adicione o bot ao grupo apenas como administrador necessário

## 🛠️ Manutenção

### Backup do Banco de Dados
```bash
# Faça backup regularmente
copy bot_vip.db bot_vip_backup.db
```

### Logs
Os logs são exibidos no console. Para salvar em arquivo:
```python
# No início do bot.py, adicione:
logging.basicConfig(
    filename='bot.log',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
```

## 🐛 Troubleshooting

### Bot não inicia
- Verifique se o token está correto
- Confirme que todas as dependências foram instaladas
- Verifique os logs de erro

### Pagamentos não são detectados
- Confirme que o Access Token do Mercado Pago está correto
- Verifique se está usando o token de **produção**
- Configure o webhook para notificações em tempo real

### Usuários não são removidos
- Verifique se o bot é administrador do grupo
- Confirme que tem permissão para banir usuários
- Verifique os logs do agendador

## 📞 Suporte

Para dúvidas ou problemas:
1. Verifique os logs do bot
2. Consulte a documentação do Telegram Bot API
3. Consulte a documentação do Mercado Pago

## 📄 Licença

Este projeto é fornecido como está, para uso pessoal.

## ⚖️ Aviso Legal

Este bot é uma ferramenta para gerenciamento de grupos. Certifique-se de:
- Cumprir os Termos de Serviço do Telegram
- Cumprir as políticas do Mercado Pago
- Respeitar as leis locais sobre comércio eletrônico
- Fornecer termos de uso claros aos seus clientes

---

Desenvolvido com ❤️ usando Python e python-telegram-bot
