import hashlib
import re
 
from app.conexao import db
from app.validadores import ler_texto, ler_cpf, ler_logradouro, ler_cep, ler_sim_nao

#INSERT
def create_usuario():
    global db
    mycol = db.usuario
    print("\nInserindo um novo usuário")
    nome = ler_texto("Nome: ")
    sobrenome = ler_texto("Sobrenome: ")
    cpf = ler_cpf("CPF: ")
    senha = hashlib.sha256(input("Senha: ").encode()).hexdigest()
    key = 'S'
    end = []
    while (key != 'N'):
        logradouro = ler_logradouro("Logradouro: ")
        num = input("Núm: ").strip()
        bairro = ler_texto("Bairro: ")
        cidade = ler_texto("Cidade: ")
        estado = ler_texto("Estado (sigla): ")
        cep = ler_cep("CEP: ")
        endereco = {        #isso nao eh json, isso é chave-valor, eh um obj
            "logradouro":logradouro,
            "num": num,
            "bairro": bairro,
            "cidade": cidade,
            "estado": estado,
            "cep": cep
        }
        end.append(endereco) #estou inserindo na lista
        key = ler_sim_nao("Deseja cadastrar um novo endereço (S/N)? ")
    mydoc = { "nome": nome, "sobrenome": sobrenome, "cpf": cpf, "end": end }
    x = mycol.insert_one(mydoc)
    print("Documento inserido com ID ",x.inserted_id)

#READ
def read_usuario(nome):
    global db
    mycol = db.usuario
    print("Usuários existentes: ")
    if not len(nome):
        mydoc = mycol.find().sort("nome")
        for x in mydoc:
            print(x["nome"],x["cpf"])
    else:
        myquery = {"nome": {"$regex": re.escape(nome), "$options": "i"}}
        mydoc = mycol.find(myquery)
        for x in mydoc:
            print(x)

#UPDATE
def update_usuario(identificador):
    global db
    mycol = db.usuario
    termo = identificador.strip()

    # Busca por CPF ou por Nome (case-insensitive)
    myquery = {
        "$or": [
            {"cpf": termo},
            {"nome": {"$regex": re.escape(termo), "$options": "i"}}
        ]
    }
    mydoc = mycol.find_one(myquery)
    if mydoc is None:
        print(f"Usuário '{termo}' não encontrado.")
        return  

    # Busca case-insensitive para achar independente de maiúsculas/minúsculas
    myquery = {"nome": {"$regex": re.escape(nome), "$options": "i"}}

    mydoc = mycol.find_one(myquery)

    # Se não encontrar, avisa e encerra sem dar erro
    if mydoc is None:
        print(f"Usuário '{nome}' não encontrado.")
        return

    print("Dados do usuário: ",mydoc)
    novo_nome = input("Mudar Nome:").strip()
    if len(novo_nome):
        mydoc["nome"] = novo_nome

    sobrenome = input("Mudar Sobrenome:")
    if len(sobrenome):
        mydoc["sobrenome"] = sobrenome

    cpf = input("Mudar CPF:")
    if len(cpf):
        while not cpf.isdigit() or len(cpf) != 11:
            print("CPF inválido! Digite 11 números.")
            cpf = input("Mudar CPF:")
        mydoc["cpf"] = cpf

    senha = input("Mudar Senha:")
    if len(senha):
        mydoc["senha"] = hashlib.sha256(senha.encode()).hexdigest()

    newvalues = { "$set": mydoc }
    mycol.update_one({"_id": mydoc["_id"]}, newvalues)
    print("Usuário atualizado com sucesso!")
    
#DELETE
def delete_usuario(nome, sobrenome):
    global db
    mycol = db.usuario
    myquery = {"nome": nome, "sobrenome":sobrenome}
    mydoc = mycol.delete_one(myquery)
    print("Deletado o usuário ",mydoc)
