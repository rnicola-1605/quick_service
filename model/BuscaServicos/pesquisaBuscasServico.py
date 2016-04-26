from DB.BancoDB import Banco


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

    def busca_usuarios_proximos_by_coord(self, lat_busca,
                                         long_busca, lista_servico=[]):

        self.query = "SELECT" +\
                "u_cliente.id_usuario," +\
                "u_cliente.nome" +\
                "FROM " +\
                "usuarios_prestam_servicos ups" +\
                "INNER JOIN usuarios u_prestador ON u_prestador.id_usuario = ups.id_usuario " +\
                "INNER JOIN servicos s_prestador ON s_prestador.id_servico = ups.id_servico " +\
                "WHERE " +\
                " 1=1" +\
                " AND ups.cep_atual IS NOT NULL" +\
                " AND ups.latitude_atual IS NOT NULL" +\
                " AND ups.longitude_atual IS NOT NULL" +\
                " AND s_prestador.id_servico IN (%s)" +\
                " AND ups.valido is TRUE "


        return None
