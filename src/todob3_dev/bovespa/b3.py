import pandas as pd

pd.set_option('display.min_rows', 50)
pd.set_option('display.max_rows', 200)

def busca_carteira_teorica(indice):
  url = 'http://bvmf.bmfbovespa.com.br/indices/ResumoCarteiraTeorica.aspx?Indice={}&idioma=pt-br'.format(indice.upper())
  return pd.read_html(url, decimal=',', thousands='.', index_col='Código')[0][:-1]



ibov = busca_carteira_teorica('ibov')

lista = ibov.sort_values('Part. (%)', ascending=False)

codigos = lista.index