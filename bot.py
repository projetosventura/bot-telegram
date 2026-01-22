# -*- coding: utf-8 -*-
"""
Bot VIP Telegram - Gerenciamento de Assinaturas
"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import logging
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ChatMemberHandler,
    ContextTypes
)
from telegram.constants import ChatMemberStatus

import config
import database
from pagamentos import gerar_link_pagamento
from scheduler import iniciar_verificacoes_automaticas

# Configuração de logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /start - Apresenta o bot e os planos"""
    keyboard = [
        [InlineKeyboardButton("📸 Plano Fotos - R$ {:.2f}".format(config.PLANO_FOTOS['valor']), 
                             callback_data='plano_fotos')],
        [InlineKeyboardButton("🎬 Plano Completo - R$ {:.2f}".format(config.PLANO_COMPLETO['valor']), 
                             callback_data='plano_completo')],
        [InlineKeyboardButton("ℹ️ Minha Assinatura", callback_data='minha_assinatura')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    mensagem = """
🌟 Bem-vindo ao Bot VIP! 🌟

Escolha seu plano e tenha acesso ao conteúdo exclusivo:

📸 *Plano Fotos VIP* - R$ {:.2f}/mês
   • Acesso a todas as fotos exclusivas
   • Conteúdo atualizado diariamente
   • Suporte prioritário

🎬 *Plano Completo VIP* - R$ {:.2f}/mês
   • Tudo do Plano Fotos +
   • Acesso a vídeos exclusivos
   • Conteúdo em alta qualidade
   • Lançamentos antecipados

Selecione uma opção abaixo:
""".format(config.PLANO_FOTOS['valor'], config.PLANO_COMPLETO['valor'])
    
    await update.message.reply_text(mensagem, reply_markup=reply_markup, parse_mode='Markdown')


async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gerencia callbacks dos botões"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    username = query.from_user.username
    nome = query.from_user.full_name
    
    if query.data == 'plano_fotos':
        await processar_escolha_plano(query, user_id, username, nome, 'fotos')
    
    elif query.data == 'plano_completo':
        await processar_escolha_plano(query, user_id, username, nome, 'completo')
    
    elif query.data == 'minha_assinatura':
        await mostrar_assinatura(query, user_id)
    
    elif query.data == 'voltar_inicio':
        # Mostra o menu inicial novamente
        keyboard = [
            [InlineKeyboardButton("📸 Plano Fotos - R$ {:.2f}".format(config.PLANO_FOTOS['valor']), 
                                 callback_data='plano_fotos')],
            [InlineKeyboardButton("🎬 Plano Completo - R$ {:.2f}".format(config.PLANO_COMPLETO['valor']), 
                                 callback_data='plano_completo')],
            [InlineKeyboardButton("ℹ️ Minha Assinatura", callback_data='minha_assinatura')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        mensagem = """
🌟 Bem-vindo ao Bot VIP! 🌟

Escolha seu plano e tenha acesso ao conteúdo exclusivo:

📸 *Plano Fotos VIP* - R$ {:.2f}/mês
   • Acesso a todas as fotos exclusivas
   • Conteúdo atualizado diariamente
   • Suporte prioritário

🎬 *Plano Completo VIP* - R$ {:.2f}/mês
   • Tudo do Plano Fotos +
   • Acesso a vídeos exclusivos
   • Conteúdo em alta qualidade
   • Lançamentos antecipados

Selecione uma opção abaixo:
""".format(config.PLANO_FOTOS['valor'], config.PLANO_COMPLETO['valor'])
        
        await query.edit_message_text(mensagem, reply_markup=reply_markup, parse_mode='Markdown')
    
    elif query.data.startswith('renovar_'):
        plano = query.data.split('_')[1]
        await processar_escolha_plano(query, user_id, username, nome, plano)


async def processar_escolha_plano(query, user_id, username, nome, plano_tipo):
    """Processa a escolha de um plano e gera link de pagamento"""
    try:
        # Gera link de pagamento
        resultado = gerar_link_pagamento(user_id, username, plano_tipo)
        
        # Valida se o link foi gerado
        if not resultado or not resultado.get('url'):
            await query.edit_message_text(
                "❌ Erro ao gerar link de pagamento.\n\n"
                "⚠️ Verifique se o Mercado Pago está configurado corretamente.\n\n"
                "💡 Dica: Se estiver usando TOKEN DE TESTE, certifique-se de que está correto."
            )
            return
        
        plano_info = config.PLANO_FOTOS if plano_tipo == 'fotos' else config.PLANO_COMPLETO
        
        keyboard = [
            [InlineKeyboardButton("💳 Pagar Agora", url=resultado['url'])],
            [InlineKeyboardButton("« Voltar", callback_data='voltar_inicio')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        mensagem = f"""
✅ *Plano Selecionado: {plano_info['nome']}*

💰 Valor: R$ {plano_info['valor']:.2f}
📅 Validade: {plano_info['duracao_dias']} dias

Clique no botão abaixo para realizar o pagamento:

⚡ Após a confirmação do pagamento, você será automaticamente adicionado ao grupo VIP!
"""
        
        await query.edit_message_text(mensagem, reply_markup=reply_markup, parse_mode='Markdown')
        
    except Exception as e:
        logger.error(f"Erro ao processar plano: {e}")
        await query.edit_message_text("❌ Erro ao processar. Tente novamente mais tarde.")


async def mostrar_assinatura(query, user_id):
    """Mostra informações da assinatura do usuário"""
    usuario = database.get_usuario(user_id)
    
    if not usuario or not usuario.ativo:
        keyboard = [[InlineKeyboardButton("📝 Assinar Agora", callback_data='start')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "❌ Você não possui uma assinatura ativa.\n\nClique abaixo para assinar!",
            reply_markup=reply_markup
        )
        return
    
    plano_info = config.PLANO_FOTOS if usuario.plano == 'fotos' else config.PLANO_COMPLETO
    dias_restantes = usuario.dias_para_vencer()
    
    status_emoji = "✅" if dias_restantes > config.DIAS_AVISO_VENCIMENTO else "⚠️"
    
    keyboard = [
        [InlineKeyboardButton("🔄 Renovar Assinatura", callback_data=f'renovar_{usuario.plano}')],
        [InlineKeyboardButton("« Voltar", callback_data='start')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    mensagem = f"""
{status_emoji} *Sua Assinatura*

📋 Plano: {plano_info['nome']}
📅 Vencimento: {usuario.data_vencimento.strftime('%d/%m/%Y')}
⏰ Dias restantes: {dias_restantes}
💰 Valor mensal: R$ {plano_info['valor']:.2f}

{'⚠️ *Sua assinatura está próxima do vencimento!*' if dias_restantes <= config.DIAS_AVISO_VENCIMENTO else ''}
"""
    
    await query.edit_message_text(mensagem, reply_markup=reply_markup, parse_mode='Markdown')


async def planos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /planos - Mostra os planos disponíveis"""
    mensagem = f"""
💎 *PLANOS VIP DISPONÍVEIS*

📸 *Plano Fotos VIP* - R$ {config.PLANO_FOTOS['valor']:.2f}/mês
   • Acesso a todas as fotos exclusivas
   • Conteúdo atualizado diariamente
   • Suporte prioritário

🎬 *Plano Completo VIP* - R$ {config.PLANO_COMPLETO['valor']:.2f}/mês
   • Tudo do Plano Fotos +
   • Acesso a vídeos exclusivos
   • Conteúdo em alta qualidade
   • Lançamentos antecipados

💳 *Como assinar?*
Envie /start no privado do bot para escolher seu plano e realizar o pagamento!

👉 Clique aqui para iniciar: @VIP\_Mel\_bot
"""
    
    await update.message.reply_text(mensagem, parse_mode='Markdown')


async def admin_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando admin para ver estatísticas (apenas para admins)"""
    if update.effective_user.id != config.ADMIN_USER_ID:
        await update.message.reply_text("❌ Você não tem permissão para este comando.")
        return
    
    session = database.get_session()
    
    total_usuarios = session.query(database.Usuario).count()
    usuarios_ativos = session.query(database.Usuario).filter_by(ativo=True).count()
    plano_fotos = session.query(database.Usuario).filter_by(ativo=True, plano='fotos').count()
    plano_completo = session.query(database.Usuario).filter_by(ativo=True, plano='completo').count()
    
    # Pagamentos
    total_pagamentos = session.query(database.Pagamento).count()
    pagamentos_aprovados = session.query(database.Pagamento).filter_by(status='approved').count()
    
    session.close()
    
    mensagem = f"""
📊 *Estatísticas do Bot VIP*

👥 *Usuários*
   • Total: {total_usuarios}
   • Ativos: {usuarios_ativos}
   • Plano Fotos: {plano_fotos}
   • Plano Completo: {plano_completo}

💰 *Pagamentos*
   • Total: {total_pagamentos}
   • Aprovados: {pagamentos_aprovados}
   • Pendentes: {total_pagamentos - pagamentos_aprovados}
"""
    
    await update.message.reply_text(mensagem, parse_mode='Markdown')


async def verificar_pagamento_manual(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando admin para aprovar pagamento manualmente"""
    if update.effective_user.id != config.ADMIN_USER_ID:
        await update.message.reply_text("❌ Você não tem permissão para este comando.")
        return
    
    if len(context.args) != 2:
        await update.message.reply_text(
            "Uso: /aprovar <telegram_id> <plano>\n"
            "Exemplo: /aprovar 123456789 fotos"
        )
        return
    
    try:
        telegram_id = int(context.args[0])
        plano = context.args[1]
        
        if plano not in ['fotos', 'completo']:
            await update.message.reply_text("❌ Plano inválido. Use 'fotos' ou 'completo'")
            return
        
        plano_info = config.PLANO_FOTOS if plano == 'fotos' else config.PLANO_COMPLETO
        
        # Cria/atualiza usuário
        usuario = database.criar_usuario(
            telegram_id=telegram_id,
            username=None,
            nome=None,
            plano=plano,
            duracao_dias=plano_info['duracao_dias']
        )
        
        # Adiciona ao grupo e canais baseado no plano
        links = []
        try:
            # Link do grupo (ambos os planos)
            if config.GROUP_ID and config.GROUP_ID != 0:
                try:
                    chat_member = await context.bot.get_chat_member(config.GROUP_ID, telegram_id)
                    if chat_member.status in [ChatMemberStatus.LEFT, ChatMemberStatus.KICKED]:
                        invite_link = await context.bot.create_chat_invite_link(
                            config.GROUP_ID,
                            member_limit=1
                        )
                        links.append(f"👥 Grupo VIP: {invite_link.invite_link}")
                except Exception as e:
                    logger.error(f"Erro ao gerar link do grupo: {e}")
            
            # Canal de Fotos (ambos os planos) - sempre gera link
            if config.CANAL_FOTOS_ID and config.CANAL_FOTOS_ID != 0:
                try:
                    # Se estiver banido, desbanir primeiro
                    try:
                        canal_member = await context.bot.get_chat_member(config.CANAL_FOTOS_ID, telegram_id)
                        if canal_member.status == ChatMemberStatus.KICKED:
                            await context.bot.unban_chat_member(config.CANAL_FOTOS_ID, telegram_id)
                    except:
                        pass
                    
                    canal_invite = await context.bot.create_chat_invite_link(
                        config.CANAL_FOTOS_ID,
                        member_limit=1
                    )
                    links.append(f"📸 Canal de Fotos VIP: {canal_invite.invite_link}")
                except Exception as e:
                    logger.error(f"Erro ao gerar link do canal de fotos: {e}")
            
            # Canal Completo (apenas Plano Completo) - sempre gera link
            if plano == 'completo' and config.CANAL_COMPLETO_ID and config.CANAL_COMPLETO_ID != 0:
                try:
                    # Se estiver banido, desbanir primeiro
                    try:
                        canal_completo_member = await context.bot.get_chat_member(config.CANAL_COMPLETO_ID, telegram_id)
                        if canal_completo_member.status == ChatMemberStatus.KICKED:
                            await context.bot.unban_chat_member(config.CANAL_COMPLETO_ID, telegram_id)
                    except:
                        pass
                    
                    canal_completo_invite = await context.bot.create_chat_invite_link(
                        config.CANAL_COMPLETO_ID,
                        member_limit=1
                    )
                    links.append(f"🎬 Canal Completo (Fotos + Vídeos): {canal_completo_invite.invite_link}")
                except Exception as e:
                    logger.error(f"Erro ao gerar link do canal completo: {e}")
            
            if links:
                mensagem_links = "✅ Usuário aprovado!\n\n" + "\n\n".join(links)
                await update.message.reply_text(mensagem_links)
            else:
                await update.message.reply_text("✅ Usuário aprovado e já está no grupo/canal!")
        except Exception as e:
            logger.error(f"Erro ao verificar membro: {e}")
            await update.message.reply_text("✅ Usuário aprovado! Adicione-o manualmente.")
        
        # Notifica o usuário
        try:
            mensagem = config.MENSAGEM_PAGAMENTO_APROVADO.format(
                plano=plano_info['nome'],
                data_vencimento=usuario.data_vencimento.strftime('%d/%m/%Y')
            )
            await context.bot.send_message(telegram_id, mensagem)
        except:
            pass
        
    except ValueError:
        await update.message.reply_text("❌ ID do Telegram inválido")
    except Exception as e:
        logger.error(f"Erro ao aprovar pagamento: {e}")
        await update.message.reply_text(f"❌ Erro: {str(e)}")


async def enviar_previa(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando admin para enviar mensagem/foto no canal de prévias"""
    if update.effective_user.id != config.ADMIN_USER_ID:
        await update.message.reply_text("❌ Você não tem permissão para este comando.")
        return
    
    if config.GRUPO_PREVIAS_ID == 0:
        await update.message.reply_text("❌ Canal de prévias não configurado.")
        return
    
    # Se for resposta a uma mensagem com foto/vídeo
    if update.message.reply_to_message:
        try:
            # Copia a mensagem para o canal de prévias
            await update.message.reply_to_message.copy(
                chat_id=config.GRUPO_PREVIAS_ID
            )
            await update.message.reply_text("✅ Conteúdo enviado para o canal de prévias!")
        except Exception as e:
            logger.error(f"Erro ao enviar para canal de prévias: {e}")
            await update.message.reply_text(f"❌ Erro ao enviar: {str(e)}")
    
    # Se for texto após o comando
    elif len(context.args) > 0:
        mensagem = ' '.join(context.args)
        try:
            await context.bot.send_message(
                chat_id=config.GRUPO_PREVIAS_ID,
                text=mensagem,
                parse_mode='Markdown'
            )
            await update.message.reply_text("✅ Mensagem enviada para o canal de prévias!")
        except Exception as e:
            logger.error(f"Erro ao enviar mensagem: {e}")
            await update.message.reply_text(f"❌ Erro ao enviar: {str(e)}")
    
    else:
        await update.message.reply_text(
            "📝 *Como usar o comando /enviar_previa:*\n\n"
            "1️⃣ Responda a uma foto/vídeo/mensagem com /enviar_previa\n"
            "   (o bot vai copiar para o canal de prévias)\n\n"
            "2️⃣ Ou digite: /enviar_previa Sua mensagem aqui\n\n"
            "Exemplo: /enviar_previa 🔥 Nova prévia disponível! Use /planos para ver os planos VIP",
            parse_mode='Markdown'
        )


async def post_init(application):
    """Executa após o bot iniciar - envia primeira divulgação"""
    from scheduler import divulgar_planos_previas_async
    
    logger.info("📢 Enviando primeira divulgação ao iniciar o bot...")
    try:
        await divulgar_planos_previas_async(application.bot)
    except Exception as e:
        logger.error(f"Erro ao enviar primeira divulgação: {e}")


async def novo_membro(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gerencia novos membros no grupo"""
    chat_id = update.effective_chat.id
    
    for member in update.message.new_chat_members:
        user_id = member.id
        
        # Se for no grupo de prévias (gratuito)
        if chat_id == config.GRUPO_PREVIAS_ID and config.GRUPO_PREVIAS_ID != 0:
            # Boas-vindas com marketing dos planos VIP
            mensagem = config.MENSAGEM_BEM_VINDO_PREVIAS.format(
                plano_fotos=config.PLANO_FOTOS['valor'],
                plano_completo=config.PLANO_COMPLETO['valor']
            )
            await update.message.reply_text(
                f"👋 {member.mention_html()}\n\n{mensagem}",
                parse_mode='HTML'
            )
        
        # Se for no grupo VIP (pago)
        elif chat_id == config.GROUP_ID and config.GROUP_ID != 0:
            # Verifica se tem assinatura ativa
            usuario = database.get_usuario(user_id)
            
            if not usuario or not usuario.ativo:
                # Remove do grupo se não tiver assinatura
                try:
                    await context.bot.ban_chat_member(config.GROUP_ID, user_id)
                    await context.bot.unban_chat_member(config.GROUP_ID, user_id)
                    await update.message.reply_text(
                        f"❌ {member.mention_html()} foi removido. "
                        "É necessário ter uma assinatura ativa para entrar no grupo.",
                        parse_mode='HTML'
                    )
                except Exception as e:
                    logger.error(f"Erro ao remover membro: {e}")
            else:
                # Boas-vindas
                await update.message.reply_text(
                    f"🌟 Bem-vindo {member.mention_html()} ao Grupo VIP!\n\n"
                    f"{config.MENSAGEM_BEM_VINDO}",
                    parse_mode='HTML'
                )


def main():
    """Inicia o bot"""
    # Inicializa banco de dados
    database.init_db()
    
    # Cria aplicação
    application = Application.builder().token(config.TELEGRAM_BOT_TOKEN).post_init(post_init).build()
    
    # Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("planos", planos))
    application.add_handler(CommandHandler("stats", admin_stats))
    application.add_handler(CommandHandler("aprovar", verificar_pagamento_manual))
    application.add_handler(CommandHandler("enviar_previa", enviar_previa))
    application.add_handler(CallbackQueryHandler(callback_handler))
    
    # Handler para novos membros
    from telegram.ext import MessageHandler, filters
    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, novo_membro))
    
    # Inicia verificações automáticas
    iniciar_verificacoes_automaticas(application.bot)
    
    # Inicia o bot
    logger.info("🤖 Bot iniciado!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
