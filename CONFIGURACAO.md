# 🔧 Guia de Configuração Completo

Este guia detalha todas as etapas para configurar e usar o bot.

## 📋 Índice

1. [Instalação](#instalação)
2. [Configuração do Bot Telegram](#configuração-do-bot-telegram)
3. [Configuração do Mercado Pago](#configuração-do-mercado-pago)
4. [Descobrindo IDs](#descobrindo-ids)
5. [Testando o Bot](#testando-o-bot)
6. [Uso Diário](#uso-diário)

---

## 1️⃣ Instalação

### Windows

1. **Baixe e instale Python**
   - Acesse: https://www.python.org/downloads/
   - Baixe a versão mais recente
   - ⚠️ **IMPORTANTE**: Marque "Add Python to PATH" durante instalação

2. **Execute o instalador**
   ```bash
   # Duplo clique em:
   install.bat
   ```

3. **Configure as credenciais**
   ```bash
   # Copie o arquivo de exemplo
   copy env.example .env
   
   # Edite com Notepad
   notepad .env
   ```

### Linux/Mac

```bash
# Clone ou baixe o projeto
cd bot-telegram

# Crie ambiente virtual
python3 -m venv venv

# Ative o ambiente
source venv/bin/activate  # Linux/Mac

# Instale dependências
pip install -r requirements.txt

# Configure credenciais
cp env.example .env
nano .env  # ou vim, code, etc.
```

---

## 2️⃣ Configuração do Bot Telegram

### Passo 1: Criar o Bot

1. Abra o Telegram
2. Busque por: `@BotFather`
3. Envie: `/newbot`
4. Escolha um nome: `Meu Bot VIP`
5. Escolha um username: `meubotvip_bot` (deve terminar em \_bot)
6. **Copie o token** fornecido (algo como: `1234567890:ABCdef...`)

### Passo 2: Configurar o Bot

Envie os seguintes comandos para o @BotFather:

```
/setdescription
# Cole a descrição do seu bot

/setabouttext
# Cole informações sobre o bot

/setuserpic
# Envie uma foto para o bot

/setcommands
# Cole:
start - Iniciar bot e ver planos
minha - Ver minha assinatura
ajuda - Ajuda e suporte
```

### Passo 3: Adicionar Token no .env

Edite o arquivo `.env`:
```env
TELEGRAM_BOT_TOKEN=1234567890:ABCdef_seu_token_aqui
```

---

## 3️⃣ Configuração do Mercado Pago

### Passo 1: Criar Conta

1. Acesse: https://www.mercadopago.com.br
2. Crie uma conta ou faça login
3. Complete seu cadastro (necessário para receber pagamentos)

### Passo 2: Criar Aplicação

1. Acesse: https://www.mercadopago.com.br/developers/panel
2. Faça login
3. Vá em **"Suas integrações"** ou **"Suas aplicações"**
4. Clique em **"Criar aplicação"**
5. Escolha um nome: `Bot VIP Telegram`
6. Selecione: **"Pagamentos online"**

### Passo 3: Obter Access Token

1. Na aplicação criada, vá em **"Credenciais"**
2. Escolha **"Credenciais de produção"**
3. Copie o **"Access Token"** (começa com `APP_USR-...`)

⚠️ **IMPORTANTE**: 
- Use o token de **PRODUÇÃO** (não de teste)
- Nunca compartilhe este token
- Para testar, use o token de teste primeiro

### Passo 4: Adicionar no .env

```env
MERCADO_PAGO_ACCESS_TOKEN=APP_USR-seu_token_aqui
```

### Configurações Recomendadas no Mercado Pago

1. **Ative notificações instantâneas**:
   - Painel > Suas integrações > Notificações
   - Configure URL do webhook (se tiver servidor)

2. **Configure taxas**:
   - Verifique as taxas do Mercado Pago
   - Ajuste os valores dos planos considerando as taxas

---

## 4️⃣ Descobrindo IDs

### Seu ID do Telegram (ADMIN_USER_ID)

**Método 1: Usando bot pronto**
1. Busque no Telegram: `@userinfobot`
2. Envie `/start`
3. Copie o **"Id"** mostrado

**Método 2: Usando utilitário**
```bash
# Windows
venv\Scripts\activate.bat
python utils.py getid SEU_BOT_TOKEN

# Linux/Mac
source venv/bin/activate
python utils.py getid SEU_BOT_TOKEN
```
Envie `/start` para o bot e veja seu ID.

### ID do Grupo VIP (GROUP_ID)

**Método 1: Encaminhar mensagem**
1. Envie uma mensagem no grupo
2. Encaminhe para `@userinfobot`
3. Copie o ID (será negativo, tipo: `-1001234567890`)

**Método 2: Usando utilitário**
```bash
# Ative o ambiente
venv\Scripts\activate.bat  # Windows
source venv/bin/activate   # Linux/Mac

# Execute
python utils.py getchat SEU_BOT_TOKEN

# Envie uma mensagem no grupo
# O ID será exibido
```

**Método 3: Adicionar bot ao grupo temporariamente**
1. Adicione o bot ao grupo
2. Execute o bot normalmente
3. Envie uma mensagem no grupo
4. Veja o ID nos logs

### Configurar IDs no .env

```env
ADMIN_USER_ID=123456789
GROUP_ID=-1001234567890
```

---

## 5️⃣ Testando o Bot

### Antes de Iniciar

Execute o teste de configuração:

```bash
# Windows
testar.bat

# Linux/Mac
source venv/bin/activate
python utils.py test
```

Você deve ver:
```
✅ Bot conectado: @seu_bot
✅ Mercado Pago configurado
✅ Banco de dados OK
✅ Grupo VIP encontrado: Nome do Grupo
✅ Bot é administrador do grupo
```

### Se houver erros:

**❌ Erro ao conectar bot**
- Verifique o TELEGRAM_BOT_TOKEN
- Certifique-se que copiou todo o token

**❌ Erro no Mercado Pago**
- Verifique o MERCADO_PAGO_ACCESS_TOKEN
- Use o token de PRODUÇÃO (começa com APP_USR-)

**⚠️ Bot NÃO é administrador**
1. Adicione o bot ao grupo como administrador
2. Dê as seguintes permissões:
   - ✅ Banir usuários
   - ✅ Convidar usuários via link
   - ✅ Outras permissões de mensagens (opcional)

---

## 6️⃣ Uso Diário

### Iniciar o Bot

```bash
# Windows
iniciar.bat

# Linux/Mac
source venv/bin/activate
python bot.py
```

O bot ficará rodando e mostrará logs:
```
✅ Banco de dados inicializado!
⏰ Agendador de tarefas iniciado!
🤖 Bot iniciado!
```

### Comandos do Bot

**Para usuários:**
- `/start` - Ver planos e assinar

**Para admin (você):**
- `/stats` - Ver estatísticas
- `/aprovar <telegram_id> <plano>` - Aprovar pagamento manual

**Exemplos de uso admin:**
```
/stats
/aprovar 123456789 fotos
/aprovar 987654321 completo
```

### Fluxo do Usuário

1. Usuário envia `/start` para o bot
2. Bot mostra opções de planos
3. Usuário escolhe um plano
4. Bot gera link de pagamento do Mercado Pago
5. Usuário paga
6. Bot detecta pagamento (pode levar alguns minutos)
7. Bot envia link de convite para o grupo
8. Usuário entra no grupo VIP

### Monitoramento

O bot automaticamente:
- ✅ Verifica vencimentos a cada 6 horas
- ✅ Envia avisos 3 dias antes do vencimento às 10h
- ✅ Remove usuários vencidos do grupo
- ✅ Verifica pagamentos pendentes a cada 30 minutos

---

## 🔧 Configurações Avançadas

### Alterar Valores dos Planos

Edite o `.env`:
```env
PLANO_FOTOS_VALOR=29.90
PLANO_COMPLETO_VALOR=49.90
```

### Alterar Dias de Aviso

```env
DIAS_AVISO_VENCIMENTO=3  # Padrão: 3 dias antes
```

### Personalizar Mensagens

Edite `config.py` e altere as variáveis:
- `MENSAGEM_BEM_VINDO`
- `MENSAGEM_PAGAMENTO_APROVADO`
- `MENSAGEM_AVISO_VENCIMENTO`
- `MENSAGEM_VENCIDO`

---

## 📊 Relatórios

### Gerar Relatório Mensal

```bash
# Windows
venv\Scripts\activate.bat
python utils.py relatorio

# Linux/Mac
source venv/bin/activate
python utils.py relatorio
```

Mostrará:
- Novos usuários do mês
- Usuários ativos
- Distribuição por plano
- Receita total
- Receita média por pagamento

---

## 🆘 Problemas Comuns

### "Bot não responde"
- Verifique se está rodando (logs ativos)
- Teste com `/start`
- Verifique o token

### "Pagamento não é detectado"
- Pode levar até 30 minutos
- Verifique se usou token de PRODUÇÃO
- Use `/aprovar` para aprovar manualmente

### "Usuário não consegue entrar no grupo"
- Verifique se bot é admin
- Verifique se grupo é privado
- Envie link de convite manualmente

### "Usuário vencido não foi removido"
- Aguarde verificação (a cada 6h)
- Verifique logs
- Remova manualmente se necessário

---

## 📞 Próximos Passos

1. ✅ Configure todas as credenciais
2. ✅ Teste o bot
3. ✅ Faça um pagamento de teste
4. ✅ Monitore os logs
5. 🚀 Lance seu grupo VIP!

**Dica**: Use o token de TESTE do Mercado Pago primeiro para testar tudo antes de usar o de produção.

---

Precisa de ajuda? Revise os logs e a documentação!
