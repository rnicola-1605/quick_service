from DB.BancoDB import Banco


class pesquisaUsuarios(object):
    """
    classe que possui os metodos que executam query dos usuarios
    """

    def __init__(self):
        self.query = None
        self.ok = None

    def busca_usuarios_cep_desatualizado(self):

        self.query = "SELECT * FROM usuarios WHERE latitude_atual IS NULL OR logitude_atual IS NULL;"

        self.conexao = Banco()
        cur = self.conexao.conectar()

        cur.execute(self.query)
        sql = cur.fetchall()
        cur.close()

        return sql

    def adicionar_servico(self, id_usuario, id_servico):

        self.query = "INSERT INTO usuarios_prestam_servicos (" +\
            "id_usuario," +\
            "id_servico) VALUES (%d, %d)"

        self.query % (id_usuario,
                      id_servico)

        self.conexao = Banco().conectar()

        try:
            self.conexao.execute(self.query)
            self.ok = True
        except Exception, e:
            self.ok = False

        self.conexao.close()

        return self.ok

    def _atualizaCep(self, bairro, cep, latitude, longitude,
                     logradouro, id_usuario):

        self.query = ("UPDATE usuarios SET " +\
                      # " bairro = '%s'" +\
                      " cep_atual = %s" +\
                      # ", logradouro = '%s'" +\
                      ", latitude_atual = %f" +\
                      ", logitude_atual = %f" +\
                      " WHERE id_usuario = %d;") % (cep,
                                                    float(latitude),
                                                    float(longitude),
                                                    id_usuario)

        try:
            self.conexao = Banco()
            cur = self.conexao.conectar()

            cur.execute(self.query)
            self.conexao.getConector().commit()
            self.ok = True
        except Exception, e:
            raise Exception(e)
            self.ok = False

        cur.close()

        return self.ok
