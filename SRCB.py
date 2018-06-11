import hashlib as hs
import sqlite3 as sql
from pathlib import Path
import os
#os.system('cls' if os.name == 'nt' else 'clear')
if os.name == 'nt':
    CLEAR = 'cls'
else:
    CLEAR = 'clear'
from random import randint

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
            '1': 'interface_cidadao',

            '2': 'interface_funcionario',

            '3': 'interface_cadastro_cidadao'
        }

        while(1):
            print(''' [ Bem vindo ao sistema ]
            1) Painel de usuario
            2) Painel de funcionario
            3) Cadastrar novo usuario
            4) Sair
            ''')

            option = input("> ")

            if(option != '4'):
                try:
                    getattr(self,selection[option])()
                except KeyError:
                    print('Opcao invalida')
            else:
                break

        print('Saindo...')
        db_connection.close()

    def login_cidadao(self):
        """ Realiza o login do usuario por meio do seu identificador, pegando as informacoes
        no banco de dados e retornando o objeto de usuario """

        user = None

        print("[*] Realize o login informando o identificador do seu usuario: ")
        identificador_usuario = input("> ")

        user = self.retorna_cidadao_bd(identificador_usuario)

        return user
    
    def login_funcionario(self):
        """ Realiza o login do usuario por meio do seu identificador, pegando as informacoes
        no banco de dados e retornando o objeto de usuario """

        user = None

        print("[*] Realize o login informando o identificador do seu usuario: ")
        identificador_usuario = input("> ")

        user = self.retorna_funcionario_bd(identificador_usuario)

        return user

    def interface_cidadao(self):
        user = self.login_cidadao()
        
        if user == None:
            print('>> Falha no login!')
            return

        selection = {
            '1': 'mostrar_cadastro',
            '2': 'modificar_cadastro_cidadao',#
            '3': 'realizar_consulta_geral',#
            '4': 'consultar_arquivos_de_dano',#
            '5': 'interface_buraco',#
            '6': 'interface_dano_recebido',#
            '7': 'gerar_relatorio',#
        }

        while (1):
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

            option = input("> ")

            if(option == '8'):
                break
            elif(option == '1'):
                getattr(user, selection[option])()
            else:
                try:
                    getattr(self, selection[option])(user)
                except KeyError:
                    print('Opcao invalida')

        print('Saindo do painel de usuario...')

    def interface_funcionario(self):
        user = self.login_funcionario()

        if user == None:
            print('>> Falha no login!')
            return

        selection = {
            '1': 'consultar_cadastro_funcionario',
            '2': 'modificar_cadastro_funcionario',
            '3': 'excluir_cadastro_funcionario',
            '4': 'cadastrar_funcionario',
            '5': 'interface_material_de_reparo',
            '6': 'interface_ordem_de_trabalho',
            '7': 'interface_equipamento',
            '8': 'interface_equipe_de_reparo',
            '9': 'interface_reparo',
        }

        while 1:
            print(''' [ Bem vindo ao painel de funcionario ]
                     1) Consultar cadastro
                     2) Modificar cadastro
                     3) Excluir cadastro
                     4) Cadastrar novo funcionário
                     5) Menu Material de Reparo
                     6) Menu Ordem de Trabalho
                     7) Menu Equipamento
                     8) Menu Equipe de Reparo
                     9) Menu Reparo
                     10) Sair
                     ''')

            option = input("> ")

            if(option == '10'):
                break
            else:
                try:
                    getattr(self, selection[option])(user)
                except KeyError:
                    print('Opcao invalida')

        print('Saindo do painel de funcionario...')


    def interface_cadastro_cidadao(self):
        print(''' [ Bem vindo ao painel de cadastro ]:
        ''')

        novoUsuario = self.inserir_cadastro_cidadao()


    def inserir_cadastro_cidadao(self):
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
        cidadao.funcionario = bool(lst[11])
        cidadao.recebeuDano = bool(lst[12])

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
        funcionario.funcionario = bool(lst[11])
        funcionario.recebeuDano = bool(lst[12])

        return funcionario

    def retorna_dano_bd(self,idDano):
        dano = None

        db_cursor.execute("SELECT * FROM dano WHERE idDano = :idDano ", {'idDano': idDano})

        lst = db_cursor.fetchall()

        if not lst:
            print(">> Dano nao encontrado")
            return dano

        lst = lst[0]
        #print(lst)

        dano = Dano(lst[1], lst[2], lst[3], lst[4])

        #dano.mostrar_dano()

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
        #print(lst)

        obj = Equipamento(lst[1], lst[2], lst[3], lst[4])

        #obj.mostrar_equipamento()

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
        #print(lst)
#descricao, valor, quantidade, tipo
        obj = Material(lst[1], lst[2], lst[3], lst[4])

        #obj.mostrar_material()

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
        #print(lst)
        # numeroDePessoas, funcionarios
        obj = EquipeDeReparo(int(lst[1]), lst[2].split(','))

        #obj.mostrar_equipe_de_reparo()

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
        #print(lst)
        # endereco, tamanho, localizacao, prioridade, registradoPor
        obj = Buraco(self.retorna_obj_endereco(lst[1]), int(lst[2]), lst[3], int(lst[4]),lst[5])

        #obj.mostrar_buraco()

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

        equipamento = lst[10]
        if ',' in equipamento:
            equipamento = equipamento.split(',')

        #print(lst)
        # endereco, tamanho, localizacao, prioridade, registradoPor,
        #     descricao,situacao, equipeDeReparo, equipamentos, horasAplicadas
        obj = OrdemDeTrabalho(self.retorna_obj_endereco(lst[1]), int(lst[2]), lst[3], int(lst[4]), lst[5],
                              lst[7],lst[8],lst[9],equipamento,int(lst[11]))

        #obj.mostrar_ordem_de_trabalho()

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

        equipamento = lst[10]
        if ',' in equipamento:
            equipamento = equipamento.split(',')

        material = lst[15]
        if ',' in material:
            material = material.split(',')

        #print(lst)
        # endereco, tamanho, localizacao, prioridade, registradoPor,
        #     descricao,situacao, equipeDeReparo, equipamentos, horasAplicadas
        # descricaoReparo, status, materialUtilizado
        obj = Reparo(self.retorna_obj_endereco(lst[1]), int(lst[2]), lst[3], int(lst[4]), lst[5],
                              lst[7], lst[8], lst[9], equipamento, int(lst[11]),
                              lst[13],lst[14],material)

        #obj.mostrar_reparo()

        return obj

    def interface_buraco(self,user):

        selection = {
            '1': 'consultar_buracos',
            '2': 'registrar_buraco',  #
            '3': 'modificar_buraco',  #
            '4': 'excluir_buraco',  #
        }

        while (1):
            print(''' [ Bem vindo ao painel de buracos ]
                             1) Consultar buracos registrados pelo seu usuario
                             2) Registrar buraco
                             3) Modificar buraco
                             4) Excluir buraco
                             5) Sair
                             ''')

            option = input("> ")

            if (option == '5'):
                break
            else:
                try:
                    getattr(self, selection[option])(user)
                except KeyError:
                    print('Opcao invalida')

        print('Saindo do painel de buracos...')

    def consultar_buracos(self, user):

        db_cursor.execute("SELECT * FROM buraco WHERE registradoPor = :registradoPor ",
                          {'registradoPor': user.identificador})
        lst = db_cursor.fetchall()

        if not lst:
            print(">> Nenhum buraco encontrado")
            return

        for entry in lst:
            buraco = self.retorna_buraco_bd(entry[0])
            buraco.mostrar_buraco()

    def registrar_buraco(self,user):#endereco, tamanho, localizacao, prioridade, registradoPor
        endereco = self.novo_endereco()
        print('>> Insira o tamanho: ')
        tamanho = self.valid_int_input()
        localizacao = input('>> Insira a localizacao :')
        prioridade = randint(0,9)
        print(f'>> Prioridade: {prioridade}')
        registradoPor = user.identificador

        buraco = Buraco(endereco, tamanho, localizacao, prioridade, registradoPor)

        buraco.inserir_buraco_db()

    def modificar_buraco(self,user):
        idBuraco = input('>> Insira o identificador do buraco:\n> ')
        buraco = self.retorna_buraco_bd(idBuraco)
        if buraco is None:
            print('>> Buraco nao encontrado')
            return

        selection = {
            '1': 'atualizar_endereco',
            '2': 'atualizar_tamanho',
            '3': 'atualizar_localizacao',
            '4': 'atualizar_prioridade',
            '5': 'atualizar_registradoPor',
        }

        identificador_old = buraco.identificador

        while 1:
            print(''' [ Bem vindo ao painel de atualizacao de buraco ]\n [ Selecione o atributo a ser atualizado: ]
                                     1) Endereco
                                     2) Tamanho
                                     3) Localizacao
                                     4) Prioridade
                                     5) Por quem foi registrado
                                     6) Sair
                                     ''')

            option = input("> ")

            if option == '6':
                break
            elif option == '1':
                novo_endereco = self.novo_endereco()
                getattr(buraco, selection[option])(novo_endereco)

            elif option == '2' or option == '4':
                print('>> Insira o novo valor do atributo: ')
                novo_valor = self.valid_int_input()
                try:
                    getattr(buraco, selection[option])(novo_valor)
                    print('> Valor atualizado!')
                except KeyError:
                    print('Opcao invalida')

            else:
                print('>> Insira o novo valor do atributo: ')
                novo_valor = input('> ')
                try:
                    getattr(buraco, selection[option])(novo_valor)
                    print('> Valor atualizado!')
                except KeyError:
                    print('Opcao invalida')

        self.buraco_modificado_atualiza_ordem_e_reparo(buraco, identificador_old)

        print('Saindo do painel de atualizacao de buraco...')

    def excluir_buraco(self,user):
        idBuraco = input('>> Insira o identificador do buraco:\n> ')
        confirm = input('>> Deseja realmente excluir o buraco ? [S/s]')
        if confirm == 'S' or confirm == 's':
            buraco = self.retorna_buraco_bd(idBuraco)
            if buraco is None:
                return
            buraco.remover_buraco_db()

        print('Voltando...')
        return

    def modificar_cadastro_cidadao(self, user):

        selection = {
            '1': 'atualizar_nome',
            '2': 'atualizar_cpf',
            '3': 'atualizar_identidade',
            '4': 'atualizar_filiacao',
            '5': 'atualizar_sexo',
            '6': 'atualizar_estadoCivil',
            '7': 'atualizar_naturalidade',
            '8': 'atualizar_endereco',
            '9': 'atualizar_email',
            '10': 'atualizar_profissao'
        }

        identificador_old = user.identificador

        while 1:
            print(''' [ Bem vindo ao painel de atualizacao de usuario ]\n [ Selecione o atributo a ser atualizado: ]
                             1) Nome
                             2) CPF
                             3) Identidade
                             4) Filiacao
                             5) Sexo
                             6) Estado Civil
                             7) Naturalidade
                             8) Endereco
                             9) Email
                             10) Profissao
                             11) Sair
                             ''')

            option = input("> ")

            if (option == '11'):
                break
            elif option == '8':
                novo_endereco = self.novo_endereco()
                getattr(user, selection[option])(novo_endereco)

            else:
                print('>> Insira o novo valor do atributo: ')
                novo_valor = input('> ')
                try:
                    getattr(user, selection[option])(novo_valor)
                    print('> Valor atualizado!')
                except KeyError:
                    print('Opcao invalida')

        if user.funcionario:
            funcionario = self.retorna_funcionario_bd(identificador_old)
            #funcionario.mostrar_cadastro_funcionario()
            funcionario.cidadao_atualizado(user)
            #funcionario.mostrar_cadastro_funcionario()
            print('>> Cadastro de funcionario atualizado!')

        if identificador_old != user.identificador:
            self.cidadao_modificado_atualiza_dano(user, identificador_old)  # tem que atualizar o identificador
            self.cidadao_modificado_atualiza_buraco(user, identificador_old)  # ja deve conter a atualizacao de ordem de trabalho e reparo

        print('Saindo do painel de atualizacao de usuario...')

    def cidadao_modificado_atualiza_dano(self,user,identificador_old):
        db_cursor.execute("SELECT * FROM dano WHERE idCidadao = :id_usuario ",
                          {'id_usuario': identificador_old})

        lst = db_cursor.fetchall()

        print(lst)

        for entry in lst:
            dano = self.retorna_dano_bd(entry[0])
            dano.mostrar_dano()
            dano.atualizar_idCidadao(user.identificador)
            dano.mostrar_dano()

    def cidadao_modificado_atualiza_buraco(self,user,identificador_old):
        db_cursor.execute("SELECT * FROM buraco WHERE registradoPor = :id_usuario ",
                         {'id_usuario': identificador_old})

        lst = db_cursor.fetchall()

        for entry in lst:
            buraco = self.retorna_buraco_bd(entry[0])
            buraco.atualizar_registradoPor(user.identificador)
            ordem = self.retorna_ordem_de_trabalho_bd(entry[0])
            if ordem is not None:
                ordem.buraco_atualizado(buraco)
                reparo = self.retorna_reparo_bd(entry[0])
                if reparo is not None:
                    reparo.ordem_atualizada(ordem)

    def buraco_modificado_atualiza_ordem_e_reparo(self,buraco,identificador_old):
        db_cursor.execute("SELECT * FROM ordemDeTrabalho WHERE identificador = :identificador ",
                          {'identificador': identificador_old})

        lst = db_cursor.fetchall()

        for entry in lst:
            ordem = self.retorna_ordem_de_trabalho_bd(entry[0])
            if ordem is not None:
                ordem.buraco_atualizado(buraco)
                reparo = self.retorna_reparo_bd(entry[0])
                if reparo is not None:
                    reparo.ordem_atualizada(ordem)

    def interface_dano_recebido(self,user):

        selection = {
            '1': 'consultar_danos',
            '2': 'registrar_dano',  #
            '3': 'modificar_dano',  #
            '4': 'excluir_dano',  #
        }

        while (1):
            print(''' [ Bem vindo ao painel de danos recebidos ]
                                 1) Consultar danos registrados pelo seu usuario
                                 2) Registrar dano recebido
                                 3) Modificar dano recebido
                                 4) Excluir dano recebido
                                 5) Sair
                                 ''')

            option = input("> ")

            if (option == '5'):
                break
            else:
                try:
                    getattr(self, selection[option])(user)
                except KeyError:
                    print('Opcao invalida')

        print('Saindo do painel de danos recebidos...')

    def consultar_danos(self, user):

        db_cursor.execute("SELECT * FROM dano WHERE idCidadao = :idCidadao ",
                          {'idCidadao': user.identificador})
        lst = db_cursor.fetchall()

        if not lst:
            print(">> Nenhum dano encontrado")
            return

        for entry in lst:
            dano = self.retorna_dano_bd(entry[0])
            dano.mostrar_dano()

    def registrar_dano(self, user):  # tipoDeDano, pagamento, idBuraco, idCidadao
        tipoDeDano = input('>> Informe o tipo de dano:')
        pagamento = randint(0,9999)
        idBuraco = input('>> Insira o identificador do buraco causador do dano :')
        idCidadao = user.identificador

        dano = Dano(tipoDeDano,pagamento,idBuraco,idCidadao)

        user.atualizar_recebeuDano(True)

        dano.inserir_dano_db()

    def modificar_dano(self, user):
        idDano = input('>> Insira o identificador do dano:\n> ')
        dano = self.retorna_dano_bd(idDano)
        if dano is None:
            print('>> Dano nao encontrado')
            return

        selection = {
            '1': 'atualizar_tipoDeDano',
            '2': 'atualizar_pagamento',
            '3': 'atualizar_idBuraco',
            '4': 'atualizar_idCidadao',
        }

        identificador_old = dano.idDano

        while 1:
            print(''' [ Bem vindo ao painel de atualizacao de dano ]\n [ Selecione o atributo a ser atualizado: ]
                                         1) Tipo de dano
                                         2) Pagamento
                                         3) Buraco que causou o dano
                                         4) Cidadao que recebeu o dano
                                         5) Sair
                                         ''')

            option = input("> ")

            if option == '5':
                break
            elif option == '2' :
                print('>> Insira o novo valor do atributo: ')
                novo_valor = self.valid_int_input()
                dano.atualizar_pagamento(novo_valor)
                print('> Valor atualizado!')

            else:
                print('>> Insira o novo valor do atributo: ')
                novo_valor = input('> ')
                try:
                    getattr(dano, selection[option])(novo_valor)
                    print('> Valor atualizado!')
                except KeyError:
                    print('Opcao invalida')

        #verificar se mudancas em dano repercutem em mudancas em outros registros

        print('Saindo do painel de atualizacao de buraco...')

    def excluir_dano(self, user):
        idDano = input('>> Insira o identificador do dano:\n> ')
        confirm = input('>> Deseja realmente excluir o dano ? [S/s]')
        if confirm == 'S' or confirm == 's':
            dano = self.retorna_dano_bd(idDano)
            dano.remover_dano_db()

        print('Voltando...')
        return

    def realizar_consulta_geral(self, user):
        print('[ Consulta geral ]')
        self.consultar_danos(user)

        db_cursor.execute("SELECT * FROM buraco WHERE registradoPor = :registradoPor ",
                          {'registradoPor': user.identificador})
        lst = db_cursor.fetchall()

        if not lst:
            print(">> Nenhum buraco encontrado")
            return

        for entry in lst:
            buraco = self.retorna_buraco_bd(entry[0])
            ordem = self.retorna_ordem_de_trabalho_bd(entry[0])
            reparo = self.retorna_reparo_bd(entry[0])
            if ordem is not None:
                if reparo is not None:
                    reparo.mostrar_reparo()
                else:
                    ordem.mostrar_ordem_de_trabalho()
            else:
                buraco.mostrar_buraco()

    def consultar_arquivos_de_dano(self, user):
        print('[ Arquivo de danos do usuario ]')
        self.consultar_danos(user)

    def gerar_relatorio(self,user):
        db_cursor.execute("SELECT * FROM dano WHERE idCidadao = :idCidadao ",
                          {'idCidadao': user.identificador})
        lst = db_cursor.fetchall()

        if not lst:
            print(">> Nenhum dano encontrado")
            return
        dano_total = 0
        for entry in lst:
            dano = self.retorna_dano_bd(entry[0])
            dano.mostrar_dano()
            dano_total += int(dano.pagamento)

        print(f'\t[Pagamento total = {dano_total} ]')

    def consultar_cadastro_funcionario(self, user):
        while 1:
            print('''[ Painel de consulta de cadastro ]
                        1) Consultar o proprio cadastro
                        2) Consultar outro cadastro
                        3) Mostrar todos os cadastros
                        4) Sair
            ''')
            option = input('> ')
            if option == '1':
                user.mostrar_cadastro_funcionario()
            elif option == '2':
                identificador = input('>> Insira o identificador do usuario: \n> ')
                other_user = self.retorna_funcionario_bd(identificador)
                if other_user is None:
                    other_user = self.retorna_cidadao_bd(identificador)
                    if other_user is None:
                        print('>> Cadastro nao encontrado')
                    else:
                        other_user.mostrar_cadastro()
                else:
                    other_user.mostrar_cadastro_funcionario()

            elif option == '3':

                with db_connection:
                    db_cursor.execute("SELECT * FROM cidadao")
                    lst = db_cursor.fetchall()

                    for entry in lst:
                        user = self.retorna_funcionario_bd(entry[0])

                        if user is None:
                            user = self.retorna_cidadao_bd(entry[0])
                            user.mostrar_cadastro()

                        else:
                            user.mostrar_cadastro_funcionario()

            elif option == '4':
                print('Saindo...')
                return
            else:
                print('>> Opcao invalida')

    def modificar_cadastro_funcionario(self, user):
        while 1:
            print('''[ Painel de modificacao de cadastro ]
                        1) Modificar o proprio cadastro
                        2) Modificar outro cadastro
                        3) Sair
            ''')
            option = input('> ')
            if option == '1':
                print('''
                            1) Modificar informacoes de cidadao
                            2) Modificar informacoes de funcionario
                ''')
                option = input('> ')
                if option == '1':
                    self.modificar_cadastro_cidadao(user)

                elif option == '2':
                    print('''[ Selecione o campo a ser modificado ]
                                1) Cargo
                                2) Salario
                            ''')
                    option = input('> ')
                    novo_valor = input('>> Insira o novo valor: \n> ')

                    if option == '1':
                        user.atualizar_cargo(novo_valor)

                    elif option == '2':
                        user.atualizar_salario(novo_valor)

                    else:
                        print('>> Opcao invalida')

                else:
                    print('>> Opcao invalida')

            elif option == '2':
                identificador = input('>> Insira o identificador do usuario: \n> ')
                other_user = self.retorna_funcionario_bd(identificador)

                if other_user is None:
                    other_user = self.retorna_cidadao_bd(identificador)
                    self.modificar_cadastro_cidadao(other_user)

                else:
                    print('''
                                1) Modificar informacoes de cidadao
                                2) Modificar informacoes de funcionario
                                    ''')
                    option = input('> ')

                    if option == '1':
                        self.modificar_cadastro_cidadao(other_user)

                    elif option == '2':
                        print('''[ Selecione o campo a ser modificado ]
                                    1) Cargo
                                    2) Salario
                                                ''')
                        option = input('> ')
                        novo_valor = input('>> Insira o novo valor: \n> ')

                        if option == '1':
                            other_user.atualizar_cargo(novo_valor)

                        elif option == '2':
                            other_user.atualizar_salario(novo_valor)

                        else:
                            print('>> Opcao invalida')

                    else:
                        print('>> Opcao invalida')
            elif option == '3':
                print('Saindo...')
                return
            else:
                print('>> Opcao invalida')

    def excluir_cadastro_funcionario(self, user):
        while 1:
            print('''[ Painel de exclusao de cadastro ]
                        1) Excluir o proprio cadastro
                        2) Excluir outro cadastro
                        3) Sair
            ''')
            option = input('> ')

            if option == '1':
                confirm = input('>> Deseja realmente excluir o seu usuario ? [S/s]')
                if confirm == 'S' or confirm == 's':
                    user.remover_funcionario_db()

            elif option == '2':
                identificador = input('>> Insira o identificador do usuario: \n> ')
                other_user = self.retorna_funcionario_bd(identificador)
                if other_user is None:
                    other_user = self.retorna_cidadao_bd(identificador)
                    confirm = input('>> Deseja realmente excluir usuario (cidadao) ? [S/s]\n> ')
                    if confirm == 'S' or confirm == 's':
                        other_user.remover_cidadao_db()
                else:
                    confirm = input('>> Deseja realmente excluir usuario (funcionario) ? [S/s]\n> ')
                    if confirm == 'S' or confirm == 's':
                        other_user.remover_funcionario_db()

            elif option == '3':
                print('Saindo...')
                return
            else:
                print('>> Opcao invalida')

    def cadastrar_funcionario(self, user):
        print('''[ Painel de cadastro de funcionario ]''')
        identificador = input('>> Insira o identificador do cidadao a ser cadastrado como funcionario: \n> ')

        cidadao = self.retorna_cidadao_bd(identificador)

        if cidadao is None:
            print('>> Cidadao nao encontrado')
            return
        else:
            cargo = input('> Insira o cargo: ')
            salario = input('> Insira o salario: ')
            funcionario = Funcionario(cidadao.nome, cidadao.cpf, cidadao.identidade, cidadao.filiacao, cidadao.sexo,
                                      cidadao.estadoCivil, cidadao.naturalidade, cidadao.endereco, cidadao.email,
                                      cidadao.profissao, cargo, salario)
            cidadao.atualizar_funcionario(True)
            funcionario.inserir_funcionario_db()

    def interface_material_de_reparo(self, user):

        selection = {
            '1': 'consultar_material',
            '2': 'registrar_material',
            '3': 'modificar_material',
            '4': 'excluir_material',
        }

        while 1:
            print(''' [ Bem vindo ao painel de material de reparo ]
                                 1) Consultar material de reparo
                                 2) Registrar material de reparo
                                 3) Modificar material de reparo
                                 4) Excluir material de reparo
                                 5) Sair
                                 ''')

            option = input("> ")

            if option == '5':
                break
            else:
                try:
                    getattr(self, selection[option])()
                except KeyError:
                    print('Opcao invalida')

        print('Saindo do painel de material de reparo...')

    def consultar_material(self):

        selection = {
            '1': 'consultar_todos_materiais',
            '2': 'consultar_material_especifico'
        }

        while 1:
            print('''[ Painel de consulta de material de reparo ]
                        1) Consultar todos os materiais
                        2) Consultar material especifico
                        3) Sair
            ''')
            option = input('> ')

            if option == '3':
                break
            else:
                try:
                    getattr(self, selection[option])()
                except KeyError:
                    print('Opcao invalida')

    def consultar_todos_materiais(self):
        #with db_connection:
        db_cursor.execute("SELECT * FROM material")
        lst = db_cursor.fetchall()
        for entry in lst:
            material = self.retorna_material_bd(entry[0])
            material.mostrar_material()

    def consultar_material_especifico(self):
        codigo = input('>> Insira o codigo do material a ser consultado: \n> ')
        #with db_connection:
        db_cursor.execute("SELECT * FROM material WHERE codigo = :codigo",{'codigo':codigo})
        lst = db_cursor.fetchall()
        if not lst:
            print('>> Material nao encontrado')
            return
        entry = lst[0]
        material = self.retorna_material_bd(entry[0])
        material.mostrar_material()

    def registrar_material(self):#descricao, valor, quantidade, tipo
        descricao = input('>> Insira a descricao do material: ')
        print('>> Insira o valor do material: ')
        valor = self.valid_int_input()
        print('>> Insira a quantidade do material: ')
        quantidade = self.valid_int_input()
        tipo = input('>> Insira o tipo do material: ')

        material = Material(descricao,valor,quantidade,tipo)

        material.inserir_material_db()

    def modificar_material(self):
        identificador = input('>> Insira o identificador do material:\n> ')
        material = self.retorna_material_bd(identificador)
        if material is None:
            print('>> Material nao encontrado')
            return

        selection = {
            '1': 'atualizar_descricao',
            '2': 'atualizar_valor',
            '3': 'atualizar_quantidade',
            '4': 'atualizar_tipo',
        }

        while 1:
            print(''' [ Bem vindo ao painel de atualizacao de material ]\n [ Selecione o atributo a ser atualizado: ]
                                                     1) Descricao
                                                     2) Valor
                                                     3) Quantidade
                                                     4) Tipo
                                                     5) Sair
                                                     ''')

            option = input("> ")

            if option == '5':
                break

            elif option == '2' or option == '3':
                print('>> Insira o novo valor do atributo: ')
                novo_valor = self.valid_int_input()
                getattr(material, selection[option])(novo_valor)
                print('> Valor atualizado!')

            else:
                print('>> Insira o novo valor do atributo: ')
                novo_valor = input('> ')
                try:
                    getattr(material, selection[option])(novo_valor)
                    print('> Valor atualizado!')
                except KeyError:
                    print('Opcao invalida')

        ## afeta reparo

        print('Saindo do painel de atualizacao de material...')

    def excluir_material(self):
        print('''[ Painel de exclusao de material ]''')
        codigo = input('>> Insira o codigo do material a ser excluido: \n> ')
        material = self.retorna_material_bd(codigo)

        if material is None:
            print('> Material nao encontrado!')
            return

        confirm = input('>> Deseja realmente excluir o material ? [S/s]')
        if confirm == 'S' or confirm == 's':
            material.remover_material_db()
            print('> Material excluido com sucesso')


    def interface_equipamento(self, user):

        selection = {
            '1': 'consultar_equipamento',
            '2': 'registrar_equipamento',
            '3': 'modificar_equipamento',
            '4': 'excluir_equipamento',
        }

        while (1):
            print(''' [ Bem vindo ao painel de equipamento ]
                                 1) Consultar equipamento
                                 2) Registrar equipamento
                                 3) Modificar equipamento
                                 4) Excluir equipamento
                                 5) Sair
                                 ''')

            option = input("> ")

            if option == '5':
                break
            else:
                try:
                    getattr(self, selection[option])()
                except KeyError:
                    print('Opcao invalida')

        print('Saindo do painel de equipamentos...')


    def consultar_equipamento(self):

        selection = {
            '1': 'consultar_todos_equipamentos',
            '2': 'consultar_equipamento_especifico'
        }

        while 1:
            print('''[ Painel de consulta de equipamento ]
                        1) Consultar todos os equipamentos
                        2) Consultar equipamento especifico
                        3) Sair
            ''')
            option = input('> ')

            if option == '3':
                break
            else:
                try:
                    getattr(self, selection[option])()
                except KeyError:
                    print('Opcao invalida')

    def consultar_todos_equipamentos(self):
        #with db_connection:
        db_cursor.execute("SELECT * FROM equipamento")
        lst = db_cursor.fetchall()
        for entry in lst:
            equipamento = self.retorna_equipamento_bd(entry[0])
            equipamento.mostrar_equipamento()

    def consultar_equipamento_especifico(self):
        codigo = input('>> Insira o codigo do equipamento a ser consultado: \n> ')
        #with db_connection:
        db_cursor.execute("SELECT * FROM equipamento WHERE codigo = :codigo", {'codigo': codigo})
        lst = db_cursor.fetchall()
        if not lst:
            print('>> Equipamento nao encontrado')
            return

        entry = lst[0]
        equipamento = self.retorna_equipamento_bd(entry[0])
        equipamento.mostrar_equipamento()

    def registrar_equipamento(self):# descricao, fabricante, tamanho, peso
        descricao = input('>> Insira a descricao do equipamento: ')
        fabricante = input('>> Insira o fabricante do equipamento: ')
        print('>> Insira o tamanho do equipamento: ')
        tamanho = self.valid_int_input()
        print('>> Insira o peso do equipamento: ')
        peso = self.valid_int_input()

        equipamento = Equipamento(descricao, fabricante, tamanho, peso)

        equipamento.inserir_equipamento_db()

    def modificar_equipamento(self):
        identificador = input('>> Insira o identificador do equipamento:\n> ')
        equipamento = self.retorna_equipamento_bd(identificador)
        if equipamento is None:
            print('>> Equipamento nao encontrado')
            return

        selection = {
            '1': 'atualizar_descricao',
            '2': 'atualizar_fabricante',
            '3': 'atualizar_tamanho',
            '4': 'atualizar_peso',
        }

        while 1:
            print(''' [ Bem vindo ao painel de atualizacao de equipamento ]\n [ Selecione o atributo a ser atualizado: ]
                                                             1) Descricao
                                                             2) Fabricante
                                                             3) Tamanho
                                                             4) Peso
                                                             5) Sair
                                                             ''')

            option = input("> ")

            if option == '5':
                break

            elif option == '3' or option == '4':
                print('>> Insira o novo valor do atributo: ')
                novo_valor = self.valid_int_input()
                getattr(equipamento, selection[option])(novo_valor)
                print('> Valor atualizado!')

            else:
                print('>> Insira o novo valor do atributo: ')
                novo_valor = input('> ')
                try:
                    getattr(equipamento, selection[option])(novo_valor)
                    print('> Valor atualizado!')
                except KeyError:
                    print('Opcao invalida')

        # gera mudancas em ordem de trabalho
        print('Saindo do painel de atualizacao de equipamento...')

    def excluir_equipamento(self):
        print('''[ Painel de exclusao de equipamento ]''')
        codigo = input('>> Insira o codigo do equipamento a ser excluido: \n> ')
        equipamento = self.retorna_equipamento_bd(codigo)

        if equipamento is None:
            print('> Equipamento nao encontrado!')
            return

        confirm = input('>> Deseja realmente excluir o equipamento ? [S/s]')
        if confirm == 'S' or confirm == 's':
            equipamento.remover_equipamento_db()
            print('> Equipamento excluido com sucesso')

    def interface_equipe_de_reparo(self, user):

        selection = {
            '1': 'consultar_equipe',
            '2': 'registrar_equipe',
            '3': 'modificar_equipe',
            '4': 'excluir_equipe',
        }

        while 1:
            print(''' [ Bem vindo ao painel de equipe de reparo ]
                                 1) Consultar equipe de reparo
                                 2) Registrar equipe de reparo
                                 3) Modificar equipe de reparo
                                 4) Excluir equipe de reparo
                                 5) Sair
                                 ''')

            option = input("> ")

            if option == '5':
                break
            else:
                try:
                    getattr(self, selection[option])()
                except KeyError:
                    print('Opcao invalida')

        print('Saindo do painel de equipe de reparo...')

    def consultar_equipe(self):

        selection = {
            '1': 'consultar_todas_equipes',
            '2': 'consultar_equipe_especifica'
        }

        while 1:
            print('''[ Painel de consulta de equipe ]
                        1) Consultar todas as equipes de reparo
                        2) Consultar equipe de reparo especifica
                        3) Sair
            ''')
            option = input('> ')

            if option == '3':
                break
            else:
                try:
                    getattr(self, selection[option])()
                except KeyError:
                    print('Opcao invalida')

    def consultar_todas_equipes(self):
        #with db_connection:
        db_cursor.execute("SELECT * FROM equipeDeReparo")
        lst = db_cursor.fetchall()
        for entry in lst:
            equipe_de_reparo = self.retorna_equipe_de_reparo_bd(entry[0])
            equipe_de_reparo.mostrar_equipe_de_reparo()

    def consultar_equipe_especifica(self):
        identificador = input('>> Insira o identificador da equipe a ser consultada: \n> ')
        #with db_connection:
        db_cursor.execute("SELECT * FROM equipeDeReparo WHERE identificador = :identificador",
                          {'identificador': identificador})
        lst = db_cursor.fetchall()

        if not lst:
            print('>> Equipe nao encontrada!')
            return

        entry = lst[0]
        equipe_de_reparo = self.retorna_equipe_de_reparo_bd(entry[0])
        equipe_de_reparo.mostrar_equipe_de_reparo()

    def registrar_equipe(self):#numeroDePessoas, funcionarios
        print('>> Insira o numero de pessoas na equipe: ')
        numero_de_pessoas = self.valid_int_input()
        funcionarios = []

        for i in range(0, numero_de_pessoas):
            temp = input('>> Insira o nome do integrante da equipe: ')
            funcionarios.append(temp)

        equipe = EquipeDeReparo(numero_de_pessoas, funcionarios)

        equipe.inserir_equipe_de_reparo_db()

    def modificar_equipe(self): # gera mudancas em ordem
        identificador = input('>> Insira o identificador da equipe:\n> ')
        equipe = self.retorna_equipe_de_reparo_bd(identificador)

        if equipe is None:
            print('>> Equipe nao encontrado')
            return

        identificador_old = equipe.identificador

        print('>> Insira o numero de pessoas na equipe: ')
        numero_de_pessoas = self.valid_int_input()
        funcionarios = []

        for i in range(0, numero_de_pessoas):
            temp = input('>> Insira o nome do integrante da equipe: ')
            funcionarios.append(temp)

        funcionarios = ','.join(funcionarios)

        equipe.atualizar_numeroDePessoas(numero_de_pessoas)
        equipe.atualizar_funcionarios(funcionarios)

        self.equipe_modificada_atualiza_ordem(identificador_old)
        print('>> Equipe atualizada!')
        print('>> Saindo do painel de atualizacao de equipamento...')

    def equipe_modificada_atualiza_ordem(self, identificador_equipe):
        db_cursor.execute("SELECT * FROM ordemDeTrabalho WHERE equipeDeReparo = :identificador ",
                          {'identificador': identificador_equipe})

        lst = db_cursor.fetchall()

        for entry in lst:
            ordem = self.retorna_ordem_de_trabalho_bd(entry[0])
            if ordem is not None:
                id_old_ordem = ordem.identificador
                ordem.atualizar_equipeDeReparo(identificador_equipe)
                self.ordem_modificada_atualiza_reparo(ordem,id_old_ordem)

    def excluir_equipe(self):
        print('''[ Painel de exclusao de equipe ]''')
        codigo = input('>> Insira o codigo da equipe a ser excluida: \n> ')
        equipe = self.retorna_equipe_de_reparo_bd(codigo)

        if equipe is None:
            print('> Equipe nao encontrada!')
            return

        confirm = input('>> Deseja realmente excluir a equipe ? [S/s] \n> ')
        if confirm == 'S' or confirm == 's':
            equipe.remover_equipe_de_reparo_db()
            print('> Equipe excluida com sucesso')

    def interface_ordem_de_trabalho(self, user):

        selection = {
            '1': 'consultar_ordem',
            '2': 'registrar_ordem',
            '3': 'modificar_ordem',
            '4': 'excluir_ordem',
        }

        while 1:
            print(''' [ Bem vindo ao painel de ordem de trabalho ]
                                 1) Consultar ordem de trabalho
                                 2) Registrar ordem de trabalho
                                 3) Modificar ordem de trabalho
                                 4) Excluir ordem de trabalho
                                 5) Sair
                                 ''')

            option = input("> ")

            if option == '5':
                break
            else:
                try:
                    getattr(self, selection[option])()
                except KeyError:
                    print('Opcao invalida')

        print('Saindo do painel de ordem de trabalho...')

    def consultar_ordem(self):

        selection = {
            '1': 'consultar_todas_ordens',
            '2': 'consultar_ordem_especifica'
        }

        while 1:
            print('''[ Painel de consulta de ordens ]
                        1) Consultar todas as ordens de trabalho
                        2) Consultar ordem de trabalho especifica
                        3) Sair
            ''')
            option = input('> ')

            if option == '3':
                break
            else:
                try:
                    getattr(self, selection[option])()
                except KeyError:
                    print('Opcao invalida')

    def consultar_todas_ordens(self):
        #with db_connection:
        db_cursor.execute("SELECT * FROM ordemDeTrabalho")
        lst = db_cursor.fetchall()
        for entry in lst:
            ordem = self.retorna_ordem_de_trabalho_bd(entry[0])
            ordem.mostrar_ordem_de_trabalho()

    def consultar_ordem_especifica(self):
        identificador = input('>> Insira o identificador da ordem a ser consultada: \n> ')
        #with db_connection:
        db_cursor.execute("SELECT * FROM ordemDeTrabalho WHERE identificador = :identificador",
                          {'identificador': identificador})
        lst = db_cursor.fetchall()
        if not lst:
            print('> Ordem nao encontrada')
            return
        entry = lst[0]
        ordem = self.retorna_ordem_de_trabalho_bd(entry[0])
        ordem.mostrar_ordem_de_trabalho()

    def registrar_ordem(self):
        # endereco, tamanho, localizacao, prioridade,registradoPor,
        # descricao,situacao, equipeDeReparo, equipamentos, horasAplicadas

        identificador_buraco = input('>> Insira o identificador do buraco sobre o qual sera criado a ordem de trabalho:'
                                     '\n> ')
        buraco = self.retorna_buraco_bd(identificador_buraco)

        if buraco is None:
            print('> Buraco nao encontrado ')
            return

        descricao = input('>> Insira a descricao da ordem de trabalho: ')
        situacao = input('>> Insira a situacao da ordem de trabalho: ')
        equipeDeReparo = input('>> Insira o identificador da equipe de reparo responsavel: ')

        print('>> Insira o numero de equipamentos utilizados: ')
        numero_de_equipamentos = self.valid_int_input()
        equipamentos = []
        for i in range(0, numero_de_equipamentos):
            temp = input('>> Insira o identificador do equipamento: ')
            equipamentos.append(temp)

        ##debug
        #print('####' + equipamentos)

        print('>> Insira a quantidade de horas aplicadas: ')
        horasAplicadas = self.valid_int_input()

        ordem = OrdemDeTrabalho(buraco.endereco, buraco.tamanho, buraco.localizacao, buraco.prioridade,
                                buraco.registradoPor, descricao, situacao, equipeDeReparo, equipamentos, horasAplicadas)

        ordem.inserir_ordem_de_trabalho_db()

    def modificar_ordem(self):
        identificador = input('>> Insira o identificador da ordem:\n> ')
        ordem = self.retorna_ordem_de_trabalho_bd(identificador)
        if ordem is None:
            print('>> Ordem nao encontrada')
            return

        selection = {
            '1': 'atualizar_descricao',
            '2': 'atualizar_situacao',
            '3': 'atualizar_equipeDeReparo',
            '4': 'atualizar_equipamentos',
            '5': 'atualizar_horasAplicadas'
        }

        identificador_old = ordem.identificador

        while 1:
            print(''' [ Bem vindo ao painel de atualizacao de ordem de reparo ]\n [ Selecione o atributo a ser atualizado: ]
                                                 1) Descricao
                                                 2) Situacao
                                                 3) Equipe de reparo
                                                 4) Equipamentos
                                                 5) Horas aplicadas
                                                 6) Sair
                                                 ''')

            option = input("> ")

            if option == '6':
                break

            elif option == '5':
                print('>> Insira o novo valor do atributo: ')
                novo_valor = self.valid_int_input()
                getattr(ordem, selection[option])(novo_valor)
                print('> Valor atualizado!')

            elif option == '4':
                print('>> Insira o numero de equipamentos utilizados: ')
                numero_de_equipamentos = self.valid_int_input()
                equipamentos = []
                for i in range(0, numero_de_equipamentos):
                    temp = input('>> Insira o identificador do equipamento: ')
                    equipamentos.append(temp)

                getattr(ordem, selection[option])(equipamentos)
                print('> Valor atualizado!')

            else:
                print('>> Insira o novo valor do atributo: ')
                novo_valor = input('> ')
                try:
                    getattr(ordem, selection[option])(novo_valor)
                    print('> Valor atualizado!')
                except KeyError:
                    print('Opcao invalida')

        self.ordem_modificada_atualiza_reparo(ordem, identificador_old)

        print('Saindo do painel de atualizacao de buraco...')

    def ordem_modificada_atualiza_reparo(self,ordem,identificador_old):
        db_cursor.execute("SELECT * FROM reparo WHERE identificador = :identificador ",
                          {'identificador': identificador_old})

        lst = db_cursor.fetchall()

        for entry in lst:
            reparo = self.retorna_reparo_bd(entry[0])
            if reparo is not None:
                reparo.ordem_atualizada(ordem)

    def excluir_ordem(self):
        print('''[ Painel de exclusao de ordem de trabalho ]''')
        codigo = input('>> Insira o codigo da ordem de trabalho a ser excluida: \n> ')
        ordem = self.retorna_ordem_de_trabalho_bd(codigo)

        if ordem is None:
            print('> Ordem nao encontrada!')
            return

        confirm = input('>> Deseja realmente excluir a ordem ? [S/s] \n> ')
        if confirm == 'S' or confirm == 's':
            ordem.remover_ordem_de_trabalho_db()
            print('> Ordem excluida com sucesso')

    def interface_reparo(self, user):

        selection = {
            '1': 'consultar_reparo',
            '2': 'registrar_reparo',
            '3': 'modificar_reparo',
            '4': 'excluir_reparo',
            '5': 'calcula_custo_reparo'
        }

        while 1:
            print(''' [ Bem vindo ao painel de reparos ]
                                 1) Consultar reparo
                                 2) Registrar reparo
                                 3) Modificar reparo
                                 4) Excluir reparo
                                 5) Calcular custo do reparo
                                 6) Sair
                                 ''')

            option = input("> ")

            if option == '6':
                break
            else:
                try:
                    getattr(self, selection[option])()
                except KeyError:
                    print('Opcao invalida')

        print('Saindo do painel de reparos...')

    def consultar_reparo(self):

        selection = {
            '1': 'consultar_todos_reparos',
            '2': 'consultar_reparo_especifico'
        }

        while 1:
            print('''[ Painel de consulta de reparo ]
                        1) Consultar todas os reparos
                        2) Consultar reparo especifica
                        3) Sair
            ''')
            option = input('> ')

            if option == '3':
                break
            else:
                try:
                    getattr(self, selection[option])()
                except KeyError:
                    print('Opcao invalida')

    def consultar_todos_reparos(self):
        #with db_connection:
        db_cursor.execute("SELECT * FROM reparo")
        lst = db_cursor.fetchall()
        for entry in lst:
            reparo = self.retorna_reparo_bd(entry[0])
            reparo.mostrar_reparo()

    def consultar_reparo_especifico(self):
        identificador = input('>> Insira o identificador do reparo a ser consultado: \n> ')
        #with db_connection:
        db_cursor.execute("SELECT * FROM reparo WHERE identificador = :identificador",
                          {'identificador': identificador})
        lst = db_cursor.fetchall()
        if not lst:
            print('>> Reparo nao encontrado')
            return
        entry = lst[0]
        reparo = self.retorna_reparo_bd(entry[0])
        reparo.mostrar_reparo()

    def registrar_reparo(self):
        # endereco, tamanho, localizacao, prioridade, registradoPor, descricao, situacao,
        # equipeDeReparo, equipamentos, horasAplicadas,
        # descricaoReparo, status, materialUtilizado

        identificador_ordem = input('>> Insira o identificador da ordem de trabalho sobre a qual sera criado o reparo:'
                                    '\n> ')

        ordem = self.retorna_ordem_de_trabalho_bd(identificador_ordem)

        #ordem.mostrar_ordem_de_trabalho()

        if ordem is None:
            print('> Ordem nao encontrada ')
            return

        descricaoReparo = input('>> Insira a descricao do reparo: ')
        status = input('>> Insira a situacao do reparo: ')

        print('>> Insira o numero de materiais utilizados: ')
        numero_de_materiais = self.valid_int_input()
        materialUtilizado = []
        for i in range(0, numero_de_materiais):
            temp = input('>> Insira o identificador do material: ')
            materialUtilizado.append(temp)
        if len(materialUtilizado) > 1:
            materialUtilizado = ','.join(materialUtilizado)
        else:
            materialUtilizado = materialUtilizado[0]

        if not isinstance(ordem.equipamentos, str):
            equipamentos = ','.join(ordem.equipamentos)
        else:
            equipamentos = ordem.equipamentos

        reparo = Reparo(ordem.endereco, ordem.tamanho, ordem.localizacao, ordem.prioridade, ordem.registradoPor,
                        ordem.descricao, ordem.situacao, ordem.equipeDeReparo, equipamentos, ordem.horasAplicadas,
                        descricaoReparo, status, materialUtilizado)

        reparo.mostrar_reparo()

        reparo.inserir_reparo_db()

    def modificar_reparo(self):
        identificador = input('>> Insira o identificador do reparo:\n> ')
        reparo = self.retorna_reparo_bd(identificador)
        if reparo is None:
            #print('>> Reparo nao encontrado')
            return

        selection = {
            '1': 'atualizar_descricaoReparo',
            '2': 'atualizar_status',
            '3': 'atualizar_materialUtilizado',
            '4': 'atualizar_custo',
        }

        while 1:
            print(''' [ Bem vindo ao painel de atualizacao de reparo ]\n [ Selecione o atributo a ser atualizado: ]
                                             1) Descricao do reparo
                                             2) Status
                                             3) Material Utilizado
                                             4) Custo
                                             5) Sair
                                             ''')

            option = input("> ")

            if option == '5':
                break

            elif option == '3':
                print('>> Insira o numero de materiais utilizados: ')
                numero_de_materiais = self.valid_int_input()
                materialUtilizado = []
                for i in range(0, numero_de_materiais):
                    temp = input('>> Insira o identificador do material: ')
                    materialUtilizado.append(temp)

                getattr(reparo, selection[option])(materialUtilizado)
                print('> Valor atualizado!')

            elif option == '4':
                print('>> Insira o novo valor do atributo: ')
                novo_valor = self.valid_int_input()
                getattr(reparo, selection[option])(novo_valor)
                print('> Valor atualizado!')

            else:
                print('>> Insira o novo valor do atributo: ')
                novo_valor = input('> ')
                try:
                    getattr(reparo, selection[option])(novo_valor)
                    print('> Valor atualizado!')
                except KeyError:
                    print('Opcao invalida')

        print('Saindo do painel de atualizacao de reparo...')

    def excluir_reparo(self):
        print('''[ Painel de exclusao de reparo ]''')
        codigo = input('>> Insira o codigo do reparo a ser excluido: \n> ')
        reparo = self.retorna_reparo_bd(codigo)

        if reparo is None:
            print('> Reparo nao encontrado!')
            return

        confirm = input('>> Deseja realmente excluir o reparo ? [S/s] \n> ')
        if confirm == 'S' or confirm == 's':
            reparo.remover_reparo_db()
            print('> Reparo excluido com sucesso')

    def calcula_custo_reparo(self):
        identificador = input('>> Insira o identificador do reparo: \n> ')
        # with db_connection:
        db_cursor.execute("SELECT * FROM reparo WHERE identificador = :identificador",
                          {'identificador': identificador})
        lst = db_cursor.fetchall()
        if not lst:
            print('>> Reparo nao encontrado')
            return
        entry = lst[0]
        reparo = self.retorna_reparo_bd(entry[0])
        custo = reparo.calcula_custo()
        print(f'\t [ Custo total do reparo: {custo} ]')
        reparo.atualizar_custo(custo)

    def int_input(self):
        while True:
            valor = input('> ')
            try:
                valor = int(valor)
                return valor
            except ValueError:
                print('>> Insira um inteiro valido')

    def valid_int_input(self):
        while True:
            valor = self.int_input()
            if valor > 0:
                return valor
            else:
                print('>> Insira um valor positivo')





