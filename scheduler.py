"""
Agendador de Tarefas Automáticas
Verifica vencimentos e envia avisos
"""
import logging
import asyncio
from apscheduler.schedulers.background import BackgroundScheduler
from telegram.constants import ChatMemberStatus
import config
import database

logger = logging.getLogger(__name__)


def verificar_vencimentos(bot):
    """Verifica assinaturas vencidas e remove usuários do grupo"""
    logger.info("🔍 Verificando assinaturas vencidas...")
    
    usuarios_vencidos = database.get_usuarios_vencidos()
    
    for usuario in usuarios_vencidos:
        try:
            # Desativa usuário no banco
            database.desativar_usuario(usuario.telegram_id)
            
            # Remove do grupo
            try:
                bot.ban_chat_member(config.GROUP_ID, usuario.telegram_id)
                bot.unban_chat_member(config.GROUP_ID, usuario.telegram_id)
                logger.info(f"❌ Usuário {usuario.telegram_id} removido do grupo (vencido)")
            except Exception as e:
                logger.error(f"Erro ao remover usuário {usuario.telegram_id}: {e}")
            
            # Notifica o usuário
            try:
                keyboard = [[{
                    'text': '🔄 Renovar Assinatura',
                    'callback_data': f'renovar_{usuario.plano}'
                }]]
                
                bot.send_message(
                    usuario.telegram_id,
                    config.MENSAGEM_VENCIDO,
                    reply_markup={'inline_keyboard': keyboard}
                )
            except Exception as e:
                logger.error(f"Erro ao notificar usuário {usuario.telegram_id}: {e}")
                
        except Exception as e:
            logger.error(f"Erro ao processar usuário vencido {usuario.telegram_id}: {e}")
    
    if usuarios_vencidos:
        logger.info(f"✅ {len(usuarios_vencidos)} usuários processados (vencidos)")
    else:
        logger.info("✅ Nenhuma assinatura vencida")


def enviar_avisos_vencimento(bot):
    """Envia avisos de vencimento próximo"""
    logger.info("🔍 Verificando assinaturas próximas do vencimento...")
    
    usuarios_avisar = database.get_usuarios_para_avisar()
    
    for usuario in usuarios_avisar:
        try:
            plano_info = config.PLANO_FOTOS if usuario.plano == 'fotos' else config.PLANO_COMPLETO
            dias = usuario.dias_para_vencer()
            
            keyboard = [[{
                'text': '🔄 Renovar Agora',
                'callback_data': f'renovar_{usuario.plano}'
            }]]
            
            mensagem = config.MENSAGEM_AVISO_VENCIMENTO.format(
                plano=plano_info['nome'],
                data_vencimento=usuario.data_vencimento.strftime('%d/%m/%Y'),
                dias=dias
            )
            
            bot.send_message(
                usuario.telegram_id,
                mensagem,
                reply_markup={'inline_keyboard': keyboard}
            )
            
            # Marca aviso como enviado
            database.marcar_aviso_enviado(usuario.telegram_id)
            logger.info(f"⚠️ Aviso enviado para {usuario.telegram_id}")
            
        except Exception as e:
            logger.error(f"Erro ao enviar aviso para {usuario.telegram_id}: {e}")
    
    if usuarios_avisar:
        logger.info(f"✅ {len(usuarios_avisar)} avisos enviados")
    else:
        logger.info("✅ Nenhum aviso a enviar")


def verificar_pagamentos_pendentes(bot):
    """Verifica pagamentos pendentes e atualiza status"""
    logger.info("🔍 Verificando pagamentos pendentes...")
    
    from pagamentos import GerenciadorPagamentos
    
    session = database.get_session()
    pagamentos_pendentes = session.query(database.Pagamento).filter_by(status='pending').all()
    session.close()
    
    if not pagamentos_pendentes:
        logger.info("✅ Nenhum pagamento pendente")
        return
    
    gerenciador = GerenciadorPagamentos()
    
    for pagamento in pagamentos_pendentes:
        try:
            resultado = gerenciador.verificar_pagamento(pagamento.payment_id)
            
            if resultado['approved']:
                # Pagamento aprovado!
                plano_info = config.PLANO_FOTOS if pagamento.plano == 'fotos' else config.PLANO_COMPLETO
                
                # Cria/atualiza usuário
                usuario = database.criar_usuario(
                    telegram_id=pagamento.telegram_id,
                    username=None,
                    nome=None,
                    plano=pagamento.plano,
                    duracao_dias=plano_info['duracao_dias']
                )
                
                # Notifica usuário
                try:
                    mensagem = config.MENSAGEM_PAGAMENTO_APROVADO.format(
                        plano=plano_info['nome'],
                        data_vencimento=usuario.data_vencimento.strftime('%d/%m/%Y')
                    )
                    
                    # Gera link de convite para o grupo
                    invite_link = bot.create_chat_invite_link(
                        config.GROUP_ID,
                        member_limit=1
                    )
                    
                    keyboard = [[{
                        'text': '🎉 Entrar no Grupo VIP',
                        'url': invite_link.invite_link
                    }]]
                    
                    bot.send_message(
                        pagamento.telegram_id,
                        mensagem + "\n\nClique no botão abaixo para entrar:",
                        reply_markup={'inline_keyboard': keyboard}
                    )
                    
                    logger.info(f"✅ Pagamento aprovado para {pagamento.telegram_id}")
                    
                except Exception as e:
                    logger.error(f"Erro ao notificar aprovação: {e}")
                    
        except Exception as e:
            logger.error(f"Erro ao verificar pagamento {pagamento.id}: {e}")
    
    logger.info(f"✅ {len(pagamentos_pendentes)} pagamentos verificados")


async def divulgar_planos_previas_async(bot):
    """Envia mensagem automática divulgando os planos VIP no canal de prévias (async)"""
    if config.GRUPO_PREVIAS_ID == 0:
        logger.warning("⚠️ Canal de prévias não configurado. Pulando divulgação.")
        return
    
    logger.info("📢 Enviando divulgação dos planos VIP no canal de prévias...")
    
    try:
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

👉 Clique aqui para iniciar: @VIP_Mel_bot
"""
        
        await bot.send_message(
            chat_id=config.GRUPO_PREVIAS_ID,
            text=mensagem,
            parse_mode='Markdown'
        )
        
        logger.info("✅ Divulgação enviada com sucesso para o canal de prévias!")
        
    except Exception as e:
        logger.error(f"❌ Erro ao enviar divulgação para canal de prévias: {e}")


def divulgar_planos_previas(bot):
    """Wrapper síncrono para executar a função async no scheduler"""
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # Se já existe um loop rodando, cria uma task
            asyncio.create_task(divulgar_planos_previas_async(bot))
        else:
            # Se não, executa diretamente
            loop.run_until_complete(divulgar_planos_previas_async(bot))
    except Exception as e:
        logger.error(f"❌ Erro ao executar divulgação: {e}")


def iniciar_verificacoes_automaticas(bot):
    """Inicia o agendador de tarefas"""
    scheduler = BackgroundScheduler()
    
    # Verifica vencimentos a cada 6 horas
    scheduler.add_job(
        verificar_vencimentos,
        'interval',
        hours=6,
        args=[bot],
        id='verificar_vencimentos'
    )
    
    # Envia avisos de vencimento diariamente às 10h
    scheduler.add_job(
        enviar_avisos_vencimento,
        'cron',
        hour=10,
        minute=0,
        args=[bot],
        id='avisos_vencimento'
    )
    
    # Verifica pagamentos pendentes a cada 30 minutos
    scheduler.add_job(
        verificar_pagamentos_pendentes,
        'interval',
        minutes=30,
        args=[bot],
        id='verificar_pagamentos'
    )
    
    # Divulga planos VIP no canal de prévias a cada 3 horas
    scheduler.add_job(
        divulgar_planos_previas,
        'interval',
        hours=3,
        args=[bot],
        id='divulgar_planos'
    )
    
    scheduler.start()
    logger.info("⏰ Agendador de tarefas iniciado!")
    logger.info("   - Verificação de vencimentos: a cada 6 horas")
    logger.info("   - Avisos de vencimento: diariamente às 10h")
    logger.info("   - Verificação de pagamentos: a cada 30 minutos")
    logger.info("   - Divulgação de planos (prévias): a cada 3 horas")
