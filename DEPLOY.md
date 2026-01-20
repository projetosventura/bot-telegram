# 🚀 Guia de Deploy

Este guia mostra como fazer deploy do bot em diferentes plataformas.

## 📋 Pré-requisitos

- Conta na plataforma escolhida
- Git instalado
- Repositório do bot (pode ser privado)

## 🔧 Preparação

### 1. Criar repositório Git

```bash
cd bot-telegram
git init
git add .
git commit -m "Initial commit"
```

### 2. Criar repositório no GitHub (ou GitLab/Bitbucket)

```bash
git remote add origin https://github.com/seu-usuario/bot-telegram.git
git branch -M main
git push -u origin main
```

## ☁️ Opções de Deploy

### Opção 1: Railway (Recomendado - Grátis)

Railway oferece 500 horas grátis por mês.

1. Acesse [railway.app](https://railway.app)
2. Faça login com GitHub
3. Clique em "New Project"
4. Selecione "Deploy from GitHub repo"
5. Escolha seu repositório
6. Configure as variáveis de ambiente:
   - Vá em "Variables"
   - Adicione todas as variáveis do arquivo `env.example`
7. O deploy inicia automaticamente!

**Configurações adicionais:**
- Em "Settings" > "Deploy", adicione:
  - Build Command: `pip install -r requirements.txt`
  - Start Command: `python bot.py`

### Opção 2: Heroku

1. Crie arquivo `Procfile` na raiz:
```
bot: python bot.py
webhook: gunicorn webhook:app
```

2. Crie arquivo `runtime.txt`:
```
python-3.11.0
```

3. Deploy via Heroku CLI:
```bash
heroku login
heroku create seu-bot-vip
git push heroku main

# Configure variáveis de ambiente
heroku config:set TELEGRAM_BOT_TOKEN=seu_token
heroku config:set MERCADO_PAGO_ACCESS_TOKEN=seu_token
# ... outras variáveis
```

4. Ative o dyno:
```bash
heroku ps:scale bot=1
```

### Opção 3: DigitalOcean (VPS)

Para maior controle e recursos.

1. Crie um Droplet (Ubuntu 22.04)

2. Conecte via SSH:
```bash
ssh root@seu-ip
```

3. Instale dependências:
```bash
apt update
apt install python3 python3-pip python3-venv git -y
```

4. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/bot-telegram.git
cd bot-telegram
```

5. Configure ambiente:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

6. Configure variáveis:
```bash
cp env.example .env
nano .env  # Edite com suas credenciais
```

7. Crie serviço systemd (`/etc/systemd/system/bot-vip.service`):
```ini
[Unit]
Description=Bot VIP Telegram
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/bot-telegram
Environment="PATH=/root/bot-telegram/venv/bin"
ExecStart=/root/bot-telegram/venv/bin/python bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

8. Inicie o serviço:
```bash
systemctl daemon-reload
systemctl enable bot-vip
systemctl start bot-vip
systemctl status bot-vip
```

### Opção 4: Google Cloud Run

1. Crie `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "bot.py"]
```

2. Build e deploy:
```bash
gcloud builds submit --tag gcr.io/seu-projeto/bot-vip
gcloud run deploy bot-vip --image gcr.io/seu-projeto/bot-vip --platform managed
```

### Opção 5: AWS EC2

Similar ao DigitalOcean, mas usando AWS:

1. Crie instância EC2 (t2.micro é grátis por 12 meses)
2. Configure security group para permitir SSH
3. Siga passos similares ao DigitalOcean

## 🌐 Configurando Webhook (Opcional)

Se você configurou um servidor com IP público para webhook:

### 1. Configure Nginx

Instale Nginx:
```bash
apt install nginx -y
```

Configure (`/etc/nginx/sites-available/webhook`):
```nginx
server {
    listen 80;
    server_name seu-dominio.com;

    location /webhook {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Ative:
```bash
ln -s /etc/nginx/sites-available/webhook /etc/nginx/sites-enabled/
systemctl restart nginx
```

### 2. Configure SSL com Let's Encrypt

```bash
apt install certbot python3-certbot-nginx -y
certbot --nginx -d seu-dominio.com
```

### 3. Inicie servidor webhook

Crie serviço (`/etc/systemd/system/webhook-vip.service`):
```ini
[Unit]
Description=Webhook Bot VIP
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/bot-telegram
Environment="PATH=/root/bot-telegram/venv/bin"
ExecStart=/root/bot-telegram/venv/bin/gunicorn -c gunicorn_config.py webhook:app
Restart=always

[Install]
WantedBy=multi-user.target
```

Inicie:
```bash
systemctl daemon-reload
systemctl enable webhook-vip
systemctl start webhook-vip
```

### 4. Configure no Mercado Pago

No painel do Mercado Pago:
1. Vá em "Suas integrações"
2. Configure a URL de notificação: `https://seu-dominio.com/webhook`

## 📊 Monitoramento

### Logs no Railway/Heroku
Use o dashboard da plataforma para ver logs em tempo real.

### Logs no VPS
```bash
# Bot
journalctl -u bot-vip -f

# Webhook
journalctl -u webhook-vip -f
```

### Banco de dados
Faça backup regularmente:
```bash
# Crie cron job
crontab -e

# Adicione (backup diário às 3h):
0 3 * * * cp /root/bot-telegram/bot_vip.db /root/backups/bot_vip_$(date +\%Y\%m\%d).db
```

## 🔒 Segurança

1. **Nunca commite o arquivo .env**
```bash
# Certifique-se que está no .gitignore
echo ".env" >> .gitignore
```

2. **Use secrets/variáveis de ambiente**
   - Railway: Use "Variables"
   - Heroku: Use `heroku config`
   - VPS: Use arquivo `.env`

3. **Restrinja acesso SSH** (VPS)
```bash
# Desabilite login root direto
nano /etc/ssh/sshd_config
# PermitRootLogin no

# Use chaves SSH ao invés de senha
```

4. **Configure firewall** (VPS)
```bash
ufw allow ssh
ufw allow http
ufw allow https
ufw enable
```

## 🔄 Atualizações

### Railway/Heroku
Apenas faça push para o repositório:
```bash
git add .
git commit -m "Atualização"
git push origin main
```

### VPS
```bash
cd bot-telegram
git pull
systemctl restart bot-vip
systemctl restart webhook-vip
```

## 📞 Troubleshooting

### Bot não inicia
```bash
# Verifique logs
python utils.py test

# Verifique variáveis de ambiente
printenv | grep TELEGRAM
```

### Webhook não recebe notificações
```bash
# Teste endpoint
curl -X POST https://seu-dominio.com/webhook

# Verifique logs do Nginx
tail -f /var/log/nginx/error.log
```

### Banco de dados corrompido
```bash
# Restaure backup
cp /root/backups/bot_vip_20240120.db bot_vip.db
systemctl restart bot-vip
```

---

## 🎉 Deploy Concluído!

Seu bot está no ar! Teste enviando `/start` para o bot.

Para suporte, verifique os logs e a documentação das plataformas.
