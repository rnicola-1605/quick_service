import os


class Usuario(object):
    """
    Classe abstrata de usuario
    """

    def __init__(self, id_usuario=None, id_tipo_usuario=None,
                 nome=None, ddd_telefone=None, telefone=None,
                 ddd_celular=None, celular=None,
                 email=None, cep_atual=None,
                 latidade_atual=None, longitude_atual=None):
        self.id_usuario = id_usuario
        self.id_tipo_usuario = id_tipo_usuario
        self.nome = nome
        self.ddd_telefone = ddd_telefone
        self.telefone = telefone
        self.ddd_celular = ddd_celular
        self.celular = celular
        self.email = email
        self.cep_atual = cep_atual
        self.latidade_atual = latidade_atual
        self.longitude_atual = longitude_atual

    def getId(self):
        return self.id_usuario

    def getNome(self):
        return self.nome

    def setId(self, id):
        self.id_usuario = id

    def setNome(self, nome):
        self.nome = nome

    def persiste(self, id_usuario, id_tipo_usuario,
                 nome, ddd_telefone, telefone,
                 ddd_celular, celular,
                 email, cep_atual,
                 latidade_atual, longitude_atual):

        self.setId(id_usuario)
        self.setNome(nome)
        self.id_tipo_usuario = id_tipo_usuario
        self.ddd_telefone = ddd_telefone
        self.telefone = telefone
        self.ddd_celular = ddd_celular
        self.celular = celular
        self.email = email
        self.cep_atual = cep_atual
        self.latidade_atual = latidade_atual
        self.longitude_atual = longitude_atual

    def getToString(self):
        return {'id_usuario': self.getId(),
                'id_tipo_usuario': self.id_tipo_usuario,
                'nome': self.getNome(),
                'ddd_telefone': self.ddd_telefone,
                'telefone': self.telefone,
                'ddd_celular': self.ddd_celular,
                'celular': self.celular,
                'email': self.email,
                'cep_atual': self.cep_atual,
                'latitude_atual': self.latitude_atual,
                'logitude_atual': self.logitude_atual}

    def inserir(self):

        return 'nao implementado'

    def mapear(self):

        return 'nao implementado'
