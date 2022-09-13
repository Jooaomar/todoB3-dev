from datetime import datetime
from fastapi import FastAPI
from fastapi.responses import RedirectResponse, HTMLResponse

from starlette.requests import Request
from starlette.templating import Jinja2Templates
 
# import db
from . import db
from .models import Task
# from models import Task

from .bovespa.b3 import codigos

 
app = FastAPI(
  title='Aplicação ToDo feita com FastAPI',
  description='Tutorial FastAPI: Crie um aplicativo de tarefas simples com FastAPI (e starlette).',
  version='0.9 beta'
)


# configurações relacionadas ao modelo (jinja2)
templates = Jinja2Templates(directory="templates")
jinja_env = templates.env  # Jinja2.Environment : para filtro e configurações globais


def index(request: Request):
  task = db.session.query(Task).filter().all()
  task = [t for t in task]
  
  
  return templates.TemplateResponse('index.html',
                                    {'request': request,
                                     'task': task,
                                     'codigos': codigos}) 


async def get():
  """Exibição"""
  # Obter registros do usuário
  task = db.session.query(Task).filter().all()
  # db.session.commit()
  
  # lista de dados
  task = [t for t in task]
  
  return task
  

async def add(request: Request):
  
  # Obter dados do formulário HTML
  data = await request.form()
  cr_data = str(data['cr_data'])
  codigo = str(data['codigo'])
  quantidade = int(data['quantidade'])
  valor_unitario = float(data['valor_unitario'])
  tipo_op = str(data['tipo_op'])
  tx_corretagem = float(data['tx_corretagem'])
  tx_b3 = float(data['tx_b3'])
  
  # Crie uma nova tarefa e confirme
  task = Task(created_date=cr_data,codigo=codigo, quantidade=quantidade, valor_unitario=valor_unitario, 
              tipo_op=tipo_op, tx_corretagem=tx_corretagem, taxa_b3=tx_b3)
  
  db.session.add(task)
  db.session.commit()
  db.session.close()
  
  task = await get()
  
  return templates.TemplateResponse("index.html", 
                                    {"request": request,
                                     'codigos': codigos,
                                     'task': task})

  


async def update(request: Request, t_id):
  
  # Obter dados do formulário HTML
  data = await request.form()
  cr_data = str(data['cr_data'])
  codigo = str(data['codigo'])
  quantidade = int(data['quantidade'])
  valor_unitario = float(data['valor_unitario'])
  tipo_op = str(data['tipo_op'])
  valor_total = valor_unitario * quantidade # Calcula o total
  tx_corretagem = float(data['tx_corretagem'])
  tx_b3 = float(data['tx_b3'])
  
  custo_b3 = (valor_total * tx_b3) / 100
  
  if tipo_op == 'compra':
    valor_operacao = valor_total + tx_corretagem + custo_b3
  else:
    valor_operacao = valor_total - tx_corretagem - custo_b3
  
  try:
    db.session.query(Task).filter(Task.id == t_id).\
      update({Task.cr_data: cr_data,
              Task.codigo: codigo,
              Task.quantidade: quantidade,
              Task.valor_unitario: valor_unitario,
              Task.tipo_op: tipo_op,
              Task.valor_total: valor_total,
              Task.valor_operacao: valor_operacao,
              Task.tx_corretagem: tx_corretagem,
              Task.tx_b3: custo_b3}, synchronize_session='evaluate')
      
  except:
    """Problema resolvido: rollback não é executado até que chamemos rollback 
    explicitamente a 'session.query' """
    db.session.rollback()
    
  
  db.session.commit()
  db.session.close()
  
  return RedirectResponse("/")



async def delete(request: Request, t_id):
  
  # Obter tarefa correspondente e excluir
  try:
    db.session.query(Task).filter(Task.id == t_id).delete()
  except:
    """Problema resolvido: rollback não é executado até que chamemos rollback 
    explicitamente a 'session.query' """
    db.session.rollback()

  db.session.commit()
  db.session.close()
  
  # Atualisa lista
  task = await get()

  return templates.TemplateResponse("index.html", 
                                    {"request": request,
                                     "task": task,
                                     "codigos": codigos})