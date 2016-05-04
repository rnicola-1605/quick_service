from pesquisaBuscasServico import pesquisaBuscaServico
from model.servicos import Servico

class BuscaServicos(object):
    """
    classe para buscar os servicos escolhidos mais proximo
    """

    def __init__(self):
        self.pesquisa = pesquisaBuscaServico()

    def buscarServicoProximo(self, usuario, servicos,
                             proximidade=4.99):

        pesquisa_srv = [Servico(id_servico=x) for x in servicos]

        return self.pesquisa.busca_usuarios_proximos_by_coord(
            objUsuario=usuario,
            lista_servico=pesquisa_srv)
