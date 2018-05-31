import hashlib as hs
import sqlite3 as sql
from pathlib import Path

from Endereco import Endereco
from Cidadao import Cidadao
from Cidadao import Funcionario

database = 'srcb.db'
#myFile = Path(database)
#if myFile.is_file():
    #run the script to create the db

db_connection = sql.connect(database)
db_cursor = db_connection.cursor()

class SRCB(object):

    def __init__(self,debugCode=0):
        self.debugCode = debugCode

    def interfacePrincipal(self):

        selection = {
            '1': 'interfaceUsuario',

            '2': 'interfaceFuncionario',

            '3': 'interfaceCadastroUsuario'
        }

        print(''' Bem vindo ao sistema
        1) Painel de usuario
        2) Painel de funcionario
        3) Cadastrar novo usuario
        4) Sair
        ''')

        while(1):
            option = input("> ")

            if(option != '4'):
                try:
                    getattr(self,selection[option])()
                except KeyError:
                    print('Opcao invalida')
            else:
                break

        print('Saindo...')

    def login(self):
        """ Realiza o login do usuario por meio do seu identificador, pegando as informacoes
        no banco de dados e retornando o objeto de usuario """

        if(self.debugCode == 1):
            nome = "Admin"
            cpf = "919.231.890-85"
            identidade = "45.772.060-8"
            filiacao = "UNB"
            sexo = "ND"
            estadoCivil = "Solteiro"
            naturalidade = "Brasilia"
            endereco = Endereco(cidade="Brasilia", uf= "DF", bairro="Asa Norte")
            email = "admin@thissite.com"
            profissao = "Website Admin"
            funcionario = True
            recebeuDano = False
            codigo = "000"
            cargo = "Administrator"
            salario = "999"
            identificador = hs.sha224((nome + cpf).encode('utf-8')).hexdigest()

            temp = Funcionario(identificador, nome, cpf, identidade, filiacao,
                           sexo, estadoCivil, naturalidade, endereco, email,
                           profissao, funcionario, recebeuDano, codigo, cargo, salario)

            return temp

        user = None

        print("[*] Realize o login informando o identificador do seu usuario: ")
        identificadorUsuario = input("> ")

        #inserir o procedimento de busca no banco de dados

        return user

    def interfaceUsuario(self):
        user = self.login()

        print(''' [ Bem vindo ao painel de usuario ]
         1) Consultar cadastro
         2) Modificar cadastro
         3) Realizar consulta geral
         4) Consultar arquivos de dano
         5) Menu Buraco
         6) Menu Dano Recebido
         7) Gerar relatorio 
         8) Sair
         ''')

        selection = {
            '1': 'mostrar_cadastro',
            '2': 'modificarCadastro',#
            '3': 'realizarConsultaGeral',#
            '4': 'consultaArquivosDeDano',#
            '5': 'interfaceBuraco',#
            '6': 'interfaceDanoRecebido',#
            '7': 'gerarRelatorio',#
        }

        while (1):
            option = input("> ")

            if(option == '8'):
                break
            elif(option == '1' or option == '2'):
                getattr(user, selection[option])()
            else:
                try:
                    getattr(self, selection[option])(user)
                except KeyError:
                    print('Opcao invalida')



        print('Saindo do painel de usuario...')

    def interfaceFuncionario(self):
        user = self.login()

        print(''' [ Bem vindo ao painel de funcionario ]
         1) Consultar cadastro
         2) Cadastrar novo funcionário
         3) Modificar cadastro
         4) Excluir cadastro
         5) Menu Material de Reparo
         6) Menu Ordem de Trabalho
         7) Menu Equipamento
         8) Menu Equipe de Reparo
         9) Menu Reparo
         10) Sair
         ''')

        selection = {
            '1': 'consultaCadastroFuncionario',
            '2': 'cadastroFuncionario',
            '3': 'modificarCadastroFuncionario',
            '4': 'excluirCadastroFuncionario',
            '5': 'interfaceMaterialDeReparo',
            '6': 'interfaceOrdemDeTrabalho',
            '7': 'interfaceEquipamento',
            '8': 'interfaceEquipeDeReparo',
            '9': 'interfaceReparo',
        }

        while (1):
            option = input("> ")

            if(option == '10'):
                break
            else:
                try:
                    getattr(self, selection[option])(user)
                except KeyError:
                    print('Opcao invalida')



        print('Saindo do painel de funcionario...')


    def interfaceCadastroUsuario(self):
        print(''' [ Bem vindo ao painel de cadastro ]:
        ''')

        novoUsuario = self.inserirCadastro()


    def inserirCadastro(self):
        nome = input('>> Insira o nome: ')
        cpf = input('>> Insira o cpf: ')
        identidade = input('>> Insira a identidade: ')
        filiacao = input('>> Insira a filiacao: ')
        sexo = input('>> Insira o sexo: ')
        estadoCivil = input('>> Insira o estado civil: ')
        naturalidade = input('>> Insira a naturalidade: ')
        endereco = self.novoEndereco()
        email = input('>> Insira o email: ')
        profissao = input('>> Insira a profissao:')
        funcionario = False
        recebeuDano = False

        novoUsuario = Cidadao(nome, cpf, identidade, filiacao, sexo, estadoCivil, naturalidade, endereco, email, profissao, funcionario, recebeuDano)

        if(self.debugCode == 1):
            novoUsuario.mostrar_cadastro()

        return novoUsuario

    def novoEndereco(self):
        cidade = input('>> Insira a cidade: ')
        uf = input('>> Insira a UF: ')
        bairro = input('>> Insira o bairro: ')

        enderecoUsuario = Endereco(cidade,uf,bairro)

        return enderecoUsuario

    def realizarConsultaGeral(self):
        pass

    def consultaArquivosDeDano(self):
        pass

    def interfaceBuraco(self):
        pass

    def interfaceDanoRecebido(self):
        pass

    def gerarRelatorio(self):
        pass

    def consultaCadastroFuncionario(self):
        pass

    def cadastroFuncionario(self):
        pass

    def modificarCadastroFuncionario(self):
        pass

    def excluirCadastroFuncionario(self):
        pass

    def interfaceMaterialDeReparo(self):
        pass

    def interfaceOrdemDeTrabalho(self):
        pass

    def interfaceEquipamento(self):
        pass

    def interfaceEquipeDeReparo(self):
        pass

    def interfaceReparo(self):
        pass