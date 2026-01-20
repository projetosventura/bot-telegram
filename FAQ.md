# ❓ Perguntas Frequentes (FAQ)

## 📱 Sobre o Bot

### O que este bot faz?
Gerencia assinaturas de um grupo VIP no Telegram com pagamentos automatizados via Mercado Pago. Inclui:
- Sistema de planos (Fotos e Completo)
- Pagamentos recorrentes
- Notificações de vencimento
- Remoção automática de inadimplentes

### Quanto custa manter o bot rodando?
- **Grátis**: Se usar Railway, Heroku (tier free) ou rodar no seu PC
- **Pago**: VPS a partir de R$ 20/mês (DigitalOcean, AWS)
- **Taxas Mercado Pago**: ~4.99% + R$ 0,49 por transação

### Preciso de um servidor?
Não necessariamente:
- **Sem servidor**: Use Railway ou Heroku (grátis)
- **Com servidor**: Melhor desempenho e controle total
- **PC local**: Funciona, mas precisa ficar ligado 24/7

---

## 💰 Pagamentos

### Quais formas de pagamento são aceitas?
Todas as aceitas pelo Mercado Pago:
- Cartão de crédito
- Pix
- Boleto bancário
- Saldo Mercado Pago

### O bot renova automaticamente?
**Não**. O sistema atual:
1. Usuário paga mês a mês
2. Bot avisa 3 dias antes do vencimento
3. Se não renovar, é removido do grupo

Para pagamentos recorrentes verdadeiros, seria necessário:
- Implementar assinaturas do Mercado Pago
- Salvar dados de cartão (PCI compliance)

### Quando o pagamento é detectado?
- **Com webhook**: Instantâneo (segundos)
- **Sem webhook**: Até 30 minutos (verificação automática)
- **Manual**: Imediato (comando `/aprovar`)

### Como reembolsar um cliente?
1. Acesse o painel do Mercado Pago
2. Encontre a transação
3. Clique em "Devolver pagamento"
4. Use `/aprovar telegram_id plano` se ele quiser continuar

---

## 👥 Usuários e Grupos

### Quantos usuários o bot suporta?
Não há limite técnico. O SQLite aguenta milhares de usuários. Para escala maior (10k+):
- Migre para PostgreSQL ou MySQL
- Use servidor mais robusto

### Posso ter múltiplos grupos?
Sim, mas precisaria modificar o código:
1. Adicionar campo `grupo_id` no banco
2. Modificar lógica de adição/remoção
3. Criar planos específicos por grupo

### Como importar membros existentes?
Use o comando `/aprovar` para cada um:
```bash
/aprovar 123456789 completo
/aprovar 987654321 fotos
```

Ou crie um script:
```python
# import_users.py
usuarios = [
    (123456789, 'completo'),
    (987654321, 'fotos'),
    # ...
]

for telegram_id, plano in usuarios:
    database.criar_usuario(telegram_id, None, None, plano, 30)
```

### Usuário não consegue entrar no grupo. O que fazer?
1. Verifique se bot é administrador
2. Gere link manualmente:
   - Telegram: Adicionar membros > Criar link
   - Envie para o usuário
3. Verifique se grupo não está cheio (limite: 200k membros)

---

## 🔧 Configuração

### Como descobrir meu Telegram ID?
```bash
# Método 1: Use bot pronto
@userinfobot

# Método 2: Use utilitário
python utils.py getid SEU_BOT_TOKEN
```

### Como descobrir ID do grupo?
```bash
# Método 1: Encaminhe mensagem do grupo para
@userinfobot

# Método 2: Use utilitário
python utils.py getchat SEU_BOT_TOKEN
```

### Posso mudar os valores dos planos depois?
Sim! Edite o `.env`:
```env
PLANO_FOTOS_VALOR=39.90
PLANO_COMPLETO_VALOR=59.90
```

Reinicie o bot. Usuários ativos mantêm o plano anterior até renovar.

### Como personalizar as mensagens?
Edite `config.py`:
```python
MENSAGEM_BEM_VINDO = """
Sua mensagem personalizada aqui
"""
```

---

## 🐛 Problemas e Soluções

### "Bot não responde aos comandos"
**Causas comuns:**
- Bot não está rodando
- Token incorreto
- Bot bloqueado pelo usuário

**Soluções:**
1. Verifique se bot está ativo (logs)
2. Teste `/start` você mesmo
3. Reinicie o bot

### "Pagamento aprovado mas não liberou acesso"
**Causas:**
- Verificação ainda não rodou (aguarde até 30min)
- Token do Mercado Pago incorreto
- Erro nos logs

**Soluções:**
1. Verifique logs para erros
2. Aprove manualmente: `/aprovar telegram_id plano`
3. Verifique se usou token de PRODUÇÃO

### "Usuário vencido não foi removido"
**Causas:**
- Verificação roda a cada 6h
- Bot não é admin do grupo
- Usuário já saiu

**Soluções:**
1. Aguarde próxima verificação
2. Remova manualmente do grupo
3. Verifique permissões do bot

### "ImportError: No module named 'telegram'"
**Causa:** Dependências não instaladas

**Solução:**
```bash
venv\Scripts\activate.bat  # Windows
source venv/bin/activate   # Linux
pip install -r requirements.txt
```

### "Database is locked"
**Causa:** SQLite não suporta muitas escritas simultâneas

**Soluções:**
1. Reinicie o bot
2. Para muitos usuários, migre para PostgreSQL:
```python
# Em .env
DATABASE_URL=postgresql://user:pass@localhost/dbname
```

---

## 📊 Estatísticas e Relatórios

### Como ver estatísticas?
Use o comando `/stats` (apenas admin):
```
/stats
```

Mostra:
- Total de usuários
- Usuários ativos
- Distribuição por plano
- Pagamentos aprovados

### Como gerar relatório mensal?
```bash
python utils.py relatorio
```

### Onde ficam os dados?
No arquivo `bot_vip.db` (SQLite)

**IMPORTANTE**: Faça backup regularmente!
```bash
# Windows
copy bot_vip.db backups\bot_vip_%date%.db

# Linux
cp bot_vip.db backups/bot_vip_$(date +%Y%m%d).db
```

---

## 🔒 Segurança

### É seguro salvar dados de pagamento?
**Não salvamos dados sensíveis**:
- ✅ Salvamos: IDs, valores, status
- ❌ NÃO salvamos: Números de cartão, CVV, senhas

Tudo via Mercado Pago (PCI compliance).

### Alguém pode hackear o bot?
**Proteções implementadas:**
- Comandos admin restritos por ID
- Tokens em variáveis de ambiente
- Sem exposição de dados sensíveis

**Boas práticas:**
- Nunca compartilhe o `.env`
- Use HTTPS para webhook
- Mantenha tokens seguros
- Atualize dependências regularmente

### Como proteger o arquivo .env?
```bash
# Nunca commite para Git
echo ".env" >> .gitignore

# Permissões restritas (Linux)
chmod 600 .env

# Backup criptografado
zip -e backup.zip .env
```

---

## 🚀 Melhorias e Customizações

### Como adicionar mais planos?
1. Edite `config.py`:
```python
PLANO_PREMIUM = {
    'nome': 'Plano Premium',
    'valor': 99.90,
    'duracao_dias': 30,
    'tipo': 'premium'
}
```

2. Adicione botão em `bot.py`:
```python
[InlineKeyboardButton("🌟 Premium - R$ 99.90", 
                     callback_data='plano_premium')]
```

3. Adicione handler no callback

### Como adicionar cupons de desconto?
Adicione tabela no `database.py`:
```python
class Cupom(Base):
    __tablename__ = 'cupons'
    codigo = Column(String, primary_key=True)
    desconto = Column(Float)  # Percentual
    valido = Column(Boolean, default=True)
```

Implemente validação antes do pagamento.

### Como fazer assinatura anual?
Edite `config.py`:
```python
PLANO_ANUAL = {
    'nome': 'Plano Anual',
    'valor': 299.90,
    'duracao_dias': 365,
    'tipo': 'completo'
}
```

### Como adicionar múltiplos grupos?
Modifique `database.py`:
```python
class Usuario(Base):
    # ...
    grupo_id = Column(Integer, nullable=False)
```

Modifique lógica em `bot.py` e `scheduler.py`.

---

## 📞 Deploy e Produção

### Qual a melhor plataforma para deploy?
**Para iniciantes:**
- Railway (mais fácil, grátis)
- Heroku (popular, grátis com limites)

**Para profissionais:**
- DigitalOcean VPS (controle total)
- AWS EC2 (escalável)

### Preciso de webhook?
**Não é obrigatório**, mas recomendado:
- **Sem webhook**: Pagamentos detectados em até 30min
- **Com webhook**: Detecção instantânea

### Como fazer backup automático?
**No VPS (Linux):**
```bash
# Crie script backup.sh
#!/bin/bash
cp bot_vip.db backups/bot_vip_$(date +%Y%m%d).db

# Adicione ao cron
crontab -e
# Backup diário às 3h:
0 3 * * * /root/bot-telegram/backup.sh
```

**No Windows (Task Scheduler):**
```batch
# backup.bat
copy bot_vip.db backups\bot_vip_%date:~-4,4%%date:~-7,2%%date:~-10,2%.db
```

---

## 💡 Dicas e Boas Práticas

### Como evitar chargebacks?
1. Deixe termos de uso claros
2. Não faça promessas falsas
3. Responda dúvidas rapidamente
4. Forneça o conteúdo prometido

### Como aumentar conversão?
1. Ofereça teste grátis de 3 dias
2. Crie urgência (vagas limitadas)
3. Mostre depoimentos
4. Facilite o pagamento (Pix)

### Como reter clientes?
1. Conteúdo de qualidade
2. Regularidade nas postagens
3. Interação com membros
4. Bônus exclusivos
5. Programa de fidelidade

### Como lidar com suporte?
1. Crie grupo de suporte separado
2. Configure respostas automáticas
3. Documente perguntas comuns
4. Seja profissional e educado

---

## 📈 Escalando o Bot

### Quantos usuários antes de precisar de VPS?
- **0-100 usuários**: Railway/Heroku grátis
- **100-1000 usuários**: VPS básico ($5-10/mês)
- **1000+ usuários**: VPS robusto ($20+/mês) ou múltiplas instâncias

### Como migrar de SQLite para PostgreSQL?
1. Instale PostgreSQL
2. Altere `DATABASE_URL` no `.env`
3. Execute:
```python
python -c "import database; database.init_db()"
```
4. Migre dados (export/import ou script)

### Como otimizar desempenho?
1. Use índices no banco:
```python
telegram_id = Column(Integer, unique=True, index=True)
```

2. Cache de dados frequentes
3. Reduza frequência de verificações
4. Use conexões pooling para banco

---

## ❓ Outras Dúvidas

### Posso revender este bot?
Depende da licença. Este código é fornecido como está para uso pessoal/comercial próprio.

### Preciso de CNPJ?
Depende do volume. Consulte um contador:
- **Pessoa Física**: Até certo valor mensal
- **MEI**: Recomendado para formalização
- **Empresa**: Para volumes maiores

### É legal vender conteúdo adulto?
**Cuidados legais:**
- Apenas conteúdo próprio ou com direitos
- Proibido conteúdo ilegal
- Respeite leis locais
- Termos de uso do Telegram
- Política do Mercado Pago

**Recomendações:**
- Consulte advogado
- Tenha termos de uso claros
- Verifique idade dos compradores (18+)

---

## 🆘 Ainda tem dúvidas?

1. **Revise a documentação:**
   - README.md
   - CONFIGURACAO.md
   - DEPLOY.md

2. **Verifique os logs:**
   - Ative o bot e veja mensagens de erro
   - Execute `python utils.py test`

3. **Teste passo a passo:**
   - Configure uma variável por vez
   - Teste após cada mudança

4. **Documentação oficial:**
   - [Telegram Bot API](https://core.telegram.org/bots/api)
   - [Mercado Pago Docs](https://www.mercadopago.com.br/developers)
   - [python-telegram-bot](https://docs.python-telegram-bot.org/)

---

**Última atualização**: Janeiro 2026
