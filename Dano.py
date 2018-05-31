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
