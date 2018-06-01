import hashlib as hs
import sqlite3 as sql
from pathlib import Path

DEBUG_FLAG = True

database = 'srcb.db'
#myFile = Path(database)
#if myFile.is_file():
    #run the script to create the db

db_connection = sql.connect(database)
db_cursor = db_connection.cursor()

class EquipeDeReparo(object):
    def __init__(self, numeroDePessoas, funcionarios):
        self.numeroDePessoas = numeroDePessoas
        self.funcionarios = ",".join(funcionarios)
        self.identificador = hs.sha224(self.funcionarios.encode('utf-8')).hexdigest()
        # o paramentro passado deve ser uma lista de strings com os nomes dos func

    def mostrar_equipe_de_reparo(self):
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
                               'funcionarios': self.funcionarios})

            db_connection.commit()

            if DEBUG_FLAG:
                db_cursor.execute("SELECT * FROM equipeDeReparo WHERE identificador = :identificador ",
                                 {'identificador': self.identificador})
                print(db_cursor.fetchall())

            print('>> Nova equipe de reparos  adicionada a base de dados!\n')

        else:
            print('>> Equipe de reparo ja cadastrada!')
            if DEBUG_FLAG:
                print(lst)

    def remover_equipe_de_reparo_db(self):
        with db_connection:
            db_cursor.execute("DELETE FROM equipeDeReparo WHERE identificador = :identificador",
                              {'identificador': self.identificador})

    def atualizar_identificador(self):
        novo_identificador = hs.sha224(self.funcionarios.encode('utf-8')).hexdigest()
        with db_connection:
            db_cursor.execute("UPDATE equipeDeReparo SET identificador = :novo_identificador "
                              "WHERE identificador = :identificador",
                              {'novo_identificador': novo_identificador, 'identificador': self.identificador})

        self.identificador = novo_identificador

    def atualizar_numeroDePessoas(self, novo_valor):
        self.numeroDePessoas = novo_valor
        with db_connection:
            db_cursor.execute("UPDATE equipeDeReparo SET numeroDePessoas = :numeroDePessoas WHERE identificador = :identificador",
                              {'numeroDePessoas': self.numeroDePessoas, 'identificador': self.identificador})

    def atualizar_funcionarios(self, novo_valor):
        self.funcionarios = novo_valor
        with db_connection:
            db_cursor.execute("UPDATE dano SET funcionarios = :funcionarios WHERE identificador = :identificador",
                              {'funcionarios': self.funcionarios, 'identificador': self.identificador})

        self.atualizar_identificador()

