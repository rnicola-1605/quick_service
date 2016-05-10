from flask import Flask, request, current_app, render_template
from model.usuarios import UsuariosPersistencia
from model.BuscaServicos.buscaServicos import BuscaServicos


class Usuarios(object):
    """
    Classe controller para usuarios
    """

    def __init__(self):
        self.uPersistencia = UsuariosPersistencia()

    def buscar_usuario(self, dados={}):
        """
        Busca dados de um usuario
        """

        self.user = self.uPersistencia.buscarUsuario(
            id_usuario=dados['id_usuario'],
            email=dados['email'])

        if self.user.getId():
            return {'status': 0,
                    'msg': 'usuario nao encontrado',
                    'dados': self.user.getToString()}
        else:
            return {'status': 1,
                    'msg': 'usuario encontrado',
                    'dados': self.user.getToString()}

    def cadastrar_usuario(self, dados={}):
        """
        Recebe na request dicionarios com as informacoes
        necessarias para cadastrar um novo usuario
        """

        if self.busca_usuario(email=dados['email']):
            # retorna false pois ja existe usuario cadastrado com
            # tal email e assim o novo cadastrado nao foi efetuado
            # com sucesso
            return {'status': False,
                    'msg': 'usuario ja existe',
                    'dados': dados}
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

            return {'status': res,
                    'msg': (res and 'usuario cadastrado com sucesso' or
                            'usuario nao cadastrado'),
                    'dados': self.user.getToString()}

    def adiciona_servico(self, dados={}):
        """
        Recebe na request dict com dados para cadastrar novo servico
        em usuario
        """

        self.user = self.uPersistencia.buscarUsuario(
            id_usuario=dados['id_usuario'])

        if not self.user.getId():
            return {'status': False,
                    'msg': 'usuario nao existe',
                    'dados': dados}
        elif self.user.getIdTipo() != 2:
            # apenas usuarios do tipo prestador (2) podem adicionar
            # servicos
            return {'status': False,
                    'msg': 'adicionar servico apenas valido para prestadores',
                    'dados': dados}
        else:
            # instancia da model de servicos
            self.srv = BuscaServicos()

            if self.srv.busca_servico_usuario(id_usuario=self.user.getId(),
                                              id_servico=dados['id_servico']):
                # usuario ja presta o servico solicitado para cadastrar.
                # entao retornamos msg de operacao nao concluida
                return {'status': 0,
                        'msg': (('%s (%d) ja presta esse servico,' +
                                 ' operacao cancelada.') % (self.getNome(),
                                                            self.getId())),
                        'dados': dados}

            res = self.user.adicionar_servico(id_servico=dados['id_servico'])

            return {'status': (res and 1 or 0),
                    'msg': (res and 'servico cadastrado com sucesso' or
                            'servico nao cadastrado'),
                    'dados': dados}

    def deleta_servico(self, dados={}):
        """
        Recebe na request dict para deletar um servico que um prestador
        presta
        """

        self.user = self.uPersistencia.buscarUsuario(
            id_usuario=dados['id_usuario'])

        if not self.user.getId():
            return {'status': False,
                    'msg': 'usuario nao existe',
                    'dados': dados}
        elif self.user.getIdTipo() != 2:
            # apenas usuarios do tipo prestador (2) podem adicionar
            # servicos
            return {'status': False,
                    'msg': 'deletar servicos valido apenas para prestadores',
                    'dados': dados}
        else:
            res = self.user.deletar_servico(id_servico=dados['id_servico'])

            return {'status': (res and 1 or 0),
                    'msg': (res and 'servico deletado com sucesso' or
                            'servico nao cadastrado'),
                    'dados': dados}

    def atualiza_usuario(self, dados={}):
        """
        Atualiza dados de um usuario ja existente
        """

        if self.busca_usuario(id_usuario=dados['id_usuario']):
            self.user = self.uPersistencia.buscarUsuario(
                id_usuario=dados['id_usuario'])
            return None
        else:
            return {'status': False,
                    'msg': 'nenhum usuario encontrado',
                    'dados': dados}

    def busca_usuario(self, id_usuario=None, email=None):
        """
        Busca se um usuario ja existe cadastrado a partir de id ou email
        """

        if self.uPersistencia.buscarUsuario(id_usuario=id_usuario,
                                            email=email).getId():
            return True
        return False
