import os
from usuario import Usuario
from servicos import Servico, ServicosPersistencia


class Cliente(object, Usuario):
    """
    Classe abstrata do cliente que herda do usuario
    """

    def __init__(self, id_usuario=None, id_tipo_usuario=None,
                 nome=None, ddd_telefone=None, telefone=None,
                 ddd_celular=None, celular=None,
                 email=None, cep_atual=None,
                 latidade_atual=None, longitude_atual=None):
    
        Usuario.__init__(self, id_usuario=None, id_tipo_usuario=2,
                         nome=None, ddd_telefone=None, telefone=None,
                         ddd_celular=None, celular=None,
                         email=None, cep_atual=None,
                         latidade_atual=None, longitude_atual=None)

        self.servicos_buscados = [Servico()]


class ClientePersistente(Cliente):
    """
    classe persistente do objeto usuario que grava, mapeia e atualiza
    """

    def __init__(self, id_usuario=None, id_tipo_usuario=None,
                 nome=None, ddd_telefone=None, telefone=None,
                 ddd_celular=None, celular=None,
                 email=None, cep_atual=None,
                 latidade_atual=None, longitude_atual=None):

        Cliente.__init__(id_usuario=id_usuario,
                         id_tipo_usuario=id_tipo_usuario,
                         nome=nome, ddd_telefone=ddd_telefone,
                         telefone=telefone,
                         ddd_celular=ddd_celular, celular=celular,
                         email=email, cep_atual=cep_atual,
                         latidade_atual=latidade_atual,
                         longitude_atual=longitude_atual)
