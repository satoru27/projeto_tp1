import hashlib as hs
import sqlite3 as sql
from pathlib import Path


database = 'srcb.db'
#myFile = Path(database)
#if myFile.is_file():
    #run the script to create the db

db_connection = sql.connect(database)
db_cursor = db_connection.cursor()

class EquipeDeReparo(object):
    def __init__(self, identificador, numeroDePessoas, funcionarios):
        self.identificador = identificador
        self.numeroDePessoas = numeroDePessoas
        self.funcionarios = funcionarios

    def mostrarEquipeDeReparo(self):
        print(f''' <Equipe de reparo>
        Identificador: {self.identificador}
        Numero de pessoas: {self.numeroDePessoas}
        Funcionarios: {self.funcionarios}
        ''')

    def inserir_equipe_de_reparo_db(self):
        db_cursor.execute("SELECT * FROM equipeDeReparo WHERE identificador = :identificador ",
                          {'identificador': self.identificador})

        lst = db_cursor.fetchall()

        if not lst:  # se nao encontrarmos o registro o colocamos na database
            db_cursor.execute("INSERT INTO equipeDeReparo VALUES(:identificador, :numeroDePessoas, :funcionarios)",
                              {'identificador':self.identificador, 'numeroDePessoas': self.numeroDePessoas,
                               'funcionario': self.funcionarios})

            db_connection.commit()

            #debug
            #db_cursor.execute("SELECT * FROM cidadao WHERE identificador = :identificador ",
            #                  {'identificador': self.identificador})
            #print(db_cursor.fetchall())

            print('>> Novo  adicionado a base de dados!\n')

        else:
            print('>>  ja cadastrado!')
            #debug
            #print(lst)
