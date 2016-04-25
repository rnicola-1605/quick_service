from DB.BancoDB import Banco


class pesquisaUsuarios(object):
    """
    classe que possui os metodos que executam query dos usuarios
    """

    def __init__(self):
        self.query = None
        self.ok = None

    def _atualizaCep(self, bairro, cep, latitude, longitude,
                     logradouro, id_usuario):

        self.query = "UPDATE usuarios SET " +\
            "bairro = %s" +\
            ", cep_atual = %s" +\
            ", logradouro = %s" +\
            ", latitude_atual = %f" +\
            ", longitude_atual = %f" +\
            " WHERE id_usuario = %d;"

        self.query % (bairro,
                      cep,
                      logradouro,
                      latitude,
                      longitude,
                      id_usuario)

        self.conexao = Banco().conectar()

        try:
            self.conexao.execute(self.query)
            self.ok = True
        except Exception, e:
            self.ok = False

        self.conexao.close()

        return self.ok
