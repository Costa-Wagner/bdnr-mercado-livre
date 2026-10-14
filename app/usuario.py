import hashlib
import re
 
from app.conexao import db
from app.validadores import ler_texto, ler_cpf, ler_logradouro, ler_cep, ler_sim_nao

def ler_email(msg, mycol):
    """Pede o e-mail até ser válido e ainda não cadastrado (ele vira a chave no Redis)."""
    while True:
        email = input(msg).strip().lower()
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
            print("E-mail inválido. Exemplo: paola.silva@teste.com")
            continue
        if mycol.find_one({"email": email}):
            print("Esse e-mail já está cadastrado.")
            continue
        return email
    
#INSERT
def create_usuario():
    global db
    mycol = db.usuario
    print("\nInserindo um novo usuário")
    nome = ler_texto("Nome: ")
    sobrenome = ler_texto("Sobrenome: ")
    cpf = ler_cpf("CPF: ")
    senha = hashlib.sha256(input("Senha: ").encode()).hexdigest()
    email = ler_email("E-mail: ", mycol)
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
    mydoc = { "nome": nome, "sobrenome": sobrenome, "cpf": cpf, "end": end, "email": email, "end": end, "favoritos": [] }
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
    achados = list(mycol.find(myquery))
    if not achados:
        print(f"Usuário '{termo}' não encontrado.")
        return
    if len(achados) == 1:
        mydoc = achados[0]
    else:
        print("Mais de um usuário encontrado:")
        for i, u in enumerate(achados):
            print(f"  [{i}] {u.get('nome', '')} {u.get('sobrenome', '')} - CPF {u.get('cpf', '')}")
        escolha = input("Número do usuário a atualizar: ").strip()
        if not (escolha.isdigit() and int(escolha) < len(achados)):
            print("Número inválido.")
            return
        mydoc = achados[int(escolha)]    

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

    atual = mydoc.get("email", "sem e-mail")
    email = input(f"Mudar E-mail [{atual}] (Enter mantém): ").strip().lower()
    if email and email != mydoc.get("email"):
        while not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email) or mycol.find_one({"email": email}):
            print("E-mail inválido ou já cadastrado.")
            email = input("Mudar E-mail (Enter mantém): ").strip().lower()
            if not email:
                break
        if email:
            mydoc["email"] = email
            print("Atenção: rode a opção 5 para criar as chaves do novo e-mail no Redis.")

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
