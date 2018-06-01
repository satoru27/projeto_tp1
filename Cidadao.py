import hashlib as hs
import sqlite3 as sql
from pathlib import Path

from Endereco import Endereco
from Funcionario import Funcionario
DEBUG_FLAG = True

database = 'srcb.db'
#myFile = Path(database)
#if myFile.is_file():
    #run the script to create the db

db_connection = sql.connect(database)
db_cursor = db_connection.cursor()


class Cidadao(object):
    def __init__(self, nome, cpf, identidade, filiacao, sexo, estadoCivil, naturalidade, endereco, email,
                 profissao):
        self.identificador = hs.sha224((nome + cpf).encode('utf-8')).hexdigest()
        self.nome = nome
        self.cpf = cpf
        self.identidade = identidade
        self.filiacao = filiacao
        self.sexo = sexo
        self.estadoCivil = estadoCivil
        self.naturalidade = naturalidade
        self.endereco = endereco
        self.email = email
        self.profissao = profissao
        self.funcionario = False #deve ser mudado no cadastro do funcionario caso ocorra
        self.recebeuDano = False #deve ser mudado se o cidadao recebeu dano

    #def inserirCadastro(self):
    #    pass

    #def removerCadastro(self):
    #    pass

    def modificar_cadastro(self):
        pass

    def mostrar_cadastro(self):
        print(f'''<Informacoes do cidadao>
        Identificador: {self.identificador}
        Nome: {self.nome}
        CPF: {self.cpf}
        Identidade: {self.identidade}
        Filiacao: {self.filiacao}
        Sexo: {self.sexo}
        Estado civil: {self.estadoCivil}
        Naturalidade: {self.naturalidade}
        E-mail: {self.email}
        Profissao: {self.profissao}
        Funcionario: {self.funcionario}
        Recebeu dano: {self.recebeuDano}
        ''')
        self.endereco.mostrarEndereco()

    def gerar_funcionario(self,cargo, salario):
        funcionario = Funcionario(self.nome, self.cpf, self.identidade, self.filiacao, self.sexo, self.estadoCivil,
                                  self.naturalidade, self.endereco, self.email,self.profissao, self.funcionario,
                                  self.recebeuDano, cargo, salario)
        funcionario.funcionario = True
        self.funcionario = True
        #  atualizar cadastro no BD
        return funcionario


    def inserir_cidadao_db(self):
        db_cursor.execute("SELECT * FROM cidadao WHERE identificador = :identificador ",
                          {'identificador': self.identificador})

        lst = db_cursor.fetchall()

        if not lst:  # se nao encontrarmos o registro o colocamos na database
            db_cursor.execute("INSERT INTO cidadao VALUES(:identificador, :nome, :cpf, :identidade, :filiacao, :sexo,"
                              ":estadoCivil, :naturalidade, :endereco, :email, :profissao, :funcionario, :recebeuDano)",
                              {'identificador':self.identificador, 'nome': self.nome, 'cpf': self.cpf,
                               'identidade': self.identidade,'filiacao':self.filiacao,'sexo':self.sexo,
                               'estadoCivil': self.estadoCivil, 'naturalidade': self.naturalidade,
                               'endereco': self.endereco.string_endereco(), 'email': self.email,
                               'profissao': self.profissao,'funcionario': int(self.funcionario),
                               'recebeuDano': int(self.recebeuDano)})

            db_connection.commit()

            if DEBUG_FLAG:
                db_cursor.execute("SELECT * FROM cidadao WHERE identificador = :identificador ",
                                 {'identificador': self.identificador})
                print(db_cursor.fetchall())

            print('>> Novo usuario adicionado a base de dados!\n')

        else:
            print('>> Cidadao ja cadastrado!')
            if DEBUG_FLAG:
                print(lst)


    def remover_cidadao_db(self):
        with db_connection:
            db_cursor.execute("DELETE FROM cidadao WHERE identificador = :identificador",
                              {'identificador': self.identificador})

    def atualizar_identificador(self):
        novo_identificador = hs.sha224((self.nome + self.cpf).encode('utf-8')).hexdigest()
        with db_connection:
            db_cursor.execute("UPDATE cidadao SET identificador = :novo_identificador "
                              "WHERE identificador = :identificador",
                              {'novo_identificador': novo_identificador, 'identificador': self.identificador})

        self.identificador = novo_identificador

    def atualizar_nome(self, novo_valor):
        self.nome = novo_valor
        with db_connection:
            db_cursor.execute("UPDATE cidadao SET nome = :nome WHERE identificador = :identificador",
                              {'nome': self.nome, 'identificador': self.identificador})

        self.atualizar_identificador()

    def atualizar_cpf(self, novo_valor):
        self.cpf = novo_valor
        with db_connection:
            db_cursor.execute("UPDATE cidadao SET cpf = :cpf WHERE identificador = :identificador",
                              {'cpf': self.cpf, 'identificador': self.identificador})

        self.atualizar_identificador()

    def atualizar_identidade(self, novo_valor):
        self.identidade = novo_valor
        with db_connection:
            db_cursor.execute("UPDATE cidadao SET identidade = :identidade WHERE identificador = :identificador",
                              {'identidade': self.identidade, 'identificador': self.identificador})

    def atualizar_filiacao(self, novo_valor):
        self.filiacao = novo_valor
        with db_connection:
            db_cursor.execute("UPDATE cidadao SET filiacao = :filiacao WHERE identificador = :identificador",
                              {'filiacao': self.filiacao, 'identificador': self.identificador})

    def atualizar_sexo(self, novo_valor):
        self.sexo = novo_valor
        with db_connection:
            db_cursor.execute("UPDATE cidadao SET sexo = :sexo WHERE identificador = :identificador",
                              {'sexo': self.sexo, 'identificador': self.identificador})

    def atualizar_estadoCivil(self, novo_valor):
        self.estadoCivil = novo_valor
        with db_connection:
            db_cursor.execute("UPDATE cidadao SET estadoCivil = :estadoCivil WHERE identificador = :identificador",
                              {'estadoCivil': self.estadoCivil, 'identificador': self.identificador})

    def atualizar_naturalidade(self, novo_valor):
        self.naturalidade = novo_valor
        with db_connection:
            db_cursor.execute("UPDATE cidadao SET naturalidade = :naturalidade WHERE identificador = :identificador",
                              {'naturalidade': self.naturalidade, 'identificador': self.identificador})

    def atualizar_endereco(self, novo_valor):
        self.endereco = novo_valor
        with db_connection:
            db_cursor.execute("UPDATE cidadao SET endereco = :endereco WHERE identificador = :identificador",
                              {'endereco': self.endereco, 'identificador': self.identificador})

    def atualizar_email(self, novo_valor):
        self.email = novo_valor
        with db_connection:
            db_cursor.execute("UPDATE cidadao SET email = :email WHERE identificador = :identificador",
                              {'email': self.email, 'identificador': self.identificador})

    def atualizar_profissao(self, novo_valor):
        self.profissao = novo_valor
        with db_connection:
            db_cursor.execute("UPDATE cidadao SET profissao = :profissao WHERE identificador = :identificador",
                              {'profissao': self.profissao, 'identificador': self.identificador})

    def atualizar_funcionario(self, novo_valor):
        self.funcionario = novo_valor
        with db_connection:
            db_cursor.execute("UPDATE cidadao SET funcionario = :funcionario WHERE identificador = :identificador",
                              {'funcionario': int(self.funcionario), 'identificador': self.identificador})

    def atualizar_recebeuDano(self, novo_valor):
        self.recebeuDano = novo_valor
        with db_connection:
            db_cursor.execute("UPDATE cidadao SET recebeuDano = :recebeuDano WHERE identificador = :identificador",
                              {'recebeuDano': int(self.recebeuDano), 'identificador': self.identificador})


    # def consultaArquivoDeDanos(self):
    #     pass
    #
    # def realizaConsultaGeral(self):
    #     pass
    #
    # def geraRelatorio(self):
    #     pass
    #
    # def inserirBuraco(self):
    #     pass
    #
    # def removerBuraco(self):
    #     pass
    #
    # def modificarBuraco(self):
    #     pass
    #
    # def mostrarBuraco(self):
    #     pass
    #
    # def inserirDanoRecebido(self):
    #     pass
    #
    # def removerDanoRecebido(self):
    #     pass
    #
    # def modificarDanoRecebido(self):
    #     pass
    #
    # def mostrarDanoRecebido(self):
    #     pass

