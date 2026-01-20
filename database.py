"""
Gerenciamento do Banco de Dados
"""
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
import config

Base = declarative_base()
engine = create_engine(config.DATABASE_URL)
Session = sessionmaker(bind=engine)


class Usuario(Base):
    """Modelo de Usuário"""
    __tablename__ = 'usuarios'
    
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    username = Column(String, nullable=True)
    nome = Column(String, nullable=True)
    plano = Column(String, nullable=False)  # 'fotos' ou 'completo'
    data_inicio = Column(DateTime, default=datetime.now)
    data_vencimento = Column(DateTime, nullable=False)
    ativo = Column(Boolean, default=True)
    aviso_enviado = Column(Boolean, default=False)
    
    def __repr__(self):
        return f"<Usuario {self.telegram_id} - {self.plano}>"
    
    def esta_vencido(self):
        """Verifica se o plano está vencido"""
        return datetime.now() > self.data_vencimento
    
    def dias_para_vencer(self):
        """Retorna quantos dias faltam para vencer"""
        delta = self.data_vencimento - datetime.now()
        return delta.days
    
    def precisa_avisar(self):
        """Verifica se precisa enviar aviso de vencimento"""
        dias = self.dias_para_vencer()
        return (dias <= config.DIAS_AVISO_VENCIMENTO and 
                dias > 0 and 
                not self.aviso_enviado and 
                self.ativo)


class Pagamento(Base):
    """Modelo de Pagamento"""
    __tablename__ = 'pagamentos'
    
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, nullable=False)
    plano = Column(String, nullable=False)
    valor = Column(Float, nullable=False)
    payment_id = Column(String, unique=True, nullable=True)  # ID do Mercado Pago
    status = Column(String, default='pending')  # pending, approved, rejected
    data_criacao = Column(DateTime, default=datetime.now)
    data_aprovacao = Column(DateTime, nullable=True)
    
    def __repr__(self):
        return f"<Pagamento {self.telegram_id} - {self.status}>"


def init_db():
    """Inicializa o banco de dados"""
    Base.metadata.create_all(engine)
    print("✅ Banco de dados inicializado!")


def get_session():
    """Retorna uma sessão do banco de dados"""
    return Session()


def criar_usuario(telegram_id, username, nome, plano, duracao_dias=30):
    """Cria um novo usuário"""
    session = get_session()
    try:
        # Verifica se usuário já existe
        usuario = session.query(Usuario).filter_by(telegram_id=telegram_id).first()
        
        if usuario:
            # Atualiza usuário existente
            usuario.plano = plano
            usuario.data_inicio = datetime.now()
            usuario.data_vencimento = datetime.now() + timedelta(days=duracao_dias)
            usuario.ativo = True
            usuario.aviso_enviado = False
        else:
            # Cria novo usuário
            usuario = Usuario(
                telegram_id=telegram_id,
                username=username,
                nome=nome,
                plano=plano,
                data_vencimento=datetime.now() + timedelta(days=duracao_dias)
            )
            session.add(usuario)
        
        session.commit()
        return usuario
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def get_usuario(telegram_id):
    """Busca um usuário pelo telegram_id"""
    session = get_session()
    usuario = session.query(Usuario).filter_by(telegram_id=telegram_id).first()
    session.close()
    return usuario


def desativar_usuario(telegram_id):
    """Desativa um usuário"""
    session = get_session()
    try:
        usuario = session.query(Usuario).filter_by(telegram_id=telegram_id).first()
        if usuario:
            usuario.ativo = False
            session.commit()
            return True
        return False
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def marcar_aviso_enviado(telegram_id):
    """Marca que o aviso de vencimento foi enviado"""
    session = get_session()
    try:
        usuario = session.query(Usuario).filter_by(telegram_id=telegram_id).first()
        if usuario:
            usuario.aviso_enviado = True
            session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def criar_pagamento(telegram_id, plano, valor, payment_id=None):
    """Cria um registro de pagamento"""
    session = get_session()
    try:
        pagamento = Pagamento(
            telegram_id=telegram_id,
            plano=plano,
            valor=valor,
            payment_id=payment_id
        )
        session.add(pagamento)
        session.commit()
        return pagamento
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def atualizar_status_pagamento(payment_id, status):
    """Atualiza o status de um pagamento"""
    session = get_session()
    try:
        pagamento = session.query(Pagamento).filter_by(payment_id=payment_id).first()
        if pagamento:
            pagamento.status = status
            if status == 'approved':
                pagamento.data_aprovacao = datetime.now()
            session.commit()
            return pagamento
        return None
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def get_usuarios_para_avisar():
    """Retorna usuários que precisam receber aviso de vencimento"""
    session = get_session()
    usuarios = session.query(Usuario).filter_by(ativo=True, aviso_enviado=False).all()
    usuarios_avisar = [u for u in usuarios if u.precisa_avisar()]
    session.close()
    return usuarios_avisar


def get_usuarios_vencidos():
    """Retorna usuários com assinatura vencida"""
    session = get_session()
    usuarios = session.query(Usuario).filter_by(ativo=True).all()
    usuarios_vencidos = [u for u in usuarios if u.esta_vencido()]
    session.close()
    return usuarios_vencidos
