class Dano(object):
    def __init__(self, idDano, tipoDeDano, pagamento, idBuraco, idCidadao):
        self.idDano = idDano
        self.tipoDeDano = tipoDeDano
        self.pagamento = pagamento
        self.idBuraco = idBuraco
        self.idCidadao = idCidadao

    def mostrarDano(self):
        print(f'''<Dano> 
        Identificador do Dano: {self.idDano}
        Tipo de Dano: {self.tipoDeDano}
        Pagamento: {self.pagamento}
        Identificador do Buraco: {self.idBuraco}
        Cidadao que recebeu o dano: {self.idCidadao}
        ''')
