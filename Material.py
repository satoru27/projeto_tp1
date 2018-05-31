import hashlib as hs
import sqlite3 as sql
from pathlib import Path


database = 'srcb.db'
#myFile = Path(database)
#if myFile.is_file():
    #run the script to create the db

db_connection = sql.connect(database)
db_cursor = db_connection.cursor()

class Material(object):
    def __init__(self, codigo, descricao, valor, quantidade, tipo):
        self.codigo = codigo
        self.descricao = descricao
        self.valor = valor
        self.quantidade = quantidade
        self.tipo = tipo

    def calculaCustoMaterial(self):
        pass

    def mostraMaterial(self):
        print(f'''<Informacoes do material>
          Codigo: {self.codigo}
          Descricao: {self.descricao}
          Valor:v{self.valor}
          Quantidade: {self.quantidade}
          Tipo: {self.tipo}''')

    def inserir_material_db(self):
        db_cursor.execute("SELECT * FROM material WHERE codigo = :codigo ",
                          {'identificador': self.codigo})

        lst = db_cursor.fetchall()

        if not lst:  # se nao encontrarmos o registro o colocamos na database
            db_cursor.execute("INSERT INTO material VALUES(:codigo, :descricao, :valor, :quantidade, :tipo)",
                              {'codigo':self.codigo, 'descricao':self.descricao, 'valor':self.valor, 'quantidade':self.quantidade, 'tipo':self.tipo})

            db_connection.commit()

            #debug
            #db_cursor.execute("SELECT * FROM cidadao WHERE identificador = :identificador ",
            #                  {'identificador': self.identificador})
            #print(db_cursor.fetchall())

            print('>> Novo  material adicionado a base de dados!\n')

        else:
            print('>> Material  ja cadastrado!')
            #debug
            #print(lst)