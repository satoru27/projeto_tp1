import hashlib as hs
import sqlite3 as sql
from pathlib import Path


database = 'srcb.db'
#myFile = Path(database)
#if myFile.is_file():
    #run the script to create the db

db_connection = sql.connect(database)
db_cursor = db_connection.cursor()

class Buraco(object):
    def __init__(self, identificador, endereco, tamanho, localizacao, prioridade, registradoPor):
        self.identificador = identificador
        self.endereco = endereco
        self.tamanho = tamanho
        self.localizacao = localizacao
        self.prioridade = prioridade
        self.registradoPor = registradoPor

    def mostrarBuraco(self):
        print(f''' <Buraco>
        Identificador: {self.identificador}
        Endereco: {self.endereco}
        Tamanho: {self.tamanho}
        Localizacao: {self.localizacao}
        Prioridade: {self.prioridade}
        Registrado por: {self.registradoPor}
        ''')

    def inserir_buraco_db(self):
        db_cursor.execute("SELECT * FROM buraco WHERE identificador = :identificador ",
                          {'identificador': self.identificador})

        lst = db_cursor.fetchall()

        if not lst:  # se nao encontrarmos o registro o colocamos na database
            db_cursor.execute("INSERT INTO buraco VALUES(:identificador, :endereco, :tamanho, :localizacao,"
                              " :prioridade, :registradoPor)",
                              {'identificador': self.identificador, 'endereco': self.endereco.stringEndereco(),
                               'tamanho': self.tamanho, 'localizacao': self.localizacao, 'prioridade': self.prioridade,
                               'registradoPor': self.registradoPor})

            db_connection.commit()

            #debug
            #db_cursor.execute("SELECT * FROM cidadao WHERE identificador = :identificador ",
            #                  {'identificador': self.identificador})
            #print(db_cursor.fetchall())

            print('>> Novo buraco adicionado na base de dados!\n')

        else:
            print('>> Buraco ja cadastrado!')
            #debug
            #print(lst)

class OrdemDeTrabalho(Buraco):
    def __init__(self, identificador, endereco, tamanho, localizacao, prioridade, registradoPor, codigo, descricao,
                 situacao, equipeDeReparo, equipamentos, horasAplicadas):
        super(OrdemDeTrabalho, self).__init__(identificador, endereco, tamanho, localizacao, prioridade,
                                              registradoPor)
        self.codigo = codigo
        self.descricao = descricao
        self.situacao = situacao
        self.equipeDeReparo = equipeDeReparo
        self.equipamentos = equipamentos
        self.horasAplicadas = horasAplicadas

    def mostrarOrdemDeTrabalho(self):
        print(f''' <Ordem de Trabalho>
        Codigo: {self.codigo}
        Descricao: {self.descricao}
        Situacao: {self.situacao}
        Equipe de reparo: {self.equipeDeReparo}
        Equipamentos: {self.equipamentos}
        Horas aplicadas: {self.horasAplicadas}
        ''')

    def inserir_ordem_de_trabalho_db(self):
        db_cursor.execute("SELECT * FROM ordemDeTrabalho WHERE identificador = :identificador ",
                          {'identificador': self.identificador})

        lst = db_cursor.fetchall()
##VERIFICAR SE AS CLASSES BURACO, ORDEM DE TRABALHO E ETC SÃO NECESSARIAS A HERANCA
##POR UM LADO COLOCAR A HERANCA FACILITARIA A BUSCA POIS TODAS AS INFORMCOES
        if not lst:  # se nao encontrarmos o registro o colocamos na database
            db_cursor.execute("INSERT INTO ordemDeTrabalho VALUES(:identificador, :endereco, :tamanho, :localizacao,"
                              " :prioridade, :registradoPor, :codigo, :descricao,:situacao, :equipeDeReparo,"
                              " :equipamentos, :horasAplicadas)",
                              {'identificador': self.identificador, 'endereco': self.endereco.stringEndereco(),
                               'tamanho': self.tamanho, 'localizacao': self.localizacao, 'prioridade': self.prioridade,
                               'registradoPor': self.registradoPor, 'codigo': self.codigo, 'descricao': self.descricao,
                               'situacao': self.situacao, 'equipeDeReparo': self.equipeDeReparo,
                               'equipamentos': self.equipamentos, 'horasAplicadas': self.horasAplicadas})

            db_connection.commit()

            #debug
            #db_cursor.execute("SELECT * FROM cidadao WHERE identificador = :identificador ",
            #                  {'identificador': self.identificador})
            #print(db_cursor.fetchall())

            print('>> Nova ordem de trabalho adicionada na base de dados!\n')

        else:
            print('>> Ordem de trabalho ja cadastrada!')
            #debug
            #print(lst)

class Reparo(OrdemDeTrabalho):
    def __init__(self, identificador, endereco, tamanho, localizacao, prioridade, registradoPor, codigo, descricao, situacao,
                 equipeDeReparo, equipamentos, horasAplicadas, codigoReparo, descricaoReparo, status, materialUtilizado,
                 custo):
        super(Reparo, self).__init__(identificador, endereco, tamanho, localizacao, prioridade, registradoPor,
                                     codigo, descricao, situacao, equipeDeReparo, equipamentos, horasAplicadas)
        self.codigoReparo = codigoReparo
        self.descricaoReparo = descricaoReparo
        self.status = status
        self.materialUtilizado = materialUtilizado
        self.custo = custo

    def mostraReparo(self):
        print(f'''<Reparo>
        Codigo: {self.codigoReparo}
        Descricao: {self.descricaoReparo}
        Status: {self.status}
        Material: {self.materialUtilizado}
        Custo: {self.custo}
        ''')

    def calculaReparo(self):
        pass

    def inserir_reparo_db(self):
        db_cursor.execute("SELECT * FROM reparo WHERE reparo = :identificador ",
                          {'identificador': self.identificador})

        lst = db_cursor.fetchall()

        if not lst:  # se nao encontrarmos o registro o colocamos na database
            db_cursor.execute("INSERT INTO reparo VALUES(:identificador, :endereco, :tamanho, :localizacao,"
                              " :prioridade, :registradoPor, :codigo, :descricao,:situacao, :equipeDeReparo,"
                              " :equipamentos, :horasAplicadas, :codigoReparo, :descricaoReparo, :status,"
                              " :materialUtilizado,:custo)",
                              {'identificador': self.identificador, 'endereco': self.endereco.stringEndereco(),
                               'tamanho': self.tamanho, 'localizacao': self.localizacao, 'prioridade': self.prioridade,
                               'registradoPor': self.registradoPor, 'codigo': self.codigo, 'descricao': self.descricao,
                               'situacao': self.situacao, 'equipeDeReparo': self.equipeDeReparo,
                               'equipamentos': self.equipamentos, 'horasAplicadas': self.horasAplicadas,
                               'codigoReparo': self.codigoReparo, 'descricaoReparo': self.descricaoReparo,
                               'status': self.status, 'materialUtilizado': self.materialUtilizado,
                               'custo': self.custo
                               })

            db_connection.commit()

            #debug
            #db_cursor.execute("SELECT * FROM cidadao WHERE identificador = :identificador ",
            #                  {'identificador': self.identificador})
            #print(db_cursor.fetchall())

            print('>> Novo reparo adicionado na base de dados!\n')

        else:
            print('>> Reparo ja cadastrado!')
            #debug
            #print(lst)
