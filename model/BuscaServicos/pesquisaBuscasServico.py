from model.DB.BancoDB import Banco


class pesquisaBuscaServico(object):
    """
    classe que possui os metodos que executam query dos usuarios
    """

    def __init__(self):
        self.query = None
        self.ok = None

    def busca_usuarios_proximos_by_cep(self, cep_busca):

        self.query = ""

        return None

    def busca_usuarios_proximos_by_coord(self, objUsuario, lat_busca=None,
                                         long_busca=None, lista_servico=[]):

        self.conexao = Banco()
        cur = self.conexao.conectar()

        self.query = """SELECT
                u_prestador.id_usuario,
                u_prestador.nome,
                s_prestador.id_servico,
                s_prestador.servico
            FROM 
                usuarios_prestam_servicos ups
                INNER JOIN usuarios u_prestador ON u_prestador.id_usuario = ups.id_usuario 
                INNER JOIN servicos s_prestador ON s_prestador.id_servico = ups.id_servico 
            WHERE 
                 1=1
                 AND u_prestador.cep_atual IS NOT NULL
                 AND u_prestador.latitude_atual IS NOT NULL
                 AND u_prestador.logitude_atual IS NOT NULL
                 AND s_prestador.id_servico IN (%s)
                 AND ups.valido is TRUE 
                 AND calcular_distancia_geo(%f,%f,u_prestador.latitude_atual,u_prestador.logitude_atual) between 0.00 and 4.99;"""

        self.query = self.query % (','.join(str(x.getId()) for x in lista_servico),
                                   objUsuario.getLatitude(),
                                   objUsuario.getLongitude())
        cur.execute(self.query)
        sql = cur.fetchall()
        cur.close()

        return sql
