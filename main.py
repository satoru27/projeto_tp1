from myClassFile import *
import argparse
import hashlib

parser = argparse.ArgumentParser()
parser.add_argument("--debug", help="ativa o modo de debug", action="store_true")
args = parser.parse_args()

def main():
    # if args.debug:
    #     print("Rodando SRCB em modo de debug")
    #     sistema = SRCB(debugCode=1)
    # else:
    #     sistema = SRCB(debugCode=0)
    #
    # sistema.interfacePrincipal()

    nome = "Admin"
    cpf = "919.231.890-85"
    identidade = "45.772.060-8"
    filiacao = "UNB"
    sexo = "ND"
    estadoCivil = "Solteiro"
    naturalidade = "Brasilia"
    endereco = Endereco(cidade="Brasilia", uf="DF", bairro="Asa Norte")
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

    temp.inserir_cadastro_db()

if __name__ == "__main__":
    main()