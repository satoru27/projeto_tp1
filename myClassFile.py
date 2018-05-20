
class Cidadao:
	def __init__(self,identificador,nome,cpf,identidade,filiacao,sexo,estadoCivil,naturalidade,endereco,email,profissao,funcionario,recebeuDano):
		self.identificador = identificador
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
		self.funcionario = funcionario
		self.recebeuDano = recebeuDano

	def inserirCadastro(self):
		pass

	def removerCadastro(self):
		pass

	def modificarCadastro(self):
		pass

	def consultaArquivoDeDanos(self):
		pass

	def realizaConsultaGeral(self):
		pass

	def geraRelatorio(self):
		pass

	def inserirBuraco(self):
		pass

	def removerBuraco(self):
		pass

	def modificarBuraco(self):
		pass

	def inserirDanoRecebido(self):
		pass

	def removerDanoRecebido(self):
		pass

	def modificarDanoRecebido(self):
		pass



class Endereco:
	def __init__(self,cidade,uf,bairro):
		self.cidade = cidade
		self.uf = uf
		self.bairro = bairro

class Dano:
	def __init__(self,idDano,tipoDeDano,pagamento,idBuraco,idCidadao):
		self.idDano = idDano
		self.tipoDeDano = tipoDeDano
		self.pagamento = pagamento
		self.idBuraco = idBuraco
		self.idCidadao = idCidadao

class Funcionario(Cidadao):
	def __init__(self,identificador,nome,cpf,identidade,filiacao,sexo,estadoCivil,naturalidade,endereco,email,profissao,funcionario,recebeuDano,codigo,cargo,salario):
		super(Funcionario,self).__init__(self,identificador,nome,cpf,identidade,filiacao,sexo,estadoCivil,naturalidade,endereco,email,profissao,funcionario,recebeuDano)
		self.codigo = codigo
		self.cargo = cargo
		self.salario = salario

	def inserirCadastroFuncionario(self):
		pass

	def modificarCadastroFuncionario(self):
		pass

	def removerCadastroFuncionario(self):
		pass

	def inserirMaterialDeReparo(self):
		pass
	
	def modificarMaterialDeReparo(self):
		pass
	
	def removerMaterialDeReparo(self):
		pass
	
	def inserirEquipamento(self):
		pass
	
	def modificarEquipamento(self):
		pass
	
	def removerEquipamento(self):
		pass
	
	def inserirEquipe(self):
		pass

	def modificarEquipe(self):
		pass
		
	def removerEquipe(self):
		pass
		
	def inserirReparo(self):
		pass
		
	def removerReparo(self):
		pass
		
	def modificarReparo(self):
		pass
		
	def inserirOrdemDeTrabalho(self):
		pass
		
	def removerOrdemDeTrabalho(self):
		pass
		
	def modificarOrdemDeTrabalho(self):
		pass


class Buraco:
	def __init__(self,identificador,endereco,tamanho,localizacao,prioridade,registradoPor):
		self.identificador = identificador
		self.endereco = endereco
		self.tamanho = tamanho
		self.localizacao = localizacao
		self.prioridade = prioridade
		self.registradoPor = registradoPor

class OrdemDeTrabalho(Buraco):
	def __init__(self,identificador,endereco,tamanho,localizacao,prioridade,registradoPor,codigo,descricao,situacao,equipeDeReparo,equipamentos,horasAplicadas):
		super(OrdemDeTrabalho,self).__init__(self,identificador,endereco,tamanho,localizacao,prioridade,registradoPor)
		self.codigo = codigo
		self.descricao = descricao
		self.situacao = situacao
		self.equipeDeReparo = equipeDeReparo
		self.equipamentos = equipamentos
		self.horasAplicadas = horasAplicadas

class Reparo(OrdemDeTrabalho):
	def __init__(self,id,endereco,tamanho,localizacao,prioridade,registradoPor,codigo,descricao,situacao,equipeDeReparo,equipamentos,horasAplicadas,codigoReparo,descricaoReparo,status,materialUtilizado,custo):
		super(Reparo,self).__init__(self,identificador,endereco,tamanho,localizacao,prioridade,registradoPor,codigo,descricao,situacao,equipeDeReparo,equipamentos,horasAplicadas)
		self.codigoReparo = codigoReparo
		self.descricaoReparo = descricaoReparo
		self.status = status
		self.materialUtilizado = materialUtilizado
		self.custo = custo

	def calculaReparo(self):
		pass


class EquipeDeReparo:
	def __init__(self,identificador,numeroDePessoas,funcionarios):
		self.identificador = identificador
		self.numeroDePessoas = numeroDePessoas
		self.funcionarios = funcionarios

class Equipamento:
	def __init__(self,codigo,descricao,fabricante,tamanho,peso):
		self.codigo = codigo
		self.descricao = descricao
		self.fabricante = fabricante
		self.tamanho = tamanho
		self.peso = peso

	def calculaCustoEquipamento():
		pass

class Material:
	def __init__(self,codigo,descricao,valor,quantidade,tipo):
		self.codigo = codigo
		self.descricao = descricao
		self.valor = valor
		self.quantidade = quantidade
		self.tipo = tipo

	def calculaCustoMaterial():
		pass
