import os
from usuario import Usuario
from servicos import Servico, ServicosPersistencia
from cep.cep import *


class Prestador(object, Usuario):
    """
    Classe abstrata do prestador que herda do usuario
    """

    def __init__(self, id_usuario=None, id_tipo_usuario=None,
                 nome=None, ddd_telefone=None, telefone=None,
                 ddd_celular=None, celular=None,
                 email=None, cep_atual=None,
                 latidade_atual=None, longitude_atual=None):

        Usuario.__init__(self, id_usuario=None, id_tipo_usuario=1,
                         nome=None, ddd_telefone=None, telefone=None,
                         ddd_celular=None, celular=None,
                         email=None, cep_atual=None,
                         latidade_atual=None, longitude_atual=None)

        self.servicos_prestados = [Servico()]


class PrestadorPersistente(Prestador):
    """
    classe persistente do objeto usuario que grava, mapeia e atualiza
    """

    self.cepPersistencia = CepData()

    def __init__(self, id_usuario=None, id_tipo_usuario=None,
                 nome=None, ddd_telefone=None, telefone=None,
                 ddd_celular=None, celular=None,
                 email=None, cep_atual=None,
                 latidade_atual=None, longitude_atual=None):

        Prestador.__init__(id_usuario=id_usuario,
                           id_tipo_usuario=id_tipo_usuario,
                           nome=nome, ddd_telefone=ddd_telefone,
                           telefone=telefone,
                           ddd_celular=ddd_celular, celular=celular,
                           email=email, cep_atual=cep_atual,
                           latidade_atual=latidade_atual,
                           longitude_atual=longitude_atual)

    def atualizar_cpf(self, cep_novo):
        self.conexao = Banco().conectar()

        cep_novo = cep2str(cep_novo)

        if cep_novo != self.getCep():
            return self.cepPersistencia.get_cep_full(cep=cep_novo)

        self.conexao.close()
