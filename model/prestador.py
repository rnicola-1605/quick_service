import os
from usuario import Usuario
from pesquisaUsuarios import pesquisaUsuarios
from servicos import Servico, ServicosPersistencia
from cep.cep import *


class Prestador(Usuario):
    """
    Classe abstrata do prestador que herda do usuario
    """

    def __init__(self, id_usuario=None, id_tipo_usuario=None,
                 nome=None, ddd_telefone=None, telefone=None,
                 ddd_celular=None, celular=None,
                 email=None, cep_atual=None,
                 latitude_atual=None, longitude_atual=None):

        Usuario.__init__(self, id_usuario=id_usuario, id_tipo_usuario=1,
                         nome=nome, ddd_telefone=ddd_telefone,
                         telefone=telefone,
                         ddd_celular=ddd_celular, celular=celular,
                         email=email, cep_atual=cep_atual,
                         latitude_atual=latitude_atual,
                         longitude_atual=longitude_atual)

        self.servicos_prestados = [Servico()]


class PrestadorPersistente(Prestador):
    """
    classe persistente do objeto usuario que grava, mapeia e atualiza
    """

    cepPersistencia = CepData()
    pesquisaUsuarios = pesquisaUsuarios()

    def __init__(self, id_usuario=None, id_tipo_usuario=None,
                 nome=None, ddd_telefone=None, telefone=None,
                 ddd_celular=None, celular=None,
                 email=None, cep_atual=None,
                 latitude_atual=None, longitude_atual=None):

        Prestador.__init__(self, id_usuario=id_usuario,
                           id_tipo_usuario=id_tipo_usuario,
                           nome=nome, ddd_telefone=ddd_telefone,
                           telefone=telefone,
                           ddd_celular=ddd_celular, celular=celular,
                           email=email, cep_atual=cep_atual,
                           latitude_atual=latitude_atual,
                           longitude_atual=longitude_atual)

    def adicionar_servico(self, id_servico):

        if self.getId() and id_servico:
            self.pesquisaUsuarios.adicionar_servico(
                id_usuario=self.getId(),
                id_servico=id_servico)

    def deletar_servico(self, id_servico):

        if self.getId() and id_servico:
            self.pesquisaUsuarios.deletar_servico(
                id_usuario=self.getId(),
                id_servico=id_servico)

    def atualizar_cep(self, cep_novo):

        cep_novo = cep2str(cep_novo)

        _dados = self.cepPersistencia.get_cep_full(cep=cep_novo)

        if _dados:
            return self.pesquisaUsuarios._atualizaCep(
                cep=_dados['cep'],
                latitude=_dados['latitude'],
                longitude=_dados['longitude'],
                id_usuario=self.getId())

    def atualizar_cep_by_lat_long(self, lat_novo, long_novo):

        _dados = self.cepPersistencia.get_cep_by_lat_long(lat=lat_novo,
                                                          lngt=long_novo)

        return self.pesquisaUsuarios._atualizaCep(
            cep=_dados['cep'],
            latitude=_dados['latitude'],
            longitude=_dados['longitude'],
            id_usuario=self.getId())
