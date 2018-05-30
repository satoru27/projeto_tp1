import sqlite3
import hashlib as hs
import myClassFile

conn = sqlite3.connect('srcb.db')

c = conn.cursor()

# c.execute("""CREATE TABLE cidadao (
# identificador text,
# nome text,
# cpf text,
# identidade text,
# filiacao text,
# sexo text,
# estadoCivil text,
# naturalidade text,
# endereco text,
# email text,
# profissao text,
# funcionario integer,
# recebeuDano integer
# )""")

# c.execute("""CREATE TABLE funcionario(
# identificador TEXT,
# nome TEXT,cpf TEXT, identidade TEXT, filiacao TEXT,
#  sexo TEXT, estadoCivil TEXT, naturalidade TEXT, endereco TEXT, email TEXT,
#                  profissao TEXT, funcionario INTEGER, recebeuDano INTEGER, codigo TEXT, cargo TEXT, salario TEXT
# )""")
#
# c.execute(""" CREATE TABLE  endereco(
# cidade TEXT,
# uf TEXT,
# bairro TEXT
# )""")
#
# c.execute("""CREATE TABLE dano(
# idDano text, tipoDeDano text, pagamento text, idBuraco text, idCidadao text
# )""")
#
# c.execute("""CREATE TABLE buraco(
# identificador TEXT, endereco TEXT, tamanho INTEGER, localizacao TEXT, prioridade INTEGER, registradoPor TEXT
# )""")
#
# c.execute("""CREATE TABLE ordemDeTrabalho(
# identificador text, endereco text, tamanho integer, localizacao text, prioridade integer,
#  registradoPor text, codigo text, descricao text,
#                  situacao text, equipeDeReparo text, equipamentos text, horasAplicadas integer
# )""")
#
# c.execute("""CREATE TABLE reparo(
# identificador TEXT, endereco TEXT, tamanho INTEGER, localizacao TEXT, prioridade INTEGER, registradoPor TEXT,
#  codigo TEXT, descricao TEXT, situacao TEXT,
#                  equipeDeReparo TEXT, equipamentos TEXT, horasAplicadas INTEGER, codigoReparo TEXT,
#                   descricaoReparo TEXT, status TEXT, materialUtilizado TEXT,
#                  custo TEXT
# )""")
#
# c.execute("""CREATE TABLE equipeDeReparo (
# identificador TEXT, numeroDePessoas INTEGER, funcionarios TEXT
# )""")
#
# c.execute("""CREATE TABLE equipamento(
# codigo text, descricao text, fabricante text, tamanho integer, peso integer
# )""")
#
# c.execute("""CREATE TABLE material(
# codigo TEXT, descricao TEXT, valor INTEGER, quantidade INTEGER, tipo TEXT
# )""")

nome = "Admin"
cpf = "919.231.890-85"
identidade = "45.772.060-8"
filiacao = "UNB"
sexo = "ND"
estadoCivil = "Solteiro"
naturalidade = "Brasilia"
endereco = ",".join(["Brasilia", "DF", "Asa Norte"]) #atencao a isso
email = "admin@thissite.com"
profissao = "Website Admin"
funcionario = int(True) #atencao
recebeuDano = int(False)
codigo = "000"
cargo = "Administrator"
salario = "999"
identificador = hs.sha224((nome + cpf).encode('utf-8')).hexdigest()
#identificador = "batata"

#c.execute("INSERT INTO funcionario VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(identificador,nome,cpf,identidade,filiacao,sexo,estadoCivil,naturalidade,endereco,email,profissao,funcionario,recebeuDano,codigo,cargo,salario))
idDano = ""
tipoDeDano = ""
pagamento = ""
idBuraco = ""
idCidadao = ""

dano1 = myClassFile.Dano("3122141","quebrou tudo","100000","321421","421037218")

#checar antes do insert se nao há registros duplicados, checar o id antes de executar o insert
c.execute("INSERT INTO dano VALUES(:idDano, :tipoDeDano, :pagamento, :idBuraco, :idCidadao)",{'idDano':dano1.idDano, 'tipoDeDano':dano1.tipoDeDano, 'pagamento':dano1.pagamento, 'idBuraco':dano1.idBuraco, 'idCidadao':dano1.idCidadao})

c.execute("SELECT * FROM dano")

print(c.fetchall())

conn.commit()

conn.close()