"""AMOSTRAS: Cria banco de dados e inserir dados de amostra do usuário admin"""

from .models import *
from . import db
# import db

# Para formatação de data
from datetime import date

def criar_tabela():
  Base.metadata.create_all(db.engine)
 
  # adicionar a tabela uma tarefa de amostra
  task = Task(
    
    # created_date=date.today(),
    created_date='2022-09-09',  
    codigo='ITSA4',
    quantidade=100,
    valor_unitario = 20,
    tipo_op = 'Venda',
    # tx_corretagem = 2.5,
    # taxa_b3=0.06
    )

  db.session.add(task)
  db.session.commit()  

 
# if __name__ == "__main__":
  
#   # criar uma tabela
#   Base.metadata.create_all(db.engine)
 
#   # adicionar a tabela uma tarefa de amostra
#   task = Task(
#     quantidade=12,
#     valor_unitario = 3.30,
#     tipo_op = 'Venda',
#     tx_corretagem = 2.5,)

#   db.session.add(task)
#   db.session.commit()

#   db.session.close()  # Fechar sessão