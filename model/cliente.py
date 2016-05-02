import os
from usuario import Usuario
from pesquisaUsuarios import pesquisaUsuarios
from servicos import Servico, ServicosPersistencia
from cep.cep import *


class Cliente(Usuario):
    """
    Classe abstrata do cliente que herda do usuario
    """

    def __init__(self, id_usuario=None, id_tipo_usuario=None,
                 nome=None, ddd_telefone=None, telefone=None,
                 ddd_celular=None, celular=None,
                 email=None, cep_atual=None,
                 latitude_atual=None, longitude_atual=None):

        Usuario.__init__(self, id_usuario=id_usuario, id_tipo_usuario=2,
                         nome=nome, ddd_telefone=ddd_telefone,
                         telefone=telefone, ddd_celular=ddd_celular,
                         celular=celular, email=email,
                         cep_atual=cep_atual, latitude_atual=latitude_atual,
                         longitude_atual=longitude_atual)

        self.servicos_buscados = [Servico()]


class ClientePersistente(Cliente):
    """
    classe persistente do objeto usuario que grava, mapeia e atualiza
    """

    pesquisaUsuarios = pesquisaUsuarios()

    def __init__(self, id_usuario=None, id_tipo_usuario=None,
                 nome=None, ddd_telefone=None, telefone=None,
                 ddd_celular=None, celular=None,
                 email=None, cep_atual=None,
                 latitude_atual=None, longitude_atual=None):

        Cliente.__init__(id_usuario=id_usuario,
                         id_tipo_usuario=id_tipo_usuario,
                         nome=nome, ddd_telefone=ddd_telefone,
                         telefone=telefone,
                         ddd_celular=ddd_celular, celular=celular,
                         email=email, cep_atual=cep_atual,
                         latitude_atual=latitude_atual,
                         longitude_atual=longitude_atual)

    def atualizar_cep(self, cep_novo):

        cep_novo = cep2str(cep_novo)

        # if cep_novo != self.getCep():
        _dados = self.cepPersistencia.get_cep_full(cep=cep_novo)

        return self.pesquisaUsuarios._atualizaCep(
            bairro=_dados['bairro'],
            cep=_dados['cep'],
            latitude=_dados['latitude'],
            longitude=_dados['longitude'],
            logradouro=_dados['logradouro'])
