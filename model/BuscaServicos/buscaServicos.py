from DB.BancoDB import Banco
from pesquisaBuscasServico import pesquisaBuscaServico


class BuscaServicos(object):
    """
    classe para buscar os servicos escolhidos mais proximo
    """

    def __init__(self):
        self.conexao = Banco().conectar()
        self.pesquisa = pesquisaBuscaServico()

    def buscarServicoProximo(self, usuario, servicos,
                             proximidade=5):

        query = ""
