# ⚡ Início Rápido - 5 Minutos

Guia ultrarrápido para colocar o bot funcionando.

## 🚀 Passo a Passo (Windows)

### 1. Instale Python
Baixe em: https://www.python.org/downloads/
✅ Marque "Add Python to PATH"

### 2. Execute o Instalador
```bash
# Duplo clique em:
install.bat
```
Aguarde a instalação das dependências.

### 3. Configure Credenciais

#### 3.1. Crie o Bot no Telegram
1. Abra Telegram
2. Busque: `@BotFather`
3. Envie: `/newbot`
4. Copie o **token**

#### 3.2. Descubra seu ID
1. Busque: `@userinfobot`
2. Envie: `/start`
3. Copie seu **ID**

#### 3.3. Configure o Grupo
1. Crie um grupo no Telegram
2. Adicione o bot como **administrador**
3. Dê permissões: Banir usuários, Convidar
4. Encaminhe mensagem do grupo para `@userinfobot`
5. Copie o **ID do grupo** (negativo, ex: -1001234567890)

#### 3.4. Configure Mercado Pago
1. Acesse: https://www.mercadopago.com.br/developers/panel
2. Crie aplicação
3. Copie **Access Token** de produção

#### 3.5. Crie arquivo .env
```bash
# Copie o exemplo
copy env.example .env

# Edite com Notepad
notepad .env
```

Cole suas credenciais:
```env
TELEGRAM_BOT_TOKEN=seu_token_aqui
ADMIN_USER_ID=seu_id_aqui
GROUP_ID=-1001234567890
MERCADO_PAGO_ACCESS_TOKEN=APP_USR-seu_token_aqui
PLANO_FOTOS_VALOR=29.90
PLANO_COMPLETO_VALOR=49.90
DIAS_AVISO_VENCIMENTO=3
DATABASE_URL=sqlite:///bot_vip.db
```

### 4. Teste
```bash
# Duplo clique em:
testar.bat
```

Deve mostrar:
```
✅ Bot conectado
✅ Mercado Pago configurado
✅ Banco de dados OK
✅ Grupo VIP encontrado
✅ Bot é administrador
```

### 5. Inicie o Bot
```bash
# Duplo clique em:
iniciar.bat
```

### 6. Teste no Telegram
1. Envie `/start` para o bot
2. Escolha um plano
3. Teste o pagamento

---

## 🐧 Linux/Mac

```bash
# 1. Clone o projeto
cd bot-telegram

# 2. Instale dependências
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. Configure
cp env.example .env
nano .env  # Edite com suas credenciais

# 4. Teste
python utils.py test

# 5. Inicie
python bot.py
```

---

## ✅ Checklist

- [ ] Python instalado
- [ ] Dependências instaladas (install.bat)
- [ ] Bot criado no @BotFather
- [ ] Grupo criado e bot adicionado como admin
- [ ] Mercado Pago configurado
- [ ] Arquivo .env criado e configurado
- [ ] Teste executado com sucesso
- [ ] Bot rodando

---

## 🎯 Próximos Passos

### Uso básico
- `/start` - Ver planos
- `/stats` - Estatísticas (admin)
- `/aprovar <id> <plano>` - Aprovar manual

### Aprenda mais
1. 📚 Leia `README.md` - Visão geral
2. 🔧 Leia `CONFIGURACAO.md` - Detalhes
3. ❓ Consulte `FAQ.md` - Dúvidas
4. 🚀 Veja `DEPLOY.md` - Produção

### Personalize
1. Valores dos planos (`.env`)
2. Mensagens (`config.py`)
3. Horários de verificação (`scheduler.py`)

---

## 🆘 Problemas?

### Bot não inicia
```bash
# Verifique o token
python utils.py test
```

### Pagamento não funciona
```bash
# Use modo teste do Mercado Pago primeiro
# Token de teste: TEST-xxx
```

### Mais ajuda
Consulte `FAQ.md` ou `CONFIGURACAO.md`

---

## 💡 Dicas

1. **Use token de TESTE primeiro**
   - Mercado Pago tem tokens de teste
   - Teste tudo antes de usar produção

2. **Faça backup**
   ```bash
   copy bot_vip.db backup.db
   ```

3. **Monitore os logs**
   - Deixe terminal aberto
   - Veja mensagens de erro

4. **Comece devagar**
   - Teste com poucos usuários
   - Aumente gradualmente

---

## 🎉 Pronto!

Seu bot está funcionando! 

Agora é só divulgar e começar a receber pagamentos! 💰

---

**Tempo estimado**: 5-10 minutos (se tiver tudo em mãos)

**Dificuldade**: ⭐⭐☆☆☆ (Fácil)

**Suporte**: Consulte a documentação completa
