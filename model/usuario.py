from DB.BancoDB import Banco
import os


class Usuario(object):
    """
    Classe abstrata de usuario
    """

    def __init__(self, id_usuario=None, id_tipo_usuario=None,
                 nome=None, ddd_telefone=None, telefone=None,
                 ddd_celular=None, celular=None,
                 email=None, cep_atual=None,
                 latitude_atual=None, longitude_atual=None):
        self.id_usuario = id_usuario
        self.id_tipo_usuario = id_tipo_usuario
        self.nome = nome
        self.ddd_telefone = ddd_telefone
        self.telefone = telefone
        self.ddd_celular = ddd_celular
        self.celular = celular
        self.email = email
        self.cep_atual = cep_atual
        self.latitude_atual = latitude_atual
        self.longitude_atual = longitude_atual

    def getId(self):
        return self.id_usuario

    def getNome(self):
        return self.nome

    def getIdTipo(self):
        return self.id_tipo_usuario

    def getCep(self):
        return self.cep_atual

    def getLatitude(self):
        return self.latitude_atual

    def getLongitude(self):
        return self.longitude_atual

    def setId(self, id):
        self.id_usuario = id

    def setNome(self, nome):
        self.nome = nome

    def setIdTipo(self, id):
        self.id_tipo_usuario = id

    def setCep(self, c):
        self.cep_atual = c

    def setLatitude(self, l):
        self.latitude_atual = l

    def setLongitude(self, l):
        self.longitude_atual = l

    def persiste(self, id_usuario, id_tipo_usuario,
                 nome, ddd_telefone, telefone,
                 ddd_celular, celular,
                 email, cep_atual,
                 latitude_atual, longitude_atual):

        self.setId(id_usuario)
        self.setNome(nome)
        self.id_tipo_usuario = id_tipo_usuario
        self.ddd_telefone = ddd_telefone
        self.telefone = telefone
        self.ddd_celular = ddd_celular
        self.celular = celular
        self.email = email
        self.cep_atual = cep_atual
        self.latitude_atual = latitude_atual
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
                'logitude_atual': self.longitude_atual}

    def inserir(self):

        self.conexao = Banco().conectar()

        query = "INSERT INTO usuarios (" +\
            "id_tipo_usuario," +\
            "nome, ddd_telefone," +\
            "telefone,  ddd_celular," +\
            "celular, email, cep_atual," +\
            "latitude_atual, longitude_atual, senha) VALUES(" +\
            "%d, %s, %d, %d, %d, %d, %s, %s, %f, %f, %s);"

        query % (self.getIdTipo(), self.getNome(),
                 self.ddd_telefone, self.telefone,
                 self.ddd_celular, self.celular,
                 self.email,
                 self.cep_atual and self.cep_atual or 'null',
                 self.latitude_atual and self.latitude_atual or 'null',
                 self.longitude_atual and self.longitude_atual or 'null')

        self.conexao.execute(query)

        self.conexao.close()

    def mapear(self):

        self.conexao = Banco().conectar()

        query = "UPDATE usuarios SET nome = %s " +\
            " AND ddd_telefone = %d" +\
            " AND telefone = %d" +\
            " AND ddd_celular = %d" +\
            " AND celular = %d" +\
            " AND email = %s" +\
            " AND cep_atual = %s" +\
            " AND latitude_atual = %f" +\
            " AND longitude_atual = %f"

        query % (self.getNome(),
                 self.ddd_telefone, self.telefone,
                 self.ddd_celular, self.celular,
                 self.email,
                 self.cep_atual and self.cep_atual or 'null',
                 self.latitude_atual and self.latitude_atual or 'null',
                 self.longitude_atual and self.longitude_atual or 'null')

        if self.getId() and self.getId() > 0:
            query += " WHERE id_usuario = %d"

        query % self.getId()

        self.conexao.execute(query)

        self.conexao.close()
