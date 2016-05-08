from flask import Flask, request, current_app, render_template
from model.usuarios import UsuariosPersistencia


class Usuarios(object):
    """
    Classe controller para usuarios
    """

    def __init__(self, app):
        self.app = app
        self.uPersistencia = UsuariosPersistencia()

    def cadastrar_usuario(self, dados={}):
        """
        Recebe na request dicionarios com as informacoes
        necessarias para cadastrar um novo usuario
        """

        if self.busca_usuario(dados['id_usuario'],
                              dados['email']):
            # retorna false pois ja existe usuario cadastrado com
            # tal email e assim o novo cadastrado nao foi efetuado
            # com sucesso
            return {'status': False, 'dados': dados}
        else:
            self.user = self.uPersistencia.criaUsuario(
                id_tipo_usuario=dados['id_tipo_usuario'],
                nome=dados['nome'],
                email=dados['email'],
                latitude_atual=dados['latitude'],
                longitude_atual=dados['longitude'],
                cep_atual=('cep' in dados.keys() and
                           dados['cep'] or
                           None),
                ddd_telefone=('ddd_telefone' in dados.keys() and
                              dados['ddd_telefone'] or None),
                telefone=('telefone' in dados.keys() and
                          dados['telefone'] or None),
                ddd_celular=('ddd_celular' in dados.keys() and
                             dados['ddd_celular'] or None),
                celular=('celular' in dados.keys() and
                         dados['celular'] or None))

            # persiste as informacoes no bd
            res = self.user.inserir()

            return {'status': res, 'dados': self.user.getToString()}

    def busca_usuario(self, id_usuario=None, email=None):
        """
        Busca se um usuario ja existe cadastrado a partir de id ou email
        """

        for u in self.uPersistencia.buscarUsuario(email=dados):
            return True
        return False
