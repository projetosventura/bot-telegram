"""
Gerenciamento de Pagamentos com Mercado Pago
"""
import mercadopago
import config
from database import criar_pagamento, atualizar_status_pagamento, get_session, Pagamento


class GerenciadorPagamentos:
    """Classe para gerenciar pagamentos via Mercado Pago"""
    
    def __init__(self):
        self.sdk = mercadopago.SDK(config.MERCADO_PAGO_ACCESS_TOKEN)
    
    def criar_link_pagamento(self, telegram_id, username, plano_tipo):
        """
        Cria um link de pagamento para o usuário
        
        Args:
            telegram_id: ID do usuário no Telegram
            username: Username do usuário
            plano_tipo: 'fotos' ou 'completo'
        
        Returns:
            dict com 'url' e 'payment_id'
        """
        # Define o plano
        if plano_tipo == 'fotos':
            plano = config.PLANO_FOTOS
        else:
            plano = config.PLANO_COMPLETO
        
        # Dados da preferência de pagamento (versão mínima para teste PIX)
        preference_data = {
            "items": [
                {
                    "id": f"{plano_tipo}_vip",
                    "title": plano['nome'],
                    "description": f"Assinatura mensal do plano {plano['nome']} com acesso ao grupo VIP exclusivo",
                    "category_id": "digital_content",
                    "quantity": 1,
                    "currency_id": "BRL",
                    "unit_price": plano['valor']
                }
            ],
            "payer": {
                "name": username or f"Usuario",
                "surname": f"TG{telegram_id}",
                "email": f"user{telegram_id}@telegram.bot"
            },
            "payment_methods": {
                "installments": 12
            },
            "external_reference": f"{telegram_id}_{plano_tipo}",
            "notification_url": "https://bot-telegram-production-cf50.up.railway.app/webhook",
            "back_urls": {
                "success": "https://t.me/Robert_VIP_bot",
                "failure": "https://t.me/Robert_VIP_bot",
                "pending": "https://t.me/Robert_VIP_bot"
            },
            "binary_mode": False
        }
        
        # Cria a preferência
        preference_response = self.sdk.preference().create(preference_data)
        preference = preference_response["response"]
        
        # Registra o pagamento no banco
        payment_id = preference.get("id")
        criar_pagamento(
            telegram_id=telegram_id,
            plano=plano_tipo,
            valor=plano['valor'],
            payment_id=payment_id
        )
        
        # Retorna URL de pagamento
        return {
            "url": preference.get("init_point"),  # URL para web
            "payment_id": payment_id
        }
    
    def verificar_pagamento(self, payment_id):
        """
        Verifica o status de um pagamento
        
        Args:
            payment_id: ID da preferência de pagamento
        
        Returns:
            dict com informações do pagamento
        """
        try:
            payment_info = self.sdk.payment().search({
                "external_reference": payment_id
            })
            
            if payment_info["response"]["results"]:
                resultado = payment_info["response"]["results"][0]
                status = resultado.get("status")
                
                # Atualiza status no banco
                atualizar_status_pagamento(payment_id, status)
                
                return {
                    "status": status,
                    "approved": status == "approved",
                    "payment_info": resultado
                }
            
            return {
                "status": "pending",
                "approved": False
            }
        except Exception as e:
            print(f"Erro ao verificar pagamento: {e}")
            return {
                "status": "error",
                "approved": False
            }
    
    def processar_webhook(self, data):
        """
        Processa notificações do webhook do Mercado Pago
        
        Args:
            data: Dados recebidos do webhook
        
        Returns:
            dict com informações processadas
        """
        try:
            # Tipo de notificação
            topic = data.get("topic") or data.get("type")
            
            if topic == "payment":
                payment_id = data.get("data", {}).get("id")
                
                # Busca informações do pagamento
                payment_info = self.sdk.payment().get(payment_id)
                payment = payment_info["response"]
                
                status = payment.get("status")
                external_reference = payment.get("external_reference")
                
                # Extrai telegram_id e plano da referência externa
                if external_reference:
                    parts = external_reference.split("_")
                    telegram_id = int(parts[0])
                    plano_tipo = parts[1]
                    
                    # Atualiza status no banco
                    atualizar_status_pagamento(payment_id, status)
                    
                    return {
                        "telegram_id": telegram_id,
                        "plano": plano_tipo,
                        "status": status,
                        "approved": status == "approved"
                    }
            
            return None
        except Exception as e:
            print(f"Erro ao processar webhook: {e}")
            return None


def gerar_link_pagamento(telegram_id, username, plano):
    """Função auxiliar para gerar link de pagamento"""
    gerenciador = GerenciadorPagamentos()
    return gerenciador.criar_link_pagamento(telegram_id, username, plano)
