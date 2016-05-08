from DB.BancoDB import Banco
from usuario import Usuario
from pesquisaUsuarios import pesquisaUsuarios
from prestador import Prestador, PrestadorPersistente
from cliente import Cliente, ClientePersistente


class UsuariosPersistencia(object):
    """
    Classe persistencia de usuarios que permite gerenciar objetos
    do tipo usuario
    """

    def __init__(self):
        self.conexao = Banco().conectar()
        self.pesquisa = pesquisaUsuarios()

    def criaUsuario(self, id_usuario=None, id_tipo_usuario=None,
                    nome=None, ddd_telefone=None, telefone=None,
                    ddd_celular=None, celular=None,
                    email=None, cep_atual=None,
                    latitude_atual=None, longitude_atual=None):

        if id_tipo_usuario is None or not id_tipo_usuario:
            return UsuariosPersistente(id_usuario=id_usuario,
                                       id_tipo_usuario=id_tipo_usuario,
                                       nome=nome, ddd_telefone=ddd_telefone,
                                       telefone=telefone,
                                       ddd_celular=ddd_celular, celular=celular,
                                       email=email, cep_atual=cep_atual,
                                       latitude_atual=latitude_atual,
                                       longitude_atual=longitude_atual)
        elif id_tipo_usuario == 1:
            return PrestadorPersistente(id_usuario=id_usuario,
                                        id_tipo_usuario=id_tipo_usuario,
                                        nome=nome, ddd_telefone=ddd_telefone,
                                        telefone=telefone,
                                        ddd_celular=ddd_celular, celular=celular,
                                        email=email, cep_atual=cep_atual,
                                        latitude_atual=latitude_atual,
                                        longitude_atual=longitude_atual)
        elif id_tipo_usuario == 2:
            return ClientePersistente(id_usuario=id_usuario,
                                      id_tipo_usuario=id_tipo_usuario,
                                      nome=nome, ddd_telefone=ddd_telefone,
                                      telefone=telefone,
                                      ddd_celular=ddd_celular, celular=celular,
                                      email=email, cep_atual=cep_atual,
                                      latitude_atual=latitude_atual,
                                      longitude_atual=longitude_atual)

    def buscarUsuario(self, id_usuario=None,
                      email=None):

        if ((not id_usuario and not email) or
                (id_usuario is None and email is None)):
            return [{}]

        query = "SELECT * FROM usuarios WHERE 1 = 1 "

        if id_usuario and isinstance(id_usuario, int) and id_usuario > 0:
            query += " AND id_usuario = %d" % id_usuario
        if email and len(email) > 10:
            query += " AND email = '%s'" % email

        self.conexao = Banco()
        cur = self.conexao.conectar()
        cur.execute(query)
        sql = cur.fetchall()
        cur.close()

        for a in sql:
            return self.criaUsuario(
                id_usuario=a['id_usuario'],
                id_tipo_usuario=a['id_tipo_usuario'],
                nome=a['nome'],
                ddd_telefone=a['ddd_telefone'],
                telefone=a['telefone'],
                ddd_celular=a['ddd_celular'],
                celular=a['celular'],
                email=a['email'],
                cep_atual=a['cep_atual'],
                latitude_atual=a['latitude_atual'],
                longitude_atual=a['logitude_atual'])
        else:
            return self.criaUsuario()

    def buscaListaUsuarios(self, lista=None):

        lst = []

        if lista is None:
            for u in self.pesquisa.busca_usuarios_cep_desatualizado():
                u = dict(u)
                lst.append(self.criaUsuario(
                    id_usuario=u['id_usuario'],
                    id_tipo_usuario=u['id_tipo_usuario'],
                    nome=u['nome'],
                    email=u['email'],
                    cep_atual=u['cep_atual'],
                    latitude_atual=u['latitude_atual'],
                    longitude_atual=u['logitude_atual']))
        return lst


class UsuariosPersistente(Usuario):
    """
    classe persistente do objeto usuario que grava, mapeia e atualiza
    """

    def __init__(self, id_usuario=None, id_tipo_usuario=None,
                 nome=None, ddd_telefone=None, telefone=None,
                 ddd_celular=None, celular=None,
                 email=None, cep_atual=None,
                 latitude_atual=None, longitude_atual=None):

        Usuario.__init__(self, id_usuario=id_usuario,
                         id_tipo_usuario=id_tipo_usuario,
                         nome=nome, ddd_telefone=ddd_telefone,
                         telefone=telefone,
                         ddd_celular=ddd_celular, celular=celular,
                         email=email, cep_atual=cep_atual,
                         latitude_atual=latitude_atual,
                         longitude_atual=longitude_atual)
