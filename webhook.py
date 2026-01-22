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


@app.route('/webhook', methods=['POST'])
def webhook():
    """Recebe notificações do Mercado Pago"""
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
            
            # Gera links de convite
            from telegram import InlineKeyboardButton, InlineKeyboardMarkup
            
            keyboard = []
            
            # Link do grupo
            if config.GROUP_ID and config.GROUP_ID != 0:
                invite_link = telegram_bot.create_chat_invite_link(
                    config.GROUP_ID,
                    member_limit=1
                )
                keyboard.append([InlineKeyboardButton("👥 Entrar no Grupo VIP", url=invite_link.invite_link)])
            
            # Link do canal (se configurado)
            if config.CANAL_ID and config.CANAL_ID != 0:
                try:
                    canal_invite = telegram_bot.create_chat_invite_link(
                        config.CANAL_ID,
                        member_limit=1
                    )
                    keyboard.append([InlineKeyboardButton("📢 Entrar no Canal VIP", url=canal_invite.invite_link)])
                except Exception as e:
                    logger.error(f"Erro ao gerar link do canal: {e}")
            
            reply_markup = InlineKeyboardMarkup(keyboard) if keyboard else None
            
            mensagem = config.MENSAGEM_PAGAMENTO_APROVADO.format(
                plano=plano_info['nome'],
                data_vencimento=usuario.data_vencimento.strftime('%d/%m/%Y')
            )
            
            if len(keyboard) > 1:
                mensagem += "\n\n🎉 Clique nos botões abaixo para acessar:"
            elif len(keyboard) == 1:
                mensagem += "\n\n🎉 Clique no botão abaixo para acessar:"
            
            telegram_bot.send_message(
                telegram_id,
                mensagem,
                reply_markup=reply_markup
            )
            
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
