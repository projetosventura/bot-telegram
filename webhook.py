"""
Servidor Webhook para receber notificações do Mercado Pago
Execute este arquivo separadamente se quiser usar webhooks
"""
from flask import Flask, request, jsonify
import logging
from pagamentos import GerenciadorPagamentos
import database
import config
from telegram import Bot
from telegram.constants import ChatMemberStatus

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicializa o bot do Telegram
telegram_bot = Bot(token=config.TELEGRAM_BOT_TOKEN)


async def processar_pagamento_aprovado(telegram_id, plano, plano_info, data_vencimento_str):
    """Processa pagamento aprovado de forma assíncrona"""
    from telegram import InlineKeyboardButton, InlineKeyboardMarkup
    
    keyboard = []
    
    # Link do grupo (ambos os planos)
    if config.GROUP_ID and config.GROUP_ID != 0:
        try:
            invite_link = await telegram_bot.create_chat_invite_link(
                config.GROUP_ID,
                member_limit=1
            )
            keyboard.append([InlineKeyboardButton("👥 Entrar no Grupo VIP", url=invite_link.invite_link)])
        except Exception as e:
            logger.error(f"Erro ao gerar link do grupo: {e}")
    
    # Canal de Fotos (ambos os planos têm acesso)
    if config.CANAL_FOTOS_ID and config.CANAL_FOTOS_ID != 0:
        try:
            canal_fotos_invite = await telegram_bot.create_chat_invite_link(
                config.CANAL_FOTOS_ID,
                member_limit=1
            )
            keyboard.append([InlineKeyboardButton("📸 Canal de Fotos VIP", url=canal_fotos_invite.invite_link)])
        except Exception as e:
            logger.error(f"Erro ao gerar link do canal de fotos: {e}")
    
    # Canal Completo (apenas Plano Completo)
    if plano == 'completo' and config.CANAL_COMPLETO_ID and config.CANAL_COMPLETO_ID != 0:
        try:
            canal_completo_invite = await telegram_bot.create_chat_invite_link(
                config.CANAL_COMPLETO_ID,
                member_limit=1
            )
            keyboard.append([InlineKeyboardButton("🎬 Canal Completo (Fotos + Vídeos)", url=canal_completo_invite.invite_link)])
        except Exception as e:
            logger.error(f"Erro ao gerar link do canal completo: {e}")
    
    reply_markup = InlineKeyboardMarkup(keyboard) if keyboard else None
    
    mensagem = config.MENSAGEM_PAGAMENTO_APROVADO.format(
        plano=plano_info['nome'],
        data_vencimento=data_vencimento_str
    )
    
    if len(keyboard) > 1:
        mensagem += "\n\n🎉 Clique nos botões abaixo para acessar:"
    elif len(keyboard) == 1:
        mensagem += "\n\n🎉 Clique no botão abaixo para acessar:"
    
    await telegram_bot.send_message(
        telegram_id,
        mensagem,
        reply_markup=reply_markup
    )


@app.route('/webhook', methods=['POST'])
def webhook():
    """Recebe notificações do Mercado Pago"""
    import asyncio
    
    try:
        data = request.get_json()
        logger.info(f"Webhook recebido: {data}")
        
        # Processa o webhook
        gerenciador = GerenciadorPagamentos()
        resultado = gerenciador.processar_webhook(data)
        
        if resultado and resultado['approved']:
            # Pagamento aprovado!
            telegram_id = resultado['telegram_id']
            plano = resultado['plano']
            
            plano_info = config.PLANO_FOTOS if plano == 'fotos' else config.PLANO_COMPLETO
            
            # Cria/atualiza usuário
            usuario = database.criar_usuario(
                telegram_id=telegram_id,
                username=None,
                nome=None,
                plano=plano,
                duracao_dias=plano_info['duracao_dias']
            )
            
            # Extrai data de vencimento (antes de fechar a sessão)
            data_vencimento_str = usuario.data_vencimento.strftime('%d/%m/%Y')
            
            # Processa de forma assíncrona
            asyncio.run(processar_pagamento_aprovado(telegram_id, plano, plano_info, data_vencimento_str))
            
            logger.info(f"✅ Pagamento processado via webhook para {telegram_id}")
        
        return jsonify({"status": "ok"}), 200
        
    except Exception as e:
        logger.error(f"Erro ao processar webhook: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/health', methods=['GET'])
def health():
    """Endpoint de health check"""
    return jsonify({"status": "ok"}), 200


if __name__ == '__main__':
    import os
    
    # Inicializa banco de dados
    database.init_db()
    
    # Porta do Railway ou 5000 local
    port = int(os.environ.get('PORT', 5000))
    
    # Inicia servidor
    app.run(host='0.0.0.0', port=port, debug=False)
