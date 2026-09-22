from app.conexao import db
from app.validadores import ler_texto, ler_cpf_cnpj, ler_sim_nao

#INSERT
def create_produto():
    global db
    mycol = db.produto
    mycol_vendedor = db.vendedor
    print("\nInserindo um novo produto")
    nome = input("Nome do Produto: ")
    descricao = input("Descrição: ")
    while True:
        try:
            estoque = int(input("Estoque: "))
            if estoque >= 0:
                break
            print("Estoque inválido! Digite um número maior ou igual a zero.")
        except ValueError:
            print("Estoque inválido! Digite apenas números inteiros.")
    categoria = ler_texto("Categoria: ")
    while True:
        try:
            valor = float(input("Valor: "))
            if valor >= 0:
                break
            print("Valor inválido! Digite um valor maior ou igual a zero.")
        except ValueError:
            print("Valor inválido! Digite um número válido.")

    fotos = []
    key = 'S'
    while (key != 'N'):
        foto = input("URL da Foto: ")
        fotos.append(foto)
        key = ler_sim_nao("Deseja cadastrar outra foto (S/N)? ")

    cpf_cnpj_vendedor = ler_cpf_cnpj("CPF/CNPJ do Vendedor deste produto: ")
    vend = mycol_vendedor.find_one({"cpf_cnpjVendedor": cpf_cnpj_vendedor})
    if vend is None:
        print("Vendedor não encontrado. Produto não cadastrado.")
        return

    endereco_envio = ""
    enderecos_vendedor = vend.get("enderecoVendedor", [])
    for e in enderecos_vendedor:
        if e.get("tipo") == "entrega":
            endereco_envio = e.get("logradouro", "") + " - " + e.get("cidade", "")
            break
    if not endereco_envio and enderecos_vendedor:
        e = enderecos_vendedor[0]
        endereco_envio = e.get("logradouro", "") + " - " + e.get("cidade", "")

    vendedor_embutido = {
        "vendedor_id": vend["_id"],
        "nomefantasiaVendedor": vend["nomeFantasiaVendedor"],
        "razaosociaVendedor": vend["razaoSocialVendedor"],
        "cnpjVendedor": vend["cpf_cnpjVendedor"],
        "enderecoEnvioVendedor": endereco_envio,
        "telefoneVendedor": vend["telefoneVendedor"],
        "emailVendedor": vend["emailVendedor"]
    }

    mydoc = {
        "nomeProduto": nome,
        "descricaoProduto": descricao,
        "estoqueProduto": estoque,
        "categoriaProduto": categoria,
        "fotoProduto": fotos,
        "valorProduto": valor,
        "vendedor": vendedor_embutido
    }
    x = mycol.insert_one(mydoc)
    print("Documento inserido com ID ", x.inserted_id)

#READ
def read_produto(nome, categoria):
    global db
    mycol = db.produto
    print("Produtos existentes: ")
    if not len(nome) and not len(categoria):
        mydoc = mycol.find().sort("nomeProduto")
        for x in mydoc:
            print(x["nomeProduto"], x["valorProduto"])
    else:
        myquery = {}
        if len(nome):
            myquery["nomeProduto"] = nome
        if len(categoria):
            myquery["categoriaProduto"] = categoria
        mydoc = mycol.find(myquery)
        for x in mydoc:
            print(x)

#UPDATE
def update_produto(nome):
    global db
    mycol = db.produto
    myquery = {"nomeProduto": nome}
    mydoc = mycol.find_one(myquery)
    print("Dados do produto: ", mydoc)

    novo_nome = input("Mudar Nome:")
    if len(novo_nome):
        mydoc["nomeProduto"] = novo_nome

    descricao = input("Mudar Descrição:")
    if len(descricao):
        mydoc["descricaoProduto"] = descricao

    estoque = input("Mudar Estoque:")
    if len(estoque):
        while True:
            try:
                estoque_int = int(estoque)
                if estoque_int >= 0:
                    mydoc["estoqueProduto"] = estoque_int
                    break
                print("Estoque inválido! Digite um número maior ou igual a zero.")
            except ValueError:
                print("Estoque inválido! Digite apenas números inteiros.")
            estoque = input("Mudar Estoque:")

    categoria = input("Mudar Categoria:")
    if len(categoria):
        while not categoria.replace(' ', '').isalpha():
            print("Categoria inválida! Digite apenas letras.")
            categoria = input("Mudar Categoria:")
        mydoc["categoriaProduto"] = categoria

    valor = input("Mudar Valor:")
    if len(valor):
        while True:
            try:
                valor_float = float(valor)
                if valor_float >= 0:
                    mydoc["valorProduto"] = valor_float
                    break
                print("Valor inválido! Digite um valor maior ou igual a zero.")
            except ValueError:
                print("Valor inválido! Digite um número válido.")
            valor = input("Mudar Valor:")

    newvalues = {"$set": mydoc}
    mycol.update_one(myquery, newvalues)

#DELETE
def delete_produto(nome, cnpj_vendedor):
    global db
    mycol = db.produto
    myquery = {"nomeProduto": nome, "vendedor.cnpjVendedor": cnpj_vendedor}
    mydoc = mycol.delete_one(myquery)
    print("Deletado o produto ", mydoc)