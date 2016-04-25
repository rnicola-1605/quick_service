from DB.BancoDB import Banco


class BuscaServicos(object):
    """
    classe para buscar os servicos escolhidos mais proximo
    """

    def __init__(self):
        self.conexao = Banco().conectar()

    def buscarServicoProximo(self, usuario, servicos,
                             proximidade=5):

        query = ""
