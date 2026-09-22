from datetime import datetime
from bson.decimal128 import Decimal128
from bson.objectid import ObjectId
 
from app.conexao import db
from app.validadores import ler_cpf, ler_cpf_cnpj, ler_sim_nao

#INSERT
def create_compra():
    global db
    mycol = db.compra
    mycol_usuario = db.usuario
    mycol_vendedor = db.vendedor
    mycol_produto = db.produto
    print("\nInserindo uma nova compra")
 
    cpf_usuario = ler_cpf("CPF do Usuário: ")
    usu = mycol_usuario.find_one({"cpf": cpf_usuario})
    if usu is None:
        print("Usuário não encontrado. Compra não cadastrada.")
        return
 
    cpf_cnpj_vendedor = ler_cpf_cnpj("CPF/CNPJ do Vendedor: ")
    vend = mycol_vendedor.find_one({"cpf_cnpjVendedor": cpf_cnpj_vendedor})
    if vend is None:
        print("Vendedor não encontrado. Compra não cadastrada.")
        return
 
    enderecos_usuario = usu.get("end", [])
    if not enderecos_usuario:
        print("Usuário não possui endereço cadastrado. Compra não cadastrada.")
        return
    elif len(enderecos_usuario) == 1:
        endereco_escolhido = enderecos_usuario[0]
    else:
        print("Endereços cadastrados:")
        for i, e in enumerate(enderecos_usuario):
            print(i, "-", e.get("logradouro", ""), ",", e.get("cidade", ""))
        idx = int(input("Escolha o número do endereço de entrega: "))
        endereco_escolhido = enderecos_usuario[idx]
 
    endereco_entrega = {
        "logradouro": endereco_escolhido.get("logradouro", ""),
        "cidade": endereco_escolhido.get("cidade", "")
    }
 
    produtos = []
    key = 'S'
    while (key != 'N'):
        nome_produto = input("Nome do Produto: ")
        prod = mycol_produto.find_one({"nomeProduto": nome_produto})
        if prod is None:
            print("Produto não encontrado, tente novamente.")
        else:
            while True:
                try:
                    quantidade = int(input("Quantidade: "))
                    if quantidade > 0:
                        break
                    print("Quantidade inválida! Digite um número maior que zero.")
                except ValueError:
                    print("Quantidade inválida! Digite apenas números inteiros.")
            item = {
                "produto_id": prod["_id"],
                "quantidade": quantidade,
                "precoUnitario": Decimal128(str(prod["valorProduto"]))
            }
            produtos.append(item)
        key = ler_sim_nao("Deseja adicionar outro produto (S/N)? ")
 
    mydoc = {
        "dataCompras": datetime.now(),
        "statusCompras": True,
        "enderecoEntrega": endereco_entrega,
        "usuario_id": usu["_id"],
        "vendedor_id": vend["_id"],
        "produtos": produtos
    }
    x = mycol.insert_one(mydoc)
    print("Documento inserido com ID ", x.inserted_id)
 
#READ
def read_compra(cpf_usuario):
    global db
    mycol = db.compra
    print("Compras existentes: ")
    if not len(cpf_usuario):
        mydoc = mycol.find().sort("dataCompras")
        for x in mydoc:
            print(x)
    else:
        mycol_usuario = db.usuario
        usu = mycol_usuario.find_one({"cpf": cpf_usuario})
        if usu is None:
            print("Usuário não encontrado.")
            return
        myquery = {"usuario_id": usu["_id"]}
        mydoc = mycol.find(myquery)
        for x in mydoc:
            print(x)
 
#UPDATE
def update_compra(compra_id_str):
    global db
    mycol = db.compra
    from bson.objectid import ObjectId
    myquery = {"_id": ObjectId(compra_id_str)}
    mydoc = mycol.find_one(myquery)
    print("Dados da compra: ", mydoc)
 
    status = input("Mudar Status (S para ativa, N para cancelada, Enter para não mudar): ").strip().upper()
    if status == 'S':
        mydoc["statusCompras"] = True
    elif status == 'N':
        mydoc["statusCompras"] = False
 
    logradouro = input("Mudar Logradouro de Entrega:")
    if len(logradouro):
        mydoc["enderecoEntrega"]["logradouro"] = logradouro
 
    cidade = input("Mudar Cidade de Entrega:")
    if len(cidade):
        while not cidade.replace(' ', '').isalpha():
            print("Cidade inválida! Digite apenas letras.")
            cidade = input("Mudar Cidade de Entrega:")
        mydoc["enderecoEntrega"]["cidade"] = cidade
 
    newvalues = {"$set": mydoc}
    mycol.update_one(myquery, newvalues)
 
#DELETE
def delete_compra(compra_id_str):
    global db
    mycol = db.compra
    from bson.objectid import ObjectId
    myquery = {"_id": ObjectId(compra_id_str)}
    mydoc = mycol.delete_one(myquery)
    print("Deletada a compra ", mydoc)
 