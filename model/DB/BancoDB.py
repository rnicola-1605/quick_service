import psycopg2
import psycopg2.extras


class Banco(object):
    """
        Classe que controla o acesso ao banco
    """

    def __init__(self):
        self.conexao = 'dbname=quick_service user=postgres password=brd231616 host=localhost'
        self.conector = None

    def getConector(self):

        return self.conector

    def conectar(self):

        print self.conexao

        try:
            self.conector = psycopg2.connect(self.conexao)
            self.conector = self.conector.cursor()
        except e:
            print('Erro ao conectar no banco, erro: %s' % e)

    def testar_conexao(self):

        #cursor = self.conector.cursor()

        if self.conector is None or self.conector.closed:
            return False
        else:
            return True
