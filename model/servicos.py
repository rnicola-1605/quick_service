from DB.BancoDB import Banco


class Servico(object):
    """
    Classe de servicos prestados ou buscados pelos usuarios
    """

    def __init__(self, id_servico=None,
                 servico=None, descricao=None):
        self.id_servico = id_servico
        self.servico = servico
        self.descricao = descricao

    def getId(self):
        return self.id_servico

    def getServico(self):
        return self.servico

    def getDescricao(self):
        return self.descricao

    def setId(self, id):
        self.id_servico = id

    def setServico(self, serv):
        self.servico = serv

    def setDescricao(self, des):
        self.descricao = des

    def getToString(self):
        return {'id_servico': self.getId(),
                'servico': self.getServico(),
                'descricao': self.getDescricao()}


class ServicosPersistencia(Servico):
    """
    Classe persistencia de servico que permite gerenciar objetos
    do tipo servico
    """

    def __init__(self):
        self.conexao = Banco().conectar()

    def buscaServico(self, id):

        query = 'SELECT * FROM  servicos WHERE 1=1 id_servico = %d' % (id)

        for s in self.conexao.execute(query):
            return Servico(id_servico=s.id_servico,
                           servico=s.servico,
                           descricao=s.descricao)

    def buscaListaServicos(self, lista):

        lista = []

        query = ('SELECT * FROM  servicos WHERE 1=1 id_servico IN (%s)') %\
            (','.join(str(x) for x in lista))

        for s in self.conexao.execute(query):
            lista.append(Servico(id_servico=s.id_servico,
                                 servico=s.servico,
                                 descricao=s.descricao))

        return lista
