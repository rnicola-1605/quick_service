from DB.BancoDB import Banco


class pesquisaUsuarios(object):
    """
    classe que possui os metodos que executam query dos usuarios
    """

    def __init__(self):
        self.query = None
        self.ok = None

    def inserir_usuario(self, id_tipo_usuario, nome, ddd_telefone, telefone,
                        ddd_celular, celular, email, cep_atual,
                        latitude, longitude, senha):

        self.query = """INSERT INTO usuarios (
            id_tipo_usuario,
            nome, ddd_telefone,
            telefone,  ddd_celular,
            celular, email, cep_atual,
            latitude_atual, longitude_atual, senha) VALUES( """

        self.query += "%d, %s" % (id_tipo_usuario, nome)

        self.query += (ddd_telefone is not None and
                       (", %d" % (ddd_telefone)) or ", null")
        self.query += (telefone is not None and
                       (", %d" % (telefone)) or ", null")
        self.query += (ddd_celular is not None and
                       (", %d" % (ddd_celular)) or ", null")
        self.query += (celular is not None and
                       (", %d" % (celular)) or ", null")
        self.query += (email is not None and
                       (", %s" % (email)) or ", null")
        self.query += (cep_atual is not None and
                       (", %s" % (cep_atual)) or ", null")
        self.query += (latitude is not None and
                       (", %f" % (latitude)) or ", null")
        self.query += (longitude is not None and
                       (", %f" % (longitude)) or ", null")
        self.query += (senha is not None and
                       (", %s" % (senha)) or ", null")
        self.query += ");"

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

    def busca_usuarios_cep_desatualizado(self):

        self.query = "SELECT * FROM usuarios WHERE latitude_atual IS NULL OR logitude_atual IS NULL;"

        self.conexao = Banco()
        cur = self.conexao.conectar()

        cur.execute(self.query)
        sql = cur.fetchall()
        cur.close()

        return sql

    def adicionar_servico(self, id_usuario, id_servico):

        self.query = """INSERT INTO usuarios_prestam_servicos (
                        id_usuario,
                        id_servico) VALUES (%d, %d)"""

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

    def _atualizaCep(self, cep, latitude, longitude,
                     id_usuario):

        self.query = ("UPDATE usuarios SET " +
                      " cep_atual = %s" +
                      ", latitude_atual = %f" +
                      ", logitude_atual = %f" +
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
