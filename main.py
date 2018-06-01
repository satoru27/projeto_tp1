import argparse
import hashlib

from SRCB import SRCB

parser = argparse.ArgumentParser()
parser.add_argument("--debug", help="ativa o modo de debug", action="store_true")
args = parser.parse_args()

def main():
    if args.debug:
        print("Rodando SRCB em modo de debug")
        sistema = SRCB(debugCode=1)
    else:
        sistema = SRCB(debugCode=0)

    #sistema.interfacePrincipal()

    teste = sistema.retorna_reparo_bd('5071002941ca7b9abdfe01dc7ea7a069612b1ebb58e0a9d082998101')

    ####### TESTE #######
    # descricao_material = 'eh bem caro'
    # valor = 10
    # quantidade = 10
    # tipo = 'wut'
    # test_material = Material(descricao_material,valor,quantidade,tipo)
    # #test_material.inserir_material_db()
    # test_material.atualizar_descricao('muuuuito caro')

    #
    # descricao_equipamento = 'piche'
    # fabricante = 'quem fabrica piche ai'
    # tamanho = 10
    # peso = 20
    # test_equipamento = Equipamento(descricao_equipamento,fabricante,tamanho,peso)
    # #test_equipamento.inserir_equipamento_db()
    #
    # numeroDePessoas = 3
    # funcionarios = ['Lagostim','Camarao','Lagosta']
    # test_equipe = EquipeDeReparo(numeroDePessoas,funcionarios)
    # #test_equipe.inserir_equipe_de_reparo_db()
    #
    # endereco = Endereco(cidade="Brasilia", uf="DF", bairro="Asa Norte")
    #
    # tamanho = 1
    # localizacao = 'ao lado da faixa de pedestre'
    # prioridade = 5
    # registradoPor = 'lagosta'
    # test_buraco = Buraco(endereco,tamanho,localizacao,prioridade,registradoPor)
    # # test_buraco.inserir_buraco_db()
    #
    # descricao_equipeDeReparo = 'nem sei'
    # situacao = 'complicada'
    # equipeDeReparo = test_equipe.identificador
    # equipamentos = [test_equipamento.codigo]
    # horasAplicadas = 20
    # test_ordemDeTrabalho = test_buraco.gerar_ordem_de_trabalho(descricao_equipeDeReparo,situacao,equipeDeReparo,equipamentos,horasAplicadas)
    # #test_ordemDeTrabalho.inserir_ordem_de_trabalho_db()
    #
    # descricaoReparo = 'ta dificil'
    # status = 'incompleto'
    # materialUtilizado = [test_material.codigo]
    # test_Reparo = test_ordemDeTrabalho.gerar_reparo(descricaoReparo,status,materialUtilizado)
    # #test_Reparo.inserir_reparo_db()
    #
    # tipoDeDano = 'quebrou tudo'
    # pagamento = '100000'
    # idBuraco = 's7dba7sdysa'
    # idCidadao = 'as7dyb97sayd9sa'
    # test_Dano = Dano(tipoDeDano,pagamento,idBuraco,idCidadao)
    # test_Dano.inserir_dano_db()
    #
    # nome = "Admin2"
    # cpf = "919.231.890-85"
    # identidade = "45.772.060-8"
    # filiacao = "UNB"
    # sexo = "ND"
    # estadoCivil = "Solteiro"
    # naturalidade = "Brasilia"
    # endereco = Endereco(cidade="Brasilia", uf="DF", bairro="Asa Norte")
    # email = "admin@thissite.com"
    # profissao = "Website Admin"
    # test_Cidadao = Cidadao(nome,cpf,identidade,filiacao,sexo,estadoCivil,naturalidade,endereco,email,profissao)
    # test_Cidadao.inserir_cidadao_db()
    #
    # cargo = "Administratoooor"
    # salario = "999"
    # test_Funcionario = test_Cidadao.gerar_funcionario(cargo,salario)
    # test_Funcionario.inserir_funcionario_db()


if __name__ == "__main__":
    main()