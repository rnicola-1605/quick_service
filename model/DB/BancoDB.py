import os
import urlparse
import psycopg2
import psycopg2.extras


class Banco(object):
    """
        Classe que controla o acesso ao banco
    """

    def __init__(self):

        urlparse.uses_netloc.append("postgres")
        url = urlparse.urlparse(os.environ["DATABASE_URL"])

        # self.conexao = 'dbname=quick_service user=postgres password=brd231616 host=localhost'
        self.conexao = 'dbname=%s user=%s password=%s host=%s port=%s' % (url.path[1:],
                                                                          url.username,
                                                                          url.password,
                                                                          url.hostname,
                                                                          url.port)
        self.conector = None

    def getConector(self):

        return self.conector

    def conectar(self):

        try:
            self.conector = psycopg2.connect(self.conexao)
            return self.conector.cursor(cursor_factory=psycopg2.extras.DictCursor)
        except Exception, e:
            print('Erro ao conectar no banco, erro: %s' % e)

    def testar_conexao(self):

        if self.conector is None or self.conector.closed:
            return False
        else:
            return True

        self.conector.close()
