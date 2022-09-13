"""Aqui escrevemos as rotas e endpoints"""
from .controllers import *
# from controllers import *


""" Funções de roteamento FastAPI: Para aplicação do lado do usuário (GUI)"""
app.add_api_route('/', index, methods=['POST','GET'])
app.add_api_route('/{t_id}/', delete)
app.add_api_route('/add', add, methods=['POST', 'GET']) 
app.add_api_route('/update/{t_id}', update, methods=['POST']) 