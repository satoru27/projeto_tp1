import hashlib as hs
import sqlite3 as sql
from pathlib import Path

from Endereco import Endereco

DEBUG_FLAG = True

database = 'srcb.db'
#myFile = Path(database)
#if myFile.is_file():
    #run the script to create the db

db_connection = sql.connect(database)
db_cursor = db_connection.cursor()


class Dano(object):
    def __init__(self, tipoDeDano, pagamento, idBuraco, idCidadao):
        self.idDano = hs.sha224((tipoDeDano+idBuraco+idCidadao).encode('utf-8')).hexdigest()
        self.tipoDeDano = tipoDeDano
        self.pagamento = pagamento
        self.idBuraco = idBuraco
        self.idCidadao = idCidadao

    def mostrar_dano(self):
        print(f'''<Dano> 
        Identificador do Dano: {self.idDano}
        Tipo de Dano: {self.tipoDeDano}
        Pagamento: {self.pagamento}
        Identificador do Buraco: {self.idBuraco}
        Cidadao que recebeu o dano: {self.idCidadao}
        ''')

    def inserir_dano_db(self):
        db_cursor.execute("SELECT * FROM dano WHERE idDano = :idDano ", {'idDano': self.idDano})

        lst = db_cursor.fetchall()

        if not lst:  # se nao encontrarmos o registro o colocamos na database
            db_cursor.execute("INSERT INTO dano VALUES(:idDano, :tipoDeDano, :pagamento, :idBuraco, :idCidadao)",
                              {'idDano':self.idDano, 'tipoDeDano':self.tipoDeDano, 'pagamento':self.pagamento,
                               'idBuraco':self.idBuraco, 'idCidadao':self.idCidadao})

            db_connection.commit()

            if DEBUG_FLAG:
                db_cursor.execute("SELECT * FROM dano WHERE idDano = :idDano ", {'idDano': self.idDano})
                print(db_cursor.fetchall())

            print('>> Novo dano adicionado na base de dados!\n')

        else:
            print('>> Dano ja cadastrado!')
            if DEBUG_FLAG:
                print(lst)

    def remover_dano_db(self):
        with db_connection:
            db_cursor.execute("DELETE FROM dano WHERE idDano = :idDano",
                              {'idDano': self.idDano})

    # atualizacoes
    # tipoDeDano, pagamento, idBuraco, idCidadao
    def atualizar_idDano(self):
        novo_id = hs.sha224((self.tipoDeDano + self.idBuraco + self.idCidadao).encode('utf-8')).hexdigest()
        with db_connection:
            db_cursor.execute("UPDATE dano SET idDano = :novo_id WHERE idDano = :idDano",
                              {'novo_id': novo_id, 'idDano': self.idDano})

        self.idDano = novo_id

    def atualizar_tipoDeDano(self, novo_valor):
        self.tipoDeDano = novo_valor
        with db_connection:
            db_cursor.execute("UPDATE dano SET tipoDeDano = :tipoDeDano WHERE idDano = :idDano",
                              {'tipoDeDano': self.tipoDeDano, 'idDano': self.idDano})

        self.atualizar_idDano()

    def atualizar_pagamento(self, novo_valor):
        self.pagamento = novo_valor
        with db_connection:
            db_cursor.execute("UPDATE dano SET pagamento = :pagamento WHERE idDano = :idDano",
                              {'pagamento': self.pagamento, 'idDano': self.idDano})

    def atualizar_idBuraco(self, novo_valor):
        self.idBuraco = novo_valor
        with db_connection:
            db_cursor.execute("UPDATE dano SET idBuraco = :idBuraco WHERE idDano = :idDano",
                              {'idBuraco': self.idBuraco, 'idDano': self.idDano})

        self.atualizar_idDano()

    def atualizar_idCidadao(self, novo_valor):
        self.idCidadao = novo_valor
        with db_connection:
            db_cursor.execute("SELECT * FROM dano WHERE idDano = :idDano",
                              {'idDano': self.idDano})

            lst = db_cursor.fetchall()

            print(lst)

            db_cursor.execute("UPDATE dano SET idCidadao = :idCidadao WHERE idDano = :idDano",
                              {'idCidadao': self.idCidadao, 'idDano': self.idDano})
        self.atualizar_idDano()

