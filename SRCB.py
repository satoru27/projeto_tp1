import hashlib as hs
import sqlite3 as sql
from pathlib import Path

from Buraco import Buraco
from Cidadao import Cidadao
from Endereco import Endereco
from Dano import Dano
from Equipamento import Equipamento
from EquipeDeReparo import EquipeDeReparo
from Funcionario import Funcionario
from Material import Material
from OrdemDeTrabalho import OrdemDeTrabalho
from Reparo import Reparo

database = 'srcb.db'
#myFile = Path(database)
#if myFile.is_file():
    #run the script to create the db

db_connection = sql.connect(database)
db_cursor = db_connection.cursor()

class SRCB(object):

    def __init__(self,debugCode=0):
        self.debugCode = debugCode

    def interface_principal(self):

        selection = {
            '1': 'interface_usuario',

            '2': 'interface_funcionario',

            '3': 'interface_cadastro_usuario'
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

    def login_cidadao(self):
        """ Realiza o login do usuario por meio do seu identificador, pegando as informacoes
        no banco de dados e retornando o objeto de usuario """

        # if(self.debugCode == 1):
        #     nome = "Admin"
        #     cpf = "919.231.890-85"
        #     identidade = "45.772.060-8"
        #     filiacao = "UNB"
        #     sexo = "ND"
        #     estadoCivil = "Solteiro"
        #     naturalidade = "Brasilia"
        #     endereco = Endereco(cidade="Brasilia", uf= "DF", bairro="Asa Norte")
        #     email = "admin@thissite.com"
        #     profissao = "Website Admin"
        #     funcionario = True
        #     recebeuDano = False
        #     codigo = "000"
        #     cargo = "Administrator"
        #     salario = "999"
        #     identificador = hs.sha224((nome + cpf).encode('utf-8')).hexdigest()
        # 
        #     temp = Funcionario(identificador, nome, cpf, identidade, filiacao,
        #                    sexo, estadoCivil, naturalidade, endereco, email,
        #                    profissao, funcionario, recebeuDano, codigo, cargo, salario)
        # 
        #     return temp

        user = None

        print("[*] Realize o login informando o identificador do seu usuario: ")
        identificadorUsuario = input("> ")

        #inserir o procedimento de busca no banco de dados

        return user

    def interface_usuario(self):
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

    def interface_funcionario(self):
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


    def interface_cadastro_usuario(self):
        print(''' [ Bem vindo ao painel de cadastro ]:
        ''')

        novoUsuario = self.inserir_cadastro()


    def inserir_cadastro(self):
        nome = input('>> Insira o nome: ')
        cpf = input('>> Insira o cpf: ')
        identidade = input('>> Insira a identidade: ')
        filiacao = input('>> Insira a filiacao: ')
        sexo = input('>> Insira o sexo: ')
        estadoCivil = input('>> Insira o estado civil: ')
        naturalidade = input('>> Insira a naturalidade: ')
        endereco = self.novo_endereco()
        email = input('>> Insira o email: ')
        profissao = input('>> Insira a profissao:')

        novoUsuario = Cidadao(nome, cpf, identidade, filiacao, sexo, estadoCivil, naturalidade, endereco, email, profissao)

        novoUsuario.inserir_cidadao_db()
        
        if(self.debugCode == 1):
            novoUsuario.mostrar_cadastro()

        return novoUsuario

    def novo_endereco(self):
        cidade = input('>> Insira a cidade: ')
        uf = input('>> Insira a UF: ')
        bairro = input('>> Insira o bairro: ')

        enderecoUsuario = Endereco(cidade, uf, bairro)

        return enderecoUsuario

    def retorna_obj_endereco(self, str):
        lst = str.split(',')

        if len(lst) != 3:
            print('>> Algo de errado nao esta certo')
            return None

        endereco = Endereco(lst[0], lst[1], lst[2])

        return endereco

    def retorna_cidadao_bd(self,identificador):
        cidadao = None

        db_cursor.execute("SELECT * FROM cidadao WHERE identificador = :identificador ",
                          {'identificador': identificador})

        lst = db_cursor.fetchall()

        if not lst:
            print(">> Cidadao nao encontrado")
            return cidadao

        lst = lst[0]
        #print(lst)

        cidadao = Cidadao(lst[1], lst[2], lst[3], lst[4], lst[5], lst[6], lst[7], self.retorna_obj_endereco(lst[8]), lst[9], lst[10])

        #cidadao.mostrar_cadastro()

        return cidadao

    def retorna_funcionario_bd(self,identificador):
        funcionario = None

        db_cursor.execute("SELECT * FROM funcionario WHERE identificador = :identificador ",
                          {'identificador': identificador})

        lst = db_cursor.fetchall()

        if not lst:
            print(">> Funcionario nao encontrado")
            return funcionario

        lst = lst[0]
        # print(lst)

        funcionario = Funcionario(lst[1], lst[2], lst[3], lst[4], lst[5], lst[6], lst[7],
                                  self.retorna_obj_endereco(lst[8]),lst[9], lst[10],lst[14],lst[15])

        # funcionario.mostrar_cadastro_funcionario()

        return funcionario

    def retorna_dano_bd(self,idDano):
        dano = None

        db_cursor.execute("SELECT * FROM dano WHERE idDano = :idDano ", {'idDano': idDano})

        lst = db_cursor.fetchall()

        if not lst:
            print(">> Dano nao encontrado")
            return dano

        lst = lst[0]
        print(lst)

        dano = Dano(lst[1], lst[2], lst[3], lst[4])

        dano.mostrar_dano()

        return dano

    def retorna_equipamento_bd(self, codigo):
        obj = None

        db_cursor.execute("SELECT * FROM equipamento WHERE codigo = :codigo ",
                          {'codigo': codigo})
        lst = db_cursor.fetchall()

        if not lst:
            print(">> Equipamento nao encontrado")
            return obj

        lst = lst[0]
        print(lst)

        obj = Equipamento(lst[1], lst[2], lst[3], lst[4])

        obj.mostrar_equipamento()

        return obj

    def retorna_material_bd(self, codigo):
        obj = None

        db_cursor.execute("SELECT * FROM material WHERE codigo = :codigo ",
                          {'codigo': codigo})
        lst = db_cursor.fetchall()

        if not lst:
            print(">> Material nao encontrado")
            return obj

        lst = lst[0]
        print(lst)
#descricao, valor, quantidade, tipo
        obj = Material(lst[1], lst[2], lst[3], lst[4])

        obj.mostrar_material()

        return obj

    def retorna_equipe_de_reparo_bd(self, identificador):
        obj = None

        db_cursor.execute("SELECT * FROM equipeDeReparo WHERE identificador = :identificador ",
                          {'identificador': identificador})
        lst = db_cursor.fetchall()

        if not lst:
            print(">> Equipe nao encontrada")
            return obj

        lst = lst[0]
        print(lst)
        # numeroDePessoas, funcionarios
        obj = EquipeDeReparo(int(lst[1]), lst[2].split(','))

        obj.mostrar_equipe_de_reparo()

        return obj

    def retorna_buraco_bd(self, identificador):
        obj = None

        db_cursor.execute("SELECT * FROM buraco WHERE identificador = :identificador ",
                          {'identificador': identificador})
        lst = db_cursor.fetchall()

        if not lst:
            print(">> Buraco nao encontrado")
            return obj

        lst = lst[0]
        print(lst)
        # endereco, tamanho, localizacao, prioridade, registradoPor
        obj = Buraco(self.retorna_obj_endereco(lst[1]),int(lst[2]),lst[3],int(lst[4]),lst[5])

        obj.mostrar_buraco()

        return obj

    def retorna_ordem_de_trabalho_bd(self, identificador):
        obj = None

        db_cursor.execute("SELECT * FROM ordemDeTrabalho WHERE identificador = :identificador ",
                          {'identificador': identificador})
        lst = db_cursor.fetchall()

        if not lst:
            print(">> Ordem de trabalho nao encontrada")
            return obj

        lst = lst[0]
        print(lst)
        # endereco, tamanho, localizacao, prioridade, registradoPor,
        #     descricao,situacao, equipeDeReparo, equipamentos, horasAplicadas
        obj = OrdemDeTrabalho(self.retorna_obj_endereco(lst[1]), int(lst[2]), lst[3], int(lst[4]), lst[5],
                              lst[7],lst[8],lst[9],lst[10],int(lst[11]))

        obj.mostrar_ordem_de_trabalho()

        return obj

    def retorna_reparo_bd(self, identificador):
        obj = None

        db_cursor.execute("SELECT * FROM reparo WHERE identificador = :identificador ",
                          {'identificador': identificador})
        lst = db_cursor.fetchall()

        if not lst:
            print(">> Reparo nao encontrado")
            return obj

        lst = lst[0]
        print(lst)
        # endereco, tamanho, localizacao, prioridade, registradoPor,
        #     descricao,situacao, equipeDeReparo, equipamentos, horasAplicadas
        # descricaoReparo, status, materialUtilizado
        obj = Reparo(self.retorna_obj_endereco(lst[1]), int(lst[2]), lst[3], int(lst[4]), lst[5],
                              lst[7], lst[8], lst[9], lst[10], int(lst[11]),
                              lst[13],lst[14],lst[15])

        obj.mostrar_reparo()

        return obj
    #
    # def retorna__bd(self, identificador):
    #     pass

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