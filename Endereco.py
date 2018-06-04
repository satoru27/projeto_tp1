class Endereco(object):
    """classe de suporte para armazenar o endereco de forma estruturada
    no banco de dados ele e armazenado como uma concatenacao
    de cidade,uf e bairro separados por virgula
    """
    def __init__(self, cidade: object, uf: object, bairro: object) -> object:
        self.cidade = cidade
        self.uf = uf
        self.bairro = bairro

    def mostrar_endereco(self):
        print(f''' \t<Endereco>
        \tCidade: {self.cidade}
        \tUF: {self.uf}
        \tBairro: {self.bairro}
        ''')

    def string_endereco(self):
        return ",".join([self.cidade, self.uf, self.bairro])
