from flask import Flask, request, current_app, render_template
from model.BuscaServicos.buscaServicos import BuscaServicos


class Servicos(object):
    """
    Classe controller para servicos e busca de servicos
    """

    def __init__(self):
        self.sPersistencia = BuscaServicos()

    def buscar_servicos(self, id_servico=None, lista=None,
                        id_tipo_servico=None):
        """
        Retorna todos os servicos ou uma lista de servicos filtrados
        """

        lista = []

        for s in self.sPersistencia.busca_servicos(
                id_servico=id_servico,
                lista=lista,
                id_tipo_servico=id_tipo_servico):
            lista.append(dict(s))
        return lista

    def busca_servico_usuario(self, id_servico=None, id_usuario=None):
        """
        Busca se o o usuario possui o servico do request
        """

        return self.sPersistencia.\
            busca_servico_usuario(id_usuario=id_usuario,
                                  id_servico=id_servico)
