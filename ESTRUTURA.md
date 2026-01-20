# 📁 Estrutura do Projeto

Visão completa de todos os arquivos e suas funções.

```
bot-telegram/
│
├── 📄 bot.py                      # Bot principal do Telegram
│   └── Comandos: /start, /stats, /aprovar
│   └── Gerencia interações com usuários
│   └── Botões inline para planos
│
├── ⚙️ config.py                   # Configurações centralizadas
│   └── Carrega variáveis do .env
│   └── Define planos e valores
│   └── Templates de mensagens
│
├── 💾 database.py                 # Gerenciamento do banco de dados
│   └── Models: Usuario, Pagamento
│   └── Funções CRUD
│   └── Queries de verificação
│
├── 💳 pagamentos.py               # Integração Mercado Pago
│   └── Criação de links de pagamento
│   └── Verificação de status
│   └── Processamento de webhooks
│
├── ⏰ scheduler.py                # Tarefas agendadas
│   └── Verificação de vencimentos (6h)
│   └── Envio de avisos (diário 10h)
│   └── Checagem de pagamentos (30min)
│
├── 🌐 webhook.py                  # Servidor webhook (opcional)
│   └── Recebe notificações do MP
│   └── Processa pagamentos em tempo real
│   └── Flask server na porta 5000
│
├── 🔧 utils.py                    # Utilitários e helpers
│   └── Descobrir IDs (telegram/grupo)
│   └── Testar configurações
│   └── Gerar relatórios
│
├── 📋 requirements.txt            # Dependências Python
│   └── python-telegram-bot
│   └── mercadopago
│   └── sqlalchemy
│   └── apscheduler
│   └── ...
│
├── 🔐 .env                        # Variáveis de ambiente (CRIAR)
│   └── TELEGRAM_BOT_TOKEN
│   └── MERCADO_PAGO_ACCESS_TOKEN
│   └── Valores dos planos
│   └── ⚠️ NUNCA commite este arquivo!
│
├── 📝 env.example                 # Exemplo de .env
│   └── Template para configuração
│   └── Copie para .env e edite
│
├── 🚫 .gitignore                  # Arquivos ignorados pelo Git
│   └── .env, *.db, __pycache__, etc
│
├── 🪟 install.bat                 # Instalador Windows
│   └── Cria ambiente virtual
│   └── Instala dependências
│
├── ▶️ iniciar.bat                 # Iniciar bot Windows
│   └── Ativa venv
│   └── Executa bot.py
│
├── 🧪 testar.bat                  # Testa configuração Windows
│   └── Verifica tokens
│   └── Testa conexões
│
├── 🐳 gunicorn_config.py          # Config Gunicorn (produção)
│   └── Workers, logging, timeout
│
├── 📚 README.md                   # Documentação principal
│   └── Overview do projeto
│   └── Funcionalidades
│   └── Guia rápido
│
├── 🔧 CONFIGURACAO.md             # Guia de configuração detalhado
│   └── Passo a passo completo
│   └── Criação de bot
│   └── Setup Mercado Pago
│   └── Descobrir IDs
│
├── 🚀 DEPLOY.md                   # Guia de deploy
│   └── Railway, Heroku, VPS
│   └── Configuração de webhook
│   └── Monitoramento
│
├── ❓ FAQ.md                      # Perguntas frequentes
│   └── Troubleshooting
│   └── Dúvidas comuns
│   └── Customizações
│
├── 📁 ESTRUTURA.md                # Este arquivo
│   └── Mapa do projeto
│   └── Descrição de arquivos
│
└── 💾 bot_vip.db                  # Banco SQLite (criado automaticamente)
    └── Tabela: usuarios
    └── Tabela: pagamentos
    └── ⚠️ Faça backup regularmente!
```

---

## 📂 Diretórios que serão criados

```
bot-telegram/
│
├── venv/                          # Ambiente virtual Python
│   └── Criado por install.bat
│   └── Contém todas as dependências
│   └── Não versionar no Git
│
├── logs/                          # Logs do sistema (opcional)
│   └── access.log
│   └── error.log
│   └── Criar se usar webhook em produção
│
└── backups/                       # Backups do banco (recomendado)
    └── bot_vip_20260120.db
    └── bot_vip_20260121.db
    └── Crie e configure backup automático
```

---

## 🔄 Fluxo de Dados

### 1. Usuário interage com bot
```
Usuário → Telegram → bot.py → database.py
                            → pagamentos.py → Mercado Pago
```

### 2. Processamento de pagamento
```
Mercado Pago → webhook.py → database.py → bot.py → Usuário
              (ou scheduler.py verifica periodicamente)
```

### 3. Verificações automáticas
```
scheduler.py → database.py → bot.py → Telegram
    ↓
⏰ A cada 6h: vencimentos
⏰ Diário 10h: avisos
⏰ A cada 30min: pagamentos
```

---

## 🎯 Arquivos por Função

### Core (Essenciais)
- `bot.py` - Coração do sistema
- `config.py` - Configurações
- `database.py` - Persistência
- `pagamentos.py` - Monetização
- `scheduler.py` - Automações

### Setup (Configuração inicial)
- `.env` - Credenciais
- `requirements.txt` - Dependências
- `install.bat` - Instalação Windows

### Execução (Uso diário)
- `iniciar.bat` - Rodar o bot
- `testar.bat` - Validar config
- `utils.py` - Ferramentas úteis

### Documentação (Referência)
- `README.md` - Visão geral
- `CONFIGURACAO.md` - Setup detalhado
- `DEPLOY.md` - Produção
- `FAQ.md` - Dúvidas
- `ESTRUTURA.md` - Este arquivo

### Opcional (Avançado)
- `webhook.py` - Pagamentos real-time
- `gunicorn_config.py` - Deploy produção

---

## 🔑 Arquivos Principais Explicados

### bot.py
```python
# Principais funções:
- start()               # Comando /start
- callback_handler()    # Botões inline
- admin_stats()         # Comando /stats
- verificar_pagamento_manual()  # /aprovar
- novo_membro()         # Controle de acesso
```

### database.py
```python
# Principais funções:
- init_db()             # Cria tabelas
- criar_usuario()       # Novo/atualiza usuário
- get_usuario()         # Busca usuário
- desativar_usuario()   # Remove acesso
- get_usuarios_vencidos()      # Lista vencidos
- get_usuarios_para_avisar()   # Lista para avisar
```

### pagamentos.py
```python
# Principais funções:
- criar_link_pagamento()   # Gera link MP
- verificar_pagamento()    # Checa status
- processar_webhook()      # Processa notificação
```

### scheduler.py
```python
# Principais funções:
- verificar_vencimentos()       # Remove vencidos
- enviar_avisos_vencimento()    # Notifica antes
- verificar_pagamentos_pendentes()  # Checa MP
```

---

## 📊 Tabelas do Banco de Dados

### usuarios
```sql
id              INTEGER PRIMARY KEY
telegram_id     INTEGER UNIQUE      # ID do Telegram
username        TEXT                # @username
nome            TEXT                # Nome completo
plano           TEXT                # 'fotos' ou 'completo'
data_inicio     DATETIME            # Quando assinou
data_vencimento DATETIME            # Quando vence
ativo           BOOLEAN             # Ativo/inativo
aviso_enviado   BOOLEAN             # Aviso já enviado?
```

### pagamentos
```sql
id              INTEGER PRIMARY KEY
telegram_id     INTEGER             # ID do usuário
plano           TEXT                # Plano escolhido
valor           REAL                # Valor pago
payment_id      TEXT UNIQUE         # ID do Mercado Pago
status          TEXT                # pending/approved/rejected
data_criacao    DATETIME            # Quando criou
data_aprovacao  DATETIME            # Quando aprovou
```

---

## 🔐 Segurança dos Arquivos

### NUNCA compartilhe:
- ❌ `.env` - Contém tokens secretos
- ❌ `bot_vip.db` - Dados dos usuários
- ❌ Qualquer arquivo com credenciais

### Pode compartilhar:
- ✅ `bot.py` e demais `.py` (código)
- ✅ `requirements.txt`
- ✅ `env.example` (template)
- ✅ Arquivos `.md` (documentação)

### Configure .gitignore:
```gitignore
.env
*.db
*.sqlite
__pycache__/
venv/
```

---

## 🛠️ Ordem de Uso/Modificação

### Primeira vez:
1. `install.bat` - Instala tudo
2. `env.example` → `.env` - Configura
3. `testar.bat` - Valida
4. `iniciar.bat` - Roda!

### Customizações comuns:
1. `config.py` - Alterar mensagens/valores
2. `bot.py` - Adicionar comandos
3. `database.py` - Novos campos/tabelas
4. `scheduler.py` - Ajustar horários

### Deploy:
1. Escolha plataforma (DEPLOY.md)
2. Configure webhook (se aplicável)
3. Configure variáveis de ambiente
4. Execute e monitore

---

## 📖 Para Estudar o Código

### Iniciante:
1. Leia `README.md`
2. Execute `install.bat`
3. Siga `CONFIGURACAO.md`
4. Rode o bot e teste

### Intermediário:
1. Estude `bot.py` - lógica principal
2. Entenda `database.py` - dados
3. Veja `scheduler.py` - automações
4. Customize `config.py`

### Avançado:
1. Implemente webhook (`webhook.py`)
2. Migre para PostgreSQL
3. Adicione novos planos
4. Crie sistema de cupons
5. Deploy em produção

---

## 🎓 Recursos para Aprender

### Telegram Bots:
- [Documentação Oficial](https://core.telegram.org/bots)
- [python-telegram-bot](https://docs.python-telegram-bot.org/)

### Mercado Pago:
- [Developer Docs](https://www.mercadopago.com.br/developers)
- [SDK Python](https://github.com/mercadopago/sdk-python)

### Python:
- [SQLAlchemy](https://docs.sqlalchemy.org/)
- [APScheduler](https://apscheduler.readthedocs.io/)

---

Estrutura limpa, modular e fácil de manter! 🚀
