"""
Configurações do Bot VIP Telegram
"""
import os
from dotenv import load_dotenv

# Carrega .env apenas se existir (local), ignora no Railway
load_dotenv()

# Debug: Print para ver se as variáveis estão sendo lidas
print(f"DEBUG - TELEGRAM_BOT_TOKEN existe: {bool(os.getenv('TELEGRAM_BOT_TOKEN'))}")
print(f"DEBUG - Primeiros caracteres: {os.getenv('TELEGRAM_BOT_TOKEN', '')[:10]}...")

# Telegram
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN não configurado!")
    
ADMIN_USER_ID = int(os.getenv('ADMIN_USER_ID', 0))
GROUP_ID = int(os.getenv('GROUP_ID', 0))  # Grupo para conversa (opcional)

# Canais por plano
CANAL_FOTOS_ID = int(os.getenv('CANAL_FOTOS_ID', 0))  # Canal de fotos (Plano Fotos e Completo)
CANAL_COMPLETO_ID = int(os.getenv('CANAL_COMPLETO_ID', 0))  # Canal de vídeos (apenas Plano Completo)

# Mercado Pago
MERCADO_PAGO_ACCESS_TOKEN = os.getenv('MERCADO_PAGO_ACCESS_TOKEN')

# Planos
PLANO_FOTOS = {
    'nome': 'Plano Fotos VIP',
    'valor': float(os.getenv('PLANO_FOTOS_VALOR', 29.90)),
    'duracao_dias': 30,
    'tipo': 'fotos'
}

PLANO_COMPLETO = {
    'nome': 'Plano Completo VIP',
    'valor': float(os.getenv('PLANO_COMPLETO_VALOR', 49.90)),
    'duracao_dias': 30,
    'tipo': 'completo'
}

# Configurações
DIAS_AVISO_VENCIMENTO = int(os.getenv('DIAS_AVISO_VENCIMENTO', 3))
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///bot_vip.db')

# Mensagens
MENSAGEM_BEM_VINDO = """
🌟 Bem-vindo ao Grupo VIP! 🌟

Você tem acesso ao conteúdo exclusivo do seu plano.

Para qualquer dúvida, entre em contato com o administrador.
"""

MENSAGEM_PAGAMENTO_APROVADO = """
✅ Pagamento Aprovado!

Seu acesso foi liberado com sucesso.
Plano: {plano}
Válido até: {data_vencimento}

Você já pode acessar o grupo VIP!
"""

MENSAGEM_AVISO_VENCIMENTO = """
⚠️ Aviso de Vencimento

Olá! Seu plano está próximo do vencimento.

Plano: {plano}
Vencimento: {data_vencimento}
Faltam {dias} dias

Para renovar e manter seu acesso, clique no botão abaixo:
"""

MENSAGEM_VENCIDO = """
❌ Assinatura Vencida

Seu acesso ao grupo VIP foi removido pois sua assinatura venceu.

Para voltar ao grupo, renove sua assinatura!
"""
