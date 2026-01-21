# -*- coding: utf-8 -*-
"""
Utilitários e funções auxiliares
"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import logging
from telegram import Bot
from telegram.error import TelegramError
import config

logger = logging.getLogger(__name__)


def get_chat_id(bot_token):
    """
    Utilitário para descobrir o ID de um grupo/canal
    Execute este script e envie uma mensagem no grupo com o bot
    """
    from telegram.ext import Application, MessageHandler, filters
    
    async def show_chat_id(update, context):
        chat_id = update.effective_chat.id
        chat_type = update.effective_chat.type
        chat_title = update.effective_chat.title or "Chat Privado"
        
        mensagem = f"""
📊 Informações do Chat

🆔 Chat ID: `{chat_id}`
📝 Tipo: {chat_type}
🏷️ Título: {chat_title}
"""
        await update.message.reply_text(mensagem, parse_mode='Markdown')
        print(f"Chat ID: {chat_id}")
    
    app = Application.builder().token(bot_token).build()
    app.add_handler(MessageHandler(filters.ALL, show_chat_id))
    
    print("Bot iniciado! Envie uma mensagem no grupo para ver o ID...")
    app.run_polling()


def get_my_id(bot_token):
    """
    Utilitário para descobrir seu próprio Telegram ID
    """
    from telegram.ext import Application, CommandHandler
    
    async def show_my_id(update, context):
        user_id = update.effective_user.id
        username = update.effective_user.username
        nome = update.effective_user.full_name
        
        mensagem = f"""
👤 Suas Informações

🆔 User ID: `{user_id}`
👤 Nome: {nome}
📝 Username: @{username or 'N/A'}
"""
        await update.message.reply_text(mensagem, parse_mode='Markdown')
        print(f"User ID: {user_id}")
    
    app = Application.builder().token(bot_token).build()
    app.add_handler(CommandHandler("start", show_my_id))
    
    print("Bot iniciado! Envie /start para ver seu ID...")
    app.run_polling()


def testar_bot():
    """Testa se o bot está configurado corretamente"""
    print("🔍 Testando configurações do bot...\n")
    
    # Testa token do Telegram
    try:
        bot = Bot(token=config.TELEGRAM_BOT_TOKEN)
        me = bot.get_me()
        print(f"✅ Bot conectado: @{me.username}")
    except Exception as e:
        print(f"❌ Erro ao conectar bot: {e}")
        return False
    
    # Testa Mercado Pago
    try:
        import mercadopago
        sdk = mercadopago.SDK(config.MERCADO_PAGO_ACCESS_TOKEN)
        print("✅ Mercado Pago configurado")
    except Exception as e:
        print(f"❌ Erro no Mercado Pago: {e}")
        return False
    
    # Testa banco de dados
    try:
        import database
        database.init_db()
        print("✅ Banco de dados OK")
    except Exception as e:
        print(f"❌ Erro no banco de dados: {e}")
        return False
    
    # Testa acesso ao grupo
    try:
        if config.GROUP_ID:
            chat = bot.get_chat(config.GROUP_ID)
            print(f"✅ Grupo VIP encontrado: {chat.title}")
            
            # Verifica permissões do bot
            bot_member = bot.get_chat_member(config.GROUP_ID, me.id)
            if bot_member.status in ['administrator', 'creator']:
                print("✅ Bot é administrador do grupo")
            else:
                print("⚠️ Bot NÃO é administrador! Adicione como admin.")
        else:
            print("⚠️ GROUP_ID não configurado")
    except Exception as e:
        print(f"⚠️ Erro ao acessar grupo: {e}")
    
    print("\n✅ Testes concluídos!")
    return True


def gerar_relatorio_mensal():
    """Gera relatório mensal de assinaturas"""
    from database import get_session, Usuario, Pagamento
    from datetime import datetime, timedelta
    
    session = get_session()
    
    # Data de início do mês
    hoje = datetime.now()
    inicio_mes = datetime(hoje.year, hoje.month, 1)
    
    # Estatísticas
    novos_usuarios = session.query(Usuario).filter(
        Usuario.data_inicio >= inicio_mes
    ).count()
    
    usuarios_ativos = session.query(Usuario).filter_by(ativo=True).count()
    
    receita_mes = session.query(Pagamento).filter(
        Pagamento.data_aprovacao >= inicio_mes,
        Pagamento.status == 'approved'
    ).count()
    
    plano_fotos = session.query(Usuario).filter_by(ativo=True, plano='fotos').count()
    plano_completo = session.query(Usuario).filter_by(ativo=True, plano='completo').count()
    
    # Receita
    pagamentos = session.query(Pagamento).filter(
        Pagamento.data_aprovacao >= inicio_mes,
        Pagamento.status == 'approved'
    ).all()
    
    receita_total = sum(p.valor for p in pagamentos)
    
    session.close()
    
    relatorio = f"""
📊 RELATÓRIO MENSAL - {hoje.strftime('%B/%Y')}

👥 USUÁRIOS
   • Novos este mês: {novos_usuarios}
   • Ativos atualmente: {usuarios_ativos}
   • Plano Fotos: {plano_fotos}
   • Plano Completo: {plano_completo}

💰 FINANCEIRO
   • Pagamentos aprovados: {receita_mes}
   • Receita total: R$ {receita_total:.2f}
   • Receita média: R$ {(receita_total/receita_mes if receita_mes > 0 else 0):.2f}

📈 PROJEÇÃO
   • Receita mensal recorrente: R$ {(plano_fotos * config.PLANO_FOTOS['valor'] + plano_completo * config.PLANO_COMPLETO['valor']):.2f}
"""
    
    return relatorio


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        comando = sys.argv[1]
        
        if comando == 'test':
            testar_bot()
        elif comando == 'getid':
            if len(sys.argv) > 2:
                get_my_id(sys.argv[2])
            else:
                print("Uso: python utils.py getid <bot_token>")
        elif comando == 'getchat':
            if len(sys.argv) > 2:
                get_chat_id(sys.argv[2])
            else:
                print("Uso: python utils.py getchat <bot_token>")
        elif comando == 'relatorio':
            print(gerar_relatorio_mensal())
        else:
            print("Comandos disponíveis: test, getid, getchat, relatorio")
    else:
        print("""
Utilitários do Bot VIP

Comandos:
  python utils.py test           - Testa configurações
  python utils.py getid <token>  - Descobre seu Telegram ID
  python utils.py getchat <token> - Descobre ID de um grupo
  python utils.py relatorio      - Gera relatório mensal
        """)
