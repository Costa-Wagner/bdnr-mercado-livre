"""EX3 - CRUD dos itens no Redis (Favoritos e Endereços de cada usuário).

Colocar em app/redis_crud.py.

Cada usuário tem duas chaves no Redis, com uma lista JSON:
    fav_<email>  ->  ["<id do produto>", ...]
    end_<email>  ->  [{"logradouro": ..., "num": ..., "bairro": ..., "cidade": ...,
                       "estado": ..., "cep": ...}, ...]

O usuário é escolhido pelo NOME, CPF ou e-mail; o programa descobre o e-mail sozinho.

Fluxo do exercício:  opção 5 (Mongo -> Redis)  ->  opção 7 (CRUD aqui)  ->  opção 6 (Redis -> Mongo)
"""
import json
import re
import unicodedata

from app.redis_sessao import CAMPO_EMAIL, COLECAO, ler_sim_nao, r

CAMPOS_END = ["logradouro", "num", "bairro", "cidade", "estado", "cep"]


# ------------------------------------------------------------------ apoio
def _norm(txt):
    """Minúsculo e sem acento, para a busca não depender de maiúsculas ou acentos."""
    txt = unicodedata.normalize("NFKD", str(txt)).encode("ascii", "ignore").decode()
    return txt.lower().strip()


def _escolher_usuario():
    """Pergunta o usuário por nome, CPF ou e-mail e devolve o e-mail dele (ou None).
    Se mais de um usuário combinar, mostra a lista e pede o número."""
    bruto = input("Usuário (nome, CPF ou e-mail): ").strip()
    termo = _norm(bruto)
    if not termo:
        print("Informe o usuário.")
        return None
    cpf_busca = re.sub(r"\D", "", bruto)
    achados = []
    for u in COLECAO.find({CAMPO_EMAIL: {"$exists": True}}):
        base = _norm(f"{u.get('nome', '')} {u.get('sobrenome', '')} {u[CAMPO_EMAIL]}")
        cpf = re.sub(r"\D", "", str(u.get("cpf") or ""))
        if all(p in base for p in termo.split()) or (len(cpf_busca) == 11 and cpf_busca == cpf):
            achados.append(u)
    if not achados:
        print("Usuário não encontrado no Mongo (ou sem e-mail cadastrado).")
        return None
    if len(achados) == 1:
        escolhido = achados[0]
    else:
        print("Mais de um usuário encontrado:")
        for i, u in enumerate(achados):
            print(f"   [{i}] {u.get('nome', '')} {u.get('sobrenome', '')} - {u[CAMPO_EMAIL]}")
        txt = input("Número do usuário: ").strip()
        if not (txt.isdigit() and int(txt) < len(achados)):
            print("Número inválido.")
            return None
        escolhido = achados[int(txt)]
    print(f"Usuário: {escolhido.get('nome', '')} {escolhido.get('sobrenome', '')} ({escolhido[CAMPO_EMAIL]})")
    return escolhido[CAMPO_EMAIL]


def _escolher_tipo():
    """Pergunta se o item é Favorito ou Endereço. Retorna o prefixo da chave ou None."""
    print("1-Favoritos  2-Endereços")
    op = input("Tipo de item: ").strip()
    if op == "1":
        return "fav_"
    if op == "2":
        return "end_"
    print("Opção inválida.")
    return None


def _carregar(chave):
    """Lista guardada no Redis ([] se a chave não existe; None se o JSON estiver inválido)."""
    bruto = r.get(chave)
    if bruto is None:
        return []
    try:
        dados = json.loads(bruto)
    except json.JSONDecodeError:
        return None
    return dados if isinstance(dados, list) else None


def _salvar(chave, lista):
    r.set(chave, json.dumps(lista, ensure_ascii=False))


def _descrever(prefixo, item):
    """Uma linha por item. Endereço fora do padrão (outros nomes de campo) mostra tudo, sem esconder nada."""
    if prefixo == "fav_" or not isinstance(item, dict):
        return str(item)
    if all(c in item for c in CAMPOS_END):
        return (f"{item['logradouro']}, {item['num']} - {item['bairro']} - "
                f"{item['cidade']}/{item['estado']} - CEP {item['cep']}")
    return " | ".join(f"{k}: {v}" for k, v in item.items())


def _mostrar(chave):
    """Imprime os itens numerados. Retorna a lista, ou None se o conteúdo for inválido."""
    itens = _carregar(chave)
    print(f"\n{chave}")
    if itens is None:
        print("   (conteúdo inválido no Redis)")
        return None
    if not itens:
        print("   (vazio)")
    for i, item in enumerate(itens):
        print(f"   [{i}] {_descrever(chave[:4], item)}")
    return itens


def _ler_id(msg):
    pid = input(msg).strip()
    if re.fullmatch(r"[0-9a-fA-F]{24}", pid):
        return pid.lower()
    print("Id inválido: são 24 caracteres hexadecimais (o _id do produto no Mongo).")
    return None


def _ler_endereco(atual=None):
    """Cadastra um endereço novo (campos padrão) ou atualiza um existente.
    Na atualização percorre os campos que o endereço JÁ TEM (Enter mantém o valor) e preserva
    qualquer campo, mesmo com nome diferente do padrão, para não perder dados."""
    if atual is None:
        novo = {}
        for campo in CAMPOS_END:
            valor = input(f"{campo}: ").strip()
            while not valor:
                valor = input(f"{campo} (obrigatório): ").strip()
            novo[campo] = valor
        return novo
    novo = dict(atual)
    for campo, antigo in atual.items():
        valor = input(f"{campo} [{antigo}] (Enter mantém): ").strip()
        if valor:
            novo[campo] = valor
    return novo


# ------------------------------------------------------------------ CREATE
def create_item():
    print("\nCriar item no Redis")
    email = _escolher_usuario()
    if not email:
        return
    prefixo = _escolher_tipo()
    if not prefixo:
        return
    chave = f"{prefixo}{email}"
    itens = _carregar(chave)
    if itens is None:
        print(f"{chave} tem conteúdo inválido no Redis. Corrija ou apague a chave antes.")
        return
    if prefixo == "fav_":
        pid = _ler_id("Id do produto favorito (24 caracteres): ")
        if not pid:
            return
        if pid in itens:
            print("Esse favorito já existe.")
            return
        itens.append(pid)
    else:
        itens.append(_ler_endereco())
    _salvar(chave, itens)
    print(f"Item criado em {chave}.")


# ------------------------------------------------------------------ READ
def read_itens():
    print("\nLer itens no Redis (Enter em branco para ver todos)")
    if input("Deseja ver todos os usuários (S/N)? ").strip().upper() == "S":
        chaves = sorted(list(r.scan_iter("fav_*")) + list(r.scan_iter("end_*")))
        if not chaves:
            print("Nenhum item no Redis. Use a opção 5 (Mongo -> Redis) primeiro.")
            return
    else:
        email = _escolher_usuario()
        if not email:
            return
        chaves = [f"fav_{email}", f"end_{email}"]
    for chave in chaves:
        if r.exists(chave):
            _mostrar(chave)
        else:
            print(f"\n{chave}\n   (não existe no Redis)")


# ------------------------------------------------------------------ UPDATE
def update_item():
    print("\nAtualizar item no Redis")
    email = _escolher_usuario()
    if not email:
        return
    prefixo = _escolher_tipo()
    if not prefixo:
        return
    chave = f"{prefixo}{email}"
    if not r.exists(chave):
        print(f"{chave} não existe no Redis.")
        return
    itens = _mostrar(chave)
    if not itens:
        return
    txt = input("Número do item a atualizar: ").strip()
    if not (txt.isdigit() and int(txt) < len(itens)):
        print("Número inválido.")
        return
    i = int(txt)
    if prefixo == "fav_":
        pid = _ler_id("Novo id do produto (24 caracteres): ")
        if not pid:
            return
        itens[i] = pid
    else:
        if not isinstance(itens[i], dict):
            print("Esse item não é um endereço válido; apague-o e crie de novo.")
            return
        itens[i] = _ler_endereco(itens[i])
    _salvar(chave, itens)
    print("Item atualizado.")


# ------------------------------------------------------------------ DELETE
def delete_item():
    print("\nApagar item no Redis")
    email = _escolher_usuario()
    if not email:
        return
    prefixo = _escolher_tipo()
    if not prefixo:
        return
    chave = f"{prefixo}{email}"
    if not r.exists(chave):
        print(f"{chave} não existe no Redis.")
        return
    itens = _mostrar(chave)
    txt = input("Número do item a apagar (T para apagar a chave inteira): ").strip().upper()
    if txt == "T":
        if ler_sim_nao(f"Apagar a chave {chave} (S/N)? "):
            r.delete(chave)
            print("Chave apagada. A opção 6 não altera o Mongo para essa chave.")
        return
    if itens and txt.isdigit() and int(txt) < len(itens):
        itens.pop(int(txt))
        _salvar(chave, itens)
        print("Item apagado.")
    else:
        print("Número inválido.")