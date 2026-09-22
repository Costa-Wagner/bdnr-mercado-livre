import hashlib

from app.conexao import db
from app.validadores import ler_texto, ler_cpf_cnpj, ler_cep, ler_telefone, ler_sim_nao, cpf_cnpj_valido

#INSERT
def create_vendedor():
    mycol = db.vendedor
    print("\nInserindo um novo vendedor")

    nome_fantasia = input("Nome Fantasia: ").strip()
    razao_social = input("Razão Social: ").strip()
    cpf_cnpj = ler_cpf_cnpj("CPF/CNPJ: ")
    senha = hashlib.sha256(input("Digite a senha:").encode()).hexdigest()
    telefone = ler_telefone("Telefone: ")
    email = input("E-mail: ").strip()

    key = 'S'
    end = []
    while (key != 'N'):
        tipo = input("Tipo (comercial/entrega/cobranca): ").strip().lower()
        logradouro = input("Logradouro: ").strip()
        bairro = ler_texto("Bairro: ")
        cidade = ler_texto("Cidade: ")
        estado = ler_texto("Estado: ")
        cep = ler_cep("CEP: ")
        endereco = {
            "tipo": tipo,
            "logradouro": logradouro,
            "bairro": bairro,
            "cidade": cidade,
            "estado": estado,
            "cep": cep
        }
        end.append(endereco)
        key = ler_sim_nao("Deseja cadastrar um novo endereço (S/N)? ")
    mydoc = {
        "nomeFantasiaVendedor": nome_fantasia,
        "razaoSocialVendedor": razao_social,
        "cpf_cnpjVendedor": cpf_cnpj,
        "senhaVendedor": senha,
        "enderecoVendedor": end,
        "telefoneVendedor": telefone,
        "emailVendedor": email
    }
    x = mycol.insert_one(mydoc)
    print("Documento inserido com ID ", x.inserted_id)

#READ
def read_vendedor(nome, cpf_cnpj):
    mycol = db.vendedor
    print("Vendedores existentes: ")
    if not len(nome) and not len(cpf_cnpj):
        mydoc = mycol.find().sort("nomeFantasiaVendedor")
        for x in mydoc:
            print(x["nomeFantasiaVendedor"], x["cpf_cnpjVendedor"])
    else:
        myquery = {}
        if len(nome):
            myquery["nomeFantasiaVendedor"] = nome
        if len(cpf_cnpj):
            myquery["cpf_cnpjVendedor"] = cpf_cnpj
        mydoc = mycol.find(myquery)
        for x in mydoc:
            print(x)

#UPDATE
def update_vendedor(nome):
    mycol = db.vendedor
    myquery = {"nomeFantasiaVendedor": nome}
    mydoc = mycol.find_one(myquery)
    if mydoc is None:
        print("Vendedor não encontrado.")
        return
    print("Dados do vendedor: ", mydoc)

    novo_nome_fantasia = input("Mudar Nome Fantasia:")
    if len(novo_nome_fantasia):
        mydoc["nomeFantasiaVendedor"] = novo_nome_fantasia

    razao_social = input("Mudar Razão Social:")
    if len(razao_social):
        mydoc["razaoSocialVendedor"] = razao_social

    cpf_cnpj = input("Mudar CPF/CNPJ:")
    if len(cpf_cnpj):
        while not cpf_cnpj_valido(cpf_cnpj):
            print("CPF/CNPJ inválido! CPF: 11 números. CNPJ: 14 caracteres (12 alfanuméricos + 2 dígitos verificadores numéricos).")
            cpf_cnpj = input("Mudar CPF/CNPJ:")
        mydoc["cpf_cnpjVendedor"] = cpf_cnpj.upper()

    senha = input("Mudar Senha:")
    if len(senha):
        mydoc["senhaVendedor"] = hashlib.sha256(senha.encode()).hexdigest()

    telefone = input("Mudar Telefone:")
    if len(telefone):
        while not telefone.isdigit():
            print("Telefone inválido! Digite apenas números.")
            telefone = input("Mudar Telefone:")
        mydoc["telefoneVendedor"] = telefone
    email = input("Mudar E-mail:")
    if len(email):
        mydoc["emailVendedor"] = email

    mudar_end = ler_sim_nao("Mudar Endereço(s)? (S/N) ")
    if mudar_end == 'S':
        end = []
        key = 'S'
        while (key != 'N'):
            tipo = input("Tipo (comercial/entrega/cobranca): ").strip().lower()
            logradouro = input("Logradouro: ").strip()
            bairro = ler_texto("Bairro: ")
            cidade = ler_texto("Cidade: ")
            estado = ler_texto("Estado: ")
            cep = ler_cep("CEP: ")
            endereco = {
                "tipo": tipo,
                "logradouro": logradouro,
                "bairro": bairro,
                "cidade": cidade,
                "estado": estado,
                "cep": cep
            }
            end.append(endereco)
            key = ler_sim_nao("Cadastrar outro endereço (S/N)? ")
        mydoc["enderecoVendedor"] = end

    newvalues = {"$set": mydoc}
    mycol.update_one(myquery, newvalues)

#DELETE
def delete_vendedor(nome, cpf_cnpj):
    mycol = db.vendedor
    myquery = {"nomeFantasiaVendedor": nome, "cpf_cnpjVendedor": cpf_cnpj}
    mydoc = mycol.delete_one(myquery)
    print("Deletado o vendedor ", mydoc)