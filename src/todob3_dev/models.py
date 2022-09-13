"""Neste arquivo, descreveremos a configuração do modelo (configuração do banco de dados) 
usando SQLAlchemy."""

import datetime
from .db import Base
# from db import Base
 
from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.dialects.mysql import INTEGER
 
 
class Task(Base):
  
  __tablename__ = 'task'
  
  id = Column(
    'id',
    INTEGER(),
    primary_key=True,
    autoincrement=True,
  )
  
  cr_data = Column('cr_data', String(11))
  
  codigo = Column(
    'codigo',
    String(5)
  )

  quantidade = Column('quantidade', Integer)
  valor_unitario = Column('valor_unitario', Float(10))
  tipo_op = Column('tipo_op', String(10))
  valor_total = Column('valor_total', Float(10)) # sem taxas
  tx_corretagem = Column('tx_corretagem', Float(10))
  tx_b3 = Column('tx_b3', Float(3))
  valor_operacao = Column('valor_op', Float(10)) # com taxas - precisa calcular
  

  def __init__(self, created_date: str, codigo: str,quantidade: int, 
               valor_unitario: float,  tipo_op: str, tx_corretagem: float=None,
               taxa_b3 : float = None):
    
    self.cr_data = created_date
    self.codigo = codigo
    self.quantidade = quantidade
    self.valor_unitario = valor_unitario
    self.valor_total = self.quantidade * self.valor_unitario
    self.tipo_op = tipo_op.lower()
    self.tx_corretagem = self.custo_corretagem(tx_corretagem)
    self.tx_b3 = self.custo_b3(taxa_b3)
    self.valor_operacao = self.operacao() # calcular + ou - as taxas
  
  
  # Calculando taxas
  def operacao(self):
    if self.tipo_op == 'compra':
      return self.valor_total + self.tx_corretagem + self.tx_b3 
    if self.tipo_op == 'venda':
      return self.valor_total - self.tx_corretagem - self.tx_b3
  
  
  def custo_b3(self, tx):
    if tx == None:
      return (self.valor_total * 0.03) / 100 # taxa padrão de 0.03%
    else:
      return (self.valor_total * tx) / 100
  
  
  def custo_corretagem(self, tx):
    if tx == None:
      return 2.5 # valor padrão de 2.5
    else:
      return tx
