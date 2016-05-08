from pesquisaBuscasServico import pesquisaBuscaServico
from model.servicos import Servico


class BuscaServicos(object):
    """
    classe para buscar os servicos escolhidos mais proximo
    """

    def __init__(self):
        self.pesquisa = pesquisaBuscaServico()

    def busca_servicos(self, id_servico=None, lista=[],
                       id_tipo_servico=None):

        return self.pesquisa.busca_servicos(id_servico=id_servico,
                                            lista=lista,
                                            id_tipo_servico=id_tipo_servico)

    def buscarServicoProximo(self, usuario, servicos,
                             proximidade=4.99):

        pesquisa_srv = [Servico(id_servico=x) for x in servicos]

        return self.pesquisa.busca_usuarios_proximos_by_coord(
            objUsuario=usuario,
            lista_servico=pesquisa_srv)
