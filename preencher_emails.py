"""Script de uso único: preenche email e favoritos nos usuários existentes.

Rodar na raiz do projeto, com o (.venv) ativo:
    python preencher_emails.py

Mostra uma prévia e só grava se você confirmar com S.
Só mexe em usuários que ainda NÃO têm o campo 'email' (pode rodar de novo sem risco).
"""
import re
import unicodedata

from app.conexao import db


def limpar(txt):
    """'José da Silva' -> 'jose.da.silva' (sem acento, sem espaço)."""
    txt = unicodedata.normalize("NFKD", txt).encode("ascii", "ignore").decode()
    txt = re.sub(r"[^a-zA-Z0-9]+", ".", txt).strip(".").lower()
    return txt or "usuario"


usados = {d["email"] for d in db.usuario.find({"email": {"$exists": True}}, {"email": 1})}
plano = []

for u in db.usuario.find({"email": {"$exists": False}}):
    nomes = u.get("nome", "").split()
    sobrenomes = u.get("sobrenome", "").split()
    primeiro = limpar(nomes[0]) if nomes else "usuario"           # só o 1º nome
    ultimo = limpar(sobrenomes[-1]) if sobrenomes else ""         # só o último sobrenome
    base = f"{primeiro}.{ultimo}" if ultimo else primeiro
    email, n = f"{base}@teste.com", 2
    while email in usados:                  # evita e-mail repetido
        email, n = f"{base}{n}@teste.com", n + 1
    usados.add(email)
    plano.append((u["_id"], email))
    print(f"{u.get('nome', '?')} {u.get('sobrenome', '')}  ->  {email}")

if not plano:
    print("Nenhum usuário sem e-mail. Nada a fazer.")
elif input("\nGravar estes e-mails (e favoritos vazios)? (S/N) ").strip().upper() == "S":
    for _id, email in plano:
        db.usuario.update_one({"_id": _id}, {"$set": {"email": email}})
        # favoritos: só cria se ainda não existir
        db.usuario.update_one({"_id": _id, "favoritos": {"$exists": False}},
                              {"$set": {"favoritos": []}})
    print(f"{len(plano)} usuário(s) atualizados.")
else:
    print("Cancelado. Nada foi gravado.")